from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from tutor.workspace import ensure_lesson_in_workspace, get_workspace_path


class WorkspaceTests(unittest.TestCase):
    def test_get_workspace_path_creates_course_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_root = Path(tmp_dir) / ".study" / "workspace"

            course_workspace = get_workspace_path(workspace_root, "courses/logic")

            self.assertEqual(course_workspace, workspace_root / "courses" / "logic")
            self.assertTrue(course_workspace.exists())
            self.assertTrue(course_workspace.is_dir())

    def test_ensure_lesson_in_workspace_copies_lesson(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            lesson_path = root / "courses" / "logic" / "1_first.py"
            lesson_path.parent.mkdir(parents=True)
            lesson_path.write_text("x = 1\n", encoding="utf-8")

            workspace_root = get_workspace_path(root / ".study" / "workspace", "courses/logic")
            workspace_lesson = ensure_lesson_in_workspace(lesson_path, workspace_root)

            self.assertEqual(workspace_lesson, workspace_root / "1_first.py")
            self.assertEqual(workspace_lesson.read_text(encoding="utf-8"), "x = 1\n")

    def test_ensure_lesson_in_workspace_recopies_when_source_is_newer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            lesson_path = root / "courses" / "logic" / "1_first.py"
            lesson_path.parent.mkdir(parents=True)
            lesson_path.write_text("x = 1\n", encoding="utf-8")

            workspace_root = get_workspace_path(root / ".study" / "workspace", "courses/logic")
            workspace_lesson = ensure_lesson_in_workspace(lesson_path, workspace_root)
            workspace_lesson.write_text("x = 99\n", encoding="utf-8")

            lesson_path.write_text("x = 2\n", encoding="utf-8")
            newer_mtime = workspace_lesson.stat().st_mtime_ns + 1_000_000
            os.utime(lesson_path, ns=(newer_mtime, newer_mtime))

            recopy_path = ensure_lesson_in_workspace(lesson_path, workspace_root)

            self.assertEqual(recopy_path.read_text(encoding="utf-8"), "x = 2\n")
