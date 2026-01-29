"""
Android Automation API 主应用模块

这是 FastAPI 应用的入口模块，负责：
- 创建 FastAPI 应用实例
- 配置中间件（CORS 等）
- 注册所有 API 路由
- 提供根路径和健康检查接口

启动方式：
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

访问 API 文档：
    http://localhost:8000/api/docs
"""

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from app.api import device_router, input_router, navigation_router, app_router
from app.core.config import get_settings

settings = get_settings()


def swagger_monkey_patch(*args, **kwargs):
    """
    Swagger UI 资源替换函数

    由于 FastAPI 默认使用国外 CDN 导致国内访问 Swagger 文档较慢，
    此函数将资源 URL 替换为国内可访问的静态资源 CDN。

    Args:
        *args: 位置参数，传递给原函数。
        **kwargs: 关键字参数，传递给原函数。

    Returns:
        get_swagger_ui_html 的返回结果。
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.staticfile.org/swagger-ui/4.15.5/swagger-ui-bundle.min.js',
        swagger_css_url='https://cdn.staticfile.org/swagger-ui/4.15.5/swagger-ui.min.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.openapi_version = "3.0.0"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device_router, prefix="/api/v1")
app.include_router(input_router, prefix="/api/v1")
app.include_router(navigation_router, prefix="/api/v1")
app.include_router(app_router, prefix="/api/v1")


@app.get("/")
def root():
    """
    根路径接口

    返回应用的基本信息。

    Returns:
        dict: 包含应用名称和版本的字典。
    """
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/health")
def health():
    """
    健康检查接口

    用于服务监控和负载均衡器的健康探测。

    Returns:
        dict: 包含服务状态的字典。
    """
    return {"status": "ok"}
