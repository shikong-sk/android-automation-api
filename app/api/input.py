"""
输入操作 API 路由模块

提供点击、输入文本、滑动等用户界面交互操作的 REST API 接口。
包括元素定位和查找功能。
"""

from fastapi import APIRouter, Depends, Query
from app.dependencies.services import get_input_service
from app.services import InputService
from app.schemas import ActionRequest, ActionResponse

router = APIRouter(prefix="/input", tags=["Input"])


@router.post("/click", response_model=ActionResponse)
def click(resource_id: str = Query(..., description="元素的 resource-id"), input_service: InputService = Depends(get_input_service)):
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
def click_by_text(text: str = Query(..., description="元素的文本内容"), input_service: InputService = Depends(get_input_service)):
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
def click_by_class(class_name: str = Query(..., description="元素的类名"), input_service: InputService = Depends(get_input_service)):
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
def click_by_xpath(xpath: str = Query(..., description="XPath 表达式"), input_service: InputService = Depends(get_input_service)):
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
def exists_by_text(text: str = Query(..., description="元素的文本内容"), input_service: InputService = Depends(get_input_service)):
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
def exists_by_class(class_name: str = Query(..., description="元素的类名"), input_service: InputService = Depends(get_input_service)):
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
def exists_by_xpath(xpath: str = Query(..., description="XPath 表达式"), input_service: InputService = Depends(get_input_service)):
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
    direction: str = Query(..., description="滑动方向（up/down/left/right）"),
    percent: float = Query(0.5, description="滑动距离比例（0-1）"),
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


@router.get("/find-by-id")
def find_element_by_id(resource_id: str = Query(..., description="元素的 resource-id"), input_service: InputService = Depends(get_input_service)):
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
def find_element_by_text(text: str = Query(..., description="元素的文本内容"), input_service: InputService = Depends(get_input_service)):
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
def find_element_by_class(class_name: str = Query(..., description="元素的类名"), input_service: InputService = Depends(get_input_service)):
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
def find_elements_by_class(class_name: str = Query(..., description="元素的类名"), input_service: InputService = Depends(get_input_service)):
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
def find_element_by_xpath(xpath: str = Query(..., description="XPath 表达式"), input_service: InputService = Depends(get_input_service)):
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
def element_exists(resource_id: str = Query(..., description="元素的 resource-id"), input_service: InputService = Depends(get_input_service)):
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
def get_element_text(resource_id: str = Query(..., description="元素的 resource-id"), input_service: InputService = Depends(get_input_service)):
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
def get_element_bounds(resource_id: str = Query(..., description="元素的 resource-id"), input_service: InputService = Depends(get_input_service)):
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
def wait_for_element(resource_id: str = Query(..., description="元素的 resource-id"), timeout: float = Query(10.0, description="最大等待时间（秒）"), input_service: InputService = Depends(get_input_service)):
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
def wait_for_element_gone(resource_id: str = Query(..., description="元素的 resource-id"), timeout: float = Query(10.0, description="最大等待时间（秒）"), input_service: InputService = Depends(get_input_service)):
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
    input_service: InputService = Depends(get_input_service)
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
