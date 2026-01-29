"""
应用管理服务模块

提供应用生命周期管理相关的操作，包括：
- 启动应用
- 停止应用
- 清除应用数据
- 获取应用版本
- 检查应用运行状态
"""

from .base import AutomationService


class AppService(AutomationService):
    """
    应用管理服务

    继承自 AutomationService，提供对设备上应用的管理操作。
    通过包名 (package name) 标识目标应用。

    支持应用的启动、停止、数据清理以及信息查询等功能。
    """

    def start_app(self, package_name: str) -> bool:
        """
        启动指定应用

        通过包名启动应用。如果应用已运行，则会将其切换到前台。

        Args:
            package_name: 要启动的应用包名，如 "com.example.app"。

        Returns:
            bool: 始终返回 True。
        """
        self.device.app_start(package_name)
        return True

    def stop_app(self, package_name: str) -> bool:
        """
        停止指定应用

        强制终止指定应用的所有进程。

        Args:
            package_name: 要停止的应用包名。

        Returns:
            bool: 始终返回 True。
        """
        self.device.app_stop(package_name)
        return True

    def clear_app_data(self, package_name: str) -> bool:
        """
        清除指定应用的数据

        模拟在系统设置中清除应用数据的操作。
        这将删除应用的所有本地数据，包括设置、缓存和数据库。

        Args:
            package_name: 要清除数据的应用包名。

        Returns:
            bool: 始终返回 True。
        """
        self.device.app_clear(package_name)
        return True

    def get_app_version(self, package_name: str) -> str | None:
        """
        获取应用的版本号

        查询指定应用的版本信息。

        Args:
            package_name: 要查询的应用包名。

        Returns:
            str | None: 应用的版本名称，如果应用未安装返回 None。
        """
        return self.device.app_info(package_name).get("versionName")

    def is_app_running(self, package_name: str) -> bool:
        """
        检查应用是否正在运行

        检查指定应用是否有活跃的进程。

        Args:
            package_name: 要检查的应用包名。

        Returns:
            bool: 应用正在运行返回 True，否则返回 False。
        """
        return self.device.app_wait(package_name, timeout=1) is not None

    def get_current_app(self) -> dict:
        """
        获取当前前台应用信息

        返回当前正在前台运行的应用包名、Activity 名称和 PID。

        Returns:
            dict: 包含 package、activity、pid 的字典。
        """
        return self.device.app_current()
