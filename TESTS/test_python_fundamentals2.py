# Purpose: verify Sprint 0004 Python lessons and their documented CLI behavior.
# Location: TESTS/test_python_fundamentals2.py
# Input/output: synthetic values and subprocesses to unittest results; no persistent data changes.
# Requirements: Python 3.10+, standard library only.
# Usage: python -m unittest discover -s TESTS -p "test_*.py" -v
# Limits: subprocesses use the current interpreter; other runtimes are unverified.
"""Boundary, policy and CLI tests for the second Python fundamentals set."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

BASE = Path(__file__).resolve().parents[1] / "SCRIPTS/01-programming-languages/python-fundamentals-2"


def load(name):
    # Import each standalone lesson without executing its guarded command-line entry point.
    spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FundamentalsTwoTests(unittest.TestCase):
    def test_unique_items_order_unicode_and_nonmutation(self):
        values = ["café", "a", "café", "雪", "a"]
        before = values.copy()
        self.assertEqual(load("unique_items").unique(values), ["café", "a", "雪"])
        self.assertEqual(values, before)
        self.assertEqual(load("unique_items").unique([]), [])

    def test_unique_items_invalid(self):
        with self.assertRaises(ValueError):
            load("unique_items").unique(["ok", 2])

    def test_tuple_coordinates(self):
        result = load("tuple_coordinates").measure((0, 0), (3, 4))
        self.assertEqual(result["midpoint"], [1.5, 2.0])
        self.assertEqual(result["distance"], 5.0)

    def test_tuple_coordinates_invalid(self):
        measure = load("tuple_coordinates").measure
        for first, second in [((0,), (1, 2)), ((0, 0, 1), (1, 2)), ((float("nan"), 0), (1, 2)), ((True, 0), (1, 2))]:
            with self.subTest(first=first), self.assertRaises(ValueError):
                measure(first, second)

    def test_function_defaults_and_custom_arguments(self):
        greetings = load("function_arguments").greetings
        self.assertEqual(greetings("Ada"), ["Hello, Ada!"])
        self.assertEqual(greetings(" Ada ", repeat=2, punctuation="?"), ["Hello, Ada?", "Hello, Ada?"])

    def test_function_arguments_invalid(self):
        greetings = load("function_arguments").greetings
        for kwargs in [{"repeat": 0}, {"repeat": 11}, {"punctuation": "  "}, {"name": ""}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                greetings(kwargs.pop("name", "Ada"), **kwargs)

    def test_safe_integer_policy(self):
        parse = load("safe_integer").parse_integer
        self.assertEqual(parse("  -42 "), -42)
        self.assertEqual(parse("+0007"), 7)
        for value in ["", "1.0", "1 2", "abc", "--1"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse(value)

    def test_list_comprehension_cases_and_nonmutation(self):
        values = [-3, -2, 0, 3, 4, 4]
        before = values.copy()
        self.assertEqual(load("list_comprehensions").square_even(values), [4, 0, 16, 16])
        self.assertEqual(values, before)
        self.assertEqual(load("list_comprehensions").square_even([]), [])
        with self.assertRaises(ValueError):
            load("list_comprehensions").square_even([2, True])

    def test_documented_cli_examples(self):
        examples = [
            ("unique_items", ["red", "blue", "red"], ["red", "blue"]),
            ("tuple_coordinates", ["0", "0", "3", "4"], {"distance": 5.0, "midpoint": [1.5, 2.0]}),
            ("function_arguments", ["Ada", "--repeat", "2", "--punctuation", "?"], ["Hello, Ada?", "Hello, Ada?"]),
            ("safe_integer", ["-42"], {"value": -42}),
            ("list_comprehensions", ["-3", "-2", "0", "3", "4"], [4, 0, 16]),
        ]
        for name, args, expected in examples:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(BASE / f"{name}.py"), *args], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)
                self.assertEqual(result.stderr, "")

    def test_cli_rejects_invalid_inputs(self):
        examples = [("tuple_coordinates", ["0", "0"]), ("function_arguments", ["Ada", "--repeat", "0"]), ("safe_integer", ["1.5"]), ("list_comprehensions", ["1.5"])]
        for name, args in examples:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(BASE / f"{name}.py"), *args], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
