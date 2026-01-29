"""
输入操作服务模块

提供与设备屏幕交互相关的操作，包括：
- 点击元素
- 输入文本
- 清除文本
- 长按
- 滑动操作
"""

from .base import AutomationService
import time


class InputService(AutomationService):
    """
    输入操作服务

    继承自 AutomationService，提供所有与用户输入相关的自动化操作。
    支持通过 resource-id 定位界面元素并执行相应操作。

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
        element = self.device(resource_id=resource_id)
        if element.exists:
            element.click()
            self.device.clear_text()
            return True
        return False

    def set_text(self, resource_id: str, text: str) -> bool:
        """
        向指定元素输入文本

        先点击元素，清除已有文本，等待片刻后输入新文本。

        Args:
            resource_id: 元素的 resource-id 属性值。
            text: 要输入的文本内容。

        Returns:
            bool: 元素存在且输入成功返回 True，否则返回 False。
        """
        element = self.device(resourceId=resource_id)
        if element.exists:
            element.click()
            self.device.clear_text()
            self.device.sleep(0.5)
            element.set_text(text)
            return True
        return False

    def click(self, resource_id: str) -> bool:
        """
        点击指定元素

        通过 resource-id 定位元素并执行点击操作。

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
        if direction == "up":
            self.device.swipe_ext("up", percent=percent)
        elif direction == "down":
            self.device.swipe_ext("down", percent=percent)
        elif direction == "left":
            self.device.swipe_ext("left", percent=percent)
        elif direction == "right":
            self.device.swipe_ext("right", percent=percent)
        else:
            return False
        return True
