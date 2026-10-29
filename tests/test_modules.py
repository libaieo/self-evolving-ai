"""Tests for specialist module registration, dispatch, and failures."""

import unittest

from self_evolving_ai.dispatcher import dispatch
from self_evolving_ai.modules import ModuleResult
from self_evolving_ai.registry import ModuleNotFoundError, ModuleRegistry, create_default_registry
from self_evolving_ai.specialist_modules import ChecklistModule, SummaryModule


class ModuleRegistryTests(unittest.TestCase):
    def test_default_registry_has_two_specialists(self):
        registry = create_default_registry()
        self.assertEqual({item["name"] for item in registry.list_modules()}, {"summary", "checklist"})

    def test_duplicate_registration_is_rejected(self):
        registry = ModuleRegistry()
        registry.register(SummaryModule())
        with self.assertRaises(ValueError):
            registry.register(SummaryModule())

    def test_unknown_task_raises_from_registry(self):
        with self.assertRaises(ModuleNotFoundError):
            create_default_registry().resolve("unknown-task")

    def test_summary_module_runs(self):
        result = dispatch("summary", "This is a sample request.")
        self.assertEqual(result.status, "success")
        self.assertEqual(result.module_name, "summary")
        self.assertIn("summary", result.data)

    def test_checklist_module_runs_by_korean_alias(self):
        result = dispatch("계획", "책상 정리")
        self.assertEqual(result.status, "success")
        self.assertEqual(result.module_name, "checklist")
        self.assertEqual(len(result.data["items"]), 4)

    def test_unknown_dispatch_returns_error_result(self):
        result = dispatch("not-a-module", "hello")
        self.assertEqual(result.status, "error")
        self.assertEqual(result.data["requested_task"], "not-a-module")

    def test_module_exception_is_converted_to_error(self):
        class BrokenModule:
            name = "broken"
            description = "test module"
            supported_tasks = ("broken",)

            def run(self, request: str) -> ModuleResult:
                raise RuntimeError("intentional test failure")

        registry = ModuleRegistry()
        registry.register(BrokenModule())
        result = dispatch("broken", "test", registry)
        self.assertEqual(result.status, "error")
        self.assertEqual(result.data["error_type"], "RuntimeError")


if __name__ == "__main__":
    unittest.main()
