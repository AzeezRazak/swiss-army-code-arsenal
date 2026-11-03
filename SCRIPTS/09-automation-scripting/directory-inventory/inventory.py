# ========================================================================
# Purpose: List directory metadata without reading file contents.
# Location: SCRIPTS/09-automation-scripting/directory-inventory/inventory.py
# Input/output: Real directory root; outputs sorted JSON records of descendants.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/09-automation-scripting/directory-inventory/inventory.py EXAMPLES
# Limitations: Links are not intentionally traversed; concurrent path replacement is not prevented.
# ========================================================================
"""Read-only deterministic directory metadata inventory; never follows links."""
import argparse
import json
import os
from pathlib import Path
import stat
import sys


def is_link(info):
    # Recognize POSIX symlinks and Windows FILE_ATTRIBUTE_REPARSE_POINT.
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def inventory(root):
    root = Path(root)
    # Inspect the root itself rather than following a root symlink.
    info = root.lstat()
    if is_link(info) or not stat.S_ISDIR(info.st_mode):
        raise ValueError("root must be a real directory, not a link or reparse point")
    # Use an explicit directory stack instead of recursive Python calls.
    records, pending = [], [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                # Classify the entry itself so links are not queued for traversal.
                info = entry.stat(follow_symlinks=False)
                path = Path(entry.path)
                # Emit portable relative paths without exposing the absolute root.
                record = {"path": path.relative_to(root).as_posix()}
                if is_link(info):
                    record["type"] = "link"
                elif stat.S_ISDIR(info.st_mode):
                    record["type"] = "directory"
                    # Only real directories enter the traversal stack.
                    pending.append(path)
                elif stat.S_ISREG(info.st_mode):
                    # Read size from metadata; do not open the file contents.
                    record.update(type="file", size=info.st_size)
                else:
                    record["type"] = "other"
                records.append(record)
    # Remove filesystem enumeration-order differences from the output.
    return sorted(records, key=lambda row: row["path"])


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        # Complete enumeration before printing to avoid partial success JSON.
        result = inventory(args.root)
        # Escape Unicode for consoles that cannot display every filename.
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError) as error:
        # Keep diagnostics off stdout so successful output stays machine-readable.
        print(f"error: {error}", file=sys.stderr)
        return 1


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())
