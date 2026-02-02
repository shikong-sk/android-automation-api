# 高级用法示例

## 1. 页面对象模式

```bash
# 定义页面元素
set $LOGIN_PAGE = {
    "username": "com.example:id/username",
    "password": "com.example:id/password",
    "submit": "com.example:id/login_button"
}

set $HOME_PAGE = {
    "welcome": "com.example:id/welcome",
    "menu": "com.example:id/menu"
}

# 使用页面元素
input id:$LOGIN_PAGE.username "test@example.com"
input id:$LOGIN_PAGE.password "password123"
click id:$LOGIN_PAGE.submit
```

## 2. 智能等待模式

```bash
# 等待元素出现或超时
set $elapsed = 0
set $timeout = 30

while $elapsed < $timeout
    if exists id:"content"
        log "元素出现，耗时 ${elapsed} 秒"
        break
    end
    wait 0.5
    set $elapsed = $elapsed + 0.5
end

if $elapsed >= $timeout
    log "等待元素超时"
end
```

## 3. 数据驱动测试

```bash
# 测试数据
set $test_cases = [
    {"username": "user1", "password": "pass1", "expected": "success"},
    {"username": "user2", "password": "wrong", "expected": "fail"},
    {"username": "", "password": "", "expected": "error"}
]

# 遍历测试用例
loop 3
    set $case = $test_cases[${i}]
    log "测试用例: $case.username / $case.password"

    input id:"username" "${case.username}"
    input id:"password" "${case.password}"
    click id:"login"

    wait 2
    set $result = get_text id:"message"

    if $result == $case.expected
        log "测试通过"
    else
        log "测试失败: 期望 ${case.expected}, 实际 $result"
    end

    clear id:"username"
    clear id:"password"
end
```

## 4. 屏幕截图与调试

```bash
# 在关键步骤截图
try
    click id:"submit"
    wait 2

    if exists id:"success"
        log "操作成功"
        shell "screencap -p /sdcard/success.png"
    else
        log "操作失败，截图保存"
        shell "screencap -p /sdcard/debug.png"

        # 导出界面结构
        set $xml = dump_hierarchy
        log $xml
    end
catch
    log "发生错误，截图保存"
    shell "screencap -p /sdcard/error.png"
end
```

## 5. 性能监控

```bash
# 记录操作耗时
set $start_time = timestamp()

start_app "com.example.app"
wait 3

set $load_time = timestamp() - $start_time
log "应用启动耗时: ${load_time}ms"

# 监控内存使用
set $memory = shell "dumpsys meminfo com.example.app | grep TOTAL"
log "内存使用: $memory"
```

## 6. 批量元素操作

```bash
# 检查页面上所有按钮的状态
set $buttons = find_elements class:"android.widget.Button"

log "找到 $buttons.count 个按钮"

loop $buttons.count
    set $btn_info = get_info xpath:"(//android.widget.Button)[${i}]"

    if $btn_info.exists
        log "按钮 ${i}: $btn_info.text"
        log "  - 可用: $btn_info.enabled"
        log "  - 可点击: $btn_info.clickable"
    end
end
```

## 7. 动态等待元素状态变化

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
```

## 8. 元素位置计算与操作

```bash
# 获取元素位置并计算中心点
set $element = get_info id:"target_element"

if $element.exists
    # 计算中心点
    set $center_x = ($element.bounds.left + $element.bounds.right) / 2
    set $center_y = ($element.bounds.top + $element.bounds.bottom) / 2

    log "元素中心点: ($center_x, $center_y)"

    # 在中心点点击
    human_click $center_x, $center_y
end
```

## 9. 表单填写完整性验证

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

## 10. 列表项验证与操作

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

        # 点击该项
        click xpath:"//android.widget.TextView[@text='${target_text}']/parent::*"

        set $found = true
        break
    end
end

if not $found
    log "未找到目标项目: $target_text"
end
```

## 11. 错误状态检测与恢复

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

## 12. 滚动加载更多内容

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

## 13. 多语言界面适配

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

## 14. 复杂条件判断

```bash
# 多条件组合判断
if exists id:"button" and $is_enabled
    log "按钮存在且可用"
    click id:"button"
end

if exists id:"error" or exists id:"warning"
    log "存在异常"
end

# 嵌套条件
if exists id:"submit"
    set $btn_info = get_info id:"submit"

    if $btn_info.enabled
        if $btn_info.text == "提交"
            click id:"submit"
        else
            log "按钮文本不符合预期"
        end
    else
        log "按钮不可用"
    end
end
```

## 15. 子脚本调用与参数传递

```bash
# 主脚本
set $target_page = "settings"
set $action = "open"

# 调用子脚本
call "navigate.script"

# 子脚本 (navigate.script)
# ============================
# log "导航到 ${target_page} 页面"
# log "执行操作: ${action}"
# start_app "com.example.app"
# wait 2
# click id:"${target_page}"
```
