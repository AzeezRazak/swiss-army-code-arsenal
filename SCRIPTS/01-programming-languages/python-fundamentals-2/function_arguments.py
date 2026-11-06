# Purpose: Format repeated greetings using defaults and keyword-style options.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-2/function_arguments.py
# Input/output: a name and options to a JSON list; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-2/function_arguments.py Ada --repeat 2 --punctuation '?'
# Limits: repeat must be an integer from 1 through 10; names and punctuation are small text values.
"""Functions: use defaults and explicit arguments to format greetings."""
import argparse
import json

MAX_NAME_LENGTH = 200


def greetings(name, repeat=1, punctuation="!"):
    """Return a validated list of repeated greetings."""
    if not isinstance(name, str) or not name.strip() or len(name) > MAX_NAME_LENGTH:
        raise ValueError("name must be nonempty and at most 200 characters")
    if isinstance(repeat, bool) or not isinstance(repeat, int) or not 1 <= repeat <= 10:
        raise ValueError("repeat must be an integer from 1 through 10")
    if not isinstance(punctuation, str) or len(punctuation) != 1 or punctuation.isspace():
        raise ValueError("punctuation must be one non-whitespace character")
    clean_name = name.strip()
    # The repeated expression demonstrates a default while preserving deterministic output.
    return [f"Hello, {clean_name}{punctuation}" for _ in range(repeat)]


def main():
    # Optional flags expose the function's default and custom keyword arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--punctuation", default="!")
    args = parser.parse_args()
    try:
        print(json.dumps(greetings(args.name, repeat=args.repeat, punctuation=args.punctuation), ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
