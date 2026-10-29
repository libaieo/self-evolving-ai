"""Tests for the minimum command-line application."""

import contextlib
import io
import unittest

from self_evolving_ai import __version__
from self_evolving_ai.main import main


class MainTests(unittest.TestCase):
    def test_main_returns_success(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main()

        self.assertEqual(result, 0)

    def test_main_displays_version_and_scope(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main()

        text = output.getvalue()
        self.assertIn(__version__, text)
        self.assertIn("AI 추론 기능은 아직 포함하지 않습니다", text)


if __name__ == "__main__":
    unittest.main()
