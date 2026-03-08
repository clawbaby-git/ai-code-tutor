# agents.md 设计定稿

## 日期
2026-03-05

## 核心决策

### 1. 文件位置
项目根目录下的 `agents.md`，作为 OpenClaw/OpenCode 的 Agent 定义文件。

### 2. 项目最终结构

```
ai-code-tutor/
├── agents.md
├── courses/
│   └── 2025-logic/
│       ├── 01_starting_point.py
│       ├── ...
│       ├── 08_logic_to_data.py
│       ├── main.py
│       └── README.md
├── my-courses/
│   └── my-python-tutorial/
│       ├── 01_hello.py
│       ├── 02_functions.py
│       └── README.md
└── .gitignore
```

### 3. 已排除的设计

| 设计 | 排除原因 |
|-----|---------|
| progress.yaml | 会话级记录进度，不存文件 |
| 单独的 prompts/ 目录 | 统一放在 agents.md 中 |

### 4. agents.md 核心内容框架

```markdown
# AI Code Tutor - Agent 定义

## 角色
你是编程学习导师，专注于通过代码重构帮助新手提升编程能力。

## 工作目录规则
- 读取课程：courses/<course-id>/
- 用户课程：my-courses/<course-id>/

## 启动流程
1. 扫描 courses/ 和 my-courses/，列出可用课程
2. 询问用户要学习哪个课程
3. 加载选定课程的第一课，开始引导

## 教学原则
- 引导而非灌输
- 循序渐进
- 及时反馈
```

## 下一步

L2 内容结构已定稿，下一步进入 **L3 交互设计** 讨论。
