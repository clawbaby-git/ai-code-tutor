from __future__ import annotations

import io
import unittest
from unittest.mock import patch

from tutor import cli


class CliTests(unittest.TestCase):
    def test_next_lesson_uses_handle_progression(self) -> None:
        session = unittest.mock.Mock()
        session.courses = [unittest.mock.Mock(id="courses/logic", lessons=(1, 2))]
        session.select_course.return_value = session.courses[0]
        session.current_lesson_note.return_value = "Lesson 1/2: 1_first.py."
        session.current_lesson_code.return_value = "x = 1\n"
        session.handle_progression.side_effect = [
            unittest.mock.Mock(action="advance", message="Proceeding to the next lesson."),
        ]
        session.next_lesson.side_effect = AssertionError("CLI should use handle_progression")

        with patch("tutor.cli.TutorSession.from_workspace", return_value=session):
            with patch("builtins.input", side_effect=["1", "n", "q"]):
                with patch("sys.stdout", new_callable=io.StringIO) as stdout:
                    exit_code = cli.main()

        self.assertEqual(exit_code, 0)
        session.handle_progression.assert_called_once_with(
            user_intent="next_lesson",
            key_points_covered=True,
        )
        self.assertIn("Starting course: courses/logic", stdout.getvalue())
