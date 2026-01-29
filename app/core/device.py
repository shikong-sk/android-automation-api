"""
设备管理模块

提供与安卓设备的连接和管理功能。
使用单例模式确保全局只有一个设备管理器实例。
支持通过 USB 或 WiFi 连接设备，并提供设备信息查询能力。
"""

import uiautomator2 as u2
from typing import Optional
from contextlib import contextmanager
from dataclasses import dataclass
import threading


@dataclass
class DeviceInfo:
    """
    设备信息数据类

    用于存储已连接设备的基本信息。

    Attributes:
        serial: 设备序列号，唯一标识设备
        product_name: 设备产品名称
        api_level: Android API 级别
        battery_level: 电池电量百分比 (0-100)
    """
    serial: str
    product_name: str
    api_level: int
    battery_level: int


class DeviceManager:
    """
    设备管理器（单例类）

    负责管理设备连接生命周期，提供设备操作接口。
    采用单例模式确保全局只有一个设备管理器实例，避免重复连接。

    Attributes:
        _instance: 单例实例引用
        _lock: 线程锁，用于线程安全的单例初始化
        _device: uiautomator2 设备对象实例
    """

    _instance: Optional["DeviceManager"] = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        单例模式的 __new__ 方法

        确保在多线程环境下安全地创建唯一的 DeviceManager 实例。
        使用双重检查锁定机制提高性能。
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._device = None
        return cls._instance

    def connect(self, device_serial: Optional[str] = None) -> DeviceInfo:
        """
        连接安卓设备

        通过 uiautomator2 库连接指定的安卓设备。如果未指定设备序列号，
        则自动选择第一个可用的设备。

        Args:
            device_serial: 设备序列号。传入 None 或空字符串时自动选择设备。

        Returns:
            DeviceInfo: 包含连接设备信息的 DeviceInfo 对象。

        Raises:
            Exception: 连接失败时抛出异常。
        """
        if device_serial:
            self._device = u2.connect(device_serial)
        else:
            self._device = u2.connect()

        info = self._device.info
        return DeviceInfo(
            serial=self._device.serial,
            product_name=info.get("productName", "Unknown"),
            api_level=info.get("apiLevel", 0),
            battery_level=self._device.info.get("battery", {}).get("level", 0)
        )

    def get_device(self) -> u2.Device:
        """
        获取 uiautomator2 设备对象

        返回当前连接的设备对象，用于执行具体的设备操作。

        Returns:
            u2.Device: uiautomator2 设备对象。

        Raises:
            RuntimeError: 如果设备未连接。
        """
        if self._device is None:
            raise RuntimeError("Device not connected. Call connect() first.")
        return self._device

    def disconnect(self) -> None:
        """
        断开设备连接

        清除设备管理器中的设备引用，释放连接资源。
        """
        if self._device:
            self._device = None

    def is_connected(self) -> bool:
        """
        检查设备是否已连接

        Returns:
            bool: 如果设备已连接返回 True，否则返回 False。
        """
        return self._device is not None


@contextmanager
def device_context(device_serial: Optional[str] = None):
    """
    设备连接上下文管理器

    提供设备连接和断开的自动管理，使用 with 语句确保资源正确释放。

    Args:
        device_serial: 可选的设备序列号。

    Usage:
        with device_context("device_serial") as manager:
            device = manager.get_device()
            # 执行设备操作
        # 退出 with 块时自动断开连接
    """
    manager = DeviceManager()
    manager.connect(device_serial)
    try:
        yield manager
    finally:
        manager.disconnect()


def get_device_manager() -> DeviceManager:
    """
    获取设备管理器单例实例

    这是推荐的获取 DeviceManager 实例的方式。

    Returns:
        DeviceManager: 设备管理器单例实例。
    """
    return DeviceManager()
