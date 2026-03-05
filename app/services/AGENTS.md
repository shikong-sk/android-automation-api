# 服务层 - DSL 引擎与自动化服务

## 概述

业务逻辑层，包含自动化服务和自定义 DSL 脚本引擎。DSL 系统是本项目的主要特色功能。

## 目录结构

```
app/services/
├── base.py              # AutomationService 服务基类
├── input.py             # InputService - 点击、文本、滑动、选择器
├── navigation.py        # NavigationService - 主页、返回、菜单
├── app_service.py       # AppService - 应用启动/停止/清除
├── adb_service.py       # AdbService - shell、包管理、设备信息
├── script_parser.py     # DSL 词法分析器 + 语法分析器 (1086 行)
└── script_executor.py   # DSL 执行器 (1253 行)
```

## 开发指南

| 任务 | 文件 | 说明 |
|------|------|-------|
| 新增服务 | `base.py` + 新文件 | 继承 `AutomationService` |
| 新增 DSL 词法 | `script_parser.py:TokenType` | 添加到枚举 |
| 新增 DSL 命令 | `script_parser.py` 解析器 + `script_executor.py` `_execute_*` | Token → AST → 执行 |
| 点击/滑动逻辑 | `input.py` | uiautomator2 设备操作 |
| 人类模拟 | `input.py` | 随机偏移、贝塞尔曲线 |

## DSL 引擎架构

### 词法分析 → 语法分析 → 执行 流程

```
脚本文本
    ↓
script_parser.py: 词法分析器 (分词)
    ↓
script_parser.py: 语法分析器 (构建 AST)
    ↓
script_executor.py: 执行器 (运行 AST 节点)
```

### 核心类

| 类 | 文件 | 作用 |
|-------|------|------|
| `TokenType` | script_parser.py:12 | 60+ 种词法类型 (CLICK, IF, LOOP 等) |
| `Token` | script_parser.py | 词法分析输出 |
| `ASTNode` | script_parser.py | AST 节点基类 |
| `CommandNode` | script_parser.py | 命令 AST (click, input 等) |
| `IfNode` | script_parser.py | 条件 AST |
| `LoopNode` | script_parser.py | 循环 AST |
| `ScriptExecutor` | script_executor.py:69 | 主执行器类 |
| `ExecutionContext` | script_executor.py:47 | 变量、日志、停止标志 |

### 新增 DSL 命令步骤

1. **添加词法类型** 在 `TokenType` 枚举中
2. **添加关键字映射** 在 `Lexer._KEYWORDS` 中
3. **添加 AST 节点** 如需要（或复用 `CommandNode`）
4. **添加解析方法** 在 `Parser` 中
5. **添加执行方法** `_execute_命令名()` 在 `ScriptExecutor` 中

### 选择器语法

DSL 支持 4 种选择器类型：

```bash
id:"com.example:id/button"     # resource-id
text:"确定"                     # 文本内容
xpath:"//Button[@text='确定']" # XPath 表达式
class:"android.widget.Button"  # 类名
```

### 人类模拟参数

| 命令 | 参数 |
|---------|------------|
| `human_click` | offset_min/max, delay_min/max, duration_min/max |
| `human_drag` | trajectory (bezier/linear_jitter), speed_mode, duration, num_points |

## 编码规范

- 服务在 `__init__` 中接收 `DeviceManager`
- 通过 `self.device` 访问设备（缓存）
- 从 `execute()` 返回 `{"success": True, "result": ...}`
- DSL 命令映射到 `_execute_<命令>()` 方法
- 使用 `self.context.variables` 存储 DSL 变量

## 注意事项

- `script_parser.py` 共 1086 行 - 项目中最大的文件
- `script_executor.py` 共 1253 行 - 第二大文件
- 变量在 DSL 中使用 `$` 前缀：`$name`
- 字符串插值：`${variable}`
- Break/Continue 使用自定义异常（`BreakException`, `ContinueException`）