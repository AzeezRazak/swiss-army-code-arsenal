# Purpose: Replay saved HTTP observations through a deterministic local fixture adapter.
# Location: SCRIPTS/20-testing-quality/fixture-replay/replay_fixture.py
# Input/output: fixture JSON path to a JSON replay summary; no live network access.
# Requirements: Python 3.10+, standard library only; no detector plugins or arbitrary code execution.
# Usage from root: python SCRIPTS/20-testing-quality/fixture-replay/replay_fixture.py fixtures.json
# Limits: at most 1,000 observations and 64 KiB per body; only status/body-length comparisons are performed.
"""Replay serialized observations without contacting a server or executing code."""
import argparse
import hashlib
import json
from pathlib import Path

MAX_ITEMS = 1_000
MAX_BODY = 64 * 1024


def replay_fixture(path):
    """Summarize deterministic baseline/test differences from a local JSON fixture."""
    candidate = Path(path)
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError("fixture must be a regular non-symlink file")
    try:
        fixture = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("fixture must be readable UTF-8 JSON") from error
    observations = fixture.get("observations") if isinstance(fixture, dict) else None
    if not isinstance(observations, list) or len(observations) > MAX_ITEMS:
        raise ValueError(f"fixture observations must be a list of at most {MAX_ITEMS}")
    results = []
    for index, item in enumerate(observations, 1):
        if not isinstance(item, dict) or not isinstance(item.get("baseline"), dict) or not isinstance(item.get("test"), dict):
            raise ValueError(f"observation {index} must contain baseline and test objects")
        baseline = item["baseline"]
        test = item["test"]
        for response in (baseline, test):
            if not isinstance(response.get("status"), int) or not isinstance(response.get("body"), str) or len(response["body"].encode("utf-8")) > MAX_BODY:
                raise ValueError(f"observation {index} has an invalid or oversized response")
        results.append({"id": item.get("id", str(index)), "status_changed": baseline["status"] != test["status"], "length_changed": len(baseline["body"]) != len(test["body"]), "baseline_sha256": hashlib.sha256(baseline["body"].encode()).hexdigest(), "test_sha256": hashlib.sha256(test["body"].encode()).hexdigest()})
    return {"observations": len(results), "results": results}


def main():
    # Load only inert JSON data and compare it locally; no URL or code field is accepted.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        print(json.dumps(replay_fixture(args.path), ensure_ascii=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
