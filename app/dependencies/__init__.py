"""
依赖注入模块

提供 FastAPI 依赖注入所需的各类依赖函数。
包括服务实例的创建和管理。

导出的依赖函数：
- get_input_service: InputService 依赖
- get_navigation_service: NavigationService 依赖
- get_app_service: AppService 依赖
"""

from .services import (
    get_input_service,
    get_navigation_service,
    get_app_service,
)

__all__ = [
    "get_input_service",
    "get_navigation_service",
    "get_app_service"
]
