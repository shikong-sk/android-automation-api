# Android Automation API

基于 uiautomator2 和 adbutils 的安卓设备自动化控制 REST API 服务。

## 项目简介

本项目通过 FastAPI 提供 RESTful API 接口，实现对安卓设备的自动化控制。支持设备连接（USB/WiFi）、界面交互、导航控制、应用管理、元素定位、ADB 命令执行等操作。

## 技术栈

### 后端
- **Python 3.11+**: 开发语言
- **uiautomator2**: 安卓设备自动化控制库
- **adbutils**: ADB 命令操作库
- **FastAPI**: Web 框架
- **Pydantic**: 数据验证和序列化
- **uv**: Python 包管理工具

### 前端
- **Vue 3**: 前端框架
- **Vite**: 构建工具
- **Element Plus**: UI 组件库
- **Tailwind CSS**: 样式框架
- **@vicons/fa**: 图标库

## 项目结构

```
├── app/                          # FastAPI 后端源码
│   ├── api/                      # API 路由
│   │   ├── device.py             # 设备连接相关接口
│   │   ├── input.py              # 输入交互接口（含元素定位）
│   │   ├── navigation.py         # 系统导航接口
│   │   ├── app.py                # 应用管理接口
│   │   ├── adb.py                # ADB 命令接口
│   │   └── script.py             # 自动化脚本接口
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
│   │   ├── app_service.py        # 应用管理服务
│   │   ├── adb_service.py        # ADB 命令服务
│   │   ├── script_parser.py      # 脚本解析器（词法/语法分析）
│   │   └── script_executor.py    # 脚本执行器
│   ├── main.py                   # 应用入口
│   └── __init__.py               # 模块初始化
├── scripts/                      # 脚本存储目录
├── frontend/                     # Vue 前端源码
│   ├── src/
│   │   ├── api/                  # API 客户端
│   │   │   ├── index.js          # API 导出
│   │   │   ├── request.js        # Axios 实例
│   │   │   ├── app.js            # 应用管理 API
│   │   │   ├── device.js         # 设备相关 API
│   │   │   ├── input.js          # 输入操作 API
│   │   │   ├── navigation.js     # 导航控制 API
│   │   │   ├── adb.js            # ADB 命令 API
│   │   │   └── script.js         # 脚本管理 API（含 SSE 流式执行）
│   │   ├── components/           # Vue 组件
│   │   │   ├── AppManager.vue    # 应用管理组件
│   │   │   ├── DeviceCard.vue    # 设备状态组件
│   │   │   ├── InputControl.vue  # 输入操作组件
│   │   │   ├── NavigationControl.vue # 导航控制组件
│   │   │   ├── AdbManager.vue    # ADB 工具组件
│   │   │   ├── ScriptEditor.vue  # 脚本编辑器组件
│   │   │   └── XPathGenerator.vue # XPath 生成器组件
│   │   ├── layouts/              # 布局组件
│   │   │   └── DefaultLayout.vue
│   │   ├── pages/                # 页面组件
│   │   │   ├── Apps.vue          # 应用管理页
│   │   │   ├── Dashboard.vue     # 仪表盘
│   │   │   ├── Device.vue        # 设备页
│   │   │   ├── Input.vue         # 输入操作页
│   │   │   ├── Navigation.vue    # 导航控制页
│   │   │   ├── Adb.vue           # ADB 工具页
│   │   │   └── Script.vue        # 自动化脚本页
│   │   ├── App.vue               # 根组件
│   │   └── main.js               # 应用入口
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── pyproject.toml                # 项目配置
├── Dockerfile                    # Docker 镜像构建文件
├── docker-compose.example.yaml   # Docker Compose 示例配置
├── .env                          # 环境变量
└── README.md                     # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
uv pip install -e .
```

### 2. 启动后端服务

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端服务

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问

- 前端界面: http://localhost:5173
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Docker 部署

### 使用 Docker Compose（推荐）

1. 复制示例配置文件：

```bash
cp docker-compose.example.yaml docker-compose.yaml
```

2. 根据需要修改 `docker-compose.yaml` 中的配置

3. 构建并启动容器：

```bash
docker-compose up -d --build
```

4. 访问服务：http://localhost:8000

### 手动构建镜像

```bash
# 构建镜像
docker build -t android-automation-api:latest .

# 运行容器
docker run -d \
  --name android-automation-api \
  -p 8000:80 \
  --privileged \
  --device /dev/bus/usb:/dev/bus/usb \
  -v ./scripts:/app/scripts \
  android-automation-api:latest
```

### Docker 配置说明

| 配置项 | 说明 |
|--------|------|
| `ports: 8000:80` | 将容器 80 端口映射到主机 8000 端口 |
| `privileged: true` | 允许容器访问 USB 设备 |
| `devices` | 挂载 USB 设备目录，用于 ADB 连接 |
| `volumes` | 挂载脚本目录，支持热更新脚本 |

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `APP_NAME` | Android Automation API | 应用名称 |
| `APP_VERSION` | 1.0.0 | 应用版本 |
| `DEBUG` | false | 调试模式 |
| `DEFAULT_DEVICE_SERIAL` | 空 | 默认设备序列号 |

### 注意事项

1. **USB 设备访问**：容器需要 `privileged` 权限才能访问 USB 设备
2. **WiFi 连接**：确保容器网络可以访问目标设备 IP
3. **脚本持久化**：建议挂载 `scripts` 目录以持久化脚本文件
4. **健康检查**：容器内置健康检查，访问 `/health` 端点

## API 接口文档

### 设备管理

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/device/connect` | 连接设备（支持 USB/WiFi） |
| GET | `/api/v1/device/status` | 获取设备状态 |
| POST | `/api/v1/device/disconnect` | 断开设备连接 |

### 输入操作 - 基础交互

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/input/click` | 点击元素 |
| POST | `/api/v1/input/set-text` | 输入文本 |
| POST | `/api/v1/input/clear-text` | 清除文本 |
| POST | `/api/v1/input/swipe` | 滑动屏幕 |
| POST | `/api/v1/input/send-action` | 发送完成动作 |
| POST | `/api/v1/input/execute` | 执行自定义操作 |

### 输入操作 - 屏幕控制

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/input/screen-on` | 亮屏 |
| POST | `/api/v1/input/screen-off` | 锁屏 |
| POST | `/api/v1/input/unlock` | 解锁屏幕 |

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

### 输入操作 - 通用选择器

支持多种选择器类型（id、text、class、xpath）的统一接口：

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/input/set-text-by-selector` | 通过选择器输入文本 |
| POST | `/api/v1/input/clear-text-by-selector` | 通过选择器清除文本 |
| POST | `/api/v1/input/send-action-by-selector` | 通过选择器发送完成动作 |
| GET | `/api/v1/input/wait-appear-by-selector` | 通过选择器等待元素出现 |
| GET | `/api/v1/input/wait-gone-by-selector` | 通过选择器等待元素消失 |
| GET | `/api/v1/input/text-by-selector` | 通过选择器获取元素文本 |
| GET | `/api/v1/input/bounds-by-selector` | 通过选择器获取元素边界 |

### 输入操作 - 人类模拟

模拟真实人类的点击和拖拽行为，包含随机偏移、延迟和自然的运动轨迹：

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/input/human-click` | 模拟人类点击（随机偏移、延迟、按压时长） |
| POST | `/api/v1/input/human-double-click` | 模拟人类双击 |
| POST | `/api/v1/input/human-long-press` | 模拟人类长按 |
| POST | `/api/v1/input/human-drag` | 模拟人类拖拽（贝塞尔曲线/直线抖动轨迹） |

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
| GET | `/api/v1/app/current` | 获取当前前台应用 |

### ADB 工具 - 应用管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/adb/packages` | 获取已安装应用列表 |
| GET | `/api/v1/adb/packages/{package_name}` | 获取应用详细信息 |
| GET | `/api/v1/adb/packages-info` | 获取所有应用详细信息 |
| POST | `/api/v1/adb/install` | 安装 APK |
| DELETE | `/api/v1/adb/packages/{package_name}` | 卸载应用 |

### ADB 工具 - 设备信息

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/adb/device-info` | 获取设备详细信息 |
| GET | `/api/v1/adb/battery` | 获取电池信息 |
| GET | `/api/v1/adb/screen/resolution` | 获取屏幕分辨率 |
| GET | `/api/v1/adb/screen/density` | 获取屏幕密度 |
| GET | `/api/v1/adb/prop/{prop_name}` | 获取设备属性 |

### ADB 工具 - Shell 与文件

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/adb/shell` | 执行 Shell 命令 |
| POST | `/api/v1/adb/push` | 推送文件到设备 |
| POST | `/api/v1/adb/pull` | 从设备拉取文件 |
| POST | `/api/v1/adb/screenshot` | 截取屏幕截图 |
| POST | `/api/v1/adb/reboot` | 重启设备 |

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
# 自动选择设备
curl -X POST "http://localhost:8000/api/v1/device/connect"

# 通过序列号连接（USB）
curl -X POST "http://localhost:8000/api/v1/device/connect" \
  -H "Content-Type: application/json" \
  -d '{"device_serial": "emulator-5554"}'

# 通过 IP 连接（WiFi）
curl -X POST "http://localhost:8000/api/v1/device/connect" \
  -H "Content-Type: application/json" \
  -d '{"device_serial": "192.168.1.100:5555"}'
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
# 等待元素出现（最多10秒）- 通过 resource-id
curl "http://localhost:8000/api/v1/input/wait-appear?resource_id=com.example:id/dialog&timeout=10"

# 等待元素消失（最多10秒）- 通过 resource-id
curl "http://localhost:8000/api/v1/input/wait-gone?resource_id=com.example:id/loading&timeout=10"

# 通过选择器等待元素出现
curl "http://localhost:8000/api/v1/input/wait-appear-by-selector?selector_type=xpath&selector_value=//Button[@text='确定']&timeout=10"

# 通过选择器等待元素消失
curl "http://localhost:8000/api/v1/input/wait-gone-by-selector?selector_type=text&selector_value=加载中&timeout=10"
```

### 通用选择器操作

```bash
# 通过 XPath 输入文本
curl -X POST "http://localhost:8000/api/v1/input/set-text-by-selector?selector_type=xpath&selector_value=//EditText[@resource-id='com.example:id/input']&text=Hello"

# 通过文本定位清除文本
curl -X POST "http://localhost:8000/api/v1/input/clear-text-by-selector?selector_type=text&selector_value=请输入"

# 通过选择器获取元素文本
curl "http://localhost:8000/api/v1/input/text-by-selector?selector_type=id&selector_value=com.example:id/title"

# 通过选择器获取元素边界
curl "http://localhost:8000/api/v1/input/bounds-by-selector?selector_type=xpath&selector_value=//Button[1]"
```

### 屏幕控制

```bash
# 亮屏
curl -X POST "http://localhost:8000/api/v1/input/screen-on"

# 锁屏
curl -X POST "http://localhost:8000/api/v1/input/screen-off"

# 解锁
curl -X POST "http://localhost:8000/api/v1/input/unlock"
```

### 人类模拟操作

```bash
# 人类模拟点击 - 通过坐标
curl -X POST "http://localhost:8000/api/v1/input/human-click" \
  -H "Content-Type: application/json" \
  -d '{"x": 500, "y": 800}'

# 人类模拟点击 - 通过选择器
curl -X POST "http://localhost:8000/api/v1/input/human-click" \
  -H "Content-Type: application/json" \
  -d '{"selector_type": "id", "selector_value": "com.example:id/button"}'

# 人类模拟点击 - 自定义参数
curl -X POST "http://localhost:8000/api/v1/input/human-click" \
  -H "Content-Type: application/json" \
  -d '{
    "x": 500, "y": 800,
    "offset_min": 5, "offset_max": 15,
    "delay_min": 0.1, "delay_max": 0.5,
    "duration_min": 0.05, "duration_max": 0.2
  }'

# 人类模拟双击
curl -X POST "http://localhost:8000/api/v1/input/human-double-click" \
  -H "Content-Type: application/json" \
  -d '{"selector_type": "text", "selector_value": "确定"}'

# 人类模拟长按
curl -X POST "http://localhost:8000/api/v1/input/human-long-press" \
  -H "Content-Type: application/json" \
  -d '{"x": 500, "y": 800, "duration_min": 1.0, "duration_max": 2.0}'

# 人类模拟拖拽 - 贝塞尔曲线轨迹
curl -X POST "http://localhost:8000/api/v1/input/human-drag" \
  -H "Content-Type: application/json" \
  -d '{
    "start_x": 500, "start_y": 1500,
    "end_x": 500, "end_y": 500,
    "trajectory_type": "bezier",
    "speed_mode": "ease_in_out",
    "duration": 1.0
  }'

# 人类模拟拖拽 - 指定拖拽时间
curl -X POST "http://localhost:8000/api/v1/input/human-drag" \
  -H "Content-Type: application/json" \
  -d '{
    "start_x": 500, "start_y": 1500,
    "end_x": 500, "end_y": 500,
    "duration": 2.0
  }'

# 人类模拟拖拽 - 直线抖动轨迹
curl -X POST "http://localhost:8000/api/v1/input/human-drag" \
  -H "Content-Type: application/json" \
  -d '{
    "start_x": 100, "start_y": 1500,
    "end_x": 100, "end_y": 500,
    "trajectory_type": "linear_jitter",
    "speed_mode": "random",
    "duration": 1.5,
    "num_points": 80
  }'

# 人类模拟拖拽 - 元素到元素
curl -X POST "http://localhost:8000/api/v1/input/human-drag" \
  -H "Content-Type: application/json" \
  -d '{
    "start_selector_type": "id",
    "start_selector_value": "com.example:id/item",
    "end_selector_type": "id",
    "end_selector_value": "com.example:id/target"
  }'
```

### ADB 命令

```bash
# 获取已安装应用列表（第三方应用）
curl "http://localhost:8000/api/v1/adb/packages?filter_type=third_party"

# 获取应用详细信息
curl "http://localhost:8000/api/v1/adb/packages/com.example.app"

# 执行 Shell 命令
curl -X POST "http://localhost:8000/api/v1/adb/shell" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls /sdcard"}'

# 获取设备信息
curl "http://localhost:8000/api/v1/adb/device-info"

# 获取电池信息
curl "http://localhost:8000/api/v1/adb/battery"

# 卸载应用
curl -X DELETE "http://localhost:8000/api/v1/adb/packages/com.example.app"
```

### 脚本执行

```bash
# 执行脚本内容
curl -X POST "http://localhost:8000/api/v1/script/execute" \
  -H "Content-Type: application/json" \
  -d '{"content": "home\nwait 1\nlog \"完成\""}'

# 执行脚本文件
curl -X POST "http://localhost:8000/api/v1/script/execute/my_script.script"

# 验证脚本语法
curl -X POST "http://localhost:8000/api/v1/script/validate" \
  -H "Content-Type: application/json" \
  -d '{"content": "click id:\"button\"\nwait 1"}'

# 流式执行脚本（SSE）
curl -N -X POST "http://localhost:8000/api/v1/script/execute/stream" \
  -H "Content-Type: application/json" \
  -d '{"content": "home\nwait 1\nlog \"完成\""}'

# 停止正在执行的脚本
curl -X POST "http://localhost:8000/api/v1/script/stop/{session_id}"
```

## 前端功能页面

| 页面 | 路由 | 描述 |
|------|------|------|
| 控制台 | `/` | 设备状态总览、快捷操作 |
| 设备管理 | `/device` | 设备连接状态 |
| 输入控制 | `/input` | 点击、输入、滑动、元素定位、屏幕控制、XPath 生成器 |
| 导航控制 | `/navigation` | 返回主页、返回、菜单等导航操作 |
| 应用管理 | `/apps` | 启动、停止、清除应用数据 |
| ADB 工具 | `/adb` | 设备信息、应用列表、Shell 命令执行 |
| 自动化脚本 | `/script` | 脚本编辑、执行、管理 |

## XPath 生成器

项目提供可视化的 XPath 生成器，帮助不熟悉 XPath 语法的用户快速生成 XPath 表达式。

### 功能特性

#### 1. 快捷模板库

提供 8 种常用 XPath 模板，一键填充参数即可生成：

| 模板名称 | 模板格式 | 说明 |
|----------|----------|------|
| 按 resource-id 定位 | `//*[@resource-id="___"]` | 最常用的定位方式 |
| 按文本精确匹配 | `//*[@text="___"]` | 通过显示文本定位 |
| 按文本包含匹配 | `//*[contains(@text, "___")]` | 模糊文本匹配 |
| 按 content-desc 定位 | `//*[@content-desc="___"]` | 通过无障碍描述定位 |
| 按类型+文本组合 | `//___[@text="___"]` | 指定元素类型和文本 |
| 按类型+ID组合 | `//___[@resource-id="___"]` | 指定元素类型和 ID |
| 父子关系定位 | `//*[@resource-id="___"]/___` | 通过父元素定位子元素 |
| 索引定位 | `(//___)[___]` | 定位同类元素中的第 N 个 |

#### 2. 属性组合生成器

通过表单选择元素属性，自动组合生成 XPath：

- **元素类型选择**：支持 17 种常用 Android 控件类型
- **多条件组合**：支持 AND/OR 逻辑组合多个属性条件
- **匹配方式**：等于、包含、开头是、结尾是
- **索引定位**：可指定匹配第 N 个元素

支持的属性：
- `resource-id` - 元素 ID
- `text` - 显示文本
- `content-desc` - 无障碍描述
- `class` - 元素类名
- `package` - 包名
- `checkable/checked` - 可选中/已选中
- `clickable` - 可点击
- `enabled` - 已启用
- `focusable/focused` - 可聚焦/已聚焦
- `scrollable` - 可滚动
- `selected` - 已选择

#### 3. XML 树形选择器

将当前界面 XML 解析为可交互的树形结构：

- **可视化展示**：以树形结构展示界面元素层级
- **搜索过滤**：支持按元素名、ID、文本等搜索节点
- **点击生成**：点击任意节点自动生成 XPath
- **多种策略**：
  - 智能推荐 - 自动选择最佳定位方式
  - 优先 ID - 优先使用 resource-id
  - 优先文本 - 优先使用 text 属性
  - 完整路径 - 生成完整的层级路径

#### 4. XPath 测试验证

- 一键测试生成的 XPath 是否能找到元素
- 显示匹配元素数量和基本信息
- 实时验证，快速调试

#### 5. 快捷操作

- **复制到剪贴板**：一键复制生成的 XPath
- **插入到输入框**：直接插入到当前操作的输入框

### 使用入口

1. **界面结构卡片** - 点击 "XPath 生成器" 按钮
2. **点击元素 Tab** - 选择 "By XPath" 后，点击输入框右侧的 "生成" 按钮
3. **元素定位 Tab** - 选择 "By XPath" 后，点击输入框右侧的 "生成" 按钮
4. **输入文本 Tab** - 选择 "By XPath" 后，点击输入框右侧的 "生成" 按钮
5. **等待元素 Tab** - 选择 "By XPath" 后，点击输入框右侧的 "生成" 按钮
6. **元素信息 Tab** - 选择 "By XPath" 后，点击输入框右侧的 "生成" 按钮

### 通用选择器支持

所有输入操作 Tab 现在都支持 4 种选择器类型：

| 选择器类型 | 说明 | 示例 |
|------------|------|------|
| By ID | 通过 resource-id 定位 | `com.example:id/button` |
| By Text | 通过显示文本定位 | `确定` |
| By Class | 通过元素类名定位 | `android.widget.Button` |
| By XPath | 通过 XPath 表达式定位 | `//Button[@text='确定']` |

## 自动化脚本 DSL

项目支持自定义 DSL 脚本，实现全自动化操作。脚本文件存储在 `scripts/` 目录下。

### DSL 语法参考

#### 基础命令

```bash
# 点击元素
click id:"resource_id"           # 通过 resource-id 点击
click text:"文本"                # 通过文本点击
click xpath:"//Button[@text='确定']"  # 通过 XPath 点击

# 输入文本
input id:"input_id" "要输入的文本"

# 清除文本
clear id:"input_id"

# 滑动屏幕
swipe up 0.5                     # 向上滑动 50%
swipe down 0.3                   # 向下滑动 30%
swipe left                       # 向左滑动
swipe right                      # 向右滑动

# 等待
wait 2                           # 等待 2 秒
wait_element id:"loading" 10     # 等待元素出现，最多 10 秒
wait_gone id:"loading" 10        # 等待元素消失，最多 10 秒
```

#### 导航命令

```bash
back                             # 返回
home                             # 主页
menu                             # 菜单
recent                           # 最近应用
```

#### 应用命令

```bash
start_app "com.example.app"      # 启动应用
stop_app "com.example.app"       # 停止应用
clear_app "com.example.app"      # 清除应用数据
```

#### 屏幕控制

```bash
screen_on                        # 亮屏
screen_off                       # 锁屏
unlock                           # 解锁
```

#### 人类模拟操作

模拟真实人类的点击和拖拽行为，包含随机偏移、延迟和自然的运动轨迹：

```bash
# 人类模拟点击 - 通过选择器
human_click id:"button_id"
human_click text:"确定"
human_click xpath:"//Button[@text='提交']"

# 人类模拟点击 - 通过坐标
human_click 500, 800

# 人类模拟点击 - 自定义参数
human_click 500, 800, offset_min=5, offset_max=15, delay_min=0.1

# 人类模拟双击
human_double_click id:"item"
human_double_click 500, 800, interval_min=0.1, interval_max=0.2

# 人类模拟长按
human_long_press id:"item"
human_long_press 500, 800, duration_min=1.0, duration_max=2.0

# 人类模拟拖拽 - 坐标到坐标
human_drag 100, 1500, 100, 500

# 人类模拟拖拽 - 指定拖拽时间（秒）
human_drag 100, 1500, 100, 500, duration=1.5

# 人类模拟拖拽 - 贝塞尔曲线轨迹（推荐）
human_drag 100, 1500, 100, 500, trajectory="bezier", speed="ease_in_out"

# 人类模拟拖拽 - 直线抖动轨迹
human_drag 100, 1500, 100, 500, trajectory="linear_jitter", speed="random"
```

**人类模拟参数说明：**

| 参数 | 默认值 | 描述 |
|------|--------|------|
| `offset_min/max` | 3/10 | 随机偏移范围（像素） |
| `delay_min/max` | 0.05/0.3 | 操作前延迟范围（秒） |
| `duration_min/max` | 0.05/0.15 | 按压时长范围（秒） |
| `interval_min/max` | 0.1/0.2 | 双击间隔范围（秒） |
| `duration` | 1.0 | 拖拽总时间（秒） |
| `trajectory` | bezier | 拖拽轨迹类型：bezier, linear_jitter |
| `speed` | ease_in_out | 速度模式：ease_in_out, ease_in, ease_out, linear, random |
| `num_points` | 50 | 轨迹采样点数量 |
| `jitter_min/max` | 1/5 | 直线轨迹抖动范围（像素） |

#### 变量

```bash
set $name = "value"              # 设置变量
set $text = get_text id:"id"     # 获取元素文本
set $exists = exists id:"id"     # 检查元素是否存在

# 使用变量
click text:$name
input id:"input" $text
```

#### 条件判断

```bash
if exists id:"button"
    click id:"button"
elif $var == "value"
    log "变量匹配"
else
    log "未找到"
end

# 条件表达式
# exists id:"xxx"        - 元素存在
# not exists id:"xxx"    - 元素不存在
# $var == "value"        - 变量等于
# $var != "value"        - 变量不等于
# $var                   - 变量为真
```

#### 循环

```bash
# 固定次数循环
loop 5
    click id:"button"
    wait 1
end

# 条件循环
while exists id:"loading"
    wait 1
end

# 循环控制
loop 10
    if exists id:"done"
        break                    # 跳出循环
    end
    click id:"next"
    continue                     # 继续下一次
end
```

#### 错误处理

```bash
try
    click id:"maybe_not_exist"
    wait 1
catch
    log "元素不存在，跳过"
end
```

#### 子脚本调用

```bash
call "other_script.script"       # 调用其他脚本
```

#### 其他命令

```bash
log "日志消息"                   # 输出日志
shell "ls /sdcard"               # 执行 shell 命令
# 这是注释
```

### 脚本示例

```bash
# 自动打开设置并滑动
start_app "com.android.settings"
wait 2

# 等待界面加载
wait_element id:"android:id/title" 10

# 查找并点击 WLAN
if exists text:"WLAN"
    click text:"WLAN"
    wait 1
else
    log "未找到 WLAN"
end

# 滑动 3 次
loop 3
    swipe up 0.3
    wait 0.5
end

# 返回主页
home
log "完成"
```

### 脚本 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/script/list` | 获取脚本列表 |
| GET | `/api/v1/script/get/{name}` | 获取脚本内容 |
| POST | `/api/v1/script/save` | 保存脚本 |
| DELETE | `/api/v1/script/delete/{name}` | 删除脚本 |
| POST | `/api/v1/script/execute` | 执行脚本内容 |
| POST | `/api/v1/script/execute/{name}` | 执行脚本文件 |
| POST | `/api/v1/script/validate` | 验证脚本语法 |

### 脚本 API - 流式执行（SSE）

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/script/execute/stream` | 执行脚本并通过 SSE 实时返回日志 |
| POST | `/api/v1/script/execute/stream/{name}` | 执行脚本文件并通过 SSE 实时返回日志 |
| POST | `/api/v1/script/stop/{session_id}` | 停止正在执行的脚本 |

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
2. **WiFi 连接**：确保设备和服务器在同一网络，设备已开启 ADB over WiFi（端口默认 5555）
3. **元素定位**：建议优先使用 resource-id 定位，稳定性最高
4. **等待机制**：界面元素加载需要时间，建议使用 `wait-appear` 等待元素
5. **权限要求**：确保设备已开启 USB 调试模式

## 许可证

MIT License
