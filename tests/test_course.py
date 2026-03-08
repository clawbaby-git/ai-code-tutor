from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tutor.course import load_course, scan_courses


class CourseLoadingTests(unittest.TestCase):
    def test_scan_courses_discovers_built_in_and_user_courses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            built_in = root / "courses" / "logic"
            user = root / "my-courses" / "python-basics"
            built_in.mkdir(parents=True)
            user.mkdir(parents=True)

            (built_in / "1_intro.py").write_text("print('a')\n", encoding="utf-8")
            (user / "01_setup.py").write_text("print('b')\n", encoding="utf-8")

            courses = scan_courses(root)

            self.assertEqual(
                [course.id for course in courses],
                ["courses/logic", "my-courses/python-basics"],
            )

    def test_load_course_sorts_lessons_by_numeric_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            course_dir = Path(tmp_dir) / "courses" / "sample"
            course_dir.mkdir(parents=True)

            for name in ["10_wrap.py", "2_core.py", "01_intro.py", "main.py", "test_main.py"]:
                (course_dir / name).write_text("pass\n", encoding="utf-8")

            course = load_course(course_dir, source="courses")

            self.assertEqual(
                [lesson.filename for lesson in course.lessons],
                ["01_intro.py", "2_core.py", "10_wrap.py"],
            )
            self.assertEqual([lesson.number for lesson in course.lessons], [1, 2, 10])


if __name__ == "__main__":
    unittest.main()
