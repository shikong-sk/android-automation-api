# DSL 语法速查手册

## 快速参考

### 元素定位

```bash
# 通过 resource-id
id:"com.example:id/button"

# 通过文本
text:"确定"

# 通过类名
class:"android.widget.Button"

# 通过 XPath
xpath:"//Button[@text='确定']"
```

### 基础操作

```bash
# 点击
click id:"button"
click 500, 800

# 输入
input id:"input" "文本"

# 清除
clear id:"input"

# 滑动
swipe up 0.5
swipe 100, 500, 100, 200
```

### 等待

```bash
wait 2
wait_element id:"loading" 10
wait_gone id:"loading" 10
```

### 导航

```bash
back
home
menu
recent
```

### 应用管理

```bash
start_app "com.example.app"
stop_app "com.example.app"
clear_app "com.example.app"
```

### 屏幕控制

```bash
screen_on
screen_off
unlock
```

### 元素信息

```bash
get_text id:"button"
get_info id:"element"
find_element id:"button"
find_elements class:"Button"
dump_hierarchy
```

### 条件判断

```bash
if exists id:"button"
    click id:"button"
end

if $var == "value"
    log "匹配"
end
```

### 循环

```bash
loop 5
    click id:"next"
    wait 1
end

while exists id:"loading"
    wait 1
end
```

### 人类模拟

```bash
human_click id:"button"
human_double_click id:"item"
human_long_press id:"item"
human_drag 100, 1500, 100, 500
```

### 变量

```bash
set $name = "value"
log "Hello ${name}"
```

### 其他

```bash
log "消息"
shell "ls /sdcard"
try
    # 操作
catch
    # 处理
end
call "other.script"
```

## 选择器优先级

1. **id** - 最稳定，推荐优先使用
2. **text** - 适用于固定文本
3. **class** - 适用于批量操作
4. **xpath** - 最灵活，用于复杂场景

## 常用模式

### 等待并点击

```bash
wait_element id:"button" 10
click id:"button"
```

### 检查并操作

```bash
if exists id:"button"
    click id:"button"
end
```

### 重试机制

```bash
loop 3
    if exists id:"success"
        break
    end
    click id:"retry"
    wait 2
end
```

### 数据采集

```bash
set $items = find_elements class:"TextView"
log "找到 $items.count 个元素"
```

## 参数说明

### human_click 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| offset_min | 3 | 最小偏移（像素） |
| offset_max | 10 | 最大偏移（像素） |
| delay_min | 0.05 | 最小延迟（秒） |
| delay_max | 0.3 | 最大延迟（秒） |

### human_drag 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| trajectory | bezier | 轨迹类型：bezier, linear_jitter |
| speed | ease_in_out | 速度模式：ease_in_out, ease_in, ease_out, linear, random |
| duration | 1.0 | 拖拽时间（秒） |

## 注意事项

1. 使用 `wait_element` 确保元素加载完成
2. 优先使用 `id` 定位，稳定性最高
3. 使用 `try-catch` 处理可能的错误
4. 使用 `log` 输出调试信息
5. 变量插值必须使用 `${variable}` 格式
