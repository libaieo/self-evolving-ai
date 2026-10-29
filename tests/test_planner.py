"""Unit tests for request analysis and task planning."""

import unittest

from self_evolving_ai.planner import analyze_request, create_plan


class RequestAnalysisTests(unittest.TestCase):
    def test_rejects_empty_request(self):
        with self.assertRaises(ValueError):
            analyze_request("   ")

    def test_extracts_language_and_source_constraints(self):
        result = analyze_request("한국어로 간단히 설명하고 출처를 포함해 주세요")
        self.assertIn("한국어로 결과를 제공", result.constraints)
        self.assertIn("간결하게 작성", result.constraints)
        self.assertIn("주요 주장에 근거 또는 출처를 포함", result.constraints)

    def test_marks_external_changes_for_confirmation(self):
        result = analyze_request("운영 서버에 배포해 주세요")
        self.assertTrue(result.requires_user_confirmation)
        self.assertEqual(result.risk_level, "high")

    def test_urgent_priority_is_detected(self):
        result = analyze_request("긴급: 오류 원인을 정리해 주세요")
        self.assertEqual(result.priority, "urgent")

    def test_plan_contains_steps_and_checklist(self):
        analysis = analyze_request("한국어로 간단히 오류를 설명해 주세요")
        plan = create_plan(analysis)
        self.assertGreaterEqual(len(plan.steps), 4)
        self.assertTrue(plan.completion_checklist)

    def test_short_request_is_flagged_as_ambiguous(self):
        result = analyze_request("도와줘")
        plan = create_plan(result)
        self.assertTrue(result.ambiguities)
        self.assertTrue(plan.needs_clarification)

    def test_english_word_containing_it_is_not_automatically_ambiguous(self):
        result = analyze_request("Write a concise explanation of the system architecture.")
        self.assertFalse(any("지시 대상" in item for item in result.ambiguities))


if __name__ == "__main__":
    unittest.main()
