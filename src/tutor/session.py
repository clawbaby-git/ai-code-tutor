from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .course import Course, Lesson, scan_courses


@dataclass
class TutorSession:
    courses: list[Course] = field(default_factory=list)
    selected_course: Course | None = None
    lesson_index: int = 0

    @classmethod
    def from_workspace(cls, root: Path | None = None) -> "TutorSession":
        workspace = root or Path.cwd()
        return cls(courses=scan_courses(workspace))

    def select_course(self, index: int) -> Course:
        if index < 0 or index >= len(self.courses):
            raise IndexError("course index out of range")
        self.selected_course = self.courses[index]
        self.lesson_index = 0
        return self.selected_course

    @property
    def current_lesson(self) -> Lesson | None:
        if self.selected_course is None:
            return None
        if not self.selected_course.lessons:
            return None
        return self.selected_course.lessons[self.lesson_index]

    def current_lesson_code(self) -> str:
        lesson = self.current_lesson
        if lesson is None:
            raise RuntimeError("no course selected")
        return lesson.path.read_text(encoding="utf-8")

    def current_lesson_note(self) -> str:
        lesson = self.current_lesson
        if lesson is None:
            return "No lesson selected."
        total = len(self.selected_course.lessons)
        return (
            f"Lesson {self.lesson_index + 1}/{total}: {lesson.filename}. "
            "Read the code and identify one refactoring target."
        )

    def next_lesson(self) -> bool:
        if self.selected_course is None:
            return False
        if self.lesson_index + 1 >= len(self.selected_course.lessons):
            return False
        self.lesson_index += 1
        return True
