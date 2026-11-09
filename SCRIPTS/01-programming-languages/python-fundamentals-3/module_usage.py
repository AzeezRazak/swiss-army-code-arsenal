# Purpose: Use a local helper module to format bounded greeting messages.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-3/module_usage.py
# Input/output: name and optional repeat count to a JSON list; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; run from any directory.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-3/module_usage.py Ada --repeat 2
# Limits: names are trimmed and limited to 80 characters; repeat count is 1-10.
"""Teach importing a sibling module and keeping reusable logic separate."""
import argparse
import json

from module_helpers import format_greeting


def greetings(name, repeat=1):
    """Return repeated greetings using the imported formatter."""
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 80:
        raise ValueError("name must be 1-80 non-whitespace characters")
    if isinstance(repeat, bool) or not isinstance(repeat, int) or not 1 <= repeat <= 10:
        raise ValueError("repeat must be an integer from 1 to 10")
    return [format_greeting(name.strip()) for _ in range(repeat)]


def main():
    # Keep command-line parsing here while the reusable string formatting lives in the module.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args()
    try:
        print(json.dumps(greetings(args.name, args.repeat), ensure_ascii=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
