"""
输入操作服务模块

提供与设备屏幕交互相关的操作，包括：
- 点击元素
- 输入文本
- 清除文本
- 长按
- 滑动操作
- 查找元素
"""

from .base import AutomationService
from typing import Any, Dict, List, Optional


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
        element = self.device(xpath=xpath)
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
            element = self.device(xpath=xpath)
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
                "selected": info.get("selected", False)
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
                "enabled": info.get("enabled", False)
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
                "enabled": info.get("enabled", False)
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
                elements.append({
                    "text": info.get("text", ""),
                    "class_name": info.get("className", ""),
                    "resource_id": info.get("resourceName", ""),
                    "bounds": info.get("bounds", {}),
                    "enabled": info.get("enabled", False)
                })
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
        element = self.device(xpath=xpath)
        if element.exists:
            info = element.info
            return {
                "exists": True,
                "text": info.get("text", ""),
                "class_name": info.get("className", ""),
                "resource_id": info.get("resourceName", ""),
                "bounds": info.get("bounds", {}),
                "enabled": info.get("enabled", False)
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
