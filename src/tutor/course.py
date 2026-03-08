from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

LESSON_FILE_RE = re.compile(r"^(?P<number>\d+)_.*\.py$")


@dataclass(frozen=True)
class Lesson:
    number: int
    filename: str
    path: Path

    @property
    def title(self) -> str:
        stem = self.path.stem
        _, _, raw = stem.partition("_")
        return raw.replace("_", " ") if raw else stem


@dataclass(frozen=True)
class Course:
    name: str
    source: str
    path: Path
    lessons: tuple[Lesson, ...]

    @property
    def id(self) -> str:
        return f"{self.source}/{self.name}"


def _lesson_sort_key(path: Path) -> tuple[int, str]:
    match = LESSON_FILE_RE.match(path.name)
    if not match:
        raise ValueError(f"Not a lesson file: {path.name}")
    return int(match.group("number")), path.name


def load_course(course_path: Path, source: str) -> Course:
    lesson_paths = [
        entry
        for entry in course_path.iterdir()
        if entry.is_file() and LESSON_FILE_RE.match(entry.name)
    ]
    lessons = tuple(
        Lesson(
            number=int(LESSON_FILE_RE.match(path.name).group("number")),
            filename=path.name,
            path=path,
        )
        for path in sorted(lesson_paths, key=_lesson_sort_key)
    )
    return Course(name=course_path.name, source=source, path=course_path, lessons=lessons)


def _scan_base(base_dir: Path, source: str) -> Iterable[Course]:
    if not base_dir.exists() or not base_dir.is_dir():
        return []

    courses: list[Course] = []
    for item in sorted(base_dir.iterdir(), key=lambda p: p.name):
        if not item.is_dir():
            continue
        course = load_course(item, source=source)
        if course.lessons:
            courses.append(course)
    return courses


def scan_courses(root: Path) -> list[Course]:
    """Scan ./courses and ./my-courses for course directories."""
    courses = [
        *_scan_base(root / "courses", source="courses"),
        *_scan_base(root / "my-courses", source="my-courses"),
    ]
    return sorted(courses, key=lambda course: (course.source, course.name))
