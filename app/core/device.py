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
import subprocess
import re


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

    def _is_ip_address(self, serial: str) -> bool:
        """
        检查是否为 IP 地址格式

        Args:
            serial: 设备序列号或 IP 地址

        Returns:
            bool: 如果是 IP 地址格式返回 True
        """
        # 匹配 IP 地址格式 (可带端口)
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}(:\d+)?$"
        return bool(re.match(ip_pattern, serial))

    def _adb_connect(self, ip_address: str) -> bool:
        """
        使用 adb connect 命令连接 WiFi 设备

        Args:
            ip_address: 设备 IP 地址（可带端口，默认 5555）

        Returns:
            bool: 连接是否成功
        """
        # 如果没有指定端口，添加默认端口 5555
        if ":" not in ip_address:
            ip_address = f"{ip_address}:5555"

        try:
            result = subprocess.run(
                ["adb", "connect", ip_address], capture_output=True, text=True, timeout=10
            )
            output = result.stdout.lower()
            # 检查连接是否成功
            return "connected" in output or "already connected" in output
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"ADB connect failed: {e}")

    def _get_battery_level(self, serial: str) -> int:
        """
        通过 ADB 命令获取电池电量

        Args:
            serial: 设备序列号

        Returns:
            int: 电池电量百分比 (0-100)
        """
        try:
            result = subprocess.run(
                ["adb", "-s", serial, "shell", "dumpsys", "battery"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.split("\n"):
                line = line.strip()
                if line.startswith("level:"):
                    return int(line.split(":")[1].strip())
        except Exception:
            pass
        return 0

    def connect(self, device_serial: Optional[str] = None) -> DeviceInfo:
        """
        连接安卓设备

        通过 uiautomator2 库连接指定的安卓设备。如果未指定设备序列号，
        则自动选择第一个可用的设备。

        对于 WiFi 连接（IP 地址格式），会先执行 adb connect 命令。

        Args:
            device_serial: 设备序列号或 IP 地址。传入 None 或空字符串时自动选择设备。

        Returns:
            DeviceInfo: 包含连接设备信息的 DeviceInfo 对象。

        Raises:
            Exception: 连接失败时抛出异常。
        """
        if device_serial:
            # 如果是 IP 地址格式，先执行 adb connect
            if self._is_ip_address(device_serial):
                # 确保 IP 地址带端口
                if ":" not in device_serial:
                    device_serial = f"{device_serial}:5555"
                # 先用 adb connect 连接
                if not self._adb_connect(device_serial):
                    raise RuntimeError(f"Failed to connect to device via ADB: {device_serial}")

            self._device = u2.connect(device_serial)
        else:
            self._device = u2.connect()

        info = self._device.info
        # 通过 ADB 获取电池信息
        battery_level = self._get_battery_level(self._device.serial)

        return DeviceInfo(
            serial=self._device.serial,
            product_name=info.get("productName", "Unknown"),
            api_level=info.get("sdkInt", 0),
            battery_level=battery_level,
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
