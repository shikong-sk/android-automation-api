"""
设备相关数据模型模块

定义与设备连接、状态查询相关的数据结构和请求/响应模型。
使用 Pydantic 实现数据验证和序列化。
"""

from pydantic import BaseModel, Field


class DeviceConnectRequest(BaseModel):
    """
    设备连接请求模型

    用于请求连接安卓设备的请求体数据结构。

    Attributes:
        device_serial: 设备序列号。如果为空或为 None，将自动选择第一个可用设备。
    """
    device_serial: str | None = Field(None, description="设备序列号，为空则自动连接")


class DeviceInfoResponse(BaseModel):
    """
    设备信息响应模型

    用于返回已连接设备的基本信息。

    Attributes:
        serial: 设备序列号
        product_name: 设备产品名称
        api_level: Android API 级别
        battery_level: 电池电量 (0-100)
    """
    serial: str
    product_name: str
    api_level: int
    battery_level: int


class DeviceStatusResponse(BaseModel):
    """
    设备状态响应模型

    用于返回当前设备连接状态的完整信息。

    Attributes:
        connected: 设备是否已连接
        device_info: 已连接设备的信息，未连接时为 None
    """
    connected: bool
    device_info: DeviceInfoResponse | None = None
