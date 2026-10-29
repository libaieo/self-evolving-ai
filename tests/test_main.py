"""Tests for the command-line application."""

import contextlib
import io
import sys
import unittest
from unittest.mock import patch

from self_evolving_ai import __version__
from self_evolving_ai.main import main


class MainTests(unittest.TestCase):
    def test_main_returns_success(self):
        output = io.StringIO()
        with patch.object(sys, "argv", ["self-evolving-ai"]), contextlib.redirect_stdout(output):
            result = main()

        self.assertEqual(result, 0)

    def test_main_displays_version_and_scope(self):
        output = io.StringIO()
        with patch.object(sys, "argv", ["self-evolving-ai"]), contextlib.redirect_stdout(output):
            main()

        text = output.getvalue()
        self.assertIn(__version__, text)
        self.assertIn("AI 추론 기능은 아직 포함하지 않습니다", text)

    def test_run_summary_module_cli(self):
        output = io.StringIO()
        argv = ["self-evolving-ai", "--run", "summary", "--request", "hello world"]
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            result = main()

        self.assertEqual(result, 0)
        self.assertIn('"status": "success"', output.getvalue())

    def test_unknown_module_cli_returns_failure(self):
        output = io.StringIO()
        argv = ["self-evolving-ai", "--run", "unknown", "--request", "hello"]
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn('"status": "error"', output.getvalue())

    def test_list_modules_cli(self):
        output = io.StringIO()
        with patch.object(sys, "argv", ["self-evolving-ai", "--list-modules"]), contextlib.redirect_stdout(output):
            result = main()

        self.assertEqual(result, 0)
        self.assertIn('"summary"', output.getvalue())
        self.assertIn('"checklist"', output.getvalue())


if __name__ == "__main__":
    unittest.main()
