# JSON Lines validation (DATA-0001)

File: `SCRIPTS/03-file-data-processing/jsonl-validator/README.md`

Folder: `SCRIPTS/03-file-data-processing/jsonl-validator`


Read a file as UTF-8, validating one JSON value per line. Empty files are valid; blank lines, BOM, malformed JSON, invalid UTF-8 and NaN/Infinity constants are rejected. Stops at the first error with line number on stderr and exit 1; success exits 0. Duplicate object keys follow Python JSON behavior (last value wins). Memory scales with the longest line, not total file size; no fixed line-size limit. Extremely large or hostile lines may exhaust memory; use only appropriately sized inputs. Numeric range follows Python JSON parsing; this is syntax validation, not schema or numeric-range validation.

## Requirements and setup

Python 3.10+ with standard-library modules only (SQLite support required for the database example). No installation or third-party packages. Verified on Windows with Python 3.13.9 and SQLite 3.51.0; other versions and operating systems are unverified. Run commands from the repository root.

## Usage

```powershell
python SCRIPTS/03-file-data-processing/jsonl-validator/validate_jsonl.py EXAMPLES/sample.jsonl
```

Expected stdout:

```text
Valid: 2 lines
```

File utilities read inputs without modifying them. Data fixtures are synthetic. No credentials or network access are used. For library use, load the standalone module or add its directory to your import path.

## Verification

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

See [acceptance tests](../../../TESTS/test_utilities.py) and [sprint review](../../../TODO/SPRINT-0001/REVIEW.md).
