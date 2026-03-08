from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

STATE_FILE = Path(".study/state.json")
DEFAULT_MODE = "natural-language"
STATE_VERSION = 1


@dataclass(frozen=True)
class StudyState:
    version: int = STATE_VERSION
    course_id: str = ""
    lesson_index: int = 0
    mode: str = DEFAULT_MODE
    updated_at: str = ""
    summary: str = ""
    last_feedback: str = ""


def state_path(root: Path) -> Path:
    return root / STATE_FILE


def load_state(root: Path) -> StudyState | None:
    path = state_path(root)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    version = payload.get("version")
    course_id = payload.get("course_id")
    lesson_index = payload.get("lesson_index")
    mode = payload.get("mode")
    updated_at = payload.get("updated_at")
    summary = payload.get("summary")
    last_feedback = payload.get("last_feedback")

    if not isinstance(version, int):
        return None
    if not isinstance(course_id, str):
        return None
    if not isinstance(lesson_index, int) or lesson_index < 0:
        return None
    if not isinstance(mode, str):
        return None
    if not isinstance(updated_at, str):
        return None
    if not isinstance(summary, str):
        return None
    if not isinstance(last_feedback, str):
        return None

    return StudyState(
        version=version,
        course_id=course_id,
        lesson_index=lesson_index,
        mode=mode or DEFAULT_MODE,
        updated_at=updated_at,
        summary=summary,
        last_feedback=last_feedback,
    )


def save_state(
    root: Path,
    *,
    course_id: str,
    lesson_index: int,
    mode: str = DEFAULT_MODE,
    summary: str = "",
    last_feedback: str = "",
) -> Path:
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": STATE_VERSION,
        "course_id": course_id,
        "lesson_index": lesson_index,
        "mode": mode or DEFAULT_MODE,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "last_feedback": last_feedback,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path
