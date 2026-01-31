"""
API 路由模块

聚合所有 API 路由路由器，统一管理路由前缀和标签。

包含以下子路由模块：
- device: 设备管理相关接口
- input: 输入交互相关接口
- navigation: 系统导航相关接口
- app: 应用管理相关接口
- adb: ADB 命令相关接口
- script: 自动化脚本相关接口
"""

from .device import router as device_router
from .input import router as input_router
from .navigation import router as navigation_router
from .app import router as app_router
from .adb import router as adb_router
from .script import router as script_router

__all__ = [
    "device_router",
    "input_router",
    "navigation_router",
    "app_router",
    "adb_router",
    "script_router",
]
