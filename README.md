# AI Code Tutor

AI 驱动的代码重构学习项目。

## 设计目标
- 同一套学习逻辑覆盖 Discord / Telegram / 本地目录
- 学习流程由 `agents.md` 驱动（自然语言模式）
- 支持内置课程与自定义课程
- 使用单状态文件保存当前学习上下文

## 核心结构
- `agents.md`：教学行为与流程规则
- `courses/`：内置课程
- `my-courses/`：本地自定义课程
- `.study/state.json`：当前学习上下文（单文件）

## 状态策略
- 不区分 channel
- 不记录 user_id
- 不做跨课程长期进度档案
- 只保存当前课程推进所需上下文
- `summary` 会限长，并且只保留最高价值信息
- 每次启动都重新询问课程选择，不自动恢复上次课程
- 若 `.study/state.json` 缺失、损坏或字段异常，回退为无有效 state 并继续正常选课

## 重置学习
清空状态文件：

```bash
rm -f .study/state.json
```

## 参考文档
- `docs/03-mvp-implementation-plan.md`
- `docs/05-agents-md-design.md`
- `docs/08-runtime-architecture-v1.md`
