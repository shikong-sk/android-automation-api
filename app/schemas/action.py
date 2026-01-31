"""
操作相关数据模型模块

定义通用的操作请求和响应数据结构。
支持动态执行任意服务方法的参数传递。
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class ActionRequest(BaseModel):
    """
    操作请求模型

    用于动态执行服务方法的请求体结构。

    Attributes:
        action: 要执行的操作名称，对应服务类中的方法名。
        params: 操作所需的参数字典，键为参数名，值为参数值。
    """

    action: str = Field(..., description="操作类型")
    params: Dict[str, Any] = Field(default_factory=dict, description="操作参数")


class ActionResponse(BaseModel):
    """
    操作响应模型

    用于返回操作执行结果的数据结构。

    Attributes:
        success: 操作是否执行成功
        result: 操作返回的结果数据
        message: 可选的提示信息
    """

    success: bool
    result: Optional[Any] = None
    message: Optional[str] = None
