"""
数据模型模块

定义所有 API 请求和响应使用的数据模型。
使用 Pydantic 实现数据验证、序列化和文档自动生成。

包含以下模型：
- 设备相关：DeviceConnectRequest, DeviceInfoResponse, DeviceStatusResponse
- 操作相关：ActionRequest, ActionResponse
- 人类模拟：HumanClickRequest, HumanDoubleClickRequest, HumanLongPressRequest, HumanDragRequest
"""

from .device import DeviceConnectRequest, DeviceInfoResponse, DeviceStatusResponse
from .action import (
    ActionRequest,
    ActionResponse,
    HumanClickRequest,
    HumanDoubleClickRequest,
    HumanLongPressRequest,
    HumanDragRequest,
    ClickByPointRequest,
)

__all__ = [
    "DeviceConnectRequest",
    "DeviceInfoResponse",
    "DeviceStatusResponse",
    "ActionRequest",
    "ActionResponse",
    "HumanClickRequest",
    "HumanDoubleClickRequest",
    "HumanLongPressRequest",
    "HumanDragRequest",
    "ClickByPointRequest",
]
