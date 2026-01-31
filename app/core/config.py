"""
应用配置模块

提供全局配置管理，使用 pydantic-settings 实现环境变量读取。
支持从 .env 文件加载配置，支持开发/生产环境切换。
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    应用配置类

    用于管理应用的全局配置信息，包括应用名称、版本号、调试模式等。
    配置可通过环境变量或 .env 文件进行覆盖。

    Attributes:
        APP_NAME: 应用名称，默认为 "Android Automation API"
        APP_VERSION: 应用版本号，默认为 "1.0.0"
        DEBUG: 调试模式开关，默认为 True
        DEFAULT_DEVICE_SERIAL: 默认连接的设备序列号，为空时自动选择第一个设备
    """

    APP_NAME: str = "Android Automation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DEFAULT_DEVICE_SERIAL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    获取全局配置实例

    使用 lru_cache 缓存配置实例，确保整个应用使用同一配置对象，
    避免重复加载环境变量。

    Returns:
        Settings: 配置实例对象
    """
    return Settings()
