"""
脚本执行器模块

提供脚本的执行功能，将解析后的AST转换为实际的设备操作。
"""

import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .script_parser import (
    ASTNode,
    CommandNode,
    SetNode,
    IfNode,
    LoopNode,
    WhileNode,
    TryNode,
    CallNode,
    BreakNode,
    ContinueNode,
    ConditionNode,
    parse_script,
)
from ..core.device import DeviceManager
from .input import InputService
from .navigation import NavigationService
from .app_service import AppService
from .adb_service import AdbService


class BreakException(Exception):
    """循环中断异常"""

    pass


class ContinueException(Exception):
    """循环继续异常"""

    pass


@dataclass
class ExecutionContext:
    """执行上下文"""

    variables: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    current_line: int = 0
    script_dir: str = ""
    max_iterations: int = 10000
    stop_requested: bool = False
    log_callback: Optional[Callable[[str], None]] = None


@dataclass
class ExecutionResult:
    """执行结果"""

    success: bool = True
    logs: List[str] = field(default_factory=list)
    error: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)


class ScriptExecutor:
    """
    脚本执行器

    负责执行解析后的AST，将脚本命令转换为实际的设备操作。
    """

    def __init__(self, device_manager: DeviceManager):
        """
        初始化脚本执行器

        Args:
            device_manager: 设备管理器实例
        """
        self.device_manager = device_manager

        # 初始化各种服务（延迟初始化）
        self._input_service = None
        self._navigation_service = None
        self._app_service = None
        self._adb_service = None
        self._cached_device = None

        # 执行上下文
        self.context: Optional[ExecutionContext] = None

    def _ensure_device(self):
        """
        确保设备已连接，如果未连接则自动连接
        只有在实际需要执行设备操作时才调用此方法
        """
        if self._cached_device is None:
            if self.device_manager.is_connected():
                self._cached_device = self.device_manager.get_device()
            else:
                # 设备未连接，自动连接第一个可用设备
                self.device_manager.connect()
                self._cached_device = self.device_manager.get_device()
        return self._cached_device

    def _ensure_services(self):
        """确保所有服务已初始化"""
        if self._input_service is None:
            self._input_service = InputService(self.device_manager)
        if self._navigation_service is None:
            self._navigation_service = NavigationService(self.device_manager)
        if self._app_service is None:
            self._app_service = AppService(self.device_manager)
        if self._adb_service is None:
            device = self._ensure_device()
            if device and device.serial:
                self._adb_service = AdbService(device.serial)
            else:
                self._adb_service = AdbService("")

    @property
    def device(self):
        """获取设备对象"""
        return self._cached_device

    @property
    def input_service(self):
        self._ensure_services()
        return self._input_service

    @property
    def navigation_service(self):
        self._ensure_services()
        return self._navigation_service

    @property
    def app_service(self):
        self._ensure_services()
        return self._app_service

    @property
    def adb_service(self):
        self._ensure_services()
        return self._adb_service

    def execute_script(
        self,
        source: str,
        variables: Optional[Dict[str, Any]] = None,
        script_dir: str = "",
        log_callback: Optional[Callable[[str], None]] = None,
    ) -> ExecutionResult:
        """
        解析并执行脚本

        Args:
            source: 脚本源代码
            variables: 初始变量字典
            script_dir: 脚本所在目录（用于call命令）
            log_callback: 日志回调函数，用于实时输出日志

        Returns:
            ExecutionResult: 执行结果
        """
        try:
            # 解析脚本
            ast = parse_script(source)
            return self.execute_ast(ast, variables, script_dir, log_callback)
        except SyntaxError as e:
            error_msg = f"Syntax error: {str(e)}"
            if log_callback:
                log_callback(error_msg)
            return ExecutionResult(success=False, error=error_msg, logs=[error_msg])
        except Exception as e:
            error_msg = f"Execution error: {str(e)}"
            if log_callback:
                log_callback(error_msg)
            return ExecutionResult(
                success=False,
                error=error_msg,
                logs=[error_msg],
            )

    def execute_ast(
        self,
        ast: List[ASTNode],
        variables: Optional[Dict[str, Any]] = None,
        script_dir: str = "",
        log_callback: Optional[Callable[[str], None]] = None,
    ) -> ExecutionResult:
        """
        执行AST

        Args:
            ast: AST节点列表
            variables: 初始变量字典
            script_dir: 脚本所在目录
            log_callback: 日志回调函数

        Returns:
            ExecutionResult: 执行结果
        """
        # 初始化执行上下文
        self.context = ExecutionContext(
            variables=variables.copy() if variables else {},
            script_dir=script_dir,
            log_callback=log_callback,
        )

        try:
            for node in ast:
                if self.context.stop_requested:
                    self.log("Execution stopped by user")
                    break
                self.execute_node(node)

            return ExecutionResult(
                success=True, logs=self.context.logs, variables=self.context.variables
            )
        except BreakException:
            return ExecutionResult(
                success=False,
                error="Break outside of loop",
                logs=self.context.logs,
                variables=self.context.variables,
            )
        except ContinueException:
            return ExecutionResult(
                success=False,
                error="Continue outside of loop",
                logs=self.context.logs,
                variables=self.context.variables,
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e),
                logs=self.context.logs,
                variables=self.context.variables,
            )

    def execute_node(self, node: ASTNode) -> Any:
        """
        执行单个AST节点

        Args:
            node: AST节点

        Returns:
            节点执行结果
        """
        if self.context and self.context.stop_requested:
            raise Exception("Execution stopped by user")

        if self.context:
            self.context.current_line = node.line

        if isinstance(node, CommandNode):
            return self.execute_command(node)
        elif isinstance(node, SetNode):
            return self.execute_set(node)
        elif isinstance(node, IfNode):
            return self.execute_if(node)
        elif isinstance(node, LoopNode):
            return self.execute_loop(node)
        elif isinstance(node, WhileNode):
            return self.execute_while(node)
        elif isinstance(node, TryNode):
            return self.execute_try(node)
        elif isinstance(node, CallNode):
            return self.execute_call(node)
        elif isinstance(node, BreakNode):
            raise BreakException()
        elif isinstance(node, ContinueNode):
            raise ContinueException()
        else:
            self.log(f"Unknown node type: {type(node).__name__}")
            return None

    def _resolve_value(self, value: Any) -> Any:
        """
        解析变量引用

        Args:
            value: 原始值（可能是变量名）

        Returns:
            解析后的值
        """
        if self.context and isinstance(value, str) and value in self.context.variables:
            return self.context.variables[value]
        return value

    def _interpolate_variables(self, value: Any) -> Any:
        """
        解析字符串中的变量插值

        支持 ${variable} 语法，例如：
        - "Hello ${name}" -> "Hello World" （如果 name="World"）
        - "${x} + ${y}" -> "10 + 20" （如果 x=10, y=20）

        Args:
            value: 原始值（字符串）

        Returns:
            插值后的字符串
        """
        if not self.context or not isinstance(value, str):
            return value

        variables = self.context.variables if self.context.variables else {}
        pattern = r'\$\{([^}]+)\}'

        def replace_match(match):
            var_name = match.group(1)
            if var_name in variables:
                var_value = variables[var_name]
                return str(var_value) if var_value is not None else ""
            return match.group(0)

        return re.sub(pattern, replace_match, value)

    def _get_element(self, selector_type: Optional[str], selector_value: Optional[str]):
        """
        根据选择器获取元素

        Args:
            selector_type: 选择器类型 (id, text, xpath, class)
            selector_value: 选择器值

        Returns:
            uiautomator2 元素对象
        """
        if not selector_type or not selector_value:
            return None

        selector_value = self._interpolate_variables(self._resolve_value(selector_value))

        if selector_value is None:
            return None

        if selector_type == "id":
            return self.device(resourceId=selector_value)
        elif selector_type == "text":
            return self.device(text=selector_value)
        elif selector_type == "xpath":
            return self._ensure_device().xpath(selector_value)
        elif selector_type == "class":
            return self.device(className=selector_value)
        return None

    def execute_command(self, node: CommandNode) -> Any:
        """
        执行命令节点

        Args:
            node: 命令节点

        Returns:
            命令执行结果
        """
        command = node.command.lower()
        args = [self._interpolate_variables(self._resolve_value(arg)) for arg in node.args]

        self.log(f"Executing: {command} {args}")

        # 点击命令
        if command == "click":
            if node.selector_type and node.selector_value:
                element = self._get_element(node.selector_type, node.selector_value)
                if element and element.exists:
                    element.click()
                    return True
                return False
            elif args:
                # 坐标点击
                if len(args) >= 2:
                    x, y = int(args[0]), int(args[1])
                    self._ensure_device().click(x, y)
                    return True
            return False

        elif command == "click_text":
            text = args[0] if args else node.selector_value
            if text:
                return self.input_service.click_by_text(str(text))
            return False

        elif command == "click_id":
            resource_id = args[0] if args else node.selector_value
            if resource_id:
                return self.input_service.click(str(resource_id))
            return False

        # 输入命令
        elif command == "input":
            if node.selector_type and node.selector_value:
                element = self._get_element(node.selector_type, node.selector_value)
                if element and element.exists:
                    element.click()
                    self._ensure_device().sleep(0.3)
                    text = str(args[0]) if args else ""
                    self._ensure_device().send_keys(text, clear=False)
                    return True
            elif args:
                # 直接输入文本
                self._ensure_device().send_keys(str(args[0]), clear=False)
                return True
            return False

        # 清除文本
        elif command == "clear":
            if node.selector_type and node.selector_value:
                element = self._get_element(node.selector_type, node.selector_value)
                if element and element.exists:
                    element.click()
                    self._ensure_device().clear_text()
                    return True
            else:
                self._ensure_device().clear_text()
                return True
            return False

        # 滑动命令
        elif command == "swipe":
            if args:
                direction = str(args[0]).lower()
                percent = float(args[1]) if len(args) > 1 else 0.5
                return self.input_service.swipe(direction, percent)
            return False

        # 等待命令
        elif command == "wait":
            if args:
                duration = float(args[0])
                time.sleep(duration)
                return True
            return False

        elif command == "wait_element":
            if node.selector_type and node.selector_value:
                timeout = float(args[0]) if args else 10.0
                element = self._get_element(node.selector_type, node.selector_value)
                if element:
                    try:
                        return element.wait(timeout=timeout)
                    except Exception:
                        return element.exists
            return False

        elif command == "wait_gone":
            if node.selector_type and node.selector_value:
                timeout = float(args[0]) if args else 10.0
                element = self._get_element(node.selector_type, node.selector_value)
                if element:
                    try:
                        return element.wait_gone(timeout=timeout)
                    except Exception:
                        return not element.exists
            return False

        # 导航命令
        elif command == "back":
            return self.navigation_service.press_back()

        elif command == "home":
            return self.navigation_service.press_home()

        elif command == "menu":
            return self.navigation_service.press_menu()

        elif command == "recent":
            return self.navigation_service.open_recent_apps()

        # 应用管理命令
        elif command == "start_app":
            if args:
                package_name = str(args[0])
                return self.app_service.start_app(package_name)
            return False

        elif command == "stop_app":
            if args:
                package_name = str(args[0])
                return self.app_service.stop_app(package_name)
            return False

        elif command == "clear_app":
            if args:
                package_name = str(args[0])
                return self.app_service.clear_app_data(package_name)
            return False

        # 屏幕控制命令
        elif command == "screen_on":
            return self.input_service.screen_on()

        elif command == "screen_off":
            return self.input_service.screen_off()

        elif command == "unlock":
            return self.input_service.unlock_screen()

        # 获取文本
        elif command == "get_text":
            if node.selector_type and node.selector_value:
                element = self._get_element(node.selector_type, node.selector_value)
                if element and element.exists:
                    info = element.info
                    return info.get("text", "")
            return ""

        # 获取元素信息
        elif command == "get_info":
            if node.selector_type and node.selector_value:
                element = self._get_element(node.selector_type, node.selector_value)
                if element and element.exists:
                    info = element.info
                    result = {
                        "exists": True,
                        "text": info.get("text", ""),
                        "class_name": info.get("className", ""),
                        "resource_id": info.get("resourceName", ""),
                        "bounds": info.get("bounds", {}),
                        "enabled": info.get("enabled", False),
                        "focused": info.get("focused", False),
                        "selected": info.get("selected", False),
                        "clickable": info.get("clickable", False),
                        "checkable": info.get("checkable", False),
                        "checked": info.get("checked", False),
                    }
                    return result
                return {"exists": False}
            return {"exists": False}

        # 查找元素
        elif command == "find_element":
            if node.selector_type and node.selector_value:
                result = self._find_element_by_selector(node.selector_type, node.selector_value)
                self.log(f"Found element: {result}")
                return result
            return {"exists": False}

        # 查找所有元素
        elif command == "find_elements":
            if node.selector_type and node.selector_value:
                results = self._find_elements_by_selector(node.selector_type, node.selector_value)
                self.log(f"Found {len(results)} elements")
                return {"elements": results, "count": len(results)}
            return {"elements": [], "count": 0}

        # 导出界面结构
        elif command == "dump_hierarchy":
            xml = self.input_service.get_current_ui_xml()
            self.log(f"Hierarchy dump: {len(xml)} chars")
            return xml

        # 检查元素存在
        elif command == "exists":
            if node.selector_type and node.selector_value:
                element = self._get_element(node.selector_type, node.selector_value)
                if element:
                    return element.exists
            return False

        # 日志命令
        elif command == "log":
            if args:
                message = " ".join(str(arg) for arg in args)
                self.log(f"[LOG] {message}")
            return True

        # Shell命令
        elif command == "shell":
            if args:
                cmd = str(args[0])
                result = self.adb_service.shell(cmd)
                self.log(f"[SHELL] {cmd} -> {result}")
                return result
            return ""

        # ============ 人类模拟操作 ============

        # 人类模拟点击
        elif command == "human_click":
            return self._execute_human_click(node, args)

        # 人类模拟双击
        elif command == "human_double_click":
            return self._execute_human_double_click(node, args)

        # 人类模拟长按
        elif command == "human_long_press":
            return self._execute_human_long_press(node, args)

        # 人类模拟拖拽
        elif command == "human_drag":
            return self._execute_human_drag(node, args)

        # ============ 设备连接命令 ============

        elif command == "connect":
            if args:
                # 连接指定设备（序列号或IP）
                device_serial = str(args[0])
                info = self.device_manager.connect(device_serial)
                self.log(f"Connected to device: {info.serial} ({info.product_name})")
                return info.serial
            else:
                # 自动连接第一个可用设备
                info = self.device_manager.connect()
                self.log(f"Auto-connected to device: {info.serial} ({info.product_name})")
                return info.serial

        elif command == "get_status":
            if self.device_manager.is_connected():
                device = self.device_manager.get_device()
                info = device.info
                return {
                    "connected": True,
                    "serial": device.serial,
                    "product_name": info.get("productName", "Unknown"),
                    "api_level": info.get("sdkInt", 0),
                    "display_rotation": info.get("displayRotation", 0),
                    "display_size": info.get("displaySize"),
                }
            else:
                return {"connected": False}

        elif command == "disconnect":
            self.device_manager.disconnect()
            self.log("Device disconnected")
            return True

        # ============ 应用信息命令 ============

        elif command == "get_app_version":
            if args:
                package_name = str(args[0])
                version = self.app_service.get_app_version(package_name)
                self.log(f"App {package_name} version: {version}")
                return version
            return None

        elif command == "get_current_app":
            result = self.app_service.get_current_app()
            self.log(f"Current app: {result}")
            return result

        else:
            self.log(f"Unknown command: {command}")
            return None

    def execute_set(self, node: SetNode) -> Any:
        """
        执行变量赋值节点

        Args:
            node: 变量赋值节点

        Returns:
            赋值的值
        """
        if not self.context:
            return None

        variable = node.variable

        if node.command:
            # 执行命令并获取结果
            cmd_node = CommandNode(
                command=node.command,
                args=node.command_args,
                selector_type=node.selector_type,
                selector_value=node.selector_value,
                line=node.line,
                column=node.column,
            )
            value = self.execute_command(cmd_node)
        else:
            # 直接赋值
            value = self._interpolate_variables(self._resolve_value(node.value))

        self.context.variables[variable] = value
        self.log(f"Set {variable} = {value}")
        return value

    def execute_if(self, node: IfNode) -> Any:
        """
        执行条件判断节点

        Args:
            node: 条件判断节点

        Returns:
            执行的分支结果
        """
        # 评估主条件
        if node.condition and self.evaluate_condition(node.condition):
            for stmt in node.then_body:
                self.execute_node(stmt)
            return True

        # 评估elif分支
        for elif_condition, elif_body in node.elif_branches:
            if self.evaluate_condition(elif_condition):
                for stmt in elif_body:
                    self.execute_node(stmt)
                return True

        # 执行else分支
        if node.else_body:
            for stmt in node.else_body:
                self.execute_node(stmt)
            return True

        return False

    def execute_loop(self, node: LoopNode) -> Any:
        """
        执行循环节点

        Args:
            node: 循环节点

        Returns:
            循环执行结果
        """
        if not self.context:
            return None

        count = node.count
        variable = node.variable

        for i in range(count):
            if self.context.stop_requested:
                break

            # 设置循环变量
            if variable:
                self.context.variables[variable] = i

            try:
                for stmt in node.body:
                    self.execute_node(stmt)
            except BreakException:
                break
            except ContinueException:
                continue

        return True

    def execute_while(self, node: WhileNode) -> Any:
        """
        执行条件循环节点

        Args:
            node: 条件循环节点

        Returns:
            循环执行结果
        """
        if not self.context:
            return None

        iterations = 0

        while node.condition and self.evaluate_condition(node.condition):
            if self.context.stop_requested:
                break

            iterations += 1
            if iterations > self.context.max_iterations:
                self.log(f"Max iterations ({self.context.max_iterations}) exceeded")
                break

            try:
                for stmt in node.body:
                    self.execute_node(stmt)
            except BreakException:
                break
            except ContinueException:
                continue

        return True

    def execute_try(self, node: TryNode) -> Any:
        """
        执行错误处理节点

        Args:
            node: 错误处理节点

        Returns:
            执行结果
        """
        try:
            for stmt in node.try_body:
                self.execute_node(stmt)
            return True
        except (BreakException, ContinueException):
            # 重新抛出循环控制异常
            raise
        except Exception as e:
            self.log(f"Caught exception: {str(e)}")
            # 执行catch分支
            for stmt in node.catch_body:
                self.execute_node(stmt)
            return False

    def execute_call(self, node: CallNode) -> Any:
        """
        执行子脚本调用节点

        Args:
            node: 子脚本调用节点

        Returns:
            子脚本执行结果
        """
        if not self.context:
            return None

        function_name = node.function_name
        args = [self._resolve_value(arg) for arg in node.args]

        # 构建脚本文件路径
        if not function_name.endswith(".script"):
            function_name += ".script"

        script_path = os.path.join(self.context.script_dir, function_name)

        if not os.path.exists(script_path):
            self.log(f"Script not found: {script_path}")
            return False

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                source = f.read()

            # 准备子脚本的变量
            child_variables = self.context.variables.copy()
            for i, arg in enumerate(args):
                child_variables[f"arg{i}"] = arg

            # 执行子脚本
            result = self.execute_script(
                source, variables=child_variables, script_dir=os.path.dirname(script_path)
            )

            # 合并日志
            self.context.logs.extend(result.logs)

            return result.success
        except Exception as e:
            self.log(f"Error calling script {function_name}: {str(e)}")
            return False

    def evaluate_condition(self, cond: ConditionNode) -> bool:
        """
        评估条件节点

        Args:
            cond: 条件节点

        Returns:
            条件评估结果
        """
        command = cond.command.lower() if cond.command else ""
        args = [self._interpolate_variables(self._resolve_value(arg)) for arg in cond.args]

        result = False

        if command == "exists":
            element = self._get_element(cond.selector_type, cond.selector_value)
            if element:
                result = bool(element.exists)
        elif command == "get_text":
            element = self._get_element(cond.selector_type, cond.selector_value)
            if element and element.exists:
                text = element.info.get("text", "")
                # 如果有参数，比较文本
                if args:
                    result = text == str(args[0])
                else:
                    result = bool(text)
        else:
            # 默认执行命令并检查结果
            cmd_node = CommandNode(
                command=command,
                args=args,
                selector_type=cond.selector_type,
                selector_value=cond.selector_value,
                line=cond.line,
                column=cond.column,
            )
            result = bool(self.execute_command(cmd_node))

        # 处理否定
        if cond.negated:
            result = not result

        return result

    def log(self, message: str) -> None:
        """
        记录日志

        Args:
            message: 日志消息
        """
        if self.context:
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] Line {self.context.current_line}: {message}"
            self.context.logs.append(log_entry)
            # 调用日志回调（用于实时输出）
            if self.context.log_callback:
                self.context.log_callback(log_entry)

    def stop(self) -> None:
        """停止脚本执行"""
        if self.context:
            self.context.stop_requested = True

    # ============ 元素信息获取辅助方法 ============

    def _find_element_by_selector(self, selector_type: str, selector_value: str) -> Dict[str, Any]:
        """
        根据选择器查找元素并返回详细信息

        Args:
            selector_type: 选择器类型 (id, text, class, xpath)
            selector_value: 选择器值

        Returns:
            Dict: 元素信息字典
        """
        selector_value = self._interpolate_variables(self._resolve_value(selector_value))
        element = self._get_element(selector_type, selector_value)

        if element and element.exists:
            info = element.info
            return {
                "exists": True,
                "text": info.get("text", ""),
                "class_name": info.get("className", ""),
                "resource_id": info.get("resourceName", ""),
                "bounds": info.get("bounds", {}),
                "enabled": info.get("enabled", False),
                "focused": info.get("focused", False),
                "selected": info.get("selected", False),
                "clickable": info.get("clickable", False),
            }
        return {"exists": False}

    def _find_elements_by_selector(self, selector_type: str, selector_value: str) -> List[Dict[str, Any]]:
        """
        根据选择器查找所有匹配元素

        Args:
            selector_type: 选择器类型 (id, text, class, xpath)
            selector_value: 选择器值

        Returns:
            List[Dict]: 元素信息列表
        """
        selector_value = self._interpolate_variables(self._resolve_value(selector_value))
        elements = []

        if selector_type == "id":
            all_elements = self._ensure_device()(resourceId=selector_value)
        elif selector_type == "text":
            all_elements = self._ensure_device()(text=selector_value)
        elif selector_type == "class":
            all_elements = self._ensure_device()(className=selector_value)
        elif selector_type == "xpath":
            # xpath 返回XML元素列表，特殊处理
            try:
                xml_elements = self._ensure_device().xpath(selector_value).all()
                for xml_elem in xml_elements:
                    attrs = xml_elem.attrib
                    elements.append(
                        {
                            "text": attrs.get("text", ""),
                            "class_name": attrs.get("class", ""),
                            "resource_id": attrs.get("resource-id", ""),
                            "bounds": attrs.get("bounds", ""),
                            "enabled": attrs.get("enabled", "false") == "true",
                        }
                    )
                return elements
            except Exception:
                return []
        else:
            all_elements = []

        for element in all_elements:
            if hasattr(element, 'exists') and element.exists:
                info = element.info
                elements.append(
                    {
                        "text": info.get("text", ""),
                        "class_name": info.get("className", ""),
                        "resource_id": info.get("resourceName", ""),
                        "bounds": info.get("bounds", {}),
                        "enabled": info.get("enabled", False),
                    }
                )

        return elements

    # ============ 人类模拟操作辅助方法 ============

    def _parse_human_options(self, args: List[Any]) -> Dict[str, Any]:
        """
        解析人类模拟操作的参数

        支持的参数格式：
        - 位置参数：x, y 坐标
        - 命名参数：offset_min=3, offset_max=10, delay_min=0.05, ...

        Args:
            args: 参数列表

        Returns:
            解析后的选项字典
        """
        options: Dict[str, Any] = {}

        for arg in args:
            if isinstance(arg, str) and "=" in arg:
                # 命名参数
                key, value = arg.split("=", 1)
                key = key.strip()
                value = value.strip()
                # 应用变量插值
                value = self._interpolate_variables(value)
                # 尝试转换为数字
                try:
                    if "." in value:
                        options[key] = float(value)
                    else:
                        options[key] = int(value)
                except ValueError:
                    options[key] = value
            elif isinstance(arg, (int, float)):
                # 位置参数（坐标）
                if "x" not in options:
                    options["x"] = int(arg)
                elif "y" not in options:
                    options["y"] = int(arg)

        return options

    def _execute_human_click(self, node: CommandNode, args: List[Any]) -> bool:
        """
        执行人类模拟点击

        语法：
        - human_click id:"resource_id"
        - human_click text:"按钮文本"
        - human_click xpath:"//android.widget.Button"
        - human_click 500, 800
        - human_click 500, 800, offset_min=3, offset_max=10

        Args:
            node: 命令节点
            args: 参数列表

        Returns:
            是否成功
        """
        options = self._parse_human_options(args)

        # 从选择器获取目标
        if node.selector_type and node.selector_value:
            options["selector_type"] = node.selector_type
            options["selector_value"] = self._interpolate_variables(self._resolve_value(node.selector_value))

        # 设置默认值
        offset_range = (options.get("offset_min", 3), options.get("offset_max", 10))
        delay_range = (options.get("delay_min", 0.05), options.get("delay_max", 0.3))
        duration_range = (options.get("duration_min", 0.05), options.get("duration_max", 0.15))

        return self.input_service.human_click(
            x=options.get("x"),
            y=options.get("y"),
            selector_type=options.get("selector_type"),
            selector_value=options.get("selector_value"),
            offset_range=offset_range,
            delay_range=delay_range,
            duration_range=duration_range,
        )

    def _execute_human_double_click(self, node: CommandNode, args: List[Any]) -> bool:
        """
        执行人类模拟双击

        语法：
        - human_double_click id:"resource_id"
        - human_double_click 500, 800
        - human_double_click 500, 800, interval_min=0.1, interval_max=0.2

        Args:
            node: 命令节点
            args: 参数列表

        Returns:
            是否成功
        """
        options = self._parse_human_options(args)

        if node.selector_type and node.selector_value:
            options["selector_type"] = node.selector_type
            options["selector_value"] = self._interpolate_variables(self._resolve_value(node.selector_value))

        offset_range = (options.get("offset_min", 3), options.get("offset_max", 8))
        interval_range = (options.get("interval_min", 0.1), options.get("interval_max", 0.2))
        duration_range = (options.get("duration_min", 0.03), options.get("duration_max", 0.08))

        return self.input_service.human_double_click(
            x=options.get("x"),
            y=options.get("y"),
            selector_type=options.get("selector_type"),
            selector_value=options.get("selector_value"),
            offset_range=offset_range,
            interval_range=interval_range,
            duration_range=duration_range,
        )

    def _execute_human_long_press(self, node: CommandNode, args: List[Any]) -> bool:
        """
        执行人类模拟长按

        语法：
        - human_long_press id:"resource_id"
        - human_long_press 500, 800
        - human_long_press 500, 800, duration_min=0.8, duration_max=1.5

        Args:
            node: 命令节点
            args: 参数列表

        Returns:
            是否成功
        """
        options = self._parse_human_options(args)

        if node.selector_type and node.selector_value:
            options["selector_type"] = node.selector_type
            options["selector_value"] = self._interpolate_variables(self._resolve_value(node.selector_value))

        duration_range = (options.get("duration_min", 0.8), options.get("duration_max", 1.5))
        offset_range = (options.get("offset_min", 3), options.get("offset_max", 10))
        delay_range = (options.get("delay_min", 0.05), options.get("delay_max", 0.2))

        return self.input_service.human_long_press(
            x=options.get("x"),
            y=options.get("y"),
            selector_type=options.get("selector_type"),
            selector_value=options.get("selector_value"),
            duration_range=duration_range,
            offset_range=offset_range,
            delay_range=delay_range,
        )

    def _execute_human_drag(self, node: CommandNode, args: List[Any]) -> bool:
        """
        执行人类模拟拖拽

        语法：
        - human_drag 100, 500, 100, 200  # 从 (100,500) 拖到 (100,200)
        - human_drag id:"start_element", id:"end_element"
        - human_drag 100, 500, 100, 200, trajectory="bezier", speed="ease_in_out"
        - human_drag 100, 500, 100, 200, duration=1.5  # 指定拖拽时间

        参数说明：
        - 前四个数字参数：start_x, start_y, end_x, end_y
        - trajectory: 轨迹类型 (bezier, linear_jitter)
        - speed: 速度模式 (ease_in_out, ease_in, ease_out, linear, random)
        - duration: 拖拽总时间（秒），默认 1.0
        - num_points: 轨迹采样点数量

        Args:
            node: 命令节点
            args: 参数列表

        Returns:
            是否成功
        """
        options = self._parse_human_options(args)

        # 解析坐标参数（前四个数字）
        coords = [arg for arg in args if isinstance(arg, (int, float))]
        if len(coords) >= 4:
            options["start_x"] = int(coords[0])
            options["start_y"] = int(coords[1])
            options["end_x"] = int(coords[2])
            options["end_y"] = int(coords[3])

        # 从选择器获取起点（如果有）
        if node.selector_type and node.selector_value:
            options["start_selector_type"] = node.selector_type
            options["start_selector_value"] = self._interpolate_variables(self._resolve_value(node.selector_value))

        # 解析轨迹和速度参数
        trajectory_type = options.get("trajectory", "bezier")
        if trajectory_type not in ("bezier", "linear_jitter"):
            trajectory_type = "bezier"

        speed_mode = options.get("speed", "ease_in_out")
        if speed_mode not in ("ease_in_out", "ease_in", "ease_out", "linear", "random"):
            speed_mode = "ease_in_out"

        duration = options.get("duration", 1.0)
        num_points = options.get("num_points", 50)
        offset_range = (options.get("offset_min", 3), options.get("offset_max", 10))
        jitter_range = (options.get("jitter_min", 1), options.get("jitter_max", 5))
        delay_range = (options.get("delay_min", 0.05), options.get("delay_max", 0.2))

        return self.input_service.human_drag(
            start_x=options.get("start_x"),
            start_y=options.get("start_y"),
            end_x=options.get("end_x"),
            end_y=options.get("end_y"),
            start_selector_type=options.get("start_selector_type"),
            start_selector_value=options.get("start_selector_value"),
            end_selector_type=options.get("end_selector_type"),
            end_selector_value=options.get("end_selector_value"),
            trajectory_type=trajectory_type,  # type: ignore
            speed_mode=speed_mode,  # type: ignore
            duration=duration,
            num_points=num_points,
            offset_range=offset_range,
            jitter_range=jitter_range,
            delay_range=delay_range,
        )


# 导出的公共接口
__all__ = [
    "BreakException",
    "ContinueException",
    "ExecutionContext",
    "ExecutionResult",
    "ScriptExecutor",
]
