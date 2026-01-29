"""
应用管理 API 路由模块

提供应用生命周期管理相关的 REST API 接口，包括启动、停止、查询等操作。
"""

from fastapi import APIRouter, Depends
from app.dependencies.services import get_app_service
from app.services import AppService

router = APIRouter(prefix="/app", tags=["App"])


@router.post("/start/{package_name}")
def start_app(package_name: str, app_service: AppService = Depends(get_app_service)):
    """
    启动应用

    根据包名启动指定的应用程序。

    Args:
        package_name: 要启动的应用包名（如 "com.example.app"）。
        app_service: AppService 实例（依赖注入）。

    Returns:
        dict: 操作结果消息。
    """
    app_service.start_app(package_name)
    return {"message": f"App {package_name} started"}


@router.post("/stop/{package_name}")
def stop_app(package_name: str, app_service: AppService = Depends(get_app_service)):
    """
    停止应用

    强制终止指定应用的所有进程。

    Args:
        package_name: 要停止的应用包名。
        app_service: AppService 实例（依赖注入）。

    Returns:
        dict: 操作结果消息。
    """
    app_service.stop_app(package_name)
    return {"message": f"App {package_name} stopped"}


@router.post("/clear/{package_name}")
def clear_app(package_name: str, app_service: AppService = Depends(get_app_service)):
    """
    清除应用数据

    清除指定应用的所有本地数据（设置、缓存、数据库等）。

    Args:
        package_name: 要清除数据的应用包名。
        app_service: AppService 实例（依赖注入）。

    Returns:
        dict: 操作结果消息。
    """
    app_service.clear_app_data(package_name)
    return {"message": f"App {package_name} data cleared"}


@router.get("/version/{package_name}")
def get_version(package_name: str, app_service: AppService = Depends(get_app_service)):
    """
    获取应用版本

    查询指定应用的版本号。

    Args:
        package_name: 要查询的应用包名。
        app_service: AppService 实例（依赖注入）。

    Returns:
        dict: 包含包名和版本号的响应。
    """
    version = app_service.get_app_version(package_name)
    return {"package": package_name, "version": version}


@router.get("/status/{package_name}")
def is_running(package_name: str, app_service: AppService = Depends(get_app_service)):
    """
    检查应用运行状态

    查询指定应用当前是否正在运行。

    Args:
        package_name: 要查询的应用包名。
        app_service: AppService 实例（依赖注入）。

    Returns:
        dict: 包含包名和运行状态的响应。
    """
    running = app_service.is_app_running(package_name)
    return {"package": package_name, "running": running}
