from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

STATE_FILE = Path(".study/state.json")
DEFAULT_MODE = "natural-language"
STATE_VERSION = 1
SUMMARY_MAX_LENGTH = 600


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


def normalize_summary(summary: object, max_length: int = SUMMARY_MAX_LENGTH) -> str:
    if isinstance(summary, str):
        raw_summary = summary
    elif summary is None:
        raw_summary = ""
    else:
        try:
            raw_summary = str(summary)
        except Exception:
            raw_summary = ""

    normalized = " ".join(raw_summary.split())
    if len(normalized) <= max_length:
        return normalized

    segments = [segment.strip(" ,;，；。") for segment in raw_summary.replace("\r", "\n").splitlines()]
    sentences: list[str] = []
    for segment in segments:
        if not segment:
            continue
        parts = segment.split(". ")
        for part in parts:
            cleaned = " ".join(part.split()).strip(" ,;，；。")
            if cleaned:
                sentences.append(cleaned)

    categories = (
        ("关键盲点", ("blind", "mistake", "confus", "gap", "weak", "problem", "error", "盲点", "卡住", "不会", "混淆", "错误", "薄弱")),
        ("当前理解", ("understand", "can", "know", "progress", "learn", "理解", "掌握", "知道", "会了", "能", "进展")),
        ("下一步聚焦", ("next", "focus", "todo", "need", "practice", "follow", "下一步", "聚焦", "需要", "练习", "继续", "接下来")),
    )

    chosen: list[tuple[str, str]] = []
    used: set[str] = set()
    lowered_sentences = [(sentence, sentence.lower()) for sentence in sentences]
    for label, keywords in categories:
        match = next(
            (
                sentence
                for sentence, lowered in lowered_sentences
                if sentence not in used and any(keyword in lowered for keyword in keywords)
            ),
            "",
        )
        if match:
            chosen.append((label, match))
            used.add(match)

    for label, _ in categories:
        if any(existing_label == label for existing_label, _ in chosen):
            continue
        fallback = next((sentence for sentence in sentences if sentence not in used), "")
        if fallback:
            chosen.append((label, fallback))
            used.add(fallback)

    compressed = "; ".join(f"{label}: {text}" for label, text in chosen if text)
    if not compressed:
        compressed = normalized[:max_length]

    if len(compressed) <= max_length:
        return compressed

    ellipsis = "..."
    return compressed[: max_length - len(ellipsis)].rstrip(" ,;，；。") + ellipsis


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
    normalized_summary = normalize_summary(summary)
    payload = {
        "version": STATE_VERSION,
        "course_id": course_id,
        "lesson_index": lesson_index,
        "mode": mode or DEFAULT_MODE,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "summary": normalized_summary,
        "last_feedback": last_feedback,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path
