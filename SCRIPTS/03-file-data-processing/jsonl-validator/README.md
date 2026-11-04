# JSON Lines validation (DATA-0001)

File: `SCRIPTS/03-file-data-processing/jsonl-validator/README.md`

Folder: `SCRIPTS/03-file-data-processing/jsonl-validator`


Read a file as UTF-8, validating one JSON value per line. Empty files are valid; blank lines, BOM, malformed JSON, invalid UTF-8 and NaN/Infinity constants are rejected. Stops at the first error with line number on stderr and exit 1; success exits 0. Duplicate object keys follow Python JSON behavior (last value wins). Physical lines are limited to 1 MiB by default, including LF/CRLF bytes. The reader requests at most the limit plus one byte and rejects an oversized line before decoding or parsing it. JSON parsing still requires additional memory proportional to the accepted line; a very large configured limit can exhaust memory. Numeric range follows Python JSON parsing; this is syntax validation, not schema or numeric-range validation.

## Requirements and setup

Python 3.10+ with standard-library modules only. No installation or third-party packages. Verified on Windows with Python 3.13.9 ; other versions and operating systems are unverified. Run commands from the repository root.

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

## Configurable line budget

```powershell
python SCRIPTS/03-file-data-processing/jsonl-validator/validate_jsonl.py EXAMPLES/sample.jsonl --max-line-bytes 4096
```

This prints `Valid: 2 lines`. The library accepts `validate(path, max_line_bytes=1048576)`. Limits must be integers from 1 through sys.maxsize - 1 (booleans rejected). Oversized lines and invalid limits produce exit 1; malformed CLI argument syntax produces exit 2. The byte budget includes newline bytes; a final unterminated line has no newline charge. Increase the limit explicitly for larger valid records. Default validation now rejects records larger than 1 MiB, a deliberate behavior change from the former unbounded reader.

Additional regression checks: [TESTS/test_script_improvements.py](../../../TESTS/test_script_improvements.py).
