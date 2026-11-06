# Purpose: Remove repeated string tokens while retaining first-occurrence order.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-2/unique_items.py
# Input/output: string arguments to a JSON list; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-2/unique_items.py red blue red
# Limits: at most 100,000 tokens; tokens must be strings and remain in memory.
"""Sets: deduplicate string tokens without changing their first-seen order."""
import argparse
import json

MAX_ITEMS = 100_000


def unique(items):
    """Return first-occurrence string values without mutating the input."""
    try:
        values = list(items)
    except TypeError as error:
        raise ValueError("items must be iterable") from error
    if len(values) > MAX_ITEMS:
        raise ValueError(f"at most {MAX_ITEMS} items are supported")
    result = []
    seen = set()
    for item in values:
        if not isinstance(item, str):
            raise ValueError("all items must be strings")
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def main():
    # Parse tokens as strings so Unicode and repeated values reach the lesson unchanged.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("items", nargs="*")
    args = parser.parse_args()
    try:
        print(json.dumps(unique(args.items), ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
