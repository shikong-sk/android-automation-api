# Android Automation API - 前端界面

基于 Vue 3 + Element Plus 的安卓设备自动化控制 Web 管理界面。

## 项目简介

本前端项目提供可视化的安卓设备自动化控制界面，支持：
- 设备连接与管理
- 元素定位与操作
- 自动化脚本编辑与执行
- XPath 可视化生成
- DSL 脚本语法辅助

## 技术栈

- **Vue 3**: 前端框架
- **Vite**: 构建工具
- **Element Plus**: UI 组件库
- **Tailwind CSS**: 样式框架
- **@vicons/fa**: 图标库
- **Axios**: HTTP 客户端

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

### 3. 构建生产版本

```bash
npm run build
```

### 4. 预览生产版本

```bash
npm run preview
```

## 功能页面

| 页面 | 路由 | 描述 |
|------|------|------|
| 控制台 | `/` | 设备状态总览、快捷操作 |
| 设备管理 | `/device` | 设备连接状态 |
| 输入控制 | `/input` | 点击、输入、滑动、元素定位、屏幕控制、XPath 生成器 |
| 导航控制 | `/navigation` | 返回主页、返回、菜单等导航操作 |
| 应用管理 | `/apps` | 启动、停止、清除应用数据 |
| ADB 工具 | `/adb` | 设备信息、应用列表、Shell 命令执行 |
| 自动化脚本 | `/script` | 脚本编辑、执行、管理 |

## DSL 语法辅助功能

前端界面提供 DSL 语法辅助功能，帮助用户快速生成自动化脚本。

### 支持的 DSL 命令

#### 1. 元素定位

| 选择器类型 | DSL 格式 | 示例 |
|-----------|---------|------|
| resource-id | `id:"资源ID"` | `id:"com.example:id/button"` |
| text | `text:"文本内容"` | `text:"确定"` |
| class | `class:"类名"` | `class:"android.widget.Button"` |
| xpath | `xpath:"XPath表达式"` | `xpath:"//Button[@text='确定']"` |

#### 2. 基础操作命令

```bash
# 点击元素
click id:"button_id"
click text:"确定"
click xpath:"//Button[@text='提交']"

# 点击坐标
click 500, 800

# 输入文本
input id:"input_id" "要输入的文本"

# 清除文本
clear id:"input_id"

# 发送动作
send_action id:"input_id" "IME_ACTION_DONE"
```

#### 3. 滑动命令

```bash
# 方向滑动
swipe up 0.5              # 向上滑动 50%
swipe down 0.3            # 向下滑动 30%
swipe left                # 向左滑动
swipe right               # 向右滑动

# 坐标滑动
swipe 100, 500, 100, 200  # 从 (100,500) 滑动到 (100,200)
```

#### 4. 等待命令

```bash
# 等待时间
wait 2                    # 等待 2 秒

# 等待元素出现
wait_element id:"loading" 10    # 最多等待 10 秒

# 等待元素消失
wait_gone id:"loading" 10       # 最多等待 10 秒
```

#### 5. 导航命令

```bash
back                      # 返回
home                      # 返回桌面
menu                      # 打开菜单
recent                    # 最近任务
```

#### 6. 应用管理

```bash
start_app "com.example.app"     # 启动应用
stop_app "com.example.app"      # 停止应用
clear_app "com.example.app"     # 清除应用数据
```

#### 7. 屏幕控制

```bash
screen_on                 # 亮屏
screen_off                # 锁屏
unlock                    # 解锁
```

#### 8. 元素信息获取

```bash
# 获取元素文本
set $text = get_text id:"button_id"

# 获取元素完整信息
set $info = get_info id:"element_id"

# 查找单个元素
set $element = find_element id:"button_id"

# 查找所有匹配元素
set $elements = find_elements class:"android.widget.Button"

# 导出界面结构
set $xml = dump_hierarchy
```

#### 9. 条件判断

```bash
# 元素存在判断
if exists id:"button"
    click id:"button"
end

# 元素不存在判断
if not exists id:"loading"
    log "加载完成"
end

# 变量判断
if $status == "success"
    log "操作成功"
end
```

#### 10. 循环

```bash
# 固定次数循环
loop 5
    click id:"next"
    wait 1
end

# 条件循环
while exists id:"loading"
    wait 1
end
```

#### 11. 人类模拟操作

```bash
# 人类模拟点击
human_click id:"button"
human_click 500, 800, offset_min=5, offset_max=15

# 人类模拟双击
human_double_click id:"item"

# 人类模拟长按
human_long_press id:"item", duration_min=1.0, duration_max=2.0

# 人类模拟拖拽
human_drag 100, 1500, 100, 500, trajectory="bezier", speed="ease_in_out"
```

#### 12. 变量与插值

```bash
# 设置变量
set $name = "value"
set $count = 10

# 变量插值
log "Hello ${name}"
click id:"${element_id}"
```

#### 13. 其他命令

```bash
log "日志消息"            # 输出日志
shell "ls /sdcard"       # 执行 Shell 命令
try
    # 操作
catch
    # 错误处理
end
call "other.script"      # 调用子脚本
```

### 高级选择器

前端支持构建复杂的选择器：

```bash
# 父级选择器
click id:"child" parent=id:"parent_id"

# 兄弟选择器
click id:"target" sibling=id:"sibling_id" sibling_relation=following

# 偏移选择器
click id:"button" offset_x=10 offset_y=-5
```

### 完整示例

```bash
# 自动登录示例
start_app "com.example.app"
wait 2

# 输入账号密码
input id:"username" "test@example.com"
input id:"password" "password123"

# 点击登录
click id:"login_button"
wait 3

# 验证登录结果
if exists id:"welcome_message"
    set $welcome = get_text id:"welcome_message"
    log "登录成功: $welcome"
else
    log "登录失败"
end

# 返回主页
home
```

## XPath 生成器

前端提供可视化的 XPath 生成器，帮助快速生成元素定位表达式。

### 功能特性

1. **快捷模板库** - 常用 XPath 模板一键生成
2. **属性组合生成器** - 通过表单选择元素属性自动组合
3. **XML 树形选择器** - 可视化展示界面元素层级
4. **XPath 测试验证** - 一键测试生成的表达式

### 使用方式

1. 在输入控制页面选择对应操作 Tab
2. 选择 "By XPath" 定位方式
3. 点击 "生成" 按钮打开 XPath 生成器
4. 选择生成策略并测试
5. 点击 "插入" 将生成的 XPath 插入到输入框

## 脚本管理

前端提供完整的脚本管理功能：

- **脚本列表** - 查看所有脚本文件
- **脚本编辑** - 在线编辑脚本内容
- **语法验证** - 一键验证脚本语法
- **脚本执行** - 执行脚本并查看日志
- **流式执行** - SSE 实时查看执行过程

## API 集成

前端通过 Axios 与后端 API 通信，API 模块位于 `src/api/` 目录：

| 模块 | 文件 | 描述 |
|------|------|------|
| 设备 API | device.js | 设备连接状态管理 |
| 输入 API | input.js | 元素操作相关 |
| 导航 API | navigation.js | 导航控制 |
| 应用 API | app.js | 应用管理 |
| ADB API | adb.js | ADB 命令执行 |
| 脚本 API | script.js | 脚本管理执行 |

## 开发指南

### 添加新功能

1. 在 `src/api/` 添加对应的 API 函数
2. 在 `src/components/` 创建 Vue 组件
3. 在 `src/pages/` 创建页面组件
4. 在 `src/router/` 配置路由
5. 在 `src/layouts/` 添加布局

### 样式规范

- 使用 Tailwind CSS 进行样式开发
- 组件样式使用 `<style scoped>` 包裹
- 遵循 Element Plus 组件样式规范

## 构建部署

### Docker 部署

```bash
# 构建镜像
docker build -t android-automation-frontend:latest .

# 运行容器
docker run -d -p 5173:80 android-automation-frontend:latest
```

### Nginx 配置

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## 许可证

MIT License
