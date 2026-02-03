"""
自动化脚本 API 路由模块

提供脚本管理和执行的 REST API 接口。
"""

import os
import uuid
import asyncio
import json
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from queue import Queue
from threading import Thread

from app.core.device import get_device_manager
from app.services.script_executor import ScriptExecutor, ExecutionResult

router = APIRouter(prefix="/script", tags=["Script"])

# 脚本存储目录
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scripts")

# 确保脚本目录存在
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# 存储正在执行的脚本
running_scripts: Dict[str, ScriptExecutor] = {}

# 存储执行会话的日志队列
execution_sessions: Dict[str, Queue] = {}


class ScriptContent(BaseModel):
    """脚本内容模型"""

    content: str
    variables: Optional[Dict[str, Any]] = None


class ScriptFile(BaseModel):
    """脚本文件模型"""

    name: str
    content: str


class ScriptInfo(BaseModel):
    """脚本信息模型"""

    name: str
    size: int
    modified: float


@router.get("/list")
def list_scripts() -> List[ScriptInfo]:
    """
    获取脚本列表

    Returns:
        List[ScriptInfo]: 脚本信息列表
    """
    scripts = []
    if os.path.exists(SCRIPTS_DIR):
        for filename in os.listdir(SCRIPTS_DIR):
            if filename.endswith(".script"):
                filepath = os.path.join(SCRIPTS_DIR, filename)
                stat = os.stat(filepath)
                scripts.append(ScriptInfo(name=filename, size=stat.st_size, modified=stat.st_mtime))
    return sorted(scripts, key=lambda x: x.modified, reverse=True)


@router.get("/get/{name}")
def get_script(name: str) -> Dict[str, str]:
    """
    获取脚本内容

    Args:
        name: 脚本文件名

    Returns:
        Dict: 包含脚本内容的字典
    """
    filepath = os.path.join(SCRIPTS_DIR, name)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Script not found: {name}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return {"name": name, "content": content}


@router.post("/save")
def save_script(script: ScriptFile) -> Dict[str, str]:
    """
    保存脚本

    Args:
        script: 脚本文件信息

    Returns:
        Dict: 操作结果
    """
    if not script.name.endswith(".script"):
        script.name += ".script"

    # 验证文件名
    if "/" in script.name or "\\" in script.name or ".." in script.name:
        raise HTTPException(status_code=400, detail="Invalid script name")

    filepath = os.path.join(SCRIPTS_DIR, script.name)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script.content)

    return {"message": f"Script saved: {script.name}"}


@router.delete("/delete/{name}")
def delete_script(name: str) -> Dict[str, str]:
    """
    删除脚本

    Args:
        name: 脚本文件名

    Returns:
        Dict: 操作结果
    """
    filepath = os.path.join(SCRIPTS_DIR, name)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Script not found: {name}")

    os.remove(filepath)
    return {"message": f"Script deleted: {name}"}


@router.post("/execute")
def execute_script(script: ScriptContent) -> ExecutionResult:
    """
    执行脚本内容

    Args:
        script: 脚本内容和变量

    Returns:
        ExecutionResult: 执行结果
    """
    manager = get_device_manager()

    executor = ScriptExecutor(manager)
    result = executor.execute_script(
        script.content, variables=script.variables, script_dir=SCRIPTS_DIR
    )

    return result


@router.post("/execute/stream")
async def execute_script_stream(script: ScriptContent):
    """
    执行脚本并通过 SSE 实时返回日志

    Args:
        script: 脚本内容和变量

    Returns:
        StreamingResponse: SSE 事件流
    """
    manager = get_device_manager()

    # 创建执行会话
    session_id = str(uuid.uuid4())
    log_queue: Queue = Queue()
    execution_sessions[session_id] = log_queue

    # 创建执行器
    executor = ScriptExecutor(manager)
    running_scripts[session_id] = executor

    # 日志回调函数
    def log_callback(message: str):
        log_queue.put({"type": "log", "data": message})

    # 在后台线程中执行脚本
    def run_script():
        try:
            result = executor.execute_script(
                script.content,
                variables=script.variables,
                script_dir=SCRIPTS_DIR,
                log_callback=log_callback,
            )
            # 发送执行结果
            log_queue.put(
                {
                    "type": "result",
                    "data": {
                        "success": result.success,
                        "error": result.error,
                        "variables": result.variables,
                    },
                }
            )
        except Exception as e:
            log_queue.put({"type": "error", "data": str(e)})
        finally:
            # 发送结束信号
            log_queue.put({"type": "end", "data": None})
            # 清理会话
            if session_id in running_scripts:
                del running_scripts[session_id]
            if session_id in execution_sessions:
                del execution_sessions[session_id]

    # 启动执行线程
    thread = Thread(target=run_script, daemon=True)
    thread.start()

    # SSE 事件生成器
    async def event_generator():
        # 发送会话 ID
        yield f"data: {json.dumps({'type': 'session', 'data': session_id})}\n\n"

        while True:
            try:
                # 非阻塞方式获取日志
                await asyncio.sleep(0.05)  # 小延迟避免 CPU 占用过高
                while not log_queue.empty():
                    event = log_queue.get_nowait()
                    yield f"data: {json.dumps(event)}\n\n"

                    # 如果是结束信号，退出循环
                    if event.get("type") == "end":
                        return
            except Exception:
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/execute/stream/{name}")
async def execute_script_file_stream(name: str, variables: Optional[Dict[str, Any]] = None):
    """
    执行脚本文件并通过 SSE 实时返回日志

    Args:
        name: 脚本文件名
        variables: 初始变量

    Returns:
        StreamingResponse: SSE 事件流
    """
    filepath = os.path.join(SCRIPTS_DIR, name)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Script not found: {name}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 复用 execute_script_stream 的逻辑
    script = ScriptContent(content=content, variables=variables)
    return await execute_script_stream(script)


@router.post("/execute/{name}")
def execute_script_file(name: str, variables: Optional[Dict[str, Any]] = None) -> ExecutionResult:
    """
    执行脚本文件

    Args:
        name: 脚本文件名
        variables: 初始变量

    Returns:
        ExecutionResult: 执行结果
    """
    filepath = os.path.join(SCRIPTS_DIR, name)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Script not found: {name}")

    manager = get_device_manager()

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    executor = ScriptExecutor(manager)
    result = executor.execute_script(content, variables=variables, script_dir=SCRIPTS_DIR)

    return result


@router.post("/validate")
def validate_script(script: ScriptContent) -> Dict[str, Any]:
    """
    验证脚本语法

    Args:
        script: 脚本内容

    Returns:
        Dict: 验证结果
    """
    from app.services.script_parser import parse_script

    try:
        ast = parse_script(script.content)
        return {"valid": True, "statements": len(ast), "message": "Script is valid"}
    except SyntaxError as e:
        return {"valid": False, "error": str(e), "message": "Script has syntax errors"}


@router.post("/stop/{session_id}")
def stop_script(session_id: str) -> Dict[str, str]:
    """
    停止正在执行的脚本

    Args:
        session_id: 执行会话 ID

    Returns:
        Dict: 操作结果
    """
    if session_id not in running_scripts:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")

    executor = running_scripts[session_id]
    executor.stop()

    return {"message": f"Stop signal sent to session: {session_id}"}
