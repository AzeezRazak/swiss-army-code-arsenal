# Purpose: Validate exact, deny-by-default scope records for security research fixtures.
# Location: SCRIPTS/08-cybersecurity/scope-allowlist/validate_scope.py
# Input/output: one JSON scope object to normalized JSON; invalid scope exits 2.
# Requirements: Python 3.10+, standard library only; no network or target access.
# Usage from root: python SCRIPTS/08-cybersecurity/scope-allowlist/validate_scope.py "{\"hosts\":[\"app.test\"],\"paths\":[\"/api\"]}"
# Limits: at most 100 exact hosts, paths and callbacks; wildcards and credentials are rejected.
"""Validate explicit security-testing scope without contacting any target."""
import argparse
import json
from urllib.parse import urlparse

MAX_ITEMS = 100


def _strings(value, field):
    # Require bounded lists of non-empty strings so scope cannot silently broaden.
    if not isinstance(value, list) or len(value) > MAX_ITEMS:
        raise ValueError(f"{field} must be a list of at most {MAX_ITEMS} strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{field} must contain non-empty strings")
    return sorted(set(item.strip() for item in value))


def validate_scope(scope):
    """Return normalized exact scope, rejecting wildcard or credential-bearing values."""
    if not isinstance(scope, dict):
        raise ValueError("scope must be an object")
    result = {}
    for field in ("hosts", "paths", "callbacks"):
        values = _strings(scope.get(field, []), field)
        if any("*" in value or "?" in value for value in values):
            raise ValueError(f"{field} cannot contain wildcards")
        result[field] = values
    for callback in result["callbacks"]:
        parsed = urlparse(callback)
        if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password or not parsed.netloc:
            raise ValueError("callbacks must be credential-free HTTP(S) URLs")
    unknown = set(scope) - {"hosts", "paths", "callbacks"}
    if unknown:
        raise ValueError(f"unknown scope fields: {sorted(unknown)}")
    if not any(result.values()):
        raise ValueError("scope must contain at least one exact host, path or callback")
    return result


def main():
    # Parse only data and print the validated policy; this utility never opens a socket.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scope_json")
    args = parser.parse_args()
    try:
        print(json.dumps(validate_scope(json.loads(args.scope_json)), ensure_ascii=True))
    except (ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
