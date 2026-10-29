"""Tests for deterministic specialist-result validation."""

import unittest

from self_evolving_ai.modules import ModuleResult
from self_evolving_ai.validation import validate_result


class ResultValidationTests(unittest.TestCase):
    def test_accepts_valid_success_result(self):
        result = ModuleResult("summary", "success", "요약 완료", {"summary": "내용"})
        self.assertEqual(validate_result(result, "summary"), [])

    def test_rejects_mismatched_module_name(self):
        result = ModuleResult("other", "success", "완료", {})
        self.assertIn("결과의 모듈 이름이 등록된 이름과 일치하지 않습니다.", validate_result(result, "summary"))

    def test_rejects_unknown_status(self):
        result = ModuleResult("summary", "pending", "대기", {})
        self.assertIn("결과 상태는 success 또는 error여야 합니다.", validate_result(result, "summary"))

    def test_rejects_empty_summary(self):
        result = ModuleResult("summary", "success", "  ", {})
        self.assertIn("결과 요약이 비어 있습니다.", validate_result(result, "summary"))

    def test_error_result_requires_diagnostics(self):
        result = ModuleResult("summary", "error", "실패", {})
        self.assertIn("오류 결과에는 최소한의 진단 정보가 필요합니다.", validate_result(result, "summary"))

    def test_rejects_non_module_result(self):
        self.assertTrue(validate_result({"status": "success"}, "summary"))


if __name__ == "__main__":
    unittest.main()
