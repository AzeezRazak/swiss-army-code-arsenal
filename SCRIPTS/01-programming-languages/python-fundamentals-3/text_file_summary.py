# Purpose: Read a small UTF-8 text file and report deterministic line and word counts.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-3/text_file_summary.py
# Input/output: a regular file path to a JSON summary; invalid or unsafe paths exit 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-3/text_file_summary.py examples/notes.txt
# Limits: regular files only, no symlinks, and at most 1 MiB of UTF-8 bytes; never writes input.
"""Teach context-managed file reading, encoding errors and safe input limits."""
import argparse
import json
from pathlib import Path

MAX_BYTES = 1 * 1024 * 1024


def summarize_file(path):
    """Read a regular UTF-8 file and return byte, line, word and character counts."""
    candidate = Path(path)
    if candidate.is_symlink():
        raise ValueError("symbolic links are not accepted")
    if not candidate.is_file():
        raise ValueError("path must name a regular file")
    try:
        size = candidate.stat().st_size
        if size > MAX_BYTES:
            raise ValueError(f"files must be at most {MAX_BYTES} bytes")
        with candidate.open("r", encoding="utf-8", newline="") as handle:
            text = handle.read()
    except (OSError, UnicodeError) as error:
        raise ValueError(f"unable to read UTF-8 text: {error}") from error
    return {"bytes": size, "lines": len(text.splitlines()), "words": len(text.split()), "characters": len(text)}


def main():
    # Keep filesystem access inside the validated function and emit machine-readable output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        print(json.dumps(summarize_file(args.path), ensure_ascii=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
