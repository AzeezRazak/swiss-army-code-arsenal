# Purpose: Count whitespace-separated words after case folding.
# Location: SCRIPTS/01-programming-languages/python-fundamentals/word_counts.py
# Input/output: command-line values to JSON; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals/word_counts.py "Python python code"
# Limits: educational example; see README.md for exact policies and resource limits.
"""Dictionaries: Count whitespace-separated words after case folding."""
import argparse
import json

def count_words(text):
    """Return a sorted dictionary of case-folded whitespace-token counts."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    counts = {}
    # Case folding allows caseless matching; punctuation deliberately stays attached.
    for word in text.casefold().split():
        # get supplies zero for a new key so both first and repeated words use one update.
        counts[word] = counts.get(word, 0) + 1
    # Sort keys to make output independent of first-occurrence order.
    return dict(sorted(counts.items()))


def main():
    # Define arguments and validate their syntax before calling the lesson function.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text")
    args = parser.parse_args()
    try:
        # JSON keeps successful output predictable for callers and tests.
        print(json.dumps(count_words(args.text), allow_nan=False, ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        # argparse prints a clear diagnostic to stderr and exits with status 2.
        parser.error(str(error))


# Imports expose the reusable function without executing the command-line interface.
if __name__ == "__main__":
    main()
