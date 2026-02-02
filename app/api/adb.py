"""
ADB 操作 API 路由模块

提供基于 adbutils 的 ADB 命令相关的 REST API 接口。
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from app.dependencies.services import get_adb_service
from app.services.adb_service import AdbService

router = APIRouter(prefix="/adb", tags=["ADB"])


class ShellRequest(BaseModel):
    """Shell 命令请求模型"""

    command: str


class FileTransferRequest(BaseModel):
    """文件传输请求模型"""

    local_path: str
    remote_path: str


class InstallRequest(BaseModel):
    """APK 安装请求模型"""

    apk_path: str
    reinstall: bool = False
    grant_permissions: bool = True


# ==================== 应用管理 ====================


@router.get("/packages")
def list_packages(
    filter_type: Optional[str] = Query(
        None, description="过滤类型: third_party/3=第三方应用, system/s=系统应用, 空=全部"
    ),
    adb_service: AdbService = Depends(get_adb_service),
):
    """
    获取已安装应用包名列表

    Args:
        filter_type: 过滤类型
        adb_service: ADB 服务实例

    Returns:
        dict: 包含应用包名列表和数量
    """
    packages = adb_service.list_packages(filter_type)
    return {"count": len(packages), "packages": packages}


@router.get("/packages/{package_name}")
def get_package_info(package_name: str, adb_service: AdbService = Depends(get_adb_service)):
    """
    获取指定应用的详细信息

    Args:
        package_name: 应用包名
        adb_service: ADB 服务实例

    Returns:
        dict: 应用详细信息
    """
    info = adb_service.get_package_info(package_name)
    if info is None:
        raise HTTPException(status_code=404, detail=f"Package {package_name} not found")
    return info


@router.get("/packages-info")
def get_all_packages_info(
    filter_type: Optional[str] = Query(
        None, description="过滤类型: third_party/3=第三方应用, system/s=系统应用, 空=全部"
    ),
    adb_service: AdbService = Depends(get_adb_service),
):
    """
    获取所有应用的详细信息

    注意：此接口可能较慢，因为需要逐个查询应用信息

    Args:
        filter_type: 过滤类型
        adb_service: ADB 服务实例

    Returns:
        dict: 包含所有应用详细信息的列表
    """
    packages_info = adb_service.get_all_packages_info(filter_type)
    return {"count": len(packages_info), "packages": packages_info}


@router.post("/install")
def install_apk(request: InstallRequest, adb_service: AdbService = Depends(get_adb_service)):
    """
    安装 APK 文件

    Args:
        request: 安装请求参数
        adb_service: ADB 服务实例

    Returns:
        dict: 安装结果
    """
    success = adb_service.install_apk(
        request.apk_path, reinstall=request.reinstall, grant_permissions=request.grant_permissions
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to install APK")
    return {"message": "APK installed successfully", "apk_path": request.apk_path}


@router.delete("/packages/{package_name}")
def uninstall_package(
    package_name: str,
    keep_data: bool = Query(False, description="是否保留应用数据"),
    adb_service: AdbService = Depends(get_adb_service),
):
    """
    卸载应用

    Args:
        package_name: 应用包名
        keep_data: 是否保留数据
        adb_service: ADB 服务实例

    Returns:
        dict: 卸载结果
    """
    success = adb_service.uninstall_package(package_name, keep_data=keep_data)
    if not success:
        raise HTTPException(status_code=500, detail=f"Failed to uninstall {package_name}")
    return {"message": f"Package {package_name} uninstalled successfully"}


# ==================== 设备信息 ====================


@router.get("/device-info")
def get_device_info(adb_service: AdbService = Depends(get_adb_service)):
    """
    获取设备详细信息

    Returns:
        dict: 设备信息（型号、品牌、Android 版本等）
    """
    return adb_service.get_device_info()


@router.get("/battery")
def get_battery_info(adb_service: AdbService = Depends(get_adb_service)):
    """
    获取电池信息

    Returns:
        dict: 电池信息（电量、充电状态等）
    """
    return adb_service.get_battery_info()


@router.get("/screen/resolution")
def get_screen_resolution(adb_service: AdbService = Depends(get_adb_service)):
    """
    获取屏幕分辨率

    Returns:
        dict: 屏幕宽高
    """
    return adb_service.get_screen_resolution()


@router.get("/screen/density")
def get_screen_density(adb_service: AdbService = Depends(get_adb_service)):
    """
    获取屏幕密度

    Returns:
        dict: 屏幕密度 (dpi)
    """
    return {"density": adb_service.get_screen_density()}


@router.get("/prop/{prop_name:path}")
def get_prop(prop_name: str, adb_service: AdbService = Depends(get_adb_service)):
    """
    获取设备属性

    Args:
        prop_name: 属性名称（如 ro.product.model）

    Returns:
        dict: 属性值
    """
    value = adb_service.get_prop(prop_name)
    return {"prop": prop_name, "value": value}


# ==================== Shell 命令 ====================


@router.post("/shell")
def execute_shell(request: ShellRequest, adb_service: AdbService = Depends(get_adb_service)):
    """
    执行 shell 命令

    Args:
        request: Shell 命令请求
        adb_service: ADB 服务实例

    Returns:
        dict: 命令输出
    """
    output = adb_service.shell(request.command)
    return {"command": request.command, "output": output}


# ==================== 文件操作 ====================


@router.post("/push")
def push_file(request: FileTransferRequest, adb_service: AdbService = Depends(get_adb_service)):
    """
    推送文件到设备

    Args:
        request: 文件传输请求
        adb_service: ADB 服务实例

    Returns:
        dict: 操作结果
    """
    success = adb_service.push_file(request.local_path, request.remote_path)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to push file")
    return {
        "message": "File pushed successfully",
        "local_path": request.local_path,
        "remote_path": request.remote_path,
    }


@router.post("/pull")
def pull_file(request: FileTransferRequest, adb_service: AdbService = Depends(get_adb_service)):
    """
    从设备拉取文件

    Args:
        request: 文件传输请求
        adb_service: ADB 服务实例

    Returns:
        dict: 操作结果
    """
    success = adb_service.pull_file(request.remote_path, request.local_path)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to pull file")
    return {
        "message": "File pulled successfully",
        "remote_path": request.remote_path,
        "local_path": request.local_path,
    }


@router.post("/screenshot")
def take_screenshot(
    local_path: str = Query(..., description="保存截图的本地路径"),
    adb_service: AdbService = Depends(get_adb_service),
):
    """
    截取屏幕截图

    Args:
        local_path: 保存截图的本地路径
        adb_service: ADB 服务实例

    Returns:
        dict: 操作结果
    """
    success = adb_service.take_screenshot(local_path)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to take screenshot")
    return {"message": "Screenshot saved", "path": local_path}


@router.get("/screenshot-base64")
def take_screenshot_base64(
    adb_service: AdbService = Depends(get_adb_service),
):
    """
    截取屏幕截图并返回 base64 编码

    Returns:
        dict: 包含 base64 图片数据和屏幕尺寸
    """
    result = adb_service.take_screenshot_base64()
    if "error" in result and result.get("image") is None:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to take screenshot"))
    return result


# ==================== 设备控制 ====================


@router.post("/reboot")
def reboot_device(
    mode: Optional[str] = Query(None, description="重启模式: recovery, bootloader, 空=正常重启"),
    adb_service: AdbService = Depends(get_adb_service),
):
    """
    重启设备

    Args:
        mode: 重启模式
        adb_service: ADB 服务实例

    Returns:
        dict: 操作结果
    """
    success = adb_service.reboot(mode)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reboot device")
    return {"message": f"Device rebooting" + (f" to {mode}" if mode else "")}
