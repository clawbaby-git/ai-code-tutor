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
- `.study/workspace/{course_id}/`：用户可编辑的 lesson 副本

## 状态策略
- 不区分 channel
- 不记录 user_id
- 不做跨课程长期进度档案
- 只保存当前课程推进所需上下文
- `summary` 会限长，并且只保留最高价值信息
- 每次启动都重新询问课程选择，不自动恢复上次课程
- 若 `.study/state.json` 缺失、损坏或字段异常，回退为无有效 state 并继续正常选课
- 用户请求“下一课”时，若关键点未覆盖，会先提示缺口并请求确认；用户确认后再推进，否则保持当前课

## 用户工作区
- `courses/` 和 `my-courses/` 保持原始课程内容，只作为只读源文件
- 选课后，当前 lesson 会自动复制到 `.study/workspace/{course_id}/`
- Tutor 读取当前 lesson 时优先读取工作区副本，因此用户修改不会污染原始课程文件
- 需要对比原始版本和用户版本时，可同时读取课程源文件与工作区副本

## 重置学习
清空状态文件：

```bash
rm -f .study/state.json
```

如需连同用户工作区一起清空：

```bash
rm -rf .study
```

## 参考文档
- `docs/03-mvp-implementation-plan.md`
- `docs/05-agents-md-design.md`
- `docs/08-runtime-architecture-v1.md`
