"""
设备管理 API 路由模块

提供设备连接、状态查询和断开连接的 REST API 接口。
"""

from fastapi import APIRouter, Depends
from app.core.device import get_device_manager
from app.schemas import DeviceConnectRequest, DeviceInfoResponse, DeviceStatusResponse

router = APIRouter(prefix="/device", tags=["Device"])


@router.post("/connect", response_model=DeviceInfoResponse)
def connect_device(request: DeviceConnectRequest = None):  # type: ignore[assignment]
    """
    连接设备

    连接到指定的安卓设备或自动选择第一个可用设备。

    Args:
        request: 包含设备序列号的请求体。如果未提供或序列号为 None，则自动选择设备。

    Returns:
        DeviceInfoResponse: 包含已连接设备信息的响应。
    """
    manager = get_device_manager()
    device_serial = request.device_serial if request else None
    info = manager.connect(device_serial)
    return DeviceInfoResponse(
        serial=info.serial,
        product_name=info.product_name,
        api_level=info.api_level,
        battery_level=info.battery_level
    )


@router.get("/status", response_model=DeviceStatusResponse)
def get_device_status():
    """
    获取设备状态

    查询当前设备连接状态和设备信息。

    Returns:
        DeviceStatusResponse: 包含连接状态和设备信息的响应。
    """
    manager = get_device_manager()
    if manager.is_connected():
        info = manager.get_device().info
        battery_info = info.get("battery", {})
        return DeviceStatusResponse(
            connected=True,
            device_info=DeviceInfoResponse(
                serial=manager.get_device().serial,
                product_name=info.get("productName", "Unknown"),
                api_level=info.get("apiLevel", 0),
                battery_level=battery_info.get("level", 0)
            )
        )
    return DeviceStatusResponse(connected=False)


@router.post("/disconnect")
def disconnect_device():
    """
    断开设备连接

    断开当前连接的设备，释放连接资源。

    Returns:
        dict: 操作结果消息。
    """
    manager = get_device_manager()
    manager.disconnect()
    return {"message": "Device disconnected"}
