# L2 内容结构设计 - 讨论定稿

## 讨论日期
2026-03-05

## 核心决策

### 1. 目录结构（最终版）

```
ai-code-tutor/
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

### 2. 关键设计原则

| 原则 | 说明 |
|-----|------|
| 结构统一 | `courses/` 和 `my-courses/` 下的课程文件夹结构完全一致 |
| 文件夹为单位 | 一个课程 = 一个文件夹 |
| 进度会话级 | 不存 progress 文件，学习状态在 AI 会话中维护 |
| 用户资料隔离 | `my-courses/` 默认在 `.gitignore` 中 |

### 3. 课程内容来源

- **内置课程**：从 ArjanCodes/examples 同步，放在 `courses/`
- **用户课程**：用户自己在 `my-courses/` 中创建或导入

### 4. 一个课程文件夹内部（示例）

```
2025-logic/
├── 01_starting_point.py
├── 02_characterization_tests.py
├── 03_guard_clauses.py
├── ...
├── 08_logic_to_data.py
├── main.py
├── test_main.py
└── README.md
```

## 讨论中排除的方案

- 不使用 progress.yaml，改为会话级维护
- 用户课程不松散存放，统一使用 `my-courses/`
- 内置与用户课程不走两套结构

## 下一步

L2 内容结构已定，下一步进入 **L3 交互设计**。
