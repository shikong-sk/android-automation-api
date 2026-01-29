"""
服务模块

提供各类自动化操作服务，按功能分组：
- AutomationService: 所有服务的基类
- InputService: 输入交互操作
- NavigationService: 系统导航操作
- AppService: 应用管理操作

每个服务类都封装了特定领域的设备操作，提供简洁的 API 接口。
"""

from .base import AutomationService
from .input import InputService
from .navigation import NavigationService
from .app_service import AppService

__all__ = ["AutomationService", "InputService", "NavigationService", "AppService"]
