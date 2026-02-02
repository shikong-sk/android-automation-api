# DSL 示例脚本索引

本目录包含 Android Automation API DSL 脚本的完整示例和参考文档。

## 📚 文档索引

### 快速参考
- **[DSL_QUICK_REFERENCE.md](DSL_QUICK_REFERENCE.md)** - DSL 语法速查手册，快速查找常用命令

### 基础教程
- **[BASIC_OPERATIONS.md](BASIC_OPERATIONS.md)** - 基础操作示例，包含点击、输入、滑动等基本命令

### 高级用法
- **[ADVANCED_USAGE.md](ADVANCED_USAGE.md)** - 高级用法示例，包含页面对象模式、数据驱动测试等

### 人类模拟
- **[HUMAN_SIMULATION.md](HUMAN_SIMULATION.md)** - 人类模拟操作示例，模拟真实用户行为

## 🎯 按场景分类

### 登录流程
```bash
# 启动应用
start_app "com.example.app"
wait 2

# 输入凭据
input id:"username" "test@example.com"
input id:"password" "password123"

# 点击登录
click id:"login_button"
wait 3

# 验证结果
if exists id:"welcome_message"
    log "登录成功"
else
    log "登录失败"
end
```

### 数据采集
```bash
# 启动应用
start_app "com.example.app"
wait 2

# 采集数据
set $items = find_elements class:"android.widget.TextView"
log "找到 $items.count 个元素"

# 滚动加载更多
loop 10
    human_drag 500, 1200, 500, 200, trajectory="bezier"
    wait 2
end
```

### 表单填写
```bash
# 填写表单
input id:"username" "test@example.com"
input id:"email" "test@example.com"
input id:"password" "password123"

# 验证完整性
set $filled = 0
if exists id:"username" and get_text id:"username" != ""
    set $filled = $filled + 1
end

if $filled == 3
    click id:"submit"
end
```

### 列表操作
```bash
# 查找并点击特定项
set $target = "目标项目"
set $items = find_elements class:"android.widget.TextView"

loop $items.count
    set $item = get_info xpath:"(//android.widget.TextView)[${i}]"
    if $item.text == $target
        click xpath:"//android.widget.TextView[@text='${target}']"
        break
    end
end
```

## 🔧 按命令分类

### 元素定位
- `id:"resource-id"` - 通过 resource-id 定位
- `text:"文本"` - 通过文本定位
- `class:"类名"` - 通过类名定位
- `xpath:"XPath"` - 通过 XPath 定位

### 基础操作
- `click` - 点击元素
- `input` - 输入文本
- `clear` - 清除文本
- `swipe` - 滑动屏幕

### 等待操作
- `wait` - 等待时间
- `wait_element` - 等待元素出现
- `wait_gone` - 等待元素消失

### 导航操作
- `back` - 返回
- `home` - 返回桌面
- `menu` - 打开菜单
- `recent` - 最近任务

### 应用管理
- `start_app` - 启动应用
- `stop_app` - 停止应用
- `clear_app` - 清除应用数据

### 屏幕控制
- `screen_on` - 亮屏
- `screen_off` - 锁屏
- `unlock` - 解锁

### 元素信息
- `get_text` - 获取元素文本
- `get_info` - 获取元素信息
- `find_element` - 查找元素
- `find_elements` - 查找所有元素
- `dump_hierarchy` - 导出界面结构

### 人类模拟
- `human_click` - 人类模拟点击
- `human_double_click` - 人类模拟双击
- `human_long_press` - 人类模拟长按
- `human_drag` - 人类模拟拖拽

### 控制流
- `if/elif/else` - 条件判断
- `loop` - 循环
- `while` - 条件循环
- `try/catch` - 错误处理
- `break` - 跳出循环
- `continue` - 继续循环

### 其他
- `log` - 输出日志
- `shell` - 执行 Shell 命令
- `call` - 调用子脚本
- `set` - 设置变量

## 💡 最佳实践

### 1. 使用等待机制
```bash
# ✅ 推荐：等待元素出现
wait_element id:"button" 10
click id:"button"

# ❌ 不推荐：直接点击可能失败
click id:"button"
```

### 2. 优先使用 ID 定位
```bash
# ✅ 推荐：使用 ID 定位
click id:"com.example:id/button"

# ⚠️ 中等：使用文本定位
click text:"确定"

# ❌ 最后：使用 XPath 定位
click xpath:"//Button[@text='确定']"
```

### 3. 添加错误处理
```bash
# ✅ 推荐：添加错误处理
try
    click id:"button"
catch
    log "点击失败"
end

# ❌ 不推荐：没有错误处理
click id:"button"
```

### 4. 使用日志调试
```bash
# ✅ 推荐：添加日志
log "开始执行操作"
click id:"button"
log "操作完成"

# ❌ 不推荐：没有日志
click id:"button"
```

### 5. 使用人类模拟避免检测
```bash
# ✅ 推荐：使用人类模拟
human_click id:"button", offset_min=5, offset_max=15

# ❌ 不推荐：直接点击可能被检测
click id:"button"
```

## 📖 学习路径

### 初学者
1. 阅读 [DSL_QUICK_REFERENCE.md](DSL_QUICK_REFERENCE.md) 了解基本语法
2. 学习 [BASIC_OPERATIONS.md](BASIC_OPERATIONS.md) 掌握基础操作
3. 尝试编写简单的登录脚本

### 进阶用户
1. 学习 [ADVANCED_USAGE.md](ADVANCED_USAGE.md) 掌握高级技巧
2. 理解页面对象模式和数据驱动测试
3. 编写复杂的自动化流程

### 高级用户
1. 深入学习 [HUMAN_SIMULATION.md](HUMAN_SIMULATION.md)
2. 掌握人类模拟操作和反检测技术
3. 优化脚本性能和稳定性

## 🔗 相关资源

- [主 README](../../README.md) - 项目主文档
- [后端 DSL 文档](../../scripts/ELEMENT_INFO_README.md) - 后端 DSL 详细文档
- [前端 README](../README.md) - 前端项目文档

## 💬 获取帮助

如果遇到问题：
1. 查看本文档中的示例
2. 检查语法是否正确
3. 使用 `log` 命令输出调试信息
4. 使用 `dump_hierarchy` 导出界面结构分析

## 📝 贡献

欢迎贡献更多示例和文档！
