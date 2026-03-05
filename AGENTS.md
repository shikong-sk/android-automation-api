# 项目知识库

**生成时间:** 2026-03-06
**提交:** d802329
**分支:** master

## 概述

安卓设备自动化 API，采用 FastAPI 后端 + Vue 3 前端。使用 uiautomator2/adbutils 进行设备控制。内置自定义 DSL 脚本系统实现自动化工作流。

## 项目结构

```
.
├── app/                    # FastAPI 后端 (Python 3.11)
│   ├── api/               # REST 路由处理器
│   ├── core/              # 配置 + DeviceManager 单例
│   ├── dependencies/      # 服务工厂依赖注入
│   ├── schemas/           # Pydantic 数据模型
│   └── services/          # 业务逻辑 + DSL 引擎
├── frontend/              # Vue 3 + Vite 前端
│   └── src/
│       ├── api/           # Axios 客户端
│       ├── components/    # Vue 组件
│       ├── pages/         # 路由页面
│       ├── stores/        # Pinia 状态管理
│       └── router/        # Vue Router
├── scripts/               # .script DSL 自动化脚本文件
└── tests/                 # pytest 测试（覆盖率较低）
```

## 开发指南

| 任务 | 位置 | 说明 |
|------|----------|-------|
| 新增 API 接口 | `app/api/*.py` | 从 `__init__.py` 导入路由 |
| 新增服务方法 | `app/services/*.py` | 继承 `base.AutomationService` |
| 新增 DSL 命令 | `app/services/script_parser.py` + `script_executor.py` | Token + AST + 执行逻辑 |
| 新增 Vue 组件 | `frontend/src/components/` | 通过 unplugin 自动导入 |
| 新增前端页面 | `frontend/src/pages/` + `router/index.js` | 添加路由配置 |
| 设备操作 | `app/core/device.py` | DeviceManager 单例 |
| 配置/环境变量 | `app/core/config.py` + `.env` | Pydantic Settings |

## 代码映射

### 后端核心

| 符号 | 类型 | 位置 | 作用 |
|--------|------|----------|------|
| `Settings` | 类 | `app/core/config.py` | 应用配置（环境变量） |
| `DeviceManager` | 类 | `app/core/device.py` | 单例设备连接管理 |
| `DeviceInfo` | 数据类 | `app/core/device.py` | 设备元数据 |
| `AutomationService` | 类 | `app/services/base.py` | 服务基类 |

### DSL 引擎（核心特性）

| 符号 | 类型 | 位置 | 作用 |
|--------|------|----------|------|
| `TokenType` | 枚举 | `app/services/script_parser.py` | DSL 词法类型（60+种） |
| `ASTNode` | 类 | `app/services/script_parser.py` | AST 节点基类 |
| `ScriptExecutor` | 类 | `app/services/script_executor.py` | 执行解析后的脚本 |
| `ExecutionContext` | 数据类 | `app/services/script_executor.py` | 变量、日志、状态 |

### API 路由

| 路由器 | 文件 | 前缀 | 接口 |
|--------|------|--------|-----------|
| device_router | `app/api/device.py` | `/api/v1/device` | connect, status, disconnect |
| input_router | `app/api/input.py` | `/api/v1/input` | click, swipe, text, selectors |
| navigation_router | `app/api/navigation.py` | `/api/v1/navigation` | home, back, menu |
| app_router | `app/api/app.py` | `/api/v1/app` | start, stop, clear |
| adb_router | `app/api/adb.py` | `/api/v1/adb` | shell, packages, screenshot |
| script_router | `app/api/script.py` | `/api/v1/script` | execute, validate, list |

## 编码规范

### 后端 (Python)

- **行长度**: 100 字符 (Ruff)
- **目标版本**: Python 3.11
- **导入**: 使用 `app.*` 绝对导入
- **服务**: 继承 `AutomationService`，通过 `self.device` 访问设备
- **依赖注入**: 使用 `app/dependencies/services.py` 工厂函数
- **数据模型**: Pydantic v2，位于 `app/schemas/`
- **禁止使用 `as any` / `@ts-ignore` 等类型抑制**

### 前端 (Vue 3)

- **组合式 API** 使用 `<script setup>`
- **Tailwind CSS** 样式（preflight 已禁用）
- **Element Plus** UI 组件库
- **API 客户端**: 按领域分文件，位于 `frontend/src/api/`
- **状态管理**: Pinia，位于 `frontend/src/stores/`

## 特殊风格

### DSL 脚本文件 (`.script`)

自定义自动化 DSL，支持：
- 命令: `click`, `input`, `swipe`, `wait`, `human_click` 等
- 选择器: `id:"..."`, `text:"..."`, `xpath:"..."`, `class:"..."`
- 控制流: `if/else/end`, `loop`, `try/catch`, `break`, `continue`
- 变量: `set $name = "value"`, 插值 `${name}`
- 人类模拟: `human_drag` 支持贝塞尔曲线/抖动轨迹

### 文件命名

- 脚本文件可使用中文: `上滑.script`, `下滑.script`
- Vue 组件: PascalCase (`DeviceCard.vue`)
- Python: snake_case (`script_parser.py`)

## 常用命令

```bash
# 后端
uv pip install -e .                    # 安装依赖
uv run uvicorn app.main:app --reload   # 开发服务器 (端口 8000)

# 前端
cd frontend && npm install && npm run dev  # 开发服务器 (端口 5173)
cd frontend && npm run build               # 生产构建

# 测试
pytest                                     # 运行测试（覆盖率较低）

# Docker
docker-compose up -d --build               # 构建并运行
```

## 反模式

- **未发现明确的 DO NOT/NEVER 注释** - 代码库使用中文文档，注释清晰
- **无正式 CI 流水线** - 仅 Docker 构建，无 GitHub Actions
- **测试覆盖率较低** - 仅有 2 个基础接口测试

## 注意事项

### Swagger UI CDN 补丁

`app/main.py` 对 FastAPI 的 Swagger UI 进行了补丁，使用国内 CDN (staticfile.org) 加速加载。

### 设备连接

- USB: 自动检测或传入序列号
- WiFi: 传入 IP:port，通过 ADB 自动连接

### Docker 要求

- 需要 `--privileged` + USB 设备穿透才能访问安卓设备
- 多阶段构建: 前端在 Docker 镜像内构建
- Android SDK 在构建时下载（约 110MB）

### DSL 脚本

位于 `scripts/` 目录。通过 API 执行：
- POST `/api/v1/script/execute` - 执行脚本内容
- POST `/api/v1/script/execute/{name}` - 执行脚本文件
- POST `/api/v1/script/execute/stream` - SSE 流式执行