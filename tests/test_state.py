from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tutor.state import SUMMARY_MAX_LENGTH, normalize_summary, save_state, state_path


class NormalizeSummaryTests(unittest.TestCase):
    def test_short_summary_is_unchanged(self) -> None:
        summary = "关键盲点: 还不稳定。当前理解: 知道 guard clause。下一步聚焦: 继续练习。"

        self.assertEqual(normalize_summary(summary), summary)

    def test_long_summary_is_compressed_within_limit(self) -> None:
        long_summary = "\n".join(
            [
                "关键盲点是分不清 guard clause 和嵌套 if 的取舍，写条件时容易混淆边界。",
                "当前理解是已经知道可以先处理异常路径，再保留主流程，重复逻辑也能看出来。",
                "下一步聚焦是多做条件改写练习，优先把命名和返回路径写清楚。",
            ]
            * 20
        )

        normalized = normalize_summary(long_summary)

        self.assertLessEqual(len(normalized), SUMMARY_MAX_LENGTH)
        self.assertIn("关键盲点:", normalized)
        self.assertIn("当前理解:", normalized)
        self.assertIn("下一步聚焦:", normalized)

    def test_none_or_invalid_input_returns_safe_string(self) -> None:
        self.assertEqual(normalize_summary(None), "")

        class BrokenString:
            def __str__(self) -> str:
                raise RuntimeError("broken")

        self.assertEqual(normalize_summary(BrokenString()), "")

    def test_save_state_writes_normalized_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            long_summary = " ".join(["需要更多练习条件拆分。"] * 200)

            save_state(
                root,
                course_id="courses/logic",
                lesson_index=0,
                summary=long_summary,
            )

            payload = json.loads(state_path(root).read_text(encoding="utf-8"))
            self.assertLessEqual(len(payload["summary"]), SUMMARY_MAX_LENGTH)
            self.assertEqual(payload["summary"], normalize_summary(long_summary))


if __name__ == "__main__":
    unittest.main()
