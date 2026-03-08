from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .course import Course, Lesson, scan_courses
from .state import DEFAULT_MODE, load_state, save_state


@dataclass
class TutorSession:
    workspace: Path = field(default_factory=Path.cwd)
    courses: list[Course] = field(default_factory=list)
    selected_course: Course | None = None
    lesson_index: int = 0
    mode: str = DEFAULT_MODE
    summary: str = ""
    last_feedback: str = ""

    @classmethod
    def from_workspace(cls, root: Path | None = None) -> "TutorSession":
        workspace = root or Path.cwd()
        session = cls(workspace=workspace, courses=scan_courses(workspace))
        session._restore_state()
        return session

    def select_course(self, index: int) -> Course:
        if index < 0 or index >= len(self.courses):
            raise IndexError("course index out of range")
        self.selected_course = self.courses[index]
        self.lesson_index = 0
        self._save_state()
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
        self._save_state()
        return True

    def _restore_state(self) -> None:
        state = load_state(self.workspace)
        if state is None:
            return

        for course in self.courses:
            if course.id != state.course_id:
                continue
            if state.lesson_index < 0 or state.lesson_index >= len(course.lessons):
                return
            self.selected_course = course
            self.lesson_index = state.lesson_index
            self.mode = state.mode or DEFAULT_MODE
            self.summary = state.summary
            self.last_feedback = state.last_feedback
            return

    def _save_state(self) -> None:
        if self.selected_course is None:
            return
        save_state(
            self.workspace,
            course_id=self.selected_course.id,
            lesson_index=self.lesson_index,
            mode=self.mode,
            summary=self.summary,
            last_feedback=self.last_feedback,
        )
