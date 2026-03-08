# Runtime Architecture v1

## One Core, Multiple Channels

- Core: `agents.md`
- Content: `courses/`, `my-courses/`
- Context state: `/.study/state.json`
- Channels: Discord / Telegram / local directory via OpenClaw

Channel does not change learning logic.

## State File

Path: `/.study/state.json`

Example:

```json
{
  "version": 1,
  "course_id": "courses/2025-logic",
  "lesson_index": 0,
  "mode": "natural-language",
  "updated_at": "2026-03-09T00:00:00+00:00",
  "summary": "...",
  "last_feedback": "..."
}
```

Rules:
- Single user default.
- No `user_id`.
- No `channel` field.
- Not a long-term cross-course profile.
- `summary` is length-limited and stores only highest-value context.
- On each startup, always re-ask course selection.

## Learning Flow (Natural Language)
1. Select course.
2. Show current lesson code.
3. Ask guiding questions.
4. User answers in natural language.
5. Tutor feedback.
6. On "next lesson": remind missing points briefly, confirm, then follow user intent.

## Reset
Reset learning by clearing `/.study/state.json`.

## Why this architecture
- Minimal complexity
- Consistent behavior across channels
- Easy custom course support on local machine
