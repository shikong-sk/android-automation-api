"""
核心模块

提供应用的基础设施功能，包括：
- 配置管理 (Settings)
- 设备管理 (DeviceManager)

该模块中的组件是整个应用的基础，其他模块依赖于此模块提供的功能。
"""

from .device import DeviceManager, get_device_manager

__all__ = ["DeviceManager", "get_device_manager"]
