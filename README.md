# Android Automation API

基于 uiautomator2 的安卓设备自动化控制 REST API 服务。

## 项目简介

本项目通过 FastAPI 提供 RESTful API 接口，实现对安卓设备的自动化控制。支持设备连接、界面交互、导航控制、应用管理、元素定位等操作。

## 技术栈

- **Python 3.11+**: 开发语言
- **uiautomator2**: 安卓设备自动化控制库
- **FastAPI**: Web 框架
- **Pydantic**: 数据验证和序列化
- **uv**: Python 包管理工具

## 项目结构

```
├── app/                          # FastAPI 后端源码
│   ├── api/                      # API 路由
│   │   ├── device.py             # 设备连接相关接口
│   │   ├── input.py              # 输入交互接口（含元素定位）
│   │   ├── navigation.py         # 系统导航接口
│   │   └── app.py                # 应用管理接口
│   ├── core/                     # 核心模块
│   │   ├── config.py             # 配置管理
│   │   └── device.py             # 设备管理器（单例模式）
│   ├── dependencies/             # 依赖注入
│   │   └── services.py           # 服务依赖工厂函数
│   ├── schemas/                  # 数据模型
│   │   ├── device.py             # 设备相关模型
│   │   └── action.py             # 操作相关模型
│   ├── services/                 # 业务逻辑服务
│   │   ├── base.py               # 服务基类
│   │   ├── input.py              # 输入操作服务（含元素定位）
│   │   ├── navigation.py         # 导航操作服务
│   │   └── app_service.py        # 应用管理服务
│   ├── main.py                   # 应用入口
│   └── __init__.py               # 模块初始化
├── tests/                        # 测试文件
├── frontend/                     # Vue 前端目录 (待开发)
├── pyproject.toml                # 项目配置
├── .env                          # 环境变量
└── README.md                     # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
uv pip install -e .
```

### 2. 启动服务

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问 API 文档

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## API 接口文档

### 设备管理

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/device/connect` | 连接设备 |
| GET | `/api/v1/device/status` | 获取设备状态 |
| POST | `/api/v1/device/disconnect` | 断开设备连接 |

### 输入操作 - 基础交互

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/input/click` | 点击元素 |
| POST | `/api/v1/input/set-text` | 输入文本 |
| POST | `/api/v1/input/clear-text` | 清除文本 |
| POST | `/api/v1/input/swipe` | 滑动屏幕 |
| POST | `/api/v1/input/execute` | 执行自定义操作 |

### 输入操作 - 元素定位

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/input/find-by-id` | 通过 resource-id 查找元素 |
| GET | `/api/v1/input/find-by-text` | 通过文本内容查找元素 |
| GET | `/api/v1/input/find-by-class` | 通过类名查找元素 |
| GET | `/api/v1/input/find-elements-by-class` | 查找所有匹配元素 |
| GET | `/api/v1/input/find-by-xpath` | 通过 XPath 查找元素 |

### 输入操作 - 元素状态

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/input/exists` | 检查元素是否存在 |
| GET | `/api/v1/input/text` | 获取元素文本内容 |
| GET | `/api/v1/input/bounds` | 获取元素边界位置 |
| GET | `/api/v1/input/wait-appear` | 等待元素出现 |
| GET | `/api/v1/input/wait-gone` | 等待元素消失 |
| GET | `/api/v1/input/hierarchy` | 获取当前界面 XML 结构 |

### 导航控制

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/navigation/home` | 返回主屏幕 |
| POST | `/api/v1/navigation/back` | 返回上一页 |
| POST | `/api/v1/navigation/menu` | 打开菜单 |
| POST | `/api/v1/navigation/go-home` | 确保返回主页 |
| POST | `/api/v1/navigation/recent-apps` | 打开最近应用 |

### 应用管理

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/app/start/{package}` | 启动应用 |
| POST | `/api/v1/app/stop/{package}` | 停止应用 |
| POST | `/api/v1/app/clear/{package}` | 清除应用数据 |
| GET | `/api/v1/app/version/{package}` | 获取应用版本 |
| GET | `/api/v1/app/status/{package}` | 检查应用运行状态 |

## 配置说明

通过 `.env` 文件或环境变量进行配置：

```env
APP_NAME=Android Automation API
APP_VERSION=1.0.0
DEBUG=true
DEFAULT_DEVICE_SERIAL=     # 可选，指定默认设备序列号
```

## 示例请求

### 连接设备

```bash
curl -X POST "http://localhost:8000/api/v1/device/connect"
```

### 点击元素

```bash
curl -X POST "http://localhost:8000/api/v1/input/click" \
  -H "Content-Type: application/json" \
  -d '{"resource_id": "com.example:id/button"}'
```

### 查找元素

```bash
# 通过 resource-id 查找
curl "http://localhost:8000/api/v1/input/find-by-id?resource_id=com.example:id/button"

# 检查元素是否存在
curl "http://localhost:8000/api/v1/input/exists?resource_id=com.example:id/button"

# 获取界面 XML 结构
curl "http://localhost:8000/api/v1/input/hierarchy"
```

### 启动应用

```bash
curl -X POST "http://localhost:8000/api/v1/app/start/com.example.app"
```

### 等待元素

```bash
# 等待元素出现（最多10秒）
curl "http://localhost:8000/api/v1/input/wait-appear?resource_id=com.example:id/dialog&timeout=10"

# 等待元素消失（最多10秒）
curl "http://localhost:8000/api/v1/input/wait-gone?resource_id=com.example:id/loading&timeout=10"
```

## 元素定位方式详解

### 1. resource-id 定位

通过元素的 `resource-id` 属性定位，是最常用和稳定的定位方式：

```python
element = device(resourceId="com.example:id/button")
```

### 2. text 定位

通过元素的显示文本内容定位：

```python
element = device(text="确定")
```

### 3. className 定位

通过元素的 Android 类名定位：

```python
# 单个元素
element = device(className="android.widget.Button")

# 所有匹配元素
elements = device(className="android.widget.Button")
for elem in elements:
    print(elem.info)
```

### 4. XPath 定位

使用 XPath 表达式进行灵活定位：

```python
element = device(xpath="//android.widget.Button[@text='确定']")
element = device(xpath="//*[@resource-id='com.example:id/button']")
```

## 注意事项

1. **设备连接**：使用 API 前需先调用 `/api/v1/device/connect` 连接设备
2. **元素定位**：建议优先使用 resource-id 定位，稳定性最高
3. **等待机制**：界面元素加载需要时间，建议使用 `wait-appear` 等待元素
4. **权限要求**：确保设备已开启 USB 调试模式

## 许可证

MIT License
