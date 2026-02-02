"""
输入操作 API 路由模块

提供点击、输入文本、滑动等用户界面交互操作的 REST API 接口。
包括元素定位和查找功能，以及人类模拟操作。
"""

from fastapi import APIRouter, Depends, Query
from app.dependencies.services import get_input_service
from app.services import InputService
from app.schemas import (
    ActionRequest,
    ActionResponse,
    HumanClickRequest,
    HumanDoubleClickRequest,
    HumanLongPressRequest,
    HumanDragRequest,
)
from typing import Literal, Optional

router = APIRouter(prefix="/input", tags=["Input"])


@router.post("/click", response_model=ActionResponse)
def click(
    resource_id: str = Query(..., description="元素的 resource-id"),
    input_service: InputService = Depends(get_input_service),
):
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


@router.post("/click-by-text", response_model=ActionResponse)
def click_by_text(
    text: str = Query(..., description="元素的文本内容"),
    input_service: InputService = Depends(get_input_service),
):
    """
    点击元素

    通过 text 定位界面元素并执行点击操作。

    Args:
        text: 元素的文本内容。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.click_by_text(text)
    return ActionResponse(success=result, result={"clicked": text})


@router.post("/click-by-class", response_model=ActionResponse)
def click_by_class(
    class_name: str = Query(..., description="元素的类名"),
    input_service: InputService = Depends(get_input_service),
):
    """
    点击元素

    通过 className 定位界面元素并执行点击操作。

    Args:
        class_name: 元素的类名。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.click_by_class(class_name)
    return ActionResponse(success=result, result={"clicked": class_name})


@router.post("/click-by-xpath", response_model=ActionResponse)
def click_by_xpath(
    xpath: str = Query(..., description="XPath 表达式"),
    input_service: InputService = Depends(get_input_service),
):
    """
    点击元素

    通过 XPath 定位界面元素并执行点击操作。

    Args:
        xpath: XPath 表达式。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.click_by_xpath(xpath)
    return ActionResponse(success=result, result={"clicked": xpath})


@router.get("/exists-by-text", response_model=ActionResponse)
def exists_by_text(
    text: str = Query(..., description="元素的文本内容"),
    input_service: InputService = Depends(get_input_service),
):
    """
    检查元素是否存在

    通过 text 判断指定元素是否存在于当前界面。

    Args:
        text: 元素的文本内容。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    exists = input_service.exists_by_text(text)
    return ActionResponse(success=True, result={"exists": exists, "text": text})


@router.get("/exists-by-class", response_model=ActionResponse)
def exists_by_class(
    class_name: str = Query(..., description="元素的类名"),
    input_service: InputService = Depends(get_input_service),
):
    """
    检查元素是否存在

    通过 className 判断指定元素是否存在于当前界面。

    Args:
        class_name: 元素的类名。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    exists = input_service.exists_by_class(class_name)
    return ActionResponse(success=True, result={"exists": exists, "class_name": class_name})


@router.get("/exists-by-xpath", response_model=ActionResponse)
def exists_by_xpath(
    xpath: str = Query(..., description="XPath 表达式"),
    input_service: InputService = Depends(get_input_service),
):
    """
    检查元素是否存在

    通过 XPath 判断指定元素是否存在于当前界面。

    Args:
        xpath: XPath 表达式。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    exists = input_service.exists_by_xpath(xpath)
    return ActionResponse(success=True, result={"exists": exists, "xpath": xpath})


@router.post("/set-text", response_model=ActionResponse)
def set_text(
    resource_id: str = Query(..., description="元素的 resource-id"),
    text: str = Query(..., description="要输入的文本"),
    input_service: InputService = Depends(get_input_service),
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
def clear_text(
    resource_id: str = Query(..., description="元素的 resource-id"),
    input_service: InputService = Depends(get_input_service),
):
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
    direction: str = Query(..., description="滑动方向（up/down/left/right）"),
    percent: float = Query(0.5, description="滑动距离比例（0-1）"),
    input_service: InputService = Depends(get_input_service),
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
def execute_action(
    request: ActionRequest, input_service: InputService = Depends(get_input_service)
):
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


@router.get("/find-by-id")
def find_element_by_id(
    resource_id: str = Query(..., description="元素的 resource-id"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过 resource-id 查找元素

    根据元素的 resource-id 属性定位界面元素，并返回元素详细信息。

    Args:
        resource_id: 元素的 resource-id 属性值。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 元素信息，包含 text、bounds、className 等信息，元素不存在时返回 exists: false。
    """
    result = input_service.find_element_by_id(resource_id)
    return result or {"exists": False, "resource_id": resource_id}


@router.get("/find-by-text")
def find_element_by_text(
    text: str = Query(..., description="元素的文本内容"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过 text 查找元素

    根据元素的文本内容定位界面元素，并返回元素详细信息。

    Args:
        text: 元素的文本内容。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 元素信息，元素不存在时返回 exists: false。
    """
    result = input_service.find_element_by_text(text)
    return result or {"exists": False, "text": text}


@router.get("/find-by-class")
def find_element_by_class(
    class_name: str = Query(..., description="元素的类名"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过 className 查找元素

    根据元素的类名定位界面元素，返回第一个匹配的元素信息。

    Args:
        class_name: 元素的类名，如 android.widget.Button。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 元素信息，元素不存在时返回 exists: false。
    """
    result = input_service.find_element_by_class(class_name)
    return result or {"exists": False, "class_name": class_name}


@router.get("/find-elements-by-class")
def find_elements_by_class(
    class_name: str = Query(..., description="元素的类名"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过 className 查找所有匹配元素

    根据元素的类名定位所有匹配的界面元素，返回元素信息列表。

    Args:
        class_name: 元素的类名。
        input_service: InputService 实例（依赖注入）。

    Returns:
        list: 所有匹配元素的列表。
    """
    results = input_service.find_elements_by_class(class_name)
    return {"elements": results, "count": len(results)}


@router.get("/find-by-xpath")
def find_element_by_xpath(
    xpath: str = Query(..., description="XPath 表达式"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过 XPath 查找元素

    使用 XPath 表达式定位界面元素，这是最灵活的定位方式。

    Args:
        xpath: XPath 表达式。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 元素信息，元素不存在时返回 exists: false。
    """
    result = input_service.find_element_by_xpath(xpath)
    return result or {"exists": False, "xpath": xpath}


@router.get("/exists")
def element_exists(
    resource_id: str = Query(..., description="元素的 resource-id"),
    input_service: InputService = Depends(get_input_service),
):
    """
    检查元素是否存在

    判断指定元素是否存在于当前界面。

    Args:
        resource_id: 元素的 resource-id 属性值。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 包含 exists: true/false。
    """
    exists = input_service.element_exists(resource_id)
    return {"exists": exists, "resource_id": resource_id}


@router.get("/text")
def get_element_text(
    resource_id: str = Query(..., description="元素的 resource-id"),
    input_service: InputService = Depends(get_input_service),
):
    """
    获取元素文本内容

    获取指定元素的显示文本。

    Args:
        resource_id: 元素的 resource-id 属性值。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 包含元素文本内容。
    """
    text = input_service.get_element_text(resource_id)
    return {"resource_id": resource_id, "text": text}


@router.get("/bounds")
def get_element_bounds(
    resource_id: str = Query(..., description="元素的 resource-id"),
    input_service: InputService = Depends(get_input_service),
):
    """
    获取元素边界位置

    获取指定元素在屏幕上的位置和大小。

    Args:
        resource_id: 元素的 resource-id 属性值。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 包含元素边界信息 {left, top, right, bottom}。
    """
    bounds = input_service.get_element_bounds(resource_id)
    return {"resource_id": resource_id, "bounds": bounds}


@router.get("/wait-appear")
def wait_for_element(
    resource_id: str = Query(..., description="元素的 resource-id"),
    timeout: float = Query(10.0, description="最大等待时间（秒）"),
    input_service: InputService = Depends(get_input_service),
):
    """
    等待元素出现

    等待指定元素出现在界面上。

    Args:
        resource_id: 元素的 resource-id 属性值。
        timeout: 最大等待时间，单位为秒。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 包含等待结果。
    """
    appeared = input_service.wait_for_element(resource_id, timeout)
    return {"resource_id": resource_id, "appeared": appeared, "timeout": timeout}


@router.get("/wait-gone")
def wait_for_element_gone(
    resource_id: str = Query(..., description="元素的 resource-id"),
    timeout: float = Query(10.0, description="最大等待时间（秒）"),
    input_service: InputService = Depends(get_input_service),
):
    """
    等待元素消失

    等待指定元素从界面上消失。

    Args:
        resource_id: 元素的 resource-id 属性值。
        timeout: 最大等待时间，单位为秒。
        input_service: InputService 实例（依赖注入）。

    Returns:
        dict: 包含等待结果。
    """
    gone = input_service.wait_for_element_gone(resource_id, timeout)
    return {"resource_id": resource_id, "gone": gone, "timeout": timeout}


@router.get("/hierarchy")
def get_ui_hierarchy(input_service: InputService = Depends(get_input_service)):
    """
    获取当前界面 XML 结构

    返回当前界面的完整 XML 层次结构。

    Returns:
        dict: 包含 XML 字符串。
    """
    xml = input_service.get_current_ui_xml()
    return {"xml": xml}


@router.post("/screen-on", response_model=ActionResponse)
def screen_on(input_service: InputService = Depends(get_input_service)):
    """
    亮屏

    唤醒设备屏幕。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.screen_on()
    return ActionResponse(success=result, result={"action": "screen_on"})


@router.post("/screen-off", response_model=ActionResponse)
def screen_off(input_service: InputService = Depends(get_input_service)):
    """
    锁屏

    关闭设备屏幕。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.screen_off()
    return ActionResponse(success=result, result={"action": "screen_off"})


@router.post("/unlock", response_model=ActionResponse)
def unlock_screen(input_service: InputService = Depends(get_input_service)):
    """
    解锁屏幕

    解锁设备屏幕。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.unlock_screen()
    return ActionResponse(success=result, result={"action": "unlock"})


@router.post("/send-action", response_model=ActionResponse)
def send_action(
    resource_id: str = Query(..., description="元素的 resource-id"),
    action: str = Query("IME_ACTION_DONE", description="动作类型"),
    input_service: InputService = Depends(get_input_service),
):
    """
    发送完成动作

    向指定元素发送完成动作（如点击回车键）。

    Args:
        resource_id: 元素的 resource-id。
        action: 动作类型，默认为 IME_ACTION_DONE。
        input_service: InputService 实例（依赖注入）。

    Returns:
        ActionResponse: 操作结果响应。
    """
    result = input_service.send_action(resource_id, action)
    return ActionResponse(success=result, result={"resource_id": resource_id, "action": action})


# ============ 通用选择器 API ============


@router.post("/set-text-by-selector", response_model=ActionResponse)
def set_text_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    text: str = Query(..., description="要输入的文本"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器输入文本

    支持多种选择器类型定位元素并输入文本。
    """
    result = input_service.set_text_by_selector(selector_type, selector_value, text)
    return ActionResponse(
        success=result, result={"selector_type": selector_type, "selector_value": selector_value}
    )


@router.post("/clear-text-by-selector", response_model=ActionResponse)
def clear_text_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器清除文本

    支持多种选择器类型定位元素并清除文本。
    """
    result = input_service.clear_text_by_selector(selector_type, selector_value)
    return ActionResponse(
        success=result, result={"selector_type": selector_type, "selector_value": selector_value}
    )


@router.post("/send-action-by-selector", response_model=ActionResponse)
def send_action_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器发送完成动作

    支持多种选择器类型定位元素并发送完成动作。
    """
    result = input_service.send_action_by_selector(selector_type, selector_value)
    return ActionResponse(
        success=result, result={"selector_type": selector_type, "selector_value": selector_value}
    )


@router.get("/wait-appear-by-selector")
def wait_for_element_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    timeout: float = Query(10.0, description="最大等待时间（秒）"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器等待元素出现

    支持多种选择器类型等待元素出现。
    """
    appeared = input_service.wait_for_element_by_selector(selector_type, selector_value, timeout)
    return {
        "selector_type": selector_type,
        "selector_value": selector_value,
        "appeared": appeared,
        "timeout": timeout,
    }


@router.get("/wait-gone-by-selector")
def wait_for_element_gone_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    timeout: float = Query(10.0, description="最大等待时间（秒）"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器等待元素消失

    支持多种选择器类型等待元素消失。
    """
    gone = input_service.wait_for_element_gone_by_selector(selector_type, selector_value, timeout)
    return {
        "selector_type": selector_type,
        "selector_value": selector_value,
        "gone": gone,
        "timeout": timeout,
    }


@router.get("/text-by-selector")
def get_element_text_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器获取元素文本

    支持多种选择器类型获取元素文本内容。
    """
    result = input_service.get_element_text_by_selector(selector_type, selector_value)
    return {"selector_type": selector_type, "selector_value": selector_value, "result": result}


@router.get("/bounds-by-selector")
def get_element_bounds_by_selector(
    selector_type: str = Query(..., description="选择器类型: id, text, class, xpath"),
    selector_value: str = Query(..., description="选择器值"),
    parent_selector_type: Optional[str] = Query(None, description="父元素选择器类型"),
    parent_selector_value: Optional[str] = Query(None, description="父元素选择器值"),
    sibling_selector_type: Optional[str] = Query(None, description="兄弟元素选择器类型"),
    sibling_selector_value: Optional[str] = Query(None, description="兄弟元素选择器值"),
    sibling_relation: str = Query("following", description="兄弟关系: following(之后), preceding(之前)"),
    offset_x: int = Query(0, description="X坐标偏移量"),
    offset_y: int = Query(0, description="Y坐标偏移量"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过选择器获取元素边界

    支持多种选择器类型获取元素边界位置，支持父级/兄弟关系和偏移。
    """
    result = input_service.get_element_bounds_by_selector(
        selector_type,
        selector_value,
        parent_selector_type,
        parent_selector_value,
        sibling_selector_type,
        sibling_selector_value,
        sibling_relation,
        offset_x,
        offset_y,
    )
    return {
        "selector_type": selector_type,
        "selector_value": selector_value,
        "parent_selector_type": parent_selector_type,
        "parent_selector_value": parent_selector_value,
        "sibling_selector_type": sibling_selector_type,
        "sibling_selector_value": sibling_selector_value,
        "sibling_relation": sibling_relation,
        "offset_x": offset_x,
        "offset_y": offset_y,
        "result": result
    }


@router.get("/find-with-parent")
def find_with_parent(
    child_selector_type: str = Query(..., description="子元素选择器类型"),
    child_selector_value: str = Query(..., description="子元素选择器值"),
    parent_selector_type: str = Query(..., description="父元素选择器类型"),
    parent_selector_value: str = Query(..., description="父元素选择器值"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过父元素查找子元素

    验证子元素是否在指定的父元素内部。
    """
    result = input_service.find_with_parent(
        child_selector_type,
        child_selector_value,
        parent_selector_type,
        parent_selector_value,
    )
    return {
        "child_selector_type": child_selector_type,
        "child_selector_value": child_selector_value,
        "parent_selector_type": parent_selector_type,
        "parent_selector_value": parent_selector_value,
        "exists": result
    }


@router.get("/find-with-sibling")
def find_with_sibling(
    target_selector_type: str = Query(..., description="目标元素选择器类型"),
    target_selector_value: str = Query(..., description="目标元素选择器值"),
    sibling_selector_type: str = Query(..., description="兄弟元素选择器类型"),
    sibling_selector_value: str = Query(..., description="兄弟元素选择器值"),
    sibling_relation: str = Query("following", description="兄弟关系: following(之后), preceding(之前)"),
    input_service: InputService = Depends(get_input_service),
):
    """
    通过兄弟元素查找目标元素

    基于兄弟元素的位置关系查找目标元素。
    """
    result = input_service.find_with_sibling(
        target_selector_type,
        target_selector_value,
        sibling_selector_type,
        sibling_selector_value,
        sibling_relation,
    )
    return {
        "target_selector_type": target_selector_type,
        "target_selector_value": target_selector_value,
        "sibling_selector_type": sibling_selector_type,
        "sibling_selector_value": sibling_selector_value,
        "sibling_relation": sibling_relation,
        "exists": result
    }


# ============ 人类模拟操作 API ============


@router.post("/human-click", response_model=ActionResponse)
def human_click(
    request: HumanClickRequest,
    input_service: InputService = Depends(get_input_service),
):
    """
    模拟人类点击操作

    支持通过坐标或选择器定位目标位置，添加随机偏移、延迟和按压时长变化，
    使点击行为更接近真实人类操作。支持父级/兄弟元素定位和坐标偏移。

    特性：
    - 随机点击偏移：在目标位置周围添加随机偏移
    - 随机点击延迟：点击前添加随机延迟
    - 按压时长变化：模拟不同的按压时长
    - 父级/兄弟定位：通过父元素或兄弟元素定位目标
    - 坐标偏移：在元素坐标基础上添加偏移量

    Args:
        request: 包含目标位置和随机化参数的请求体

    Returns:
        ActionResponse: 操作结果响应
    """
    result = input_service.human_click(
        x=request.x,
        y=request.y,
        selector_type=request.selector_type,
        selector_value=request.selector_value,
        parent_selector_type=request.parent_selector_type,
        parent_selector_value=request.parent_selector_value,
        sibling_selector_type=request.sibling_selector_type,
        sibling_selector_value=request.sibling_selector_value,
        sibling_relation=request.sibling_relation,
        offset_x=request.offset_x,
        offset_y=request.offset_y,
        offset_range=(request.offset_min, request.offset_max),
        delay_range=(request.delay_min, request.delay_max),
        duration_range=(request.duration_min, request.duration_max),
    )
    return ActionResponse(
        success=result,
        result={
            "action": "human_click",
            "target": {
                "x": request.x,
                "y": request.y,
                "selector_type": request.selector_type,
                "selector_value": request.selector_value,
                "parent_selector_type": request.parent_selector_type,
                "parent_selector_value": request.parent_selector_value,
                "sibling_selector_type": request.sibling_selector_type,
                "sibling_selector_value": request.sibling_selector_value,
                "sibling_relation": request.sibling_relation,
                "offset_x": request.offset_x,
                "offset_y": request.offset_y,
            },
        },
        message="点击成功" if result else "点击失败，目标元素可能不存在",
    )


@router.post("/human-double-click", response_model=ActionResponse)
def human_double_click(
    request: HumanDoubleClickRequest,
    input_service: InputService = Depends(get_input_service),
):
    """
    模拟人类双击操作

    执行两次快速点击，两次点击之间有随机间隔，
    每次点击位置略有不同，模拟真实人类双击行为。

    Args:
        request: 包含目标位置和随机化参数的请求体

    Returns:
        ActionResponse: 操作结果响应
    """
    result = input_service.human_double_click(
        x=request.x,
        y=request.y,
        selector_type=request.selector_type,
        selector_value=request.selector_value,
        offset_range=(request.offset_min, request.offset_max),
        interval_range=(request.interval_min, request.interval_max),
        duration_range=(request.duration_min, request.duration_max),
    )
    return ActionResponse(
        success=result,
        result={
            "action": "human_double_click",
            "target": {
                "x": request.x,
                "y": request.y,
                "selector_type": request.selector_type,
                "selector_value": request.selector_value,
            },
        },
        message="双击成功" if result else "双击失败，目标元素可能不存在",
    )


@router.post("/human-long-press", response_model=ActionResponse)
def human_long_press(
    request: HumanLongPressRequest,
    input_service: InputService = Depends(get_input_service),
):
    """
    模拟人类长按操作

    执行带有随机时长的长按操作，模拟真实人类长按行为。

    Args:
        request: 包含目标位置和随机化参数的请求体

    Returns:
        ActionResponse: 操作结果响应
    """
    result = input_service.human_long_press(
        x=request.x,
        y=request.y,
        selector_type=request.selector_type,
        selector_value=request.selector_value,
        duration_range=(request.duration_min, request.duration_max),
        offset_range=(request.offset_min, request.offset_max),
        delay_range=(request.delay_min, request.delay_max),
    )
    return ActionResponse(
        success=result,
        result={
            "action": "human_long_press",
            "target": {
                "x": request.x,
                "y": request.y,
                "selector_type": request.selector_type,
                "selector_value": request.selector_value,
            },
        },
        message="长按成功" if result else "长按失败，目标元素可能不存在",
    )


@router.post("/human-drag", response_model=ActionResponse)
def human_drag(
    request: HumanDragRequest,
    input_service: InputService = Depends(get_input_service),
):
    """
    模拟人类拖拽操作

    支持贝塞尔曲线轨迹或带抖动的直线轨迹，以及加速-匀速-减速的速度变化，
    使拖拽行为更接近真实人类操作。

    轨迹类型：
    - bezier: 贝塞尔曲线轨迹，生成平滑的曲线路径，最接近人类手指移动
    - linear_jitter: 直线轨迹 + 随机抖动，模拟手抖效果

    速度模式：
    - ease_in_out: 加速-匀速-减速（推荐），模拟人类拖拽的自然速度变化
    - ease_in: 仅加速，开始慢逐渐加速
    - ease_out: 仅减速，开始快逐渐减速
    - linear: 匀速移动
    - random: 随机速度变化

    起点/终点支持：
    - 坐标到坐标
    - 坐标到元素
    - 元素到坐标
    - 元素到元素

    Args:
        request: 包含起点、终点、轨迹类型和速度模式的请求体

    Returns:
        ActionResponse: 操作结果响应
    """
    result = input_service.human_drag(
        start_x=request.start_x,
        start_y=request.start_y,
        end_x=request.end_x,
        end_y=request.end_y,
        start_selector_type=request.start_selector_type,
        start_selector_value=request.start_selector_value,
        end_selector_type=request.end_selector_type,
        end_selector_value=request.end_selector_value,
        trajectory_type=request.trajectory_type,
        speed_mode=request.speed_mode,
        duration=request.duration,
        num_points=request.num_points,
        offset_range=(request.offset_min, request.offset_max),
        jitter_range=(request.jitter_min, request.jitter_max),
        delay_range=(request.delay_min, request.delay_max),
    )
    return ActionResponse(
        success=result,
        result={
            "action": "human_drag",
            "start": {
                "x": request.start_x,
                "y": request.start_y,
                "selector_type": request.start_selector_type,
                "selector_value": request.start_selector_value,
            },
            "end": {
                "x": request.end_x,
                "y": request.end_y,
                "selector_type": request.end_selector_type,
                "selector_value": request.end_selector_value,
            },
            "trajectory_type": request.trajectory_type,
            "speed_mode": request.speed_mode,
        },
        message="拖拽成功" if result else "拖拽失败，起点或终点元素可能不存在",
    )
