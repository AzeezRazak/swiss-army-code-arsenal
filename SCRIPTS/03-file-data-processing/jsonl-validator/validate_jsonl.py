# ========================================================================
# Purpose: Validate each UTF-8 JSON Lines record without changing its file.
# Location: SCRIPTS/03-file-data-processing/jsonl-validator/validate_jsonl.py
# Input/output: File path; outputs valid line count or first failing line.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/03-file-data-processing/jsonl-validator/validate_jsonl.py EXAMPLES/sample.jsonl
# Limitations: Memory depends on longest line; syntax validation only.
# ========================================================================
"""Validate UTF-8 JSON Lines without modifying the input."""
import argparse
import json
import sys


def reject_constant(value):
    # Python accepts these constants by default, but JSON syntax does not.
    raise ValueError(f"non-JSON constant: {value}")


def validate(path):
    """Return line count or raise ValueError with the first failing line."""
    # An empty file has zero records and is considered valid.
    count = 0
    with open(path, "rb") as source:
        # Decode each physical line separately so encoding errors retain line numbers.
        for count, raw in enumerate(source, 1):
            try:
                # Reject invalid UTF-8 and nonstandard NaN/Infinity JSON constants.
                json.loads(raw.decode("utf-8"), parse_constant=reject_constant)
            except (UnicodeDecodeError, ValueError, RecursionError) as error:
                # Attach the one-based line number while preserving the original cause.
                raise ValueError(f"line {count}: {error}") from error
    return count


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        print(f"Valid: {validate(args.path)} lines")
    except (OSError, ValueError) as error:
        # Keep diagnostics off stdout so successful output stays machine-readable.
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())
