"""Read-only deterministic directory metadata inventory; never follows links."""
import argparse
import json
import os
from pathlib import Path
import stat
import sys


def is_link(info):
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def inventory(root):
    root = Path(root)
    info = root.lstat()
    if is_link(info) or not stat.S_ISDIR(info.st_mode):
        raise ValueError("root must be a real directory, not a link or reparse point")
    records, pending = [], [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                info = entry.stat(follow_symlinks=False)
                path = Path(entry.path)
                record = {"path": path.relative_to(root).as_posix()}
                if is_link(info):
                    record["type"] = "link"
                elif stat.S_ISDIR(info.st_mode):
                    record["type"] = "directory"
                    pending.append(path)
                elif stat.S_ISREG(info.st_mode):
                    record.update(type="file", size=info.st_size)
                else:
                    record["type"] = "other"
                records.append(record)
    return sorted(records, key=lambda row: row["path"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    args = parser.parse_args()
    try:
        result = inventory(args.root)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
