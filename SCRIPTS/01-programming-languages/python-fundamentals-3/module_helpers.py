# Purpose: Provide a reusable greeting formatter for the module import lesson.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-3/module_helpers.py
# Input/output: a validated name to one greeting string; no filesystem or network effects.
# Requirements: Python 3.10+, standard library only; imported by module_usage.py.
# Usage from root: imported by `python SCRIPTS/01-programming-languages/python-fundamentals-3/module_usage.py Ada`.
# Limits: callers are responsible for the name length and whitespace policy.
"""Small support module kept separate to demonstrate imports."""


def format_greeting(name):
    """Return one deterministic greeting for a non-empty name."""
    return f"Hello, {name}!"
