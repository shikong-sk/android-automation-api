"""
输入操作 API 路由模块

提供点击、输入文本、滑动等用户界面交互操作的 REST API 接口。
"""

from fastapi import APIRouter, Depends, Query
from app.dependencies.services import get_input_service
from app.services import InputService
from app.schemas import ActionRequest, ActionResponse

router = APIRouter(prefix="/input", tags=["Input"])


@router.post("/click", response_model=ActionResponse)
def click(resource_id: str, input_service: InputService = Depends(get_input_service)):
    """
    点击元素

    通过 resource-id 定位界面元素并执行点击操作。

    Args:
        resource_id: 元素的 resource-id 属性值。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.click(resource_id)
    return ActionResponse(success=result, result={"clicked": resource_id})


@router.post("/set-text", response_model=ActionResponse)
def set_text(
    resource_id: str = Query(..., description="元素的 resource-id"),
    text: str = Query(..., description="要输入的文本"),
    input_service: InputService = Depends(get_input_service)
):
    """
    输入文本

    向指定的输入框元素输入文本内容。

    Args:
        resource_id: 输入框元素的 resource-id。
        text: 要输入的文本内容。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.set_text(resource_id, text)
    return ActionResponse(success=result, result={"resource_id": resource_id, "text": text})


@router.post("/clear-text", response_model=ActionResponse)
def clear_text(resource_id: str = Query(..., description="元素的 resource-id"), input_service: InputService = Depends(get_input_service)):
    """
    清除文本

    清除指定输入框中的文本内容。

    Args:
        resource_id: 输入框元素的 resource-id。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.clear_text(resource_id)
    return ActionResponse(success=result, result={"cleared": resource_id})


@router.post("/swipe", response_model=ActionResponse)
def swipe(
    direction: str,
    percent: float = 0.5,
    input_service: InputService = Depends(get_input_service)
):
    """
    滑动屏幕

    在屏幕上执行指定方向的滑动操作。

    Args:
        direction: 滑动方向，可选值为 "up"、"down"、"left"、"right"。
        percent: 滑动距离占屏幕的比例，范围 0-1，默认 0.5。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.swipe(direction, percent)
    return ActionResponse(success=result, result={"direction": direction, "percent": percent})


@router.post("/execute", response_model=ActionResponse)
def execute_action(request: ActionRequest, input_service: InputService = Depends(get_input_service)):
    """
    执行自定义操作

    动态执行 InputService 中的任意方法。

    Args:
        request: 包含操作名称和参数的请求体。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    return input_service.execute(request.action, **request.params)
