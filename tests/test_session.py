from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tutor.session import TutorSession


class TutorSessionTests(unittest.TestCase):
    def test_session_progression_and_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            course_dir = Path(tmp_dir) / "courses" / "logic"
            course_dir.mkdir(parents=True)

            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            session = TutorSession.from_workspace(Path(tmp_dir))
            selected = session.select_course(0)

            self.assertEqual(selected.id, "courses/logic")
            self.assertEqual(session.current_lesson.filename, "1_first.py")
            self.assertEqual(session.current_lesson_code().strip(), "x = 1")

            self.assertTrue(session.next_lesson())
            self.assertEqual(session.current_lesson.filename, "2_second.py")
            self.assertFalse(session.next_lesson())


if __name__ == "__main__":
    unittest.main()
