"""
导航操作 API 路由模块

提供系统导航相关操作的 REST API 接口，包括 Home 键、返回键等。
"""

from fastapi import APIRouter, Depends
from app.dependencies.services import get_navigation_service
from app.services import NavigationService

router = APIRouter(prefix="/navigation", tags=["Navigation"])


@router.post("/home")
def press_home(nav_service: NavigationService = Depends(get_navigation_service)):
    """
    点击 Home 键

    返回到设备主屏幕。

    Returns:
        dict: 操作结果消息。
    """
    nav_service.press_home()
    return {"message": "Home pressed"}


@router.post("/back")
def press_back(nav_service: NavigationService = Depends(get_navigation_service)):
    """
    点击返回键

    返回上一个页面或关闭当前对话框。

    Returns:
        dict: 操作结果消息。
    """
    nav_service.press_back()
    return {"message": "Back pressed"}


@router.post("/menu")
def press_menu(nav_service: NavigationService = Depends(get_navigation_service)):
    """
    点击菜单键

    打开当前应用的菜单选项。

    Returns:
        dict: 操作结果消息。
    """
    nav_service.press_menu()
    return {"message": "Menu pressed"}


@router.post("/go-home")
def go_home(nav_service: NavigationService = Depends(get_navigation_service)):
    """
    返回主屏幕

    确保切换到主屏幕并等待页面加载完成。

    Returns:
        dict: 操作结果消息。
    """
    nav_service.go_home()
    return {"message": "Returned to home"}


@router.post("/recent-apps")
def recent_apps(nav_service: NavigationService = Depends(get_navigation_service)):
    """
    打开最近应用

    显示设备最近使用的应用列表。

    Returns:
        dict: 操作结果消息。
    """
    nav_service.open_recent_apps()
    return {"message": "Recent apps opened"}
