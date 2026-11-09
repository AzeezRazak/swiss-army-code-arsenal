# Purpose: verify Sprint 0005 Python lessons, boundaries and documented CLI behavior.
# Location: TESTS/test_python_fundamentals3.py
# Input/output: synthetic values, temporary files and subprocesses to unittest results.
# Requirements: Python 3.10+, standard library only; no persistent data changes.
# Usage: python -m unittest discover -s TESTS -p "test_*.py" -v
# Limits: tests use the current interpreter and do not claim cross-platform coverage.
"""Acceptance tests for the third Python fundamentals set."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / "SCRIPTS/01-programming-languages/python-fundamentals-3"


def load(name):
    # Import a standalone lesson without invoking its guarded command-line entry point.
    spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    if name == "module_usage":
        # Make the sibling support module importable during a direct test-file import.
        sys.path.insert(0, str(BASE))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.pop(0)
    else:
        spec.loader.exec_module(module)
    return module


class FundamentalsThreeTests(unittest.TestCase):
    def test_nested_records(self):
        records = [{"name": "Ada", "profile": {"city": "London"}, "active": True, "tags": ["math"]}, {"name": "Lin", "profile": {"city": "London"}, "active": False, "tags": ["code", "math"]}]
        self.assertEqual(load("nested_records").summarize_records(records), {"count": 2, "active": 1, "cities": {"London": 2}, "tags": ["code", "math"]})

    def test_nested_records_rejects_bad_shape(self):
        with self.assertRaises(ValueError):
            load("nested_records").summarize_records([{"name": "Ada", "profile": {}, "active": True}])

    def test_generator_is_lazy_and_validates(self):
        result = load("generator_pipeline").even_squares(iter([-3, -2, 0, 3, 4]))
        self.assertEqual(list(result), [4, 0, 16])
        with self.assertRaises(ValueError):
            list(load("generator_pipeline").even_squares([2, True]))

    def test_text_file_summary_and_invalid_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            path.write_text("Ada learns\nPython well", encoding="utf-8")
            self.assertEqual(load("text_file_summary").summarize_file(path), {"bytes": 23, "lines": 2, "words": 4, "characters": 23})
            with self.assertRaises(ValueError):
                load("text_file_summary").summarize_file(Path(directory) / "missing.txt")

    def test_dataclass_tasks(self):
        tasks = load("dataclass_tasks").parse_tasks([{"title": " Learn ", "priority": 1}])
        self.assertEqual(tasks[0].title, "Learn")
        self.assertFalse(tasks[0].done)
        with self.assertRaises(ValueError):
            load("dataclass_tasks").parse_tasks([{"title": "x", "priority": 6}])

    def test_module_import(self):
        self.assertEqual(load("module_usage").greetings(" Ada ", 2), ["Hello, Ada!", "Hello, Ada!"])

    def test_documented_cli_examples(self):
        examples = [
            ("nested_records", ['[{"name":"Ada","profile":{"city":"London"},"active":true,"tags":["math"]}]'], {"count": 1, "active": 1, "cities": {"London": 1}, "tags": ["math"]}),
            ("generator_pipeline", ["-3", "-2", "0", "3", "4"], [4, 0, 16]),
            ("dataclass_tasks", ['[{"title":"Learn","priority":1}]'], [{"title": "Learn", "priority": 1, "done": False}]),
            ("module_usage", ["Ada", "--repeat", "2"], ["Hello, Ada!", "Hello, Ada!"]),
        ]
        for name, args, expected in examples:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(BASE / f"{name}.py"), *args], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)
                self.assertEqual(result.stderr, "")

    def test_cli_rejects_invalid_inputs(self):
        examples = [("nested_records", ["not-json"]), ("generator_pipeline", ["1.5"]), ("dataclass_tasks", ['[{"title":"x","priority":9}]']), ("module_usage", ["Ada", "--repeat", "0"])]
        for name, args in examples:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(BASE / f"{name}.py"), *args], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
