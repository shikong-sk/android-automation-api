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
set $info = get_info id:"id"     # 获取元素完整信息
set $exists = exists id:"id"     # 检查元素是否存在

# 使用变量
click text:$name
input id:"input" $text
```

#### 变量插值

支持 `${variable}` 语法在字符串中插入变量值：

```bash
# 基础插值
set $name = "World"
log "Hello ${name}"              # 输出: Hello World

# 多变量插值
set $x = 10
set $y = 20
log "x + y = ${x} + ${y}"        # 输出: x + y = 10 + 20

# 选择器值插值
set $target_id = "com.example:id/button"
click id:"${target_id}"

# 命令参数插值
set $username = "test@example.com"
input id:"username" "${username}"
input id:"password" "${password}"

# 结合使用
set $app = "com.android.settings"
set $element_id = "search"
start_app "${app}"
click id:"com.android.settings:id/${element_id}"
```

**变量作用域：**
- 变量在整个脚本中有效
- 子脚本调用会继承父脚本的所有变量
- 子脚本是变量隔离的，修改不会影响父脚本

**语法限制：**
1. 必须使用 `${variable}` 语法进行字符串插值
   - ✅ 正确：`log "Name: ${name}"`
   - ❌ 错误：`log "Name: $name"`（不会被解析）

2. 不支持对象属性访问和方法调用
   - ❌ 错误：`${xml.length}` - 不支持 `.length`
   - ❌ 错误：`${str.substring(0,10)}` - 不支持方法调用
   - ✅ 替代：使用完整的字符串值

3. 不支持表达式求值
   - ❌ 错误：`${x + y}` - 不支持数学运算
   - ✅ 替代：先计算再赋值 `set $sum = 30`, `log "${sum}"`

4. 未定义的变量保持原样
   - `${undefined_var}` → `${undefined_var}`（不报错，保持原字符串）

5. 变量值会自动转换为字符串
   - 数字 10 会转换为 "10"
   - 布尔值 true 会转换为 "True"

#### 元素信息获取

```bash
# 获取元素文本内容
get_text id:"button_id"
get_text text:"确定"
get_text xpath:"//Button[@text='提交']"

# 获取元素完整信息（包括text、class、bounds等）
get_info id:"element_id"
get_info class:"android.widget.Button"

# 查找元素（返回元素信息）
find_element id:"com.example:id/button"
find_element text:"确定"
find_element class:"android.widget.Button"
find_element xpath:"//Button[@text='提交']"

# 查找所有匹配元素
find_elements class:"android.widget.TextView"
find_elements id:"item"

# 导出当前界面XML层次结构
dump_hierarchy
```

#### 条件判断

```bash
if exists id:"button"
    click id:"button"
else
    log "未找到"
end

# 条件表达式
# exists id:"xxx"        - 元素存在
# not exists id:"xxx"    - 元素不存在
```

#### 循环

```bash
# 固定次数循环
loop 5
    click id:"button"
    wait 1
end

# 条件循环（使用 loop + break）
loop 30
    if not exists id:"loading"
        log "加载完成"
        break
    end
    wait 0.5
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

**基础示例 - 自动打开设置并滑动：**

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

**元素信息获取示例：**

```bash
# 获取元素信息
start_app "com.android.settings"

# 获取标题文本并记录
set $title = get_text id:"android:id/title"
log "当前页面标题: $title"

# 获取按钮完整信息
set $btn_info = get_info id:"com.android.settings:id/search"
log $btn_info

# 查找所有 TextView 元素
set $textviews = find_elements class:"android.widget.TextView"
log "找到元素"

# 导出当前界面结构（用于调试）
set $xml = dump_hierarchy
log "界面结构已导出"
```

### 完整 DSL 命令参考

#### 1. 设备连接与状态

```bash
# 连接设备（自动选择第一个可用设备）
connect

# 通过序列号连接设备
connect "emulator-5554"

# 通过 WiFi IP 连接设备
connect "192.168.1.100:5555"

# 获取设备状态
get_status

# 断开设备连接
disconnect
```

#### 2. 元素定位方式详解

DSL 支持四种元素定位方式，每种方式适用于不同场景：

**2.1 resource-id 定位（推荐）**

通过元素的 `resource-id` 属性定位，是最稳定和可靠的定位方式：

```bash
# 通过完整的 resource-id 点击
click id:"com.example.app:id/submit_button"

# 通过部分 ID 定位（需要确保唯一性）
click id:"submit_button"

# 定位输入框并输入文本
input id:"username_input" "test_user"

# 清除输入框内容
clear id:"password_input"
```

**2.2 text 定位**

通过元素的显示文本内容定位，适用于文本内容固定的场景：

```bash
# 精确文本匹配
click text:"确定"
click text:"提交"
click text:"取消"

# 包含文本匹配（需要配合 XPath）
click xpath:"//*[contains(@text, '确认')]"
```

**2.3 class 定位**

通过元素的 Android 类名定位，适用于批量操作同类元素：

```bash
# 定位单个按钮
click class:"android.widget.Button"

# 定位所有按钮并操作（需要循环）
set $buttons = find_elements class:"android.widget.Button"
log "找到按钮"

# 定位列表项
click class:"android.widget.ListView"
```

**2.4 XPath 定位（最灵活）**

使用 XPath 表达式进行灵活定位，支持复杂的定位条件：

```bash
# 精确匹配
click xpath:"//android.widget.Button[@text='确定']"

# 属性包含
click xpath:"//*[contains(@text, '提交')]"

# 组合条件（AND）
click xpath:"//android.widget.Button[@clickable='true' and @enabled='true']"

# 索引定位（选择第 N 个匹配元素）
click xpath:"(//android.widget.Button)[1]"
click xpath:"(//android.widget.Button)[last()]"

# 父子关系定位
click xpath:"//android.widget.LinearLayout[@resource-id='container']/android.widget.Button"

# 跨层级定位
click xpath:"//android.widget.ListView//android.widget.Button[@text='详情']"
```

#### 3. 滑动操作详解

滑动操作支持多种方向和幅度控制：

```bash
# 基础滑动方向
swipe up              # 向上滑动（默认幅度 0.5）
swipe down            # 向下滑动
swipe left            # 向左滑动
swipe right           # 向右滑动

# 指定滑动幅度（0.1 - 1.0）
swipe up 0.3          # 向上滑动 30% 屏幕高度
swipe down 0.8        # 向下滑动 80% 屏幕高度
swipe left 0.5        # 向左滑动 50% 屏幕宽度
swipe right 0.5       # 向右滑动 50% 屏幕宽度

# 坐标滑动（从指定位置滑动）
swipe 100, 500, 100, 200    # 从 (100,500) 滑动到 (100,200)
swipe 500, 800, 500, 300    # 从 (500,800) 滑动到 (500,300)

# 带持续时间的滑动（毫秒）
swipe 100, 500, 100, 200, 500    # 滑动持续 500ms
```

#### 4. 等待操作详解

等待操作是自动化脚本中最重要的部分，确保界面元素加载完成：

```bash
# 固定时间等待
wait 1               # 等待 1 秒
wait 0.5             # 等待 0.5 秒
wait 10              # 等待 10 秒

# 等待元素出现
wait_element id:"loading" 10           # 等待 loading 元素出现，最多 10 秒
wait_element text:"确定" 5             # 等待确定按钮出现，最多 5 秒
wait_element xpath:"//Button" 8        # 等待按钮出现，最多 8 秒

# 等待元素消失
wait_gone id:"loading" 10              # 等待 loading 元素消失，最多 10 秒
wait_gone text:"加载中" 5              # 等待加载中文字消失，最多 5 秒

# 组合使用：等待元素出现后执行操作
wait_element id:"submit_button" 10
click id:"submit_button"

# 循环等待直到条件满足
loop 20
    if exists id:"content_loaded"
        log "内容已加载"
        break
    end
    wait 0.5
end
```

#### 5. 应用管理详解

```bash
# 启动应用
start_app "com.example.app"                    # 通过包名启动
start_app "com.example.app/.MainActivity"      # 指定 Activity

# 停止应用
stop_app "com.example.app"

# 清除应用数据（相当于重置应用）
clear_app "com.example.app"

# 获取应用版本
set $version = get_app_version "com.example.app"
log "应用版本: $version"

# 获取当前前台应用
set $current = get_current_app
log "当前应用: $current"
```

#### 6. 屏幕控制详解

```bash
# 亮屏
screen_on

# 锁屏
screen_off

# 解锁屏幕
unlock

# 亮屏并解锁
screen_on
wait 0.5
unlock

# 检查屏幕状态
# 需要配合 get_info 和元素定位
if exists id:"lock_screen"
    unlock
end
```

#### 7. 人类模拟操作详解

人类模拟操作通过添加随机性来模拟真实用户行为，避免被检测为自动化脚本：

**7.1 人类模拟点击**

```bash
# 基础人类模拟点击
human_click id:"button"              # 通过选择器点击
human_click 500, 800                 # 通过坐标点击

# 自定义随机参数
human_click id:"button", offset_min=5, offset_max=15
human_click 500, 800, offset_min=3, offset_max=10, delay_min=0.1, delay_max=0.5

# 参数说明
# offset_min/max: 随机偏移范围（像素），默认 3/10
# delay_min/max: 操作前延迟范围（秒），默认 0.05/0.3
# duration_min/max: 按压时长范围（秒），默认 0.05/0.15
```

**7.2 人类模拟双击**

```bash
# 基础双击
human_double_click id:"item"
human_double_click 500, 800

# 自定义双击间隔
human_double_click id:"item", interval_min=0.1, interval_max=0.3
```

**7.3 人类模拟长按**

```bash
# 基础长按
human_long_press id:"item"
human_long_press 500, 800

# 自定义长按时间
human_long_press id:"item", duration_min=1.0, duration_max=2.0
human_long_press 500, 800, duration_min=1.5, duration_max=3.0
```

**7.4 人类模拟拖拽**

```bash
# 坐标到坐标拖拽
human_drag 100, 1500, 100, 500              # 从 (100,1500) 拖到 (100,500)

# 指定拖拽时间
human_drag 100, 1500, 100, 500, duration=2.0

# 贝塞尔曲线轨迹（推荐，最自然）
human_drag 100, 1500, 100, 500, trajectory="bezier", speed="ease_in_out"

# 直线抖动轨迹（模拟手指不稳）
human_drag 100, 1500, 100, 500, trajectory="linear_jitter", speed="random"

# 元素到元素拖拽
human_drag id:"source_item", id:"target_area"

# 速度模式
human_drag 100, 1500, 100, 500, speed="ease_in"      # 慢-快
human_drag 100, 1500, 100, 500, speed="ease_out"     # 快-慢
human_drag 100, 1500, 100, 500, speed="linear"       # 匀速
human_drag 100, 1500, 100, 500, speed="random"       # 随机速度
```

#### 8. 变量与表达式详解

**8.1 变量赋值**

```bash
# 字符串变量
set $name = "value"
set $app = "com.example.app"

# 数字变量
set $count = 10
set $x = 500
set $y = 800

# 布尔变量
set $is_visible = true
set $is_enabled = false

# 元素信息变量
set $text = get_text id:"title"
set $info = get_info id:"button"
set $exists = exists id:"element"

# 表达式结果变量
set $sum = 30
```

**8.2 条件表达式**

```bash
# 元素存在判断
if exists id:"button"
    click id:"button"
end

# 元素不存在判断
if not exists id:"loading"
    log "加载完成"
end
```

**8.3 循环详解**

```bash
# 固定次数循环
loop 5
    click id:"next"
    wait 1
end

# 条件循环（当条件为真时执行）
loop 30
    if not exists id:"loading"
        log "加载完成"
        break
    end
    wait 0.5
end

# 循环直到条件满足
loop 20
    if exists id:"content"
        log "内容已加载"
        break
    end
    wait 0.5
end

# 循环控制
loop 100
    if exists id:"done"
        break                    # 跳出循环
    end

    if exists id:"skip"
        continue                 # 跳过后续代码，进入下一次循环
    end

    click id:"next"
    wait 1
end

# 嵌套循环
loop 3
    log "外层循环第 ${i} 次"
    loop 5
        log "内层循环"
        wait 0.5
    end
end
```

**8.4 错误处理详解**

```bash
# 基础错误处理
try
    click id:"maybe_not_exist"
    wait 1
catch
    log "元素不存在，跳过操作"
end

# 错误处理与重试
set $retry_count = 0
loop 3
    try
        click id:"submit"
        log "点击成功"
        break                    # 成功后跳出循环
    catch
        log "点击失败，重试"
        wait 1
    end
end

# 多个可能出错的操作
try
    click id:"button1"
    wait_element id:"result" 5
    set $result = get_text id:"result"
catch
    log "操作失败，执行备用方案"
    click id:"backup_button"
end
```

#### 9. 子脚本调用详解

```bash
# 调用同目录下的子脚本
call "login.script"
call "navigate.script"

# 调用子脚本并传递参数（通过变量）
set $target_page = "settings"
call "navigate.script"

# 子脚本示例 (navigate.script)
# ============================
# start_app "com.example.app"
# wait 2
# click id:"${target_page}"
# log "导航到 ${target_page} 页面"

# 最佳实践：将常用操作封装为子脚本
# common_actions.script
# =====================
# log "执行通用操作"
# wait_element id:"ready" 10
# click id:"confirm"
```

#### 10. Shell 命令详解

```bash
# 执行 Shell 命令
shell "ls /sdcard"                           # 列出文件
shell "cat /sdcard/test.txt"                 # 读取文件
shell "rm /sdcard/test.txt"                  # 删除文件
shell "mkdir -p /sdcard/test"                # 创建目录
shell "pm list packages"                     # 列出所有包
shell "dumpsys window"                       # 获取窗口信息

# 获取设备信息
set $info = shell "dumpsys deviceinfo"
log $info

# 截图并保存
shell "screencap -p /sdcard/screenshot.png"

# 获取屏幕分辨率
set $resolution = shell "wm size"
log "屏幕分辨率: $resolution"
```

### 高级用法与最佳实践

#### 1. 页面对象模式

将页面元素定位器集中管理，提高脚本可维护性：

```bash
# page_objects.script
# ==================
# 变量方式管理元素定位器
set $LOGIN_USERNAME = "com.example:id/username"
set $LOGIN_PASSWORD = "com.example:id/password"
set $LOGIN_SUBMIT = "com.example:id/login_button"

# 在主脚本中使用
input id:$LOGIN_USERNAME "test@example.com"
input id:$LOGIN_PASSWORD "password123"
click id:$LOGIN_SUBMIT
```

#### 2. 等待模式

```bash
# 智能等待模式：等待元素出现或超时
loop 60
    if exists id:"content"
        log "元素出现"
        break
    end
    wait 0.5
end

if not exists id:"content"
    log "等待元素超时"
end
```

#### 3. 屏幕截图与调试

```bash
# 在关键步骤截图
try
    click id:"submit"
    wait 2

    # 检查结果
    if exists id:"success"
        log "操作成功"
        shell "screencap -p /sdcard/success.png"
    else
        log "操作可能失败，截图保存"
        shell "screencap -p /sdcard/debug.png"

        # 导出界面结构用于调试
        set $xml = dump_hierarchy
        log $xml
    end
catch
    log "发生错误，截图保存"
    shell "screencap -p /sdcard/error.png"
end
```

#### 4. 性能监控

```bash
# 记录操作耗时
start_app "com.example.app"
wait 3

# 监控内存使用
set $memory = shell "dumpsys meminfo com.example.app | grep TOTAL"
log "内存使用: $memory"

# 监控帧率
set $fps = shell "dumpsys gfxinfo com.example.app"
log "帧率信息: $fps"
```

### 常见问题与解决方案

#### Q1: 元素定位失败

```bash
# 问题：元素定位失败，提示找不到元素

# 解决方案 1: 增加等待时间
wait_element id:"button" 10

# 解决方案 2: 使用更稳定的选择器
# 优先使用 id，其次是 text，最后是 XPath
click id:"submit_button"           # 最佳
click text:"提交"                   # 中等
click xpath:"//Button[@text='提交']"  # 兜底

# 解决方案 3: 检查元素是否被遮挡
set $info = get_info id:"button"
if $info
    click id:"button"
else
    log "元素不存在"
end

# 解决方案 4: 滚动到可见位置
swipe up 0.3
wait 1
```

#### Q2: 滑动不稳定

```bash
# 问题：滑动操作不稳定，有时成功有时失败

# 解决方案 1: 增加滑动幅度
swipe up 0.8              # 使用更大的幅度

# 解决方案 2: 增加滑动后的等待时间
swipe up 0.5
wait 1                    # 等待界面稳定

# 解决方案 3: 使用人类模拟滑动
human_drag 500, 1000, 500, 200, trajectory="bezier", speed="ease_in_out"
```

#### Q3: 应用启动失败

```bash
# 问题：应用启动后立即崩溃或无响应

# 解决方案 1: 检查应用是否已安装
set $packages = shell "pm list packages | grep com.example.app"
if $packages
    log "应用已安装"
else
    log "应用未安装"
end

# 解决方案 2: 清除应用数据后重试
clear_app "com.example.app"
wait 1
start_app "com.example.app"
wait 3

# 解决方案 3: 检查应用状态
set $status = get_app_version "com.example.app"
log "应用版本: $status"
```

#### Q4: 脚本执行速度过快

```bash
# 问题：脚本执行速度过快，导致界面来不及响应

# 解决方案: 在关键操作后增加等待
click id:"button"
wait 1                    # 等待界面响应

# 使用人类模拟操作（自带延迟）
human_click id:"button"

# 动态等待：等待特定元素出现
wait_element id:"result" 10
```

### 完整实战示例

#### 示例 1: 自动化登录流程

```bash
# login_automation.script
# ======================
# 自动化登录流程示例

log "=== 开始自动化登录 ==="

# 配置测试账号
set $test_username = "test@example.com"
set $test_password = "password123"
set $app_package = "com.example.app"

# 启动应用
log "1. 启动应用"
start_app "${app_package}"
wait 3

# 检查是否在登录页面
set $login_btn = get_info id:"login_button"
if not exists id:"login_button"
    log "未找到登录按钮，检查当前页面状态"

    # 如果已登录，跳过登录
    if exists id:"welcome_message"
        log "已登录，跳过登录流程"
    else
        log "未知页面状态，尝试返回主页"
        home
        wait 1
        start_app "${app_package}"
        wait 3
    end
end

# 输入账号密码
log "2. 输入账号信息"
input id:"username" "${test_username}"
wait 0.5
input id:"password" "${test_password}"
wait 0.5

# 点击登录按钮
log "3. 点击登录按钮"
click id:"login_button"

# 等待登录结果
log "4. 等待登录结果"
wait 3

# 验证登录结果
if exists id:"welcome_message"
    set $welcome = get_text id:"welcome_message"
    log "登录成功: $welcome"
else
    # 检查错误信息
    if exists id:"error_message"
        set $error = get_text id:"error_message"
        log "登录失败: $error"
    else
        log "登录结果未知"
    end

    # 截图保存
    shell "screencap -p /sdcard/login_failed.png"
end

log "=== 自动化登录完成 ==="
```

#### 示例 2: 数据采集脚本

```bash
# data_collection.script
# ======================
# 从列表页面采集数据示例

log "=== 开始数据采集 ==="

# 配置
set $app_package = "com.example.app"
set $max_pages = 10
set $output_file = "/sdcard/collected_data.txt"

# 启动应用
start_app "${app_package}"
wait 2

# 等待列表加载
wait_element id:"list_view" 10
log "列表已加载"

# 采集数据
set $total_count = 0

loop $max_pages
    log "采集数据"

    # 查找当前页面的所有数据项
    set $items = find_elements class:"android.widget.TextView"
    log "本页找到 ${items.count} 条数据"

    # 滑动到下一页
    swipe up 0.7
    wait 1.5

    # 等待新数据加载
    wait_element id:"loading" 5
    wait_gone id:"loading" 10
end

log "数据采集完成，共采集 ${total_count} 条数据"
log "数据已保存到: ${output_file}"

# 返回主页
home
log "=== 数据采集任务完成 ==="
```

#### 示例 3: 复杂流程自动化（带重试和错误处理）

```bash
# complex_workflow.script
# =======================
# 复杂业务流程自动化示例

log "=== 开始复杂流程自动化 ==="

# 配置
set $app_package = "com.example.app"
set $max_retries = 3
set $step_timeout = 30

# 主流程
# ======

# 步骤 1: 启动应用
log "步骤 1: 启动应用"
start_app $app_package
wait 3

# 步骤 2: 等待主界面加载
log "步骤 2: 等待主界面"
wait_element id:"main_content" $step_timeout

# 步骤 3: 执行主操作
log "步骤 3: 执行主操作"
if exists id:"action_button"
    click id:"action_button"
    wait 2

    # 步骤 4: 处理确认对话框
    if exists id:"confirm_dialog"
        log "步骤 4: 确认操作"
        click text:"确定"
        wait 1
    end

    # 步骤 5: 等待操作完成
    log "步骤 5: 等待操作完成"
    wait_element id:"success_message" $step_timeout

    if exists id:"success_message"
        set $message = get_text id:"success_message"
        log "操作成功: $message"
    else
        log "未找到成功提示"
    end
else
    log "未找到操作按钮"
end

# 步骤 6: 清理和返回
log "步骤 6: 清理"
home
wait 1

log "=== 复杂流程自动化完成 ==="
```

#### 示例 4: 人类行为模拟脚本

```bash
# human_behavior.script
# =====================
# 模拟真实用户行为的自动化脚本

log "=== 开始人类行为模拟 ==="

# 配置
set $app_package = "com.example.app"
set $reading_time = 2        # 阅读时间（秒）
set $scroll_speed = 0.8      # 滚动速度

# 启动应用（模拟用户点击图标）
log "1. 启动应用（模拟用户点击图标）"
human_click 300, 800         # 点击屏幕中央（假设图标位置）
wait 3

# 等待主界面（模拟用户等待）
log "2. 等待主界面加载"
wait 2

# 浏览首页（模拟用户浏览行为）
log "3. 浏览首页内容"
loop 5
    # 模拟用户阅读内容
    wait 2

    # 模拟用户下滑浏览
    human_drag 500, 1200, 500, 400, trajectory="bezier", speed="ease_in_out", duration=1.5

    wait 1
end

# 点击感兴趣的内容（模拟用户点击）
log "4. 点击感兴趣的内容"
if exists text:"热门文章"
    # 模拟用户犹豫一下再点击
    wait 1
    human_click text:"热门文章"
end

# 阅读文章详情
log "5. 阅读文章详情"
wait 3

# 模拟用户滑动阅读长文章
loop 3
    human_drag 500, 1000, 500, 300, trajectory="linear_jitter", speed="random", duration=2.0
    wait 1
end

# 点赞操作（模拟用户点赞行为）
log "6. 点赞操作"
if exists id:"like_button"
    human_click id:"like_button", offset_min=5, offset_max=15, delay_min=0.2, delay_max=0.5
end

# 返回（模拟用户返回）
log "7. 返回上一页"
human_click 100, 100         # 点击返回按钮位置
wait 2

# 继续浏览
log "8. 继续浏览"
loop 3
    human_click id:"article_item", offset_min=3, offset_max=10
    wait 3
    back
    wait 1
end

# 返回主页
log "9. 返回主页"
home
wait 1

log "=== 人类行为模拟完成 ==="
log "脚本执行完毕，模拟真实用户完成了一次完整的应用使用流程"
```

### 脚本调试技巧

#### 1. 启用详细日志

```bash
# 在脚本开头启用详细日志
log "=== 脚本开始执行 ==="
log "当前设备状态检查"

# 检查设备连接状态（通过 API 检查，这里仅作为日志示例）

# 记录关键步骤
log "步骤 1: 启动应用"
start_app "com.example.app"
log "应用已启动"

log "步骤 2: 等待界面"
wait 2
log "界面已加载"
```

#### 2. 截图调试

```bash
# 在关键位置截图
click id:"button"
wait 2
shell "screencap -p /sdcard/debug.png"

# 出错时截图
try
    click id:"maybe_exist"
catch
    log "操作失败，截图保存"
    shell "screencap -p /sdcard/error.png"
end
```

#### 3. 界面结构导出

```bash
# 导出当前界面 XML 结构
set $xml = dump_hierarchy
log "当前界面结构:"
log $xml

# 保存到文件
shell "echo '${xml}' > /sdcard/hierarchy.xml"
```

#### 4. 逐步执行

```bash
# 使用注释标记执行进度
# [STEP 1] 启动应用
start_app "com.example.app"
wait 2

# [STEP 2] 检查界面
if exists id:"main"
    log "[PASS] 主界面已显示"
else
    log "[FAIL] 主界面未显示"
end

# [STEP 3] 执行操作
click id:"button"
log "[PASS] 按钮已点击"
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

## DSL 元素信息获取详解

### get_text - 获取元素文本

获取指定元素的文本内容。

```bash
# 通过不同选择器获取文本
get_text id:"com.example:id/button"
get_text text:"确定"
get_text class:"android.widget.TextView"
get_text xpath:"//Button[@text='提交']"
```

### get_info - 获取元素完整信息

获取元素的详细属性信息，返回一个包含以下字段的字典：

```json
{
  "exists": true,
  "text": "确定",
  "class_name": "android.widget.Button",
  "resource_id": "com.example:id/button",
  "bounds": {"left": 100, "top": 200, "right": 300, "bottom": 400},
  "enabled": true,
  "focused": false,
  "selected": false,
  "clickable": true,
  "checkable": false,
  "checked": false
}
```

属性说明：
- `exists`: 元素是否存在
- `text`: 元素显示的文本内容
- `class_name`: 元素的类名
- `resource_id`: 元素的 resource-id
- `bounds`: 元素的边界坐标 {left, top, right, bottom}
- `enabled`: 元素是否可用
- `focused`: 元素是否获得焦点
- `selected`: 元素是否被选中
- `clickable`: 元素是否可点击
- `checkable`: 元素是否可被勾选
- `checked`: 元素是否已勾选

```bash
# 获取元素信息并保存到变量
set $info = get_info id:"button_id"

# 检查元素是否存在后操作
if $info
    log "元素信息: $info"
    click id:"button_id"
end
```

### find_element - 查找单个元素

查找并返回第一个匹配元素的详细信息。

```bash
# 查找元素并获取其信息
set $element = find_element text:"确定"

# 检查元素是否存在
if $element
    log "找到元素"
else
    log "未找到元素"
end
```

### find_elements - 查找所有匹配元素

查找所有匹配的元素并返回元素列表。

```bash
# 查找所有 TextView 元素
set $elements = find_elements class:"android.widget.TextView"

# 遍历所有匹配元素（需要在循环中处理）
# 注意：脚本DSL中暂不支持直接遍历列表
# 可以通过元素计数实现
loop 10
    if exists text:"目标文本"
        click text:"目标文本"
        break
    end
end
```

返回值结构：
```json
{
  "elements": [
    {"text": "标题1", "class_name": "android.widget.TextView", "bounds": {...}},
    {"text": "标题2", "class_name": "android.widget.TextView", "bounds": {...}}
  ],
  "count": 2
}
```

### dump_hierarchy - 导出界面结构

获取当前界面的完整 XML 层次结构，用于调试和元素定位。

```bash
# 导出界面结构
set $xml = dump_hierarchy
log "界面 XML 已导出"

# 保存到文件（通过shell命令）
shell "echo '${xml}' > /sdcard/hierarchy.xml"
```

### 实用示例

**示例 1: 验证元素状态后再操作**

```bash
# 获取按钮信息
set $btn = get_info id:"com.example:id/submit"

# 检查按钮是否存在
if exists id:"com.example:id/submit"
    click id:"com.example:id/submit"
    log "点击提交按钮"
else
    log "按钮不存在"
end
```

**示例 2: 根据元素状态做条件判断**

```bash
# 启动应用
start_app "com.example.app"
wait 2

# 检查登录按钮是否存在
if exists id:"com.example:id/login"
    log "在登录页面"
    input id:"username" "test@example.com"
    input id:"password" "password123"
    click id:"login"
else
    log "已登录或其他页面"
end
```

**示例 3: 查找并点击特定文本的按钮**

```bash
# 查找确定按钮
if exists text:"确定"
    # 获取按钮信息
    set $info = get_info text:"确定"
    log "按钮信息: $info"
    
    # 点击按钮
    click text:"确定"
else
    log "未找到确定按钮"
end
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
2. **WiFi 连接**：确保设备和服务器在同一网络，设备已开启 ADB over WiFi（端口默认 5555）
3. **元素定位**：建议优先使用 resource-id 定位，稳定性最高
4. **等待机制**：界面元素加载需要时间，建议使用 `wait-appear` 等待元素
5. **权限要求**：确保设备已开启 USB 调试模式

## 许可证

MIT License
