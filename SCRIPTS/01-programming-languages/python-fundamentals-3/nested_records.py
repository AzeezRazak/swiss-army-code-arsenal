# Purpose: Summarize validated records containing nested dictionaries and lists.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-3/nested_records.py
# Input/output: one JSON array argument to a JSON summary; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-3/nested_records.py "[{\"name\":\"Ada\",\"profile\":{\"city\":\"London\"},\"active\":true}]"
# Limits: at most 1,000 records and 100 tags per record; input remains in memory.
"""Teach nested dictionaries, list traversal and explicit validation."""
import argparse
import json

MAX_RECORDS = 1_000
MAX_TAGS = 100


def summarize_records(records):
    """Return record count, active count, city counts and sorted unique tags."""
    if not isinstance(records, list):
        raise ValueError("records must be a JSON array")
    if len(records) > MAX_RECORDS:
        raise ValueError(f"at most {MAX_RECORDS} records are supported")
    cities = {}
    tags = set()
    active_count = 0
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each record must be an object")
        name = record.get("name")
        profile = record.get("profile")
        city = profile.get("city") if isinstance(profile, dict) else None
        active = record.get("active")
        record_tags = record.get("tags", [])
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(city, str) or not city.strip():
            raise ValueError("profile.city must be a non-empty string")
        if not isinstance(active, bool):
            raise ValueError("active must be a boolean")
        if not isinstance(record_tags, list) or len(record_tags) > MAX_TAGS:
            raise ValueError(f"tags must be a list of at most {MAX_TAGS} strings")
        if any(not isinstance(tag, str) or not tag.strip() for tag in record_tags):
            raise ValueError("tags must contain non-empty strings")
        cities[city] = cities.get(city, 0) + 1
        tags.update(record_tags)
        active_count += active
    return {"count": len(records), "active": active_count, "cities": dict(sorted(cities.items())), "tags": sorted(tags)}


def main():
    # Decode one bounded JSON value so the lesson can focus on nested access.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records_json")
    args = parser.parse_args()
    try:
        print(json.dumps(summarize_records(json.loads(args.records_json)), ensure_ascii=True))
    except (ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
