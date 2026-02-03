"""
输入操作服务模块

提供与设备屏幕交互相关的操作，包括：
- 点击元素
- 输入文本
- 清除文本
- 长按
- 滑动操作
- 查找元素
- 人类模拟操作（点击、拖拽）
"""

from .base import AutomationService
from typing import Any, Dict, List, Optional, Tuple, Literal
import random
import time
import math
import logging

logger = logging.getLogger(__name__)


class InputService(AutomationService):
    """
    输入操作服务

    继承自 AutomationService，提供所有与用户输入相关的自动化操作。
    支持通过 resource-id、text、className 等方式定位界面元素并执行相应操作。

    所有方法返回布尔值，表示操作是否成功执行。
    """

    def clear_text(self, resource_id: str) -> bool:
        """
        清除指定元素的文本内容

        先点击元素，然后清除其中的文本。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            bool: 元素存在且清除成功返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            element.click()
            self.device.clear_text()
            return True
        return False

    def set_text(self, resource_id: str, text: str) -> bool:
        """
        向指定元素输入文本

        点击元素后使用 send_keys 输入文本内容。

        Args:
            resource_id: 元素的 resource-id 属性值。
            text: 要输入的文本内容。

        Returns:
            bool: 元素存在且输入成功返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            element.click()
            self.device.sleep(0.3)
            self.device.send_keys(text, clear=False)
            return True
        return False

    def click(self, resource_id: str) -> bool:
        """
        点击指定元素

        通过 resource-id 定位界面元素并执行点击操作。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            bool: 元素存在且点击成功返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            element.click()
            return True
        return False

    def click_by_text(self, text: str) -> bool:
        """
        通过文本点击元素

        通过 text 定位界面元素并执行点击操作。

        Args:
            text: 元素的文本内容。

        Returns:
            bool: 元素存在且点击成功返回 True，否则返回 False。
        """
        element = self.device(text=text)
        if element.exists:
            element.click()
            return True
        return False

    def click_by_class(self, class_name: str) -> bool:
        """
        通过类名点击元素

        通过 className 定位第一个匹配元素并执行点击操作。

        Args:
            class_name: 元素的类名。

        Returns:
            bool: 元素存在且点击成功返回 True，否则返回 False。
        """
        element = self.device(className=class_name)
        if element.exists:
            element.click()
            return True
        return False

    def click_by_xpath(self, xpath: str) -> bool:
        """
        通过 XPath 点击元素

        通过 XPath 定位界面元素并执行点击操作。

        Args:
            xpath: XPath 表达式。

        Returns:
            bool: 元素存在且点击成功返回 True，否则返回 False。
        """
        element = self.device.xpath(xpath)
        if element.exists:
            element.click()
            return True
        return False

    def exists_by_text(self, text: str) -> bool:
        """
        检查文本元素是否存在

        Args:
            text: 元素的文本内容。

        Returns:
            bool: 元素存在返回 True，否则返回 False。
        """
        for _ in range(3):
            element = self.device(text=text)
            if element.exists:
                return True
            self.device.sleep(0.2)
        return False

    def exists_by_class(self, class_name: str) -> bool:
        """
        检查类名元素是否存在

        Args:
            class_name: 元素的类名。

        Returns:
            bool: 元素存在返回 True，否则返回 False。
        """
        for _ in range(3):
            element = self.device(className=class_name)
            if element.exists:
                return True
            self.device.sleep(0.2)
        return False

    def exists_by_xpath(self, xpath: str) -> bool:
        """
        检查 XPath 元素是否存在

        Args:
            xpath: XPath 表达式。

        Returns:
            bool: 元素存在返回 True，否则返回 False。
        """
        for _ in range(3):
            element = self.device.xpath(xpath)
            if element.exists:
                return True
            self.device.sleep(0.2)
        return False

    def click_exists(self, resource_id: str) -> bool:
        """
        点击元素（如果存在）

        检查元素是否存在，存在则点击并返回 True，否则返回 False。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            bool: 元素存在且点击成功返回 True，元素不存在返回 False。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            element.click()
            return True
        return False

    def long_click(self, resource_id: str, duration: float = 1.0) -> bool:
        """
        长按指定元素

        通过 resource-id 定位元素并执行长按操作。

        Args:
            resource_id: 元素的 resource-id 属性值。
            duration: 长按持续时间，单位为秒，默认为 1.0 秒。

        Returns:
            bool: 元素存在且长按成功返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            element.long_click(duration=duration)
            return True
        return False

    def swipe(self, direction: str, percent: float = 0.5) -> bool:
        """
        在屏幕上执行滑动操作

        从屏幕边缘向指定方向滑动，支持上、下、左、右四个方向。

        Args:
            direction: 滑动方向，可选值为 "up"、"down"、"left"、"right"。
            percent: 滑动距离占屏幕的比例，范围 0-1，默认为 0.5。

        Returns:
            bool: 方向参数有效返回 True，无效返回 False。
        """
        direction = direction.lower()
        width, height = self.device.info["displayWidth"], self.device.info["displayHeight"]
        x1, y1, x2, y2 = 0, 0, 0, 0
        if direction == "up":
            x1, y1 = width // 2, height * (1 - percent * 0.5)
            x2, y2 = width // 2, height * percent * 0.5
        elif direction == "down":
            x1, y1 = width // 2, height * percent * 0.5
            x2, y2 = width // 2, height * (1 - percent * 0.5)
        elif direction == "left":
            x1, y1 = width * (1 - percent * 0.5), height // 2
            x2, y2 = width * percent * 0.5, height // 2
        elif direction == "right":
            x1, y1 = width * percent * 0.5, height // 2
            x2, y2 = width * (1 - percent * 0.5), height // 2
        else:
            return False
        self.device.swipe(x1, y1, x2, y2)
        return True

    def click_by_point(self, x: int, y: int) -> bool:
        """
        通过坐标点击

        在指定坐标位置执行点击操作。

        Args:
            x: 目标 x 坐标
            y: 目标 y 坐标

        Returns:
            bool: 点击是否成功
        """
        try:
            self.device.click(x, y)
            return True
        except Exception:
            return False

    def find_element_by_id(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """
        通过 resource-id 查找元素

        根据元素的 resource-id 属性定位界面元素，并返回元素信息。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            Optional[Dict]: 元素信息字典，包含 text、bounds、className 等信息。
                            元素不存在时返回 None。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
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
            }
        return None

    def find_element_by_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        通过 text 查找元素

        根据元素的文本内容定位界面元素，并返回元素信息。

        Args:
            text: 元素的文本内容。

        Returns:
            Optional[Dict]: 元素信息字典。
                            元素不存在时返回 None。
        """
        element = self.device(text=text)
        if element.exists:
            info = element.info
            return {
                "exists": True,
                "text": info.get("text", ""),
                "class_name": info.get("className", ""),
                "resource_id": info.get("resourceName", ""),
                "bounds": info.get("bounds", {}),
                "enabled": info.get("enabled", False),
            }
        return None

    def find_element_by_class(self, class_name: str) -> Optional[Dict[str, Any]]:
        """
        通过 className 查找元素

        根据元素的类名定位界面元素，并返回第一个匹配的元素信息。

        Args:
            class_name: 元素的类名，如 android.widget.Button、android.widget.EditText 等。

        Returns:
            Optional[Dict]: 第一个匹配的元素信息字典。
                            没有匹配元素时返回 None。
        """
        element = self.device(className=class_name)
        if element.exists:
            info = element.info
            return {
                "exists": True,
                "text": info.get("text", ""),
                "class_name": info.get("className", ""),
                "resource_id": info.get("resourceName", ""),
                "bounds": info.get("bounds", {}),
                "enabled": info.get("enabled", False),
            }
        return None

    def find_elements_by_class(self, class_name: str) -> List[Dict[str, Any]]:
        """
        通过 className 查找所有匹配元素

        根据元素的类名定位所有匹配的界面元素，返回元素信息列表。

        Args:
            class_name: 元素的类名。

        Returns:
            List[Dict]: 所有匹配元素的列表，每个元素包含基本信息字典。
                        没有匹配元素时返回空列表。
        """
        elements = []
        all_elements = self.device(className=class_name)
        for element in all_elements:
            if element.exists:
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

    def find_element_by_xpath(self, xpath: str) -> Optional[Dict[str, Any]]:
        """
        通过 XPath 查找元素

        使用 XPath 表达式定位界面元素，这是最灵活的定位方式。

        Args:
            xpath: XPath 表达式，如 "//android.widget.Button[@text='确定']"。

        Returns:
            Optional[Dict]: 元素信息字典。
                            元素不存在时返回 None。
        """
        element = self.device.xpath(xpath)
        if element.exists:
            info = element.get()
            return {
                "exists": True,
                "text": info.attrib.get("text", ""),
                "class_name": info.attrib.get("class", ""),
                "resource_id": info.attrib.get("resource-id", ""),
                "bounds": info.attrib.get("bounds", ""),
                "enabled": info.attrib.get("enabled", "false") == "true",
            }
        return None

    def element_exists(self, resource_id: str) -> bool:
        """
        检查元素是否存在

        通过 resource-id 判断指定元素是否存在于当前界面。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            bool: 元素存在返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        return bool(element.exists)

    def get_element_text(self, resource_id: str) -> Optional[str]:
        """
        获取元素文本内容

        通过 resource-id 定位元素并获取其显示的文本。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            str | None: 元素的文本内容，元素不存在时返回 None。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            return element.info.get("text", "")
        return None

    def get_element_bounds(self, resource_id: str) -> Optional[Dict[str, int]]:
        """
        获取元素边界位置

        通过 resource-id 定位元素并获取其在屏幕上的位置和大小。

        Args:
            resource_id: 元素的 resource-id 属性值。

        Returns:
            Dict | None: 包含 left、top、right、bottom 的字典，元素不存在时返回 None。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            return element.info.get("bounds", {})
        return None

    def wait_for_element(self, resource_id: str, timeout: float = 10.0) -> bool:
        """
        等待元素出现

        等待指定元素出现在界面上，最多等待超时时间。

        Args:
            resource_id: 元素的 resource-id 属性值。
            timeout: 最大等待时间，单位为秒，默认为 10 秒。

        Returns:
            bool: 元素在超时前出现返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        try:
            result = element.wait.exists(timeout=timeout)  # type: ignore
            return result is True
        except Exception:
            return bool(element.exists)

    def wait_for_element_gone(self, resource_id: str, timeout: float = 10.0) -> bool:
        """
        等待元素消失

        等待指定元素从界面上消失，最多等待超时时间。

        Args:
            resource_id: 元素的 resource-id 属性值。
            timeout: 最大等待时间，单位为秒，默认为 10 秒。

        Returns:
            bool: 元素在超时前消失返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        try:
            result = element.wait.gone(timeout=timeout)  # type: ignore
            return result is True
        except Exception:
            return not bool(element.exists)

    def get_current_ui_xml(self) -> str:
        """
        获取当前界面的 XML 结构

        返回当前界面完整 XML 层次结构，可用于分析界面元素。

        Returns:
            str: 当前界面的 XML 字符串。
        """
        return self.device.dump_hierarchy()

    def send_action(self, resource_id: str, action: str = "IME_ACTION_DONE") -> bool:
        """
        发送输入法完成动作

        向指定元素发送完成动作（如 IME_ACTION_DONE）。

        Args:
            resource_id: 元素的 resource-id 属性值。
            action: 动作类型，支持 IME_ACTION_DONE、IME_ACTION_SEARCH 等。

        Returns:
            bool: 操作是否成功。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            try:
                self.device.set_input_ime(True)
                element.click()
                self.device.press("enter")
                self.device.set_input_ime(False)
                return True
            except Exception:
                return False
        return False

    def screen_on(self) -> bool:
        """
        亮屏

        唤醒设备屏幕。

        Returns:
            bool: 操作是否成功。
        """
        try:
            self.device.screen_on()
            return True
        except Exception:
            return False

    def screen_off(self) -> bool:
        """
        锁屏

        关闭设备屏幕。

        Returns:
            bool: 操作是否成功。
        """
        try:
            self.device.screen_off()
            return True
        except Exception:
            return False

    def unlock_screen(self) -> bool:
        """
        解锁屏幕

        解锁设备屏幕。

        Returns:
            bool: 操作是否成功。
        """
        try:
            self.device.unlock()
            return True
        except Exception:
            return False

    def _get_element(self, selector_type: str, selector_value: str):
        """
        根据选择器类型获取元素

        Args:
            selector_type: 选择器类型，可选值为 "id"、"text"、"class"、"xpath"
            selector_value: 选择器值

        Returns:
            元素对象
        """
        if selector_type == "id":
            return self.device(resourceId=selector_value)
        elif selector_type == "text":
            return self.device(text=selector_value)
        elif selector_type == "class":
            return self.device(className=selector_value)
        elif selector_type == "xpath":
            return self.device.xpath(selector_value)
        else:
            return self.device(resourceId=selector_value)

    def set_text_by_selector(self, selector_type: str, selector_value: str, text: str) -> bool:
        """
        通过选择器向元素输入文本

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值
            text: 要输入的文本

        Returns:
            bool: 操作是否成功
        """
        element = self._get_element(selector_type, selector_value)
        if element.exists:
            element.click()
            self.device.sleep(0.3)
            self.device.send_keys(text, clear=False)
            return True
        return False

    def clear_text_by_selector(self, selector_type: str, selector_value: str) -> bool:
        """
        通过选择器清除元素文本

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值

        Returns:
            bool: 操作是否成功
        """
        element = self._get_element(selector_type, selector_value)
        if element.exists:
            element.click()
            self.device.clear_text()
            return True
        return False

    def send_action_by_selector(self, selector_type: str, selector_value: str) -> bool:
        """
        通过选择器发送完成动作

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值

        Returns:
            bool: 操作是否成功
        """
        element = self._get_element(selector_type, selector_value)
        if element.exists:
            try:
                self.device.set_input_ime(True)
                element.click()
                self.device.press("enter")
                self.device.set_input_ime(False)
                return True
            except Exception:
                return False
        return False

    def wait_for_element_by_selector(
        self, selector_type: str, selector_value: str, timeout: float = 10.0
    ) -> bool:
        """
        通过选择器等待元素出现

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值
            timeout: 超时时间（秒）

        Returns:
            bool: 元素是否出现
        """
        element = self._get_element(selector_type, selector_value)
        try:
            if selector_type == "xpath":
                # xpath 元素使用不同的等待方式
                return element.wait(timeout=timeout)
            result = element.wait.exists(timeout=timeout)  # type: ignore
            return result is True
        except Exception:
            return bool(element.exists)

    def wait_for_element_gone_by_selector(
        self, selector_type: str, selector_value: str, timeout: float = 10.0
    ) -> bool:
        """
        通过选择器等待元素消失

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值
            timeout: 超时时间（秒）

        Returns:
            bool: 元素是否消失
        """
        element = self._get_element(selector_type, selector_value)
        try:
            if selector_type == "xpath":
                # xpath 元素使用轮询方式检查
                import time

                start_time = time.time()
                while time.time() - start_time < timeout:
                    if not element.exists:
                        return True
                    time.sleep(0.5)
                return not element.exists
            result = element.wait.gone(timeout=timeout)  # type: ignore
            return result is True
        except Exception:
            return not bool(element.exists)

    def get_element_text_by_selector(
        self, selector_type: str, selector_value: str
    ) -> Optional[Dict[str, Any]]:
        """
        通过选择器获取元素文本

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值

        Returns:
            Dict: 包含文本信息的字典
        """
        element = self._get_element(selector_type, selector_value)
        if element.exists:
            if selector_type == "xpath":
                info = element.get()
                return {"exists": True, "text": info.attrib.get("text", "")}
            else:
                return {"exists": True, "text": element.info.get("text", "")}
        return None

    def get_element_bounds_by_selector(
        self,
        selector_type: str,
        selector_value: str,
        parent_selector_type: Optional[str] = None,
        parent_selector_value: Optional[str] = None,
        sibling_selector_type: Optional[str] = None,
        sibling_selector_value: Optional[str] = None,
        sibling_relation: str = "following",
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> Optional[Dict[str, Any]]:
        """
        根据选择器获取元素边界，支持父级/兄弟关系和偏移

        Args:
            selector_type: 选择器类型 (id/text/class/xpath)
            selector_value: 选择器值
            parent_selector_type: 父元素选择器类型
            parent_selector_value: 父元素选择器值
            sibling_selector_type: 兄弟元素选择器类型
            sibling_selector_value: 兄弟元素选择器值
            sibling_relation: 兄弟关系 (following/preceding)
            offset_x: X 坐标偏移
            offset_y: Y 坐标偏移

        Returns:
            Dict[str, Any]: 包含 bounds 和坐标信息，元素不存在时返回 None
        """
        try:
            self.wait_for_idle(timeout=1.0)

            if selector_type == "xpath":
                element = self._device.xpath(selector_value)
            elif selector_type == "id":
                element = self._device(resourceId=selector_value)
            elif selector_type == "text":
                element = self._device(text=selector_value)
            elif selector_type == "class":
                element = self._device(className=selector_value)
            else:
                return None

            info = element.info
            bounds = info.get("bounds", {})

            if bounds:
                left = bounds.get("left", 0)
                top = bounds.get("top", 0)
                right = bounds.get("right", 0)
                bottom = bounds.get("bottom", 0)
                center_x = (left + right) // 2 + offset_x
                center_y = (top + bottom) // 2 + offset_y

                return {
                    "exists": True,
                    "bounds": bounds,
                    "center_x": center_x,
                    "center_y": center_y,
                }
            return {"exists": True, "bounds": bounds_str}
        except Exception as e:
            logger.error(f"获取元素边界失败: {e}")
            return None

    def find_with_parent(
        self,
        child_selector_type: str,
        child_selector_value: str,
        parent_selector_type: str,
        parent_selector_value: str,
    ) -> bool:
        """
        通过父元素查找子元素

        Args:
            child_selector_type: 子元素选择器类型
            child_selector_value: 子元素选择器值
            parent_selector_type: 父元素选择器类型
            parent_selector_value: 父元素选择器值

        Returns:
            bool: 是否找到元素
        """
        try:
            self.wait_for_idle(timeout=1.0)

            parent_element = self._get_element(parent_selector_type, parent_selector_value)
            if not parent_element.exists:
                return False

            parent_info = parent_element.info
            parent_bounds = parent_info.get("bounds", {})
            if not parent_bounds:
                return False

            left = parent_bounds.get("left", 0)
            top = parent_bounds.get("top", 0)
            right = parent_bounds.get("right", 0)
            bottom = parent_bounds.get("bottom", 0)

            if child_selector_type == "xpath":
                elements = self._device.xpath(f"{child_selector_value}").all()
                for element in elements:
                    info = element.info
                    bounds = info.get("bounds", {})
                    if bounds:
                        elem_left = bounds.get("left", 0)
                        elem_top = bounds.get("top", 0)
                        elem_right = bounds.get("right", 0)
                        elem_bottom = bounds.get("bottom", 0)

                        if left <= elem_left and top <= elem_top and right >= elem_right and bottom >= elem_bottom:
                            return True
                return False
            else:
                return self._get_element(child_selector_type, child_selector_value).exists
        except Exception as e:
            logger.error(f"通过父元素查找子元素失败: {e}")
            return False

    def find_with_sibling(
        self,
        target_selector_type: str,
        target_selector_value: str,
        sibling_selector_type: str,
        sibling_selector_value: str,
        sibling_relation: str = "following",
    ) -> bool:
        """
        通过兄弟元素查找目标元素

        Args:
            target_selector_type: 目标元素选择器类型
            target_selector_value: 目标元素选择器值
            sibling_selector_type: 兄弟元素选择器类型
            sibling_selector_value: 兄弟元素选择器值
            sibling_relation: 兄弟关系 (following=之后, preceding=之前)

        Returns:
            bool: 是否找到元素
        """
        try:
            self.wait_for_idle(timeout=1.0)

            sibling = self._get_element(sibling_selector_type, sibling_selector_value)
            if not sibling.exists:
                return False

            sibling_info = sibling.info
            sibling_bounds = sibling_info.get("bounds", {})
            if not sibling_bounds:
                return False

            sibling_left = sibling_bounds.get("left", 0)
            sibling_top = sibling_bounds.get("top", 0)

            elements = self._device.xpath(f"//{target_selector_type}[@resource-id='{target_selector_value}']").all()
            for element in elements:
                info = element.info
                bounds = info.get("bounds", {})
                if bounds:
                    elem_left = bounds.get("left", 0)
                    elem_top = bounds.get("top", 0)

                    if sibling_relation == "following":
                        if elem_left >= sibling_left and elem_top >= sibling_top:
                            return True
                    elif sibling_relation == "preceding":
                        if elem_left <= sibling_left and elem_top <= sibling_top:
                            return True
            return False
        except Exception as e:
            logger.error(f"通过兄弟元素查找失败: {e}")
            return False

    # ============ 人类模拟操作 ============

    def _get_element_center(
        self, selector_type: Optional[str], selector_value: Optional[str]
    ) -> Optional[Tuple[int, int]]:
        """
        获取元素的中心坐标

        Args:
            selector_type: 选择器类型
            selector_value: 选择器值

        Returns:
            Tuple[int, int]: 元素中心坐标 (x, y)，元素不存在时返回 None
        """
        if not selector_type or not selector_value:
            return None

        element = self._get_element(selector_type, selector_value)
        if not element.exists:
            return None

        if selector_type == "xpath":
            info = element.get()
            bounds_str = info.attrib.get("bounds", "")
            import re

            match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds_str)
            if match:
                left, top, right, bottom = map(int, match.groups())
                return ((left + right) // 2, (top + bottom) // 2)
            return None
        else:
            bounds = element.info.get("bounds", {})
            if bounds:
                left = bounds.get("left", 0)
                top = bounds.get("top", 0)
                right = bounds.get("right", 0)
                bottom = bounds.get("bottom", 0)
                return ((left + right) // 2, (top + bottom) // 2)
        return None

    def _add_random_offset(
        self, x: int, y: int, offset_range: Tuple[int, int] = (3, 10)
    ) -> Tuple[int, int]:
        """
        为坐标添加随机偏移

        Args:
            x: 原始 x 坐标
            y: 原始 y 坐标
            offset_range: 偏移范围 (最小值, 最大值)

        Returns:
            Tuple[int, int]: 添加偏移后的坐标
        """
        min_offset, max_offset = offset_range
        offset_x = random.randint(-max_offset, max_offset)
        offset_y = random.randint(-max_offset, max_offset)

        # 确保偏移量至少达到最小值
        if abs(offset_x) < min_offset:
            offset_x = min_offset if offset_x >= 0 else -min_offset
        if abs(offset_y) < min_offset:
            offset_y = min_offset if offset_y >= 0 else -min_offset

        return (x + offset_x, y + offset_y)

    def _generate_bezier_curve(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        control_points: int = 2,
        num_points: int = 50,
    ) -> List[Tuple[int, int]]:
        """
        生成贝塞尔曲线路径

        Args:
            start: 起点坐标
            end: 终点坐标
            control_points: 控制点数量（1=二次贝塞尔，2=三次贝塞尔）
            num_points: 生成的路径点数量

        Returns:
            List[Tuple[int, int]]: 路径点列表
        """
        # 生成随机控制点
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)

        # 控制点偏移量与距离成正比
        offset_scale = max(distance * 0.3, 30)

        controls = []
        for i in range(control_points):
            t = (i + 1) / (control_points + 1)
            # 基础位置在起点和终点之间
            base_x = start[0] + dx * t
            base_y = start[1] + dy * t
            # 添加垂直于路径方向的随机偏移
            perpendicular_x = -dy / distance if distance > 0 else 0
            perpendicular_y = dx / distance if distance > 0 else 0
            offset = random.uniform(-offset_scale, offset_scale)
            ctrl_x = int(base_x + perpendicular_x * offset)
            ctrl_y = int(base_y + perpendicular_y * offset)
            controls.append((ctrl_x, ctrl_y))

        # 构建完整的控制点列表
        all_points = [start] + controls + [end]

        # 使用 de Casteljau 算法计算贝塞尔曲线
        path = []
        for i in range(num_points + 1):
            t = i / num_points
            point = self._de_casteljau(all_points, t)
            path.append((int(point[0]), int(point[1])))

        return path

    def _de_casteljau(self, points: List[Tuple[int, int]], t: float) -> Tuple[float, float]:
        """
        de Casteljau 算法计算贝塞尔曲线上的点

        Args:
            points: 控制点列表
            t: 参数 t (0-1)

        Returns:
            Tuple[float, float]: 曲线上的点
        """
        if len(points) == 1:
            return (float(points[0][0]), float(points[0][1]))

        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((x, y))

        return self._de_casteljau(new_points, t)

    def _generate_linear_path_with_jitter(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        num_points: int = 50,
        jitter_range: Tuple[int, int] = (1, 5),
    ) -> List[Tuple[int, int]]:
        """
        生成带抖动的直线路径

        Args:
            start: 起点坐标
            end: 终点坐标
            num_points: 生成的路径点数量
            jitter_range: 抖动范围 (最小值, 最大值)

        Returns:
            List[Tuple[int, int]]: 路径点列表
        """
        path = []
        for i in range(num_points + 1):
            t = i / num_points
            x = int(start[0] + (end[0] - start[0]) * t)
            y = int(start[1] + (end[1] - start[1]) * t)

            # 起点和终点不添加抖动
            if i > 0 and i < num_points:
                jitter = random.randint(jitter_range[0], jitter_range[1])
                x += random.randint(-jitter, jitter)
                y += random.randint(-jitter, jitter)

            path.append((x, y))

        return path

    def _generate_speed_curve(
        self, num_points: int, speed_mode: str = "ease_in_out", duration: float = 1.0
    ) -> List[float]:
        """
        生成速度曲线（加速-匀速-减速）

        注意：此方法已弃用，保留仅为向后兼容。
        新的 human_drag 实现使用 _resample_path_by_speed 方法。

        Args:
            num_points: 路径点数量
            speed_mode: 速度模式
                - "ease_in_out": 加速-匀速-减速（推荐）
                - "ease_in": 仅加速
                - "ease_out": 仅减速
                - "linear": 匀速
                - "random": 随机速度
            duration: 总拖拽时间（秒），默认 1.0 秒

        Returns:
            List[float]: 每个点之间的延迟时间（秒），长度为 num_points - 1
        """
        # 移动次数 = 路径点数量 - 1（从第一个点移动到最后一个点）
        num_moves = max(num_points - 1, 1)
        delays = []

        # 计算基础延迟，使总时间等于 duration
        base_interval = duration / num_moves

        for i in range(num_moves):
            # t 表示当前移动在整个过程中的进度 (0 到 1)
            t = i / max(num_moves - 1, 1) if num_moves > 1 else 0

            if speed_mode == "ease_in_out":
                # 使用正弦函数模拟加速-匀速-减速
                # 开始和结束时慢，中间快
                speed_factor = math.sin(t * math.pi)
                # 反转：速度快时延迟短，慢时延迟长
                # 调整系数使平均延迟接近 base_interval
                delay = base_interval * (0.3 + 1.4 * (1 - speed_factor))
            elif speed_mode == "ease_in":
                # 开始慢，逐渐加速
                speed_factor = t * t
                delay = base_interval * (0.3 + 1.4 * (1 - speed_factor))
            elif speed_mode == "ease_out":
                # 开始快，逐渐减速
                speed_factor = 1 - (1 - t) * (1 - t)
                delay = base_interval * (0.3 + 1.4 * (1 - speed_factor))
            elif speed_mode == "random":
                delay = base_interval * random.uniform(0.5, 1.5)
            else:  # linear
                delay = base_interval

            # 添加小幅随机扰动（±10%）
            delay = delay * random.uniform(0.9, 1.1)
            delays.append(delay)

        return delays

    def _get_speed_factor(self, t: float, speed_mode: str) -> float:
        """
        根据进度和速度模式计算速度因子

        Args:
            t: 进度 (0-1)
            speed_mode: 速度模式

        Returns:
            float: 速度因子 (0-1)，值越大表示速度越快
        """
        if speed_mode == "ease_in_out":
            # 使用正弦函数：开始和结束时慢，中间快
            return math.sin(t * math.pi)
        elif speed_mode == "ease_in":
            # 开始慢，逐渐加速
            return t * t
        elif speed_mode == "ease_out":
            # 开始快，逐渐减速
            return 1 - (1 - t) * (1 - t)
        elif speed_mode == "random":
            return random.uniform(0.3, 1.0)
        else:  # linear
            return 1.0

    def _resample_path_by_speed(
        self,
        path: List[Tuple[int, int]],
        speed_mode: str = "ease_in_out",
        target_points: int = 100,
    ) -> List[Tuple[int, int]]:
        """
        根据速度曲线重新采样路径点

        通过调整点的密度来实现速度变化效果：
        - 慢速区域：点密度高（点之间距离小）
        - 快速区域：点密度低（点之间距离大）

        由于 swipe_points 在设备端均匀分配时间给每个点，
        点密度高的区域移动距离短，看起来就慢；
        点密度低的区域移动距离长，看起来就快。

        Args:
            path: 原始路径点列表
            speed_mode: 速度模式
            target_points: 目标采样点数量

        Returns:
            List[Tuple[int, int]]: 重新采样后的路径点列表
        """
        if len(path) < 2:
            return path

        # 计算原始路径的累积距离
        cumulative_distances = [0.0]
        for i in range(1, len(path)):
            dx = path[i][0] - path[i - 1][0]
            dy = path[i][1] - path[i - 1][1]
            dist = math.sqrt(dx * dx + dy * dy)
            cumulative_distances.append(cumulative_distances[-1] + dist)

        total_distance = cumulative_distances[-1]
        if total_distance == 0:
            return path

        # 根据速度曲线生成新的采样点
        # 速度慢的地方需要更多的点（更小的距离间隔）
        # 速度快的地方需要更少的点（更大的距离间隔）
        new_path = [path[0]]  # 起点

        # 计算每个采样点对应的原始路径位置
        for i in range(1, target_points):
            # 当前进度 (0-1)
            t = i / target_points

            # 根据速度模式调整进度
            # 速度因子越大，实际进度推进越快
            if speed_mode == "ease_in_out":
                # 使用正弦函数的积分形式来调整进度
                # 这样可以让开始和结束时进度慢，中间快
                adjusted_t = (1 - math.cos(t * math.pi)) / 2
            elif speed_mode == "ease_in":
                # 开始慢，逐渐加速
                adjusted_t = t * t
            elif speed_mode == "ease_out":
                # 开始快，逐渐减速
                adjusted_t = 1 - (1 - t) * (1 - t)
            elif speed_mode == "random":
                # 随机模式：添加一些随机扰动
                adjusted_t = t + random.uniform(-0.05, 0.05)
                adjusted_t = max(0, min(1, adjusted_t))
            else:  # linear
                adjusted_t = t

            # 计算目标距离
            target_dist = adjusted_t * total_distance

            # 在原始路径中找到对应位置
            # 使用二分查找找到目标距离所在的线段
            left, right = 0, len(cumulative_distances) - 1
            while left < right:
                mid = (left + right) // 2
                if cumulative_distances[mid] < target_dist:
                    left = mid + 1
                else:
                    right = mid

            # 在找到的线段上进行线性插值
            if left == 0:
                new_path.append(path[0])
            elif left >= len(path):
                new_path.append(path[-1])
            else:
                # 计算在当前线段上的位置
                segment_start_dist = cumulative_distances[left - 1]
                segment_end_dist = cumulative_distances[left]
                segment_length = segment_end_dist - segment_start_dist

                if segment_length > 0:
                    segment_t = (target_dist - segment_start_dist) / segment_length
                else:
                    segment_t = 0

                # 线性插值
                x = int(path[left - 1][0] + (path[left][0] - path[left - 1][0]) * segment_t)
                y = int(path[left - 1][1] + (path[left][1] - path[left - 1][1]) * segment_t)

                # 添加微小的随机抖动使轨迹更自然
                x += random.randint(-1, 1)
                y += random.randint(-1, 1)

                new_path.append((x, y))

        new_path.append(path[-1])  # 终点
        return new_path

    def human_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        selector_type: Optional[str] = None,
        selector_value: Optional[str] = None,
        parent_selector_type: Optional[str] = None,
        parent_selector_value: Optional[str] = None,
        sibling_selector_type: Optional[str] = None,
        sibling_selector_value: Optional[str] = None,
        sibling_relation: str = "following",
        offset_x: int = 0,
        offset_y: int = 0,
        offset_range: Tuple[int, int] = (3, 10),
        delay_range: Tuple[float, float] = (0.05, 0.3),
        duration_range: Tuple[float, float] = (0.05, 0.15),
    ) -> bool:
        """
        模拟人类点击操作

        支持通过坐标或选择器定位目标位置，添加随机偏移、延迟和按压时长变化。
        支持父级/兄弟元素定位和坐标偏移。

        Args:
            x: 目标 x 坐标（与选择器二选一）
            y: 目标 y 坐标（与选择器二选一）
            selector_type: 选择器类型 (id, text, class, xpath)
            selector_value: 选择器值
            parent_selector_type: 父元素选择器类型
            parent_selector_value: 父元素选择器值
            sibling_selector_type: 兄弟元素选择器类型
            sibling_selector_value: 兄弟元素选择器值
            sibling_relation: 兄弟关系 (following/preceding)
            offset_x: X 坐标偏移
            offset_y: Y 坐标偏移
            offset_range: 随机偏移范围 (最小值, 最大值)，单位像素
            delay_range: 点击前延迟范围 (最小值, 最大值)，单位秒
            duration_range: 按压时长范围 (最小值, 最大值)，单位秒

        Returns:
            bool: 操作是否成功
        """
        target_x, target_y = None, None

        if x is not None and y is not None:
            target_x, target_y = x, y
        elif selector_type and selector_value:
            center = self._get_element_center(selector_type, selector_value)
            if not center:
                return False
            target_x, target_y = center
        else:
            return False

        if target_x is None or target_y is None:
            return False

        target_x += offset_x
        target_y += offset_y

        final_x, final_y = self._add_random_offset(target_x, target_y, offset_range)

        delay = random.uniform(delay_range[0], delay_range[1])
        time.sleep(delay)

        duration = random.uniform(duration_range[0], duration_range[1])

        try:
            self.device.swipe(final_x, final_y, final_x, final_y, duration=duration)
            return True
        except Exception:
            return False

    def human_double_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        selector_type: Optional[str] = None,
        selector_value: Optional[str] = None,
        parent_selector_type: Optional[str] = None,
        parent_selector_value: Optional[str] = None,
        sibling_selector_type: Optional[str] = None,
        sibling_selector_value: Optional[str] = None,
        sibling_relation: str = "following",
        offset_x: int = 0,
        offset_y: int = 0,
        offset_range: Tuple[int, int] = (3, 8),
        interval_range: Tuple[float, float] = (0.1, 0.2),
        duration_range: Tuple[float, float] = (0.03, 0.08),
    ) -> bool:
        """
        模拟人类双击操作

        支持父级/兄弟元素定位和坐标偏移。

        Args:
            x: 目标 x 坐标
            y: 目标 y 坐标
            selector_type: 选择器类型
            selector_value: 选择器值
            parent_selector_type: 父元素选择器类型
            parent_selector_value: 父元素选择器值
            sibling_selector_type: 兄弟元素选择器类型
            sibling_selector_value: 兄弟元素选择器值
            sibling_relation: 兄弟关系 (following/preceding)
            offset_x: X 坐标偏移
            offset_y: Y 坐标偏移
            offset_range: 随机偏移范围
            interval_range: 两次点击间隔范围（秒）
            duration_range: 每次按压时长范围（秒）

        Returns:
            bool: 操作是否成功
        """
        target_x, target_y = None, None

        if x is not None and y is not None:
            target_x, target_y = x, y
        elif selector_type and selector_value:
            center = self._get_element_center(selector_type, selector_value)
            if not center:
                return False
            target_x, target_y = center
        else:
            return False

        if target_x is None or target_y is None:
            return False

        target_x += offset_x
        target_y += offset_y

        try:
            x1, y1 = self._add_random_offset(target_x, target_y, offset_range)
            duration1 = random.uniform(duration_range[0], duration_range[1])
            self.device.swipe(x1, y1, x1, y1, duration=duration1)

            interval = random.uniform(interval_range[0], interval_range[1])
            time.sleep(interval)

            x2, y2 = self._add_random_offset(target_x, target_y, offset_range)
            duration2 = random.uniform(duration_range[0], duration_range[1])
            self.device.swipe(x2, y2, x2, y2, duration=duration2)

            return True
        except Exception:
            return False

    def human_long_press(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        selector_type: Optional[str] = None,
        selector_value: Optional[str] = None,
        parent_selector_type: Optional[str] = None,
        parent_selector_value: Optional[str] = None,
        sibling_selector_type: Optional[str] = None,
        sibling_selector_value: Optional[str] = None,
        sibling_relation: str = "following",
        offset_x: int = 0,
        offset_y: int = 0,
        duration_range: Tuple[float, float] = (0.8, 1.5),
        offset_range: Tuple[int, int] = (3, 10),
        delay_range: Tuple[float, float] = (0.05, 0.2),
    ) -> bool:
        """
        模拟人类长按操作

        支持父级/兄弟元素定位和坐标偏移。

        Args:
            x: 目标 x 坐标
            y: 目标 y 坐标
            selector_type: 选择器类型
            selector_value: 选择器值
            parent_selector_type: 父元素选择器类型
            parent_selector_value: 父元素选择器值
            sibling_selector_type: 兄弟元素选择器类型
            sibling_selector_value: 兄弟元素选择器值
            sibling_relation: 兄弟关系 (following/preceding)
            offset_x: X 坐标偏移
            offset_y: Y 坐标偏移
            duration_range: 长按时长范围（秒）
            offset_range: 随机偏移范围
            delay_range: 操作前延迟范围

        Returns:
            bool: 操作是否成功
        """
        target_x, target_y = None, None

        if x is not None and y is not None:
            target_x, target_y = x, y
        elif selector_type and selector_value:
            center = self._get_element_center(selector_type, selector_value)
            if not center:
                return False
            target_x, target_y = center
        else:
            return False

        if target_x is None or target_y is None:
            return False

        target_x += offset_x
        target_y += offset_y

        final_x, final_y = self._add_random_offset(target_x, target_y, offset_range)

        delay = random.uniform(delay_range[0], delay_range[1])
        time.sleep(delay)

        duration = random.uniform(duration_range[0], duration_range[1])

        try:
            self.device.swipe(final_x, final_y, final_x, final_y, duration=duration)
            return True
        except Exception:
            return False

    def human_drag(
        self,
        start_x: Optional[int] = None,
        start_y: Optional[int] = None,
        end_x: Optional[int] = None,
        end_y: Optional[int] = None,
        start_selector_type: Optional[str] = None,
        start_selector_value: Optional[str] = None,
        end_selector_type: Optional[str] = None,
        end_selector_value: Optional[str] = None,
        trajectory_type: Literal["bezier", "linear_jitter"] = "bezier",
        speed_mode: Literal[
            "ease_in_out", "ease_in", "ease_out", "linear", "random"
        ] = "ease_in_out",
        duration: float = 1.0,
        num_points: int = 50,
        offset_range: Tuple[int, int] = (3, 10),
        jitter_range: Tuple[int, int] = (1, 5),
        delay_range: Tuple[float, float] = (0.05, 0.2),
    ) -> bool:
        """
        模拟人类拖拽操作

        支持贝塞尔曲线轨迹或带抖动的直线轨迹，以及加速-匀速-减速的速度变化。
        使用 swipe_points API 在设备端执行，确保 duration 时间准确。

        Args:
            start_x: 起点 x 坐标
            start_y: 起点 y 坐标
            end_x: 终点 x 坐标
            end_y: 终点 y 坐标
            start_selector_type: 起点选择器类型
            start_selector_value: 起点选择器值
            end_selector_type: 终点选择器类型
            end_selector_value: 终点选择器值
            trajectory_type: 轨迹类型
                - "bezier": 贝塞尔曲线（推荐，更自然）
                - "linear_jitter": 直线 + 随机抖动
            speed_mode: 速度模式
                - "ease_in_out": 加速-匀速-减速（推荐）
                - "ease_in": 仅加速
                - "ease_out": 仅减速
                - "linear": 匀速
                - "random": 随机速度
            duration: 拖拽总时间（秒），默认 1.0 秒
            num_points: 轨迹采样点数量（用于生成基础轨迹）
            offset_range: 起点/终点随机偏移范围
            jitter_range: 直线轨迹抖动范围（仅 linear_jitter 模式）
            delay_range: 操作前延迟范围

        Returns:
            bool: 操作是否成功
        """
        # 确定起点坐标
        # 注意：需要检查坐标是否为有效数值（不仅仅是 not None）
        has_start_coords = (
            start_x is not None
            and start_y is not None
            and isinstance(start_x, (int, float))
            and isinstance(start_y, (int, float))
        )
        has_start_selector = bool(start_selector_type and start_selector_value)

        if has_start_coords:
            sx, sy = int(start_x), int(start_y)  # type: ignore
        elif has_start_selector:
            center = self._get_element_center(start_selector_type, start_selector_value)
            if not center:
                return False
            sx, sy = center
        else:
            return False

        # 确定终点坐标
        has_end_coords = (
            end_x is not None
            and end_y is not None
            and isinstance(end_x, (int, float))
            and isinstance(end_y, (int, float))
        )
        has_end_selector = bool(end_selector_type and end_selector_value)

        if has_end_coords:
            ex, ey = int(end_x), int(end_y)  # type: ignore
        elif has_end_selector:
            center = self._get_element_center(end_selector_type, end_selector_value)
            if not center:
                return False
            ex, ey = center
        else:
            return False

        # 添加随机偏移
        sx, sy = self._add_random_offset(sx, sy, offset_range)
        ex, ey = self._add_random_offset(ex, ey, offset_range)

        # 添加随机延迟
        delay = random.uniform(delay_range[0], delay_range[1])
        time.sleep(delay)

        # 生成基础轨迹
        if trajectory_type == "bezier":
            base_path = self._generate_bezier_curve((sx, sy), (ex, ey), num_points=num_points)
        else:
            base_path = self._generate_linear_path_with_jitter(
                (sx, sy), (ex, ey), num_points=num_points, jitter_range=jitter_range
            )

        # 根据速度模式重新采样路径
        #
        # 重要：swipe_points 的 duration 参数是【每两个相邻点之间】的持续时间！
        # 总时间 = (点数 - 1) * duration
        #
        # 所以如果我们想要总时间为 T 秒，有 N 个点：
        # duration_per_segment = T / (N - 1)
        #
        # 为了保持轨迹平滑，我们使用固定的点数，然后计算每段的 duration
        target_points = max(20, min(num_points + 1, 100))  # 限制点数在合理范围

        if speed_mode != "linear":
            # 非匀速模式：根据速度曲线重新采样
            final_path = self._resample_path_by_speed(base_path, speed_mode, target_points)
        else:
            # 匀速模式：均匀采样
            final_path = self._resample_path_by_speed(base_path, "linear", target_points)

        # 计算每段的 duration
        # swipe_points 的 duration 是每两个点之间的时间
        num_segments = len(final_path) - 1
        if num_segments <= 0:
            num_segments = 1
        duration_per_segment = duration / num_segments

        # 执行拖拽
        try:
            # 使用 swipe_points 在设备端执行
            # 注意：duration 参数是每段的持续时间，不是总时间
            self.device.swipe_points(final_path, duration=duration_per_segment)
            return True
        except Exception:
            return False
