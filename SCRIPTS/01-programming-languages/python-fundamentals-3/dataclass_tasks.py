# Purpose: Convert validated JSON task records into typed dataclass instances.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-3/dataclass_tasks.py
# Input/output: one JSON array argument to a normalized JSON array; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-3/dataclass_tasks.py "[{\"title\":\"Learn\",\"priority\":1}]"
# Limits: at most 1,000 tasks; titles are at most 200 characters and priorities are 1-5.
"""Teach dataclass construction, defaults and immutable-style serialization."""
import argparse
from dataclasses import asdict, dataclass
import json

MAX_TASKS = 1_000
MAX_TITLE_LENGTH = 200


@dataclass(frozen=True)
class Task:
    """A small validated task record with a default incomplete state."""

    title: str
    priority: int
    done: bool = False


def parse_tasks(records):
    """Build frozen Task objects from JSON-compatible dictionaries."""
    if not isinstance(records, list) or len(records) > MAX_TASKS:
        raise ValueError(f"records must be a list of at most {MAX_TASKS} items")
    tasks = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each task must be an object")
        title = record.get("title")
        priority = record.get("priority")
        done = record.get("done", False)
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= MAX_TITLE_LENGTH:
            raise ValueError(f"title must be 1-{MAX_TITLE_LENGTH} characters")
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 5:
            raise ValueError("priority must be an integer from 1 to 5")
        if not isinstance(done, bool):
            raise ValueError("done must be a boolean")
        tasks.append(Task(title=title.strip(), priority=priority, done=done))
    return tasks


def main():
    # Parse JSON into dataclasses, then use asdict for a predictable CLI representation.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records_json")
    args = parser.parse_args()
    try:
        tasks = parse_tasks(json.loads(args.records_json))
        print(json.dumps([asdict(task) for task in tasks], ensure_ascii=True))
    except (ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
