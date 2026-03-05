# Vue 组件

## 概述

安卓设备自动化 UI 的 Vue 3 组件。使用 Element Plus 作为 UI 基础组件，Tailwind CSS 进行样式设计。

## 目录结构

```
frontend/src/components/
├── AppManager.vue         # 应用列表，启动/停止/清除
├── DeviceCard.vue         # 设备状态显示
├── InputControl.vue       # 点击、文本、滑动、选择器
├── NavigationControl.vue  # 主页、返回、菜单按钮
├── AdbManager.vue         # Shell、包管理、设备信息
├── ScriptEditor.vue       # Monaco 编辑器，执行脚本
└── XPathGenerator.vue     # 可视化 XPath 生成器
```

## 开发指南

| 任务 | 组件 | 说明 |
|------|-----------|-------|
| 新增输入操作 | `InputControl.vue` | 多标签页：点击、文本、滑动、选择器 |
| 新增应用管理 | `AppManager.vue` | 包列表、操作按钮 |
| 新增脚本功能 | `ScriptEditor.vue` | Monaco 编辑器集成 |
| XPath 生成 | `XPathGenerator.vue` | 模板、XML 树、验证 |
| 设备状态 UI | `DeviceCard.vue` | 连接状态、信息 |

## 核心模式

### 组件结构

```vue
<script setup>
import { ref, computed } from 'vue'
import { apiFunction } from '@/api/module'

// 响应式状态
const loading = ref(false)
const data = ref(null)

// 方法
async function handleAction() { ... }
</script>

<template>
  <el-card>
    <!-- Element Plus 组件 -->
  </el-card>
</template>
```

### API 集成

组件从 `@/api/` 导入：

```js
import { deviceApi } from '@/api/device'
import { inputApi } from '@/api/input'
import { scriptApi } from '@/api/script'
```

### 选择器类型

所有输入组件支持 4 种选择器类型：

| 类型 | 用途 |
|------|-------|
| By ID | `resource-id` 属性 |
| By Text | 显示文本 |
| By Class | Android 类名 |
| By XPath | XPath 表达式 |

## 编码规范

- **组合式 API** 使用 `<script setup>`
- **Element Plus** 组件使用 `el-` 前缀
- **Tailwind** 工具类进行布局
- **API 调用** 使用 async/await 配合 try/catch
- **状态管理** 通过 `ref()` / `reactive()`

## 注意事项

- `InputControl.vue` 最为复杂 - 包含多个标签页和选择器模式
- `XPathGenerator.vue` 包含 XML 树解析器，用于可视化元素选择
- `ScriptEditor.vue` 使用 Monaco 编辑器（`@guolao/vue-monaco-editor`）
- 组件通过事件向父页面传递操作