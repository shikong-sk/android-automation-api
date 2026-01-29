"""
服务基类模块

定义所有自动化操作服务的基类。
提供通用的设备访问和方法执行框架。
"""

from typing import Any
from app.core.device import DeviceManager


class AutomationService:
    """
    自动化服务基类

    所有具体服务类（如 InputService、NavigationService 等）的基类。
    提供设备访问和方法动态执行的通用功能。

    Attributes:
        _device_manager: 设备管理器实例
        _device: 当前连接的设备对象
    """

    def __init__(self, device_manager: DeviceManager):
        """
        初始化服务实例

        Args:
            device_manager: 设备管理器实例，用于获取设备对象。
        """
        self._device_manager = device_manager
        self._device = device_manager.get_device()

    @property
    def device(self):
        """
        设备属性

        返回当前连接的设备对象，提供给子类使用。
        """
        return self._device

    def execute(self, action: str, **kwargs) -> dict:
        """
        执行指定的操作

        根据操作名称动态调用对应的方法，支持通过 API 执行任意服务方法。

        Args:
            action: 要执行的操作方法名。
            **kwargs: 要传递给方法的参数。

        Returns:
            dict: 包含执行结果的字典，格式为 {"success": bool, "result": Any}

        Raises:
            ValueError: 如果操作名称不存在。
        """
        method = getattr(self, action, None)
        if not callable(method):
            raise ValueError(f"Unknown action: {action}")
        result = method(**kwargs)
        return {"success": True, "result": result}
