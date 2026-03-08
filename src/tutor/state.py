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
    payload = json.loads(path.read_text(encoding="utf-8"))
    return StudyState(
        version=int(payload.get("version", STATE_VERSION)),
        course_id=str(payload.get("course_id", "")),
        lesson_index=int(payload.get("lesson_index", 0)),
        mode=str(payload.get("mode", DEFAULT_MODE)),
        updated_at=str(payload.get("updated_at", "")),
        summary=str(payload.get("summary", "")),
        last_feedback=str(payload.get("last_feedback", "")),
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
