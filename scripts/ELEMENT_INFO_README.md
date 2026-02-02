# 元素信息获取功能使用说明

本目录包含演示新增DSL元素信息获取功能的示例脚本。

## 新增的DSL命令

### 1. get_text - 获取元素文本

获取指定元素的文本内容。

**语法：**
```bash
get_text id:"resource_id"
get_text text:"文本内容"
get_text class:"类名"
get_text xpath:"XPath表达式"
```

**示例：**
```bash
set $title = get_text id:"android:id/title"
log "页面标题: $title"
```

### 2. get_info - 获取元素完整信息

获取元素的详细属性信息，包括text、class、bounds、enabled等。

**语法：**
```bash
get_info id:"resource_id"
get_info class:"类名"
```

**返回属性：**
- `exists`: 元素是否存在
- `text`: 元素文本
- `class_name`: 元素类名
- `resource_id`: 资源ID
- `bounds`: 边界坐标
- `enabled`: 是否可用
- `focused`: 是否聚焦
- `selected`: 是否选中
- `clickable`: 是否可点击
- `checkable`: 是否可勾选
- `checked`: 是否已勾选

**示例：**
```bash
set $btn = get_info id:"com.example:id/button"
if $btn.exists and $btn.enabled
    log "按钮可用: $btn.text"
    click id:"com.example:id/button"
end
```

### 3. find_element - 查找单个元素

查找并返回第一个匹配元素的详细信息。

**语法：**
```bash
find_element id:"resource_id"
find_element text:"文本"
find_element class:"类名"
find_element xpath:"XPath"
```

**示例：**
```bash
set $element = find_element text:"确定"
if $element.exists
    log "找到元素: $element.text"
    click text:"确定"
end
```

### 4. find_elements - 查找所有匹配元素

查找所有匹配的元素并返回元素列表。

**语法：**
```bash
find_elements class:"android.widget.TextView"
find_elements id:"item"
```

**返回值：**
```json
{
  "elements": [...],
  "count": 10
}
```

**示例：**
```bash
set $elements = find_elements class:"android.widget.TextView"
log "找到 $elements.count 个文本元素"
```

### 5. dump_hierarchy - 导出界面结构

获取当前界面的完整XML层次结构。

**语法：**
```bash
dump_hierarchy
```

**示例：**
```bash
set $xml = dump_hierarchy
log "界面 XML 长度: $xml.length"
```

## 示例脚本

### element_info_example.script

完整的元素信息获取示例，演示所有新功能的使用。

### 使用方法

1. 确保设备已连接
2. 使用Web界面或API执行脚本：
   ```bash
   curl -X POST "http://localhost:8000/api/v1/script/execute/element_info_example"
   ```

## 实用技巧

### 1. 验证元素状态后再操作

```bash
set $btn = get_info id:"submit"
if $btn.exists and $btn.enabled
    click id:"submit"
else
    log "按钮不可用"
end
```

### 2. 动态获取文本进行比较

```bash
set $expected = "完成"
set $actual = get_text id:"status"

if $actual == $expected
    log "状态正确"
else
    log "状态不正确: $actual"
end
```

### 3. 调试界面结构

```bash
# 导出界面结构用于分析
set $xml = dump_hierarchy
log $xml
```

### 4. 查找特定属性的元素

```bash
# 查找所有可点击的按钮
set $buttons = find_elements class:"android.widget.Button"
# 注意：需要结合条件判断筛选
```

## 注意事项

1. **元素必须存在**：执行get_text、get_info等命令前，建议先用exists检查元素是否存在
2. **性能考虑**：dump_hierarchy会返回完整的XML，字符串可能很长，建议仅在调试时使用
3. **选择器优先级**：建议优先使用id选择器，稳定性最高
4. **超时处理**：如果元素加载较慢，建议在获取信息前使用wait_element等待元素出现

## 完整示例：自动化测试场景

```bash
# 启动应用
start_app "com.example.app"
wait 2

# 验证登录页面
set $login_btn = get_info id:"login"
if $login_btn.exists
    log " ✓ 在登录页面"

    # 输入用户名和密码
    input id:"username" "test@example.com"
    input id:"password" "password123"

    # 点击登录
    click id:"login"
    wait 3

    # 验证登录成功
    set $welcome = get_text id:"welcome_message"
    if $welcome != ""
        log " ✓ 登录成功: $welcome"
    else
        log " ✗ 登录失败"
    end
else
    log " ✗ 未找到登录按钮"
end
```

## 高级用法示例

### 示例 1: 批量元素状态检查

```bash
# 检查页面上所有按钮的状态
set $buttons = find_elements class:"android.widget.Button"

log "找到 $buttons.count 个按钮"

loop $buttons.count
    # 获取按钮信息（需要根据实际UI结构调整）
    set $btn_info = get_info xpath:"(//android.widget.Button)[${i}]"

    if $btn_info.exists
        log "按钮 ${i}: $btn_info.text"
        log "  - 可用: $btn_info.enabled"
        log "  - 可点击: $btn_info.clickable"
        log "  - 位置: $btn_info.bounds"
    end
end
```

### 示例 2: 动态等待元素状态变化

```bash
# 等待按钮从不可用变为可用
set $max_wait = 30
set $elapsed = 0

while $elapsed < $max_wait
    set $btn = get_info id:"submit_button"

    if $btn.exists and $btn.enabled
        log "按钮已可用，耗时 ${elapsed} 秒"
        click id:"submit_button"
        break
    end

    wait 0.5
    set $elapsed = $elapsed + 0.5
end

if $elapsed >= $max_wait
    log "等待按钮超时"
end
```

### 示例 3: 元素位置计算与操作

```bash
# 获取元素位置并计算中心点
set $element = get_info id:"target_element"

if $element.exists
    # 提取边界坐标
    set $left = $element.bounds.left
    set $top = $element.bounds.top
    set $right = $element.bounds.right
    set $bottom = $element.bounds.bottom

    # 计算中心点
    set $center_x = ($left + $right) / 2
    set $center_y = ($top + $bottom) / 2

    log "元素中心点: ($center_x, $center_y)"

    # 在中心点点击
    human_click $center_x, $center_y
end
```

### 示例 4: 界面结构分析与元素定位

```bash
# 导出界面结构进行分析
set $hierarchy = dump_hierarchy
log "界面结构长度: $hierarchy.length"

# 查找特定类型的元素
set $textviews = find_elements class:"android.widget.TextView"
log "找到 ${textviews.count} 个文本元素"

# 查找可点击的元素
set $clickables = find_elements class:"android.widget.Button"
log "找到 ${clickables.count} 个按钮"

# 组合条件查找
# 注意：DSL不支持直接组合条件，需要循环过滤
loop $textviews.count
    set $tv_info = get_info xpath:"(//android.widget.TextView)[${i}]"

    if $tv_info.exists and $tv_info.enabled
        log "可用文本元素: $tv_info.text"
    end
end
```

### 示例 5: 验证表单填写完整性

```bash
# 检查表单是否填写完整
set $form_fields = ["username", "email", "password", "confirm_password"]
set $filled_count = 0
set $total_fields = 4

loop 4
    set $field_id = $form_fields[${i}]
    set $field_info = get_info id:$field_id

    if $field_info.exists
        set $field_text = get_text id:$field_id

        if $field_text != ""
            log "$field_id 已填写: $field_text"
            set $filled_count = $filled_count + 1
        else
            log "$field_id 未填写"
        end
    end
end

log "表单填写进度: ${filled_count}/${total_fields}"

if $filled_count == $total_fields
    log "表单已填写完整，启用提交按钮"
    click id:"submit"
else
    log "表单未填写完整"
end
```

### 示例 6: 列表项验证与操作

```bash
# 验证列表中的特定项并操作
set $target_text = "目标项目"

# 查找包含目标文本的元素
set $found = false
set $items = find_elements class:"android.widget.TextView"

loop $items.count
    set $item_info = get_info xpath:"(//android.widget.TextView)[${i}]"

    if $item_info.exists and $item_info.text == $target_text
        log "找到目标项目: $target_text"

        # 获取该项的父元素并点击
        # 注意：需要根据实际UI结构调整XPath
        click xpath:"//android.widget.TextView[@text='${target_text}']/parent::*"

        set $found = true
        break
    end
end

if not $found
    log "未找到目标项目: $target_text"
end
```

### 示例 7: 错误状态检测与恢复

```bash
# 检测错误状态并尝试恢复
set $recovery_attempts = 0
set $max_attempts = 3

while $recovery_attempts < $max_attempts
    # 执行操作
    click id:"action_button"
    wait 2

    # 检查结果
    if exists id:"success_message"
        log "操作成功"
        break
    elif exists id:"error_message"
        set $error = get_text id:"error_message"
        log "发生错误: $error"

        # 尝试恢复
        if exists text:"重试"
            click text:"重试"
            wait 1
            set $recovery_attempts = $recovery_attempts + 1
        elif exists text:"取消"
            log "取消操作"
            break
        else
            log "无法自动恢复"
            break
        end
    else
        log "操作结果未知"
        break
    end
end
```

### 示例 8: 性能监控与元素响应时间

```bash
# 测量元素加载响应时间
set $start_time = timestamp()

# 触发页面刷新
swipe down 0.3
wait 0.5
swipe up 0.3

# 等待特定元素出现
wait_element id:"content_loaded" 30

set $load_time = timestamp() - $start_time
log "页面加载响应时间: ${load_time}ms"

# 检查元素状态
set $content_info = get_info id:"content_loaded"

if $content_info.exists
    log "元素状态:"
    log "  - 文本: $content_info.text"
    log "  - 可用: $content_info.enabled"
    log "  - 可点击: $content_info.clickable"
    log "  - 位置: $content_info.bounds"
end
```

### 示例 9: 多语言界面适配

```bash
# 根据界面语言执行不同操作
set $page_title = get_text id:"page_title"

if contains($page_title, "Settings") or contains($page_title, "设置")
    log "在设置页面"

    # 根据实际文本点击
    if exists text:"General"
        click text:"General"
    elif exists text:"通用"
        click text:"通用"
    end
elif contains($page_title, "Profile") or contains($page_title, "个人资料")
    log "在个人资料页面"
else
    log "未知页面: $page_title"
end
```

### 示例 10: 滚动加载更多内容

```bash
# 检测并触发滚动加载
set $initial_count = 0
set $max_scrolls = 10
set $scroll_count = 0

# 获取初始数据量
set $items = find_elements class:"android.widget.TextView"
set $initial_count = $items.count
log "初始数据量: $initial_count"

# 滚动加载更多
while $scroll_count < $max_scrolls
    log "滚动加载 (${scroll_count + 1}/${max_scrolls})..."

    # 滑动到底部
    human_drag 500, 1200, 500, 200, trajectory="bezier", speed="ease_in_out", duration=2.0

    # 等待新数据加载
    wait 2

    # 检查加载动画
    if exists id:"loading"
        wait_gone id:"loading" 10
    end

    # 检查数据量变化
    set $new_items = find_elements class:"android.widget.TextView"

    if $new_items.count > $initial_count
        log "新数据已加载: ${new_items.count - $initial_count} 条"
        set $initial_count = $new_items.count
    else
        log "数据量无变化，可能已加载全部"
    end

    set $scroll_count = $scroll_count + 1
end

log "滚动加载完成，最终数据量: $initial_count"
```
