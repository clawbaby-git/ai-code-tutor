from __future__ import annotations

import shutil
from pathlib import Path


def get_workspace_path(root: Path, course_id: str) -> Path:
    workspace_path = root / Path(course_id)
    workspace_path.mkdir(parents=True, exist_ok=True)
    return workspace_path


def ensure_lesson_in_workspace(lesson_path: Path, workspace_root: Path) -> Path:
    workspace_root.mkdir(parents=True, exist_ok=True)
    workspace_lesson_path = workspace_root / lesson_path.name

    if not workspace_lesson_path.exists():
        shutil.copy2(lesson_path, workspace_lesson_path)
        return workspace_lesson_path

    if lesson_path.stat().st_mtime_ns > workspace_lesson_path.stat().st_mtime_ns:
        shutil.copy2(lesson_path, workspace_lesson_path)

    return workspace_lesson_path
