# MVP 实现计划

## 目标
一个可在 Telegram 运行的最小可用版本，支持完成 1 个完整课程（logic）的学习。

## 技术栈选择

| 组件 | 选择 | 理由 |
|-----|------|------|
| AI 后端 | OpenClaw / OpenCode | 已与 Telegram 集成，无需额外 bot 开发 |
| 课程数据 | Git 子模块 | 直接引用 ArjanCodes/examples |
| 状态存储 | 本地 JSON | MVP 阶段无需数据库 |
| 代码展示 | Markdown 代码块 | Telegram 原生支持 |

## 目录结构

```
ai-code-tutor/
├── README.md
├── .gitmodules
├── courses/
│   └── logic/
│       ├── course.yaml
│       ├── stages/
│       └── reference/
├── src/
│   └── tutor/
│       ├── __init__.py
│       ├── course.py
│       ├── review.py
│       └── diff.py
└── prompts/
    ├── system.md
    ├── lesson_intro.md
    ├── code_review.md
    └── finale.md
```

## MVP 功能范围

### 必须实现（P0）

- [ ] 课程加载：读取 `course.yaml` 和阶段代码
- [ ] 对话引导：按课程流程进行对话
- [ ] 代码展示：发送当前阶段代码给用户
- [ ] 自然语言响应：理解用户意图并给出反馈
- [ ] 课程完成：展示总结和评分

### 可以延后（P1）

- [ ] 代码审核：自动检测用户修改的质量
- [ ] diff 生成：对比用户代码和参考答案
- [ ] 状态持久化：记住用户学习进度
- [ ] 多课程支持：不只是 logic

## 快速启动方案

### 方案 A：纯提示词驱动（最快）

1. 把课程文件放进 workspace
2. 在系统提示词里定义导师角色和课程流程
3. 用 `read` 工具读取当前阶段代码
4. 对话引导用户学习

**优点**：零开发，立即可用
**缺点**：无自动化审核，纯靠 AI 理解

### 方案 B：轻量脚本驱动（半天级）

写一个小型导师引擎，负责课程加载、状态推进和审核辅助。

## 当前倾向

优先走 **方案 A**，尽快跑通真实学习闭环，再决定是否升级到脚本驱动。
