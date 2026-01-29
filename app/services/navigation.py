"""
导航操作服务模块

提供设备系统级别的导航操作，包括：
- 返回主屏幕
- 返回上一页
- 打开菜单
- 查看最近应用
"""

from .base import AutomationService


class NavigationService(AutomationService):
    """
    导航操作服务

    继承自 AutomationService，提供系统级别的导航控制操作。
    这些操作模拟用户的物理按键或系统手势。

    所有方法返回布尔值，表示操作是否成功执行。
    """

    def press_home(self) -> bool:
        """
        点击 Home 键

        模拟按下设备物理 Home 键或执行返回主屏幕的手势。
        当前页面会切换到主屏幕，但不会等待加载完成。

        Returns:
            bool: 始终返回 True。
        """
        self.device.press("home")
        return True

    def press_back(self) -> bool:
        """
        点击返回键

        模拟按下设备物理返回键。
        返回上一个页面或关闭当前对话框。

        Returns:
            bool: 始终返回 True。
        """
        self.device.press("back")
        return True

    def press_menu(self) -> bool:
        """
        点击菜单键

        模拟按下设备菜单键。
        打开应用的菜单选项。

        Returns:
            bool: 始终返回 True。
        """
        self.device.press("menu")
        return True

    def go_home(self) -> bool:
        """
        返回主屏幕

        先点击 Home 键，然后等待 0.5 秒确保页面切换完成。
        适用于需要确保停留在主屏幕的场景。

        Returns:
            bool: 始终返回 True。
        """
        self.device.press("home")
        self.device.sleep(0.5)
        return True

    def open_recent_apps(self) -> bool:
        """
        打开最近应用列表

        模拟切换到最近使用应用的界面。
        显示用户最近打开的应用列表。

        Returns:
            bool: 始终返回 True。
        """
        self.device.press("recent_apps")
        return True
