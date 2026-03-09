"""Core package for the AI Code Tutor MVP."""

from .course import Course, Lesson, load_course, scan_courses
from .progression import ProgressionDecision, decide_progression
from .session import TutorSession
from .workspace import ensure_lesson_in_workspace, get_workspace_path

__all__ = [
    "Course",
    "Lesson",
    "ProgressionDecision",
    "load_course",
    "scan_courses",
    "decide_progression",
    "TutorSession",
    "ensure_lesson_in_workspace",
    "get_workspace_path",
]
