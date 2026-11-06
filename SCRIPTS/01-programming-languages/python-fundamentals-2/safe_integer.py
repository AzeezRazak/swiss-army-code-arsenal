# Purpose: Parse signed base-10 integer text with an explicit whitespace policy.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-2/safe_integer.py
# Input/output: one integer token to a JSON object; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-2/safe_integer.py ' -42 '
# Limits: surrounding whitespace is allowed; at most 1,000 decimal digits are accepted.
"""Exceptions: safely convert a signed base-10 string to an integer."""
import argparse
import json
import re

MAX_DIGITS = 1_000
INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_integer(text):
    """Parse a string after trimming surrounding whitespace, rejecting fractions."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    token = text.strip()
    if not token or not INTEGER_PATTERN.fullmatch(token):
        raise ValueError("expected a signed base-10 integer")
    digits = token[1:] if token[:1] in "+-" else token
    if len(digits) > MAX_DIGITS:
        raise ValueError(f"at most {MAX_DIGITS} digits are supported")
    try:
        return int(token, 10)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("integer conversion failed") from error


def main():
    # Keep the raw token as text so the reusable function controls whitespace and syntax.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text")
    args = parser.parse_args()
    try:
        print(json.dumps({"value": parse_integer(args.text)}))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
