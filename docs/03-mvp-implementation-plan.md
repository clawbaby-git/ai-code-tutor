# MVP 实现计划（v1 对齐版）

## 目标
通过 OpenClaw 在不同 channel（Discord / Telegram / 本地目录）提供同一套自然语言学习体验。

## 核心原则
1. **统一入口逻辑**：channel 只是消息来源，不改变教学逻辑。
2. **最少系统复杂度**：以 `agents.md` + 课程文件为主。
3. **单状态文件**：仅用 `./.study/state.json` 维持当前学习上下文。
4. **不做跨课程历史系统**：状态仅服务当前课程推进。

## 当前目录基线

```text
ai-code-tutor/
├── agents.md
├── courses/
│   └── 2025-logic/
├── my-courses/
│   └── <custom-course>/
├── .study/
│   └── state.json
└── docs/
```

## MVP 功能范围

### P0（必须）
- [x] 课程扫描：`courses/` + `my-courses/`
- [x] lesson 顺序解析（兼容 `01_*.py` / `1_*.py`）
- [x] 单状态文件读写：`.study/state.json`
- [x] 自然语言教学模式
- [x] “下一课”流程：覆盖检查提醒 -> 二次确认 -> 遵循用户意图
- [x] 重置学习：清空状态文件

### P1（延后）
- [ ] 自动化要点覆盖评分
- [ ] diff 对比建议
- [ ] 多角色导师风格切换

## 运行策略
- 优先通过 OpenClaw 直接读取项目目录下 `agents.md` 执行教学。
- 不在产品文档中设计 CLI 指令式交互。

## 验收标准
1. 在 Discord 和 Telegram 中学习行为一致。
2. 在本地目录中学习行为与 channel 一致。
3. 删除 `.study/state.json` 后可从头开始。
4. 不引入跨课程历史跟踪复杂度。
5. 每次启动都重新询问课程选择。
6. `summary` 限长且仅保留最重要上下文。
