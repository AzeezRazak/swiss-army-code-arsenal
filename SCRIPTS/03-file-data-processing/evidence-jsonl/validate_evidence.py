# Purpose: Validate bounded, sanitized JSONL evidence records without changing the source file.
# Location: SCRIPTS/03-file-data-processing/evidence-jsonl/validate_evidence.py
# Input/output: JSONL path to a JSON validation summary; invalid records exit 2.
# Requirements: Python 3.10+, standard library only; no network or source mutation.
# Usage from root: python SCRIPTS/03-file-data-processing/evidence-jsonl/validate_evidence.py evidence.jsonl
# Limits: at most 10,000 lines and 64 KiB per line; sensitive field names are rejected.
"""Check evidence provenance and redaction markers for local research reports."""
import argparse
import json
from pathlib import Path

MAX_LINES = 10_000
MAX_LINE_BYTES = 64 * 1024
REQUIRED = {"run_id", "timestamp", "module", "summary", "redacted"}
SENSITIVE_NAMES = {"authorization", "cookie", "password", "secret", "token"}


def _contains_sensitive_key(value):
    # Walk only decoded data and reject key names that could retain credentials.
    if isinstance(value, dict):
        if any(name.lower() in SENSITIVE_NAMES for name in value):
            return True
        return any(_contains_sensitive_key(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_sensitive_key(child) for child in value)
    return False


def validate_file(path):
    """Validate each JSONL record and return counts without modifying the file."""
    candidate = Path(path)
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError("path must name a regular non-symlink file")
    valid = 0
    try:
        with candidate.open("rb") as handle:
            for number, raw in enumerate(handle, 1):
                if number > MAX_LINES:
                    raise ValueError(f"at most {MAX_LINES} lines are supported")
                if len(raw) > MAX_LINE_BYTES:
                    raise ValueError(f"line {number} exceeds {MAX_LINE_BYTES} bytes")
                try:
                    record = json.loads(raw.decode("utf-8"))
                except (UnicodeError, json.JSONDecodeError) as error:
                    raise ValueError(f"line {number} is not UTF-8 JSON") from error
                if not isinstance(record, dict) or not REQUIRED <= set(record):
                    raise ValueError(f"line {number} is missing required evidence fields")
                if record["redacted"] is not True or _contains_sensitive_key(record):
                    raise ValueError(f"line {number} is not safely redacted")
                valid += 1
    except OSError as error:
        raise ValueError(f"unable to read evidence: {error}") from error
    return {"valid": valid, "lines": valid}


def main():
    # Validate bytes incrementally to keep malformed or oversized evidence bounded.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        print(json.dumps(validate_file(args.path), ensure_ascii=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
