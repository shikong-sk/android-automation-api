# 人类模拟操作示例

## 1. 人类模拟点击

### 基础点击

```bash
# 通过选择器点击
human_click id:"button"
human_click text:"确定"
human_click xpath:"//Button[@text='提交']"

# 通过坐标点击
human_click 500, 800
```

### 自定义参数点击

```bash
# 自定义偏移范围
human_click id:"button", offset_min=5, offset_max=15

# 自定义延迟范围
human_click id:"button", delay_min=0.1, delay_max=0.5

# 完整自定义
human_click 500, 800, offset_min=3, offset_max=10, delay_min=0.05, delay_max=0.3
```

### 高级选择器点击

```bash
# 带父级选择器
human_click id:"child" parent=id:"parent_id"

# 带兄弟选择器
human_click id:"target" sibling=id:"sibling_id" sibling_relation=following

# 带偏移
human_click id:"button" offset_x=10 offset_y=-5
```

## 2. 人类模拟双击

```bash
# 基础双击
human_double_click id:"item"
human_double_click 500, 800

# 自定义双击间隔
human_double_click id:"item", interval_min=0.1, interval_max=0.2
```

## 3. 人类模拟长按

```bash
# 基础长按
human_long_press id:"item"
human_long_press 500, 800

# 自定义长按时间
human_long_press id:"item", duration_min=1.0, duration_max=2.0
human_long_press 500, 800, duration_min=1.5, duration_max=3.0
```

## 4. 人类模拟拖拽

### 坐标到坐标拖拽

```bash
# 基础拖拽
human_drag 100, 1500, 100, 500

# 指定拖拽时间
human_drag 100, 1500, 100, 500, duration=2.0
```

### 贝塞尔曲线轨迹（推荐）

```bash
# 基础贝塞尔曲线
human_drag 100, 1500, 100, 500, trajectory="bezier"

# 贝塞尔曲线 + 速度模式
human_drag 100, 1500, 100, 500, trajectory="bezier", speed="ease_in_out"

# 完整参数
human_drag 100, 1500, 100, 500, trajectory="bezier", speed="ease_in_out", duration=1.5
```

### 直线抖动轨迹

```bash
# 基础直线抖动
human_drag 100, 1500, 100, 500, trajectory="linear_jitter"

# 直线抖动 + 随机速度
human_drag 100, 1500, 100, 500, trajectory="linear_jitter", speed="random"

# 完整参数
human_drag 100, 1500, 100, 500, trajectory="linear_jitter", speed="random", duration=1.5, num_points=80
```

### 元素到元素拖拽

```bash
# 通过选择器拖拽
human_drag id:"source_item" id:"target_area"

# 混合模式（坐标 + 选择器）
human_drag 100, 1500 id:"target_area"
human_drag id:"source_item" 100, 500
```

### 速度模式说明

| 速度模式 | 说明 |
|---------|------|
| ease_in_out | 慢-快-慢（最自然） |
| ease_in | 慢-快 |
| ease_out | 快-慢 |
| linear | 匀速 |
| random | 随机速度 |

## 5. 完整示例：模拟真实用户行为

```bash
# 启动应用（模拟用户点击图标）
human_click 250, 750, offset_min=20, offset_max=50, delay_min=0.3, delay_max=0.8
wait 3

# 浏览首页（模拟用户阅读）
loop 5
    # 模拟阅读时间
    wait 2

    # 自然滑动
    human_drag 500, 1100, 500, 400, trajectory="bezier", speed="ease_in_out", duration=1.5

    wait 0.8
end

# 点击感兴趣的内容（模拟用户犹豫）
wait 1.5
human_click text:"热门推荐", offset_min=5, offset_max=15, delay_min=0.2, delay_max=0.5
wait 2

# 阅读文章（模拟滑动阅读）
loop 4
    human_drag 500, 1000, 500, 300, trajectory="bezier", speed="ease_in_out", duration=2.0
    wait 2
end

# 点赞操作（模拟用户犹豫）
wait 1
human_click id:"like_button", offset_min=3, offset_max=10, delay_min=0.1, delay_max=0.3
wait 0.5

# 返回（模拟用户返回）
human_click 80, 120, offset_min=5, offset_max=15, delay_min=0.2, delay_max=0.5
wait 2

# 返回主页
home
```

## 6. 参数对比表

### 点击参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| offset_min | 3 | 最小偏移（像素） |
| offset_max | 10 | 最大偏移（像素） |
| delay_min | 0.05 | 最小延迟（秒） |
| delay_max | 0.3 | 最大延迟（秒） |

### 双击参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| interval_min | 0.1 | 最小间隔（秒） |
| interval_max | 0.2 | 最大间隔（秒） |

### 长按参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| duration_min | 1.0 | 最小时长（秒） |
| duration_max | 2.0 | 最大时长（秒） |

### 拖拽参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| trajectory | bezier | 轨迹类型 |
| speed | ease_in_out | 速度模式 |
| duration | 1.0 | 拖拽时间（秒） |
| num_points | 50 | 轨迹采样点数 |
| jitter_min | 1 | 最小抖动（像素） |
| jitter_max | 5 | 最大抖动（像素） |

## 7. 使用建议

### 何时使用人类模拟

1. **避免检测** - 防止被识别为自动化脚本
2. **真实测试** - 模拟真实用户行为
3. **自然交互** - 更自然的操作体验

### 推荐配置

```bash
# 日常操作（平衡性能和真实性）
human_click id:"button", offset_min=3, offset_max=10, delay_min=0.05, delay_max=0.3

# 高真实性（更接近人类）
human_click id:"button", offset_min=5, offset_max=15, delay_min=0.1, delay_max=0.5

# 快速操作（性能优先）
human_click id:"button", offset_min=1, offset_max=5, delay_min=0.02, delay_max=0.1
```

### 拖拽轨迹选择

| 场景 | 推荐轨迹 | 速度模式 |
|------|---------|---------|
| 日常滑动 | bezier | ease_in_out |
| 快速滑动 | bezier | ease_in |
| 精确拖拽 | linear_jitter | linear |
| 随机行为 | linear_jitter | random |
