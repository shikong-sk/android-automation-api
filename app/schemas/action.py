"""
操作相关数据模型模块

定义通用的操作请求和响应数据结构。
支持动态执行任意服务方法的参数传递。
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Tuple, Literal, List


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


# ============ 人类模拟操作请求模型 ============


class HumanClickRequest(BaseModel):
    """
    人类模拟点击请求模型

    支持通过坐标或选择器定位目标位置，支持父级/兄弟元素定位和坐标偏移。
    """

    x: Optional[int] = Field(None, description="目标 x 坐标")
    y: Optional[int] = Field(None, description="目标 y 坐标")
    selector_type: Optional[str] = Field(None, description="选择器类型: id, text, class, xpath")
    selector_value: Optional[str] = Field(None, description="选择器值")
    parent_selector_type: Optional[str] = Field(None, description="父元素选择器类型")
    parent_selector_value: Optional[str] = Field(None, description="父元素选择器值")
    sibling_selector_type: Optional[str] = Field(None, description="兄弟元素选择器类型")
    sibling_selector_value: Optional[str] = Field(None, description="兄弟元素选择器值")
    sibling_relation: Literal["following", "preceding"] = Field("following", description="兄弟关系: following(之后), preceding(之前)")
    offset_x: int = Field(0, description="X 坐标偏移")
    offset_y: int = Field(0, description="Y 坐标偏移")
    offset_min: int = Field(3, description="随机偏移最小值（像素）")
    offset_max: int = Field(10, description="随机偏移最大值（像素）")
    delay_min: float = Field(0.05, description="点击前延迟最小值（秒）")
    delay_max: float = Field(0.3, description="点击前延迟最大值（秒）")
    duration_min: float = Field(0.05, description="按压时长最小值（秒）")
    duration_max: float = Field(0.15, description="按压时长最大值（秒）")


class HumanDoubleClickRequest(BaseModel):
    """
    人类模拟双击请求模型

    支持通过坐标或选择器定位目标位置，支持父级/兄弟元素定位和坐标偏移。
    """

    x: Optional[int] = Field(None, description="目标 x 坐标")
    y: Optional[int] = Field(None, description="目标 y 坐标")
    selector_type: Optional[str] = Field(None, description="选择器类型: id, text, class, xpath")
    selector_value: Optional[str] = Field(None, description="选择器值")
    parent_selector_type: Optional[str] = Field(None, description="父元素选择器类型")
    parent_selector_value: Optional[str] = Field(None, description="父元素选择器值")
    sibling_selector_type: Optional[str] = Field(None, description="兄弟元素选择器类型")
    sibling_selector_value: Optional[str] = Field(None, description="兄弟元素选择器值")
    sibling_relation: Literal["following", "preceding"] = Field("following", description="兄弟关系: following(之后), preceding(之前)")
    offset_x: int = Field(0, description="X 坐标偏移")
    offset_y: int = Field(0, description="Y 坐标偏移")
    offset_min: int = Field(3, description="随机偏移最小值（像素）")
    offset_max: int = Field(8, description="随机偏移最大值（像素）")
    interval_min: float = Field(0.1, description="两次点击间隔最小值（秒）")
    interval_max: float = Field(0.2, description="两次点击间隔最大值（秒）")
    duration_min: float = Field(0.03, description="按压时长最小值（秒）")
    duration_max: float = Field(0.08, description="按压时长最大值（秒）")


class HumanLongPressRequest(BaseModel):
    """
    人类模拟长按请求模型

    支持通过坐标或选择器定位目标位置，支持父级/兄弟元素定位和坐标偏移。
    """

    x: Optional[int] = Field(None, description="目标 x 坐标")
    y: Optional[int] = Field(None, description="目标 y 坐标")
    selector_type: Optional[str] = Field(None, description="选择器类型: id, text, class, xpath")
    selector_value: Optional[str] = Field(None, description="选择器值")
    parent_selector_type: Optional[str] = Field(None, description="父元素选择器类型")
    parent_selector_value: Optional[str] = Field(None, description="父元素选择器值")
    sibling_selector_type: Optional[str] = Field(None, description="兄弟元素选择器类型")
    sibling_selector_value: Optional[str] = Field(None, description="兄弟元素选择器值")
    sibling_relation: Literal["following", "preceding"] = Field("following", description="兄弟关系: following(之后), preceding(之前)")
    offset_x: int = Field(0, description="X 坐标偏移")
    offset_y: int = Field(0, description="Y 坐标偏移")
    duration_min: float = Field(0.8, description="长按时长最小值（秒）")
    duration_max: float = Field(1.5, description="长按时长最大值（秒）")
    offset_min: int = Field(3, description="随机偏移最小值（像素）")
    offset_max: int = Field(10, description="随机偏移最大值（像素）")
    delay_min: float = Field(0.05, description="操作前延迟最小值（秒）")
    delay_max: float = Field(0.2, description="操作前延迟最大值（秒）")


class ClickByPointRequest(BaseModel):
    """
    通过坐标点击请求模型

    通过屏幕坐标点直接点击目标位置。
    """

    x: int = Field(..., description="目标 x 坐标", ge=0)
    y: int = Field(..., description="目标 y 坐标", ge=0)


class HumanDragRequest(BaseModel):
    """
    人类模拟拖拽请求模型

    支持贝塞尔曲线轨迹或带抖动的直线轨迹。
    """

    # 起点（坐标或选择器二选一）
    start_x: Optional[int] = Field(None, description="起点 x 坐标")
    start_y: Optional[int] = Field(None, description="起点 y 坐标")
    start_selector_type: Optional[str] = Field(
        None, description="起点选择器类型: id, text, class, xpath"
    )
    start_selector_value: Optional[str] = Field(None, description="起点选择器值")

    # 终点（坐标或选择器二选一）
    end_x: Optional[int] = Field(None, description="终点 x 坐标")
    end_y: Optional[int] = Field(None, description="终点 y 坐标")
    end_selector_type: Optional[str] = Field(
        None, description="终点选择器类型: id, text, class, xpath"
    )
    end_selector_value: Optional[str] = Field(None, description="终点选择器值")

    # 轨迹和速度配置
    trajectory_type: Literal["bezier", "linear_jitter"] = Field(
        "bezier", description="轨迹类型: bezier(贝塞尔曲线), linear_jitter(直线+抖动)"
    )
    speed_mode: Literal["ease_in_out", "ease_in", "ease_out", "linear", "random"] = Field(
        "ease_in_out",
        description="速度模式: ease_in_out(加速-匀速-减速), ease_in(加速), ease_out(减速), linear(匀速), random(随机)",
    )
    duration: float = Field(1.0, description="拖拽总时间（秒）", ge=0.1, le=10.0)
    num_points: int = Field(50, description="轨迹采样点数量", ge=10, le=200)

    # 随机化配置
    offset_min: int = Field(3, description="起点/终点随机偏移最小值（像素）")
    offset_max: int = Field(10, description="起点/终点随机偏移最大值（像素）")
    jitter_min: int = Field(1, description="直线轨迹抖动最小值（像素）")
    jitter_max: int = Field(5, description="直线轨迹抖动最大值（像素）")
    delay_min: float = Field(0.05, description="操作前延迟最小值（秒）")
    delay_max: float = Field(0.2, description="操作前延迟最大值（秒）")
