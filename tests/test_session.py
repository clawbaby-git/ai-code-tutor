from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tutor.progression import decide_progression
from tutor.session import TutorSession
from tutor.state import state_path


class TutorSessionTests(unittest.TestCase):
    def test_select_course_creates_state_file(self) -> None:
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
            self.assertTrue(
                (Path(tmp_dir) / ".study" / "workspace" / "courses" / "logic" / "1_first.py").exists()
            )
            self.assertTrue(state_path(Path(tmp_dir)).exists())

            payload = json.loads(state_path(Path(tmp_dir)).read_text(encoding="utf-8"))
            self.assertEqual(payload["course_id"], "courses/logic")
            self.assertEqual(payload["lesson_index"], 0)
            self.assertEqual(payload["mode"], "natural-language")

    def test_startup_with_existing_state_still_requires_course_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            study_dir = root / ".study"
            study_dir.mkdir(parents=True)
            (study_dir / "state.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "course_id": "courses/logic",
                        "lesson_index": 1,
                        "mode": "natural-language",
                        "updated_at": "2026-03-09T00:00:00+00:00",
                        "summary": "s",
                        "last_feedback": "f",
                    }
                ),
                encoding="utf-8",
            )

            session = TutorSession.from_workspace(root)
            self.assertIsNone(session.selected_course)
            self.assertEqual(session.lesson_index, 0)
            self.assertEqual(session.mode, "natural-language")
            self.assertEqual(session.summary, "s")
            self.assertEqual(session.last_feedback, "f")

    def test_corrupt_state_file_falls_back_to_no_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")

            study_dir = root / ".study"
            study_dir.mkdir(parents=True)
            (study_dir / "state.json").write_text("{bad json", encoding="utf-8")

            session = TutorSession.from_workspace(root)

            self.assertIsNone(session.selected_course)
            self.assertEqual(session.lesson_index, 0)
            self.assertEqual(session.summary, "")
            self.assertEqual(session.last_feedback, "")

    def test_invalid_state_fields_fall_back_to_no_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")

            study_dir = root / ".study"
            study_dir.mkdir(parents=True)
            (study_dir / "state.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "course_id": "courses/logic",
                        "lesson_index": "1",
                        "mode": "natural-language",
                        "updated_at": "2026-03-09T00:00:00+00:00",
                        "summary": "s",
                    }
                ),
                encoding="utf-8",
            )

            session = TutorSession.from_workspace(root)

            self.assertIsNone(session.selected_course)
            self.assertEqual(session.lesson_index, 0)
            self.assertEqual(session.summary, "")
            self.assertEqual(session.last_feedback, "")

    def test_select_course_starts_from_first_lesson_even_with_existing_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            study_dir = root / ".study"
            study_dir.mkdir(parents=True)
            (study_dir / "state.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "course_id": "courses/logic",
                        "lesson_index": 1,
                        "mode": "natural-language",
                        "updated_at": "2026-03-09T00:00:00+00:00",
                        "summary": "s",
                        "last_feedback": "f",
                    }
                ),
                encoding="utf-8",
            )

            session = TutorSession.from_workspace(root)
            selected = session.select_course(0)

            self.assertEqual(selected.id, "courses/logic")
            self.assertEqual(session.lesson_index, 0)
            self.assertEqual(session.current_lesson.filename, "1_first.py")

    def test_next_lesson_writes_back_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            session = TutorSession.from_workspace(root)
            session.select_course(0)

            self.assertTrue(session.next_lesson())
            self.assertEqual(session.current_lesson.filename, "2_second.py")
            self.assertEqual(
                session.get_current_lesson_workspace_path(),
                root / ".study" / "workspace" / "courses" / "logic" / "2_second.py",
            )
            self.assertFalse(session.next_lesson())

            payload = json.loads(state_path(root).read_text(encoding="utf-8"))
            self.assertEqual(payload["lesson_index"], 1)
            self.assertEqual(payload["course_id"], "courses/logic")

    def test_current_lesson_code_reads_user_workspace_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            original_lesson = course_dir / "1_first.py"
            original_lesson.write_text("x = 1\n", encoding="utf-8")

            session = TutorSession.from_workspace(root)
            session.select_course(0)

            workspace_lesson = session.get_current_lesson_workspace_path()
            workspace_lesson.write_text("x = 99\n", encoding="utf-8")

            self.assertEqual(session.current_lesson.path, original_lesson)
            self.assertEqual(session.current_lesson_code().strip(), "x = 99")

    def test_next_lesson_gate_asks_for_confirmation_when_gaps_remain(self) -> None:
        decision = decide_progression(
            user_intent="next_lesson",
            key_points_covered=False,
            pending_gaps=["guard clauses", "naming conditions"],
            user_confirmation=None,
        )

        self.assertEqual(decision.action, "ask_confirm")
        self.assertIn("guard clauses", decision.message)
        self.assertIn("continue to the next lesson", decision.message)

    def test_next_lesson_gate_advances_after_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            session = TutorSession.from_workspace(root)
            session.select_course(0)

            decision = session.handle_progression(
                user_intent="next_lesson",
                key_points_covered=False,
                pending_gaps=["extracting intent"],
                user_confirmation=True,
            )

            self.assertEqual(decision.action, "advance")
            self.assertEqual(session.current_lesson.filename, "2_second.py")

    def test_next_lesson_gate_stays_when_not_confirmed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            session = TutorSession.from_workspace(root)
            session.select_course(0)

            decision = session.handle_progression(
                user_intent="next_lesson",
                key_points_covered=False,
                pending_gaps=["extracting intent"],
                user_confirmation=False,
            )

            self.assertEqual(decision.action, "stay")
            self.assertEqual(session.current_lesson.filename, "1_first.py")

    def test_next_lesson_gate_advances_when_key_points_are_covered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            course_dir = root / "courses" / "logic"
            course_dir.mkdir(parents=True)
            (course_dir / "1_first.py").write_text("x = 1\n", encoding="utf-8")
            (course_dir / "2_second.py").write_text("x = 2\n", encoding="utf-8")

            session = TutorSession.from_workspace(root)
            session.select_course(0)

            decision = session.handle_progression(
                user_intent="next_lesson",
                key_points_covered=True,
                pending_gaps=["extracting intent"],
                user_confirmation=None,
            )

            self.assertEqual(decision.action, "advance")
            self.assertEqual(session.current_lesson.filename, "2_second.py")


if __name__ == "__main__":
    unittest.main()
