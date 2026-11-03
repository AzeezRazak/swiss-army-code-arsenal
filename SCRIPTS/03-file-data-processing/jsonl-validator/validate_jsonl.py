"""Validate UTF-8 JSON Lines without modifying the input."""
import argparse
import json
import sys


def reject_constant(value):
    raise ValueError(f"non-JSON constant: {value}")


def validate(path):
    """Return line count or raise ValueError with the first failing line."""
    count = 0
    with open(path, "rb") as source:
        for count, raw in enumerate(source, 1):
            try:
                json.loads(raw.decode("utf-8"), parse_constant=reject_constant)
            except (UnicodeDecodeError, ValueError, RecursionError) as error:
                raise ValueError(f"line {count}: {error}") from error
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        print(f"Valid: {validate(args.path)} lines")
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
