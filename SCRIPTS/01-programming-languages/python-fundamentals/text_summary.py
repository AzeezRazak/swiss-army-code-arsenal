# Purpose: Count characters, whitespace-separated words and alphabetic characters.
# Location: SCRIPTS/01-programming-languages/python-fundamentals/text_summary.py
# Input/output: command-line values to JSON; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals/text_summary.py "Hello Python"
# Limits: educational example; see README.md for exact policies and resource limits.
"""Strings: Count characters, whitespace-separated words and alphabetic characters."""
import argparse
import json

def summarize(text):
    """Count Python characters, whitespace tokens, and Unicode letters."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    # split() collapses repeated whitespace; empty input produces no words.
    words = text.split()
    letters = 0
    for character in text:
        # isalpha recognizes Unicode letters; punctuation and digits do not count.
        if character.isalpha():
            letters += 1
    # len counts Unicode code points, not user-perceived grapheme clusters.
    return {"characters": len(text), "words": len(words), "letters": letters}


def main():
    # Define arguments and validate their syntax before calling the lesson function.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text")
    args = parser.parse_args()
    try:
        # JSON keeps successful output predictable for callers and tests.
        print(json.dumps(summarize(args.text), allow_nan=False, ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        # argparse prints a clear diagnostic to stderr and exits with status 2.
        parser.error(str(error))


# Imports expose the reusable function without executing the command-line interface.
if __name__ == "__main__":
    main()
