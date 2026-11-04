# Purpose: Count even and odd integers and calculate their sum.
# Location: SCRIPTS/01-programming-languages/python-fundamentals/list_summary.py
# Input/output: command-line values to JSON; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals/list_summary.py 1 2 3 4
# Limits: educational example; see README.md for exact policies and resource limits.
"""Loops and lists: Count even and odd integers and calculate their sum."""
import argparse
import json

def summarize(numbers):
    """Return count, total, and parity counts for an iterable of integers."""
    # Start accumulators at zero so an empty list has well-defined results.
    count = total = even = odd = 0
    for number in numbers:
        # bool subclasses int in Python, so explicitly exclude it from this lesson.
        if not isinstance(number, int) or isinstance(number, bool):
            raise ValueError("all values must be integers, not booleans")
        count += 1
        total += number
        # A remainder of zero identifies even values, including negative evens.
        if number % 2 == 0:
            even += 1
        else:
            odd += 1
    return {"count": count, "sum": total, "even": even, "odd": odd}


def main():
    # Define arguments and validate their syntax before calling the lesson function.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", type=int)
    args = parser.parse_args()
    try:
        # JSON keeps successful output predictable for callers and tests.
        print(json.dumps(summarize(args.numbers), allow_nan=False, ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        # argparse prints a clear diagnostic to stderr and exits with status 2.
        parser.error(str(error))


# Imports expose the reusable function without executing the command-line interface.
if __name__ == "__main__":
    main()
