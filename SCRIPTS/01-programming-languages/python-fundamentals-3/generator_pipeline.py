# Purpose: Generate squares for even integers without building an intermediate list.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-3/generator_pipeline.py
# Input/output: integer arguments to a JSON list; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-3/generator_pipeline.py -3 -2 0 3 4
# Limits: at most 100,000 integers; output is materialized only by the CLI.
"""Teach generator functions and lazy filtering of a finite input."""
import argparse
import json

MAX_ITEMS = 100_000


def even_squares(values):
    """Yield squares of even integer values in their original order."""
    try:
        iterator = iter(values)
    except TypeError as error:
        raise ValueError("values must be iterable") from error
    for index, value in enumerate(iterator):
        if index >= MAX_ITEMS:
            raise ValueError(f"at most {MAX_ITEMS} values are supported")
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("all values must be integers")
        if value % 2 == 0:
            yield value * value


def main():
    # Parse integers before handing them to the generator so argparse reports bad tokens.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("values", nargs="*", type=int)
    args = parser.parse_args()
    try:
        print(json.dumps(list(even_squares(args.values))))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
