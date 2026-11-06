# Purpose: Filter even integers and transform them into their squares.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-2/list_comprehensions.py
# Input/output: integer arguments to a JSON list; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-2/list_comprehensions.py -3 -2 0 3 4
# Limits: at most 100,000 integers; output remains in memory and preserves input order.
"""List comprehensions: filter even integers and square the retained values."""
import argparse
import json

MAX_ITEMS = 100_000


def square_even(numbers):
    """Return squares for integer values divisible by two, without mutating input."""
    try:
        values = list(numbers)
    except TypeError as error:
        raise ValueError("numbers must be iterable") from error
    if len(values) > MAX_ITEMS:
        raise ValueError(f"at most {MAX_ITEMS} numbers are supported")
    if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
        raise ValueError("all values must be integers, not booleans")
    # The condition filters before the expression transforms each retained integer.
    return [value * value for value in values if value % 2 == 0]


def main():
    # argparse handles the documented integer-only CLI syntax and reports malformed tokens.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", type=int)
    args = parser.parse_args()
    try:
        print(json.dumps(square_even(args.numbers)))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
