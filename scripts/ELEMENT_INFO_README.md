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
