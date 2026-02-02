# 基础操作示例

## 1. 点击元素

```bash
# 通过 ID 点击
click id:"com.example:id/button"

# 通过文本点击
click text:"确定"

# 通过 XPath 点击
click xpath:"//Button[@text='提交']"

# 通过坐标点击
click 500, 800
```

## 2. 输入文本

```bash
# 输入到指定元素
input id:"username" "test@example.com"
input text:"用户名" "张三"

# 清除输入框
clear id:"username"
clear text:"密码"
```

## 3. 滑动屏幕

```bash
# 向上滑动 50%
swipe up 0.5

# 向下滑动 30%
swipe down 0.3

# 向左滑动
swipe left

# 向右滑动
swipe right

# 坐标滑动
swipe 100, 500, 100, 200
```

## 4. 等待操作

```bash
# 等待固定时间
wait 2

# 等待元素出现
wait_element id:"loading" 10

# 等待元素消失
wait_gone id:"loading" 10
```

## 5. 导航操作

```bash
# 返回上一页
back

# 返回桌面
home

# 打开菜单
menu

# 最近任务
recent
```

## 6. 应用管理

```bash
# 启动应用
start_app "com.example.app"

# 停止应用
stop_app "com.example.app"

# 清除应用数据
clear_app "com.example.app"
```

## 7. 屏幕控制

```bash
# 亮屏
screen_on

# 锁屏
screen_off

# 解锁
unlock
```

## 8. 元素信息获取

```bash
# 获取元素文本
set $text = get_text id:"button"
log "按钮文本: $text"

# 获取元素完整信息
set $info = get_info id:"button"
log "按钮信息: $info"

# 查找元素
set $element = find_element text:"确定"
if $element.exists
    log "找到元素: $element.text"
end

# 查找所有匹配元素
set $elements = find_elements class:"android.widget.Button"
log "找到 $elements.count 个按钮"
```

## 9. 条件判断

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
elif $status == "error"
    log "操作失败"
else
    log "未知状态"
end
```

## 10. 循环操作

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

# 循环控制
loop 10
    if exists id:"done"
        break
    end
    click id:"next"
    continue
end
```

## 11. 错误处理

```bash
try
    click id:"maybe_not_exist"
    wait 1
catch
    log "元素不存在，跳过"
end
```

## 12. 变量使用

```bash
# 设置变量
set $username = "test@example.com"
set $password = "password123"

# 使用变量
input id:"username" "${username}"
input id:"password" "${password}"

# 变量插值
log "用户名: ${username}"
```

## 13. 日志输出

```bash
# 输出日志
log "开始执行操作"
log "当前状态: $status"
log "操作完成"
```

## 14. Shell 命令

```bash
# 执行 Shell 命令
shell "ls /sdcard"
shell "screencap -p /sdcard/screenshot.png"
```

## 15. 子脚本调用

```bash
# 调用其他脚本
call "login.script"
call "navigate.script"
```

## 完整示例：简单登录流程

```bash
# 启动应用
start_app "com.example.app"
wait 2

# 输入账号密码
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

# 返回主页
home
```
