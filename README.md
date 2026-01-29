# Android Automation Project

基于 uiautomator2 的安卓自动化项目，配合 FastAPI 后端和 Vue 前端。

## 项目结构

```
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   ├── device.py      # 设备连接相关
│   │   │   ├── input.py       # 输入操作
│   │   │   ├── navigation.py  # 导航操作
│   │   │   └── app.py         # 应用操作
│   │   ├── core/              # 核心模块
│   │   │   ├── config.py      # 配置管理
│   │   │   └── device.py      # 设备管理
│   │   ├── dependencies/      # 依赖注入
│   │   ├── schemas/           # Pydantic 模型
│   │   └── services/          # 业务逻辑服务
│   ├── tests/                 # 测试文件
│   └── pyproject.toml
└── frontend/                  # Vue 前端 (待创建)
```

## 快速开始

### 后端

```bash
cd backend
uv pip install -e .
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档: http://localhost:8000/api/docs

### 可用 API

- `POST /api/v1/device/connect` - 连接设备
- `GET /api/v1/device/status` - 获取设备状态
- `POST /api/v1/input/click` - 点击元素
- `POST /api/v1/input/set-text` - 输入文本
- `POST /api/v1/navigation/home` - 返回主页
- `POST /api/v1/app/start/{package}` - 启动应用
