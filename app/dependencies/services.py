"""
服务依赖注入模块

提供 FastAPI 依赖注入函数，为 API 路由提供服务实例。
每个依赖函数负责创建并yield服务实例，FastAPI 负责管理其生命周期。
"""

from typing import Generator
from app.core.device import DeviceManager, get_device_manager
from app.services import InputService, NavigationService, AppService
from app.services.adb_service import AdbService


def get_input_service() -> Generator[InputService, None, None]:
    """
    InputService 依赖注入函数

    创建 InputService 实例并通过依赖注入提供给路由使用。

    Returns:
        Generator: 生成 InputService 实例的生成器。

    Usage:
        @router.post("/click")
        def click(service: InputService = Depends(get_input_service)):
            ...
    """
    manager = get_device_manager()
    yield InputService(manager)


def get_navigation_service() -> Generator[NavigationService, None, None]:
    """
    NavigationService 依赖注入函数

    创建 NavigationService 实例并通过依赖注入提供给路由使用。

    Returns:
        Generator: 生成 NavigationService 实例的生成器。
    """
    manager = get_device_manager()
    yield NavigationService(manager)


def get_app_service() -> Generator[AppService, None, None]:
    """
    AppService 依赖注入函数

    创建 AppService 实例并通过依赖注入提供给路由使用。

    Returns:
        Generator: 生成 AppService 实例的生成器。
    """
    manager = get_device_manager()
    yield AppService(manager)


def get_adb_service() -> Generator[AdbService, None, None]:
    """
    AdbService 依赖注入函数

    创建 AdbService 实例并通过依赖注入提供给路由使用。
    使用当前连接设备的序列号初始化 AdbService。

    Returns:
        Generator: 生成 AdbService 实例的生成器。
    """
    manager = get_device_manager()
    # 获取当前连接设备的序列号
    device_serial = manager.get_device().serial if manager.is_connected() else None
    yield AdbService(device_serial)
