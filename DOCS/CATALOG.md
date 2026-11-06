# Catalog

File: `DOCS/CATALOG.md`

Folder: `DOCS`


Seventeen utility and teaching implementations across eight domains, with eighteen runnable Python scripts and a SQL schema. Latest verification: Windows/Python 3.13.9 on 2026-11-06; 63 tests passed, zero failed, one existing symlink integration skip (QA-0003). Each implementation documents usage and limitations. No cross-platform verification or benchmark claims.

| ID | Implementation | Language | Verification |
|---|---|---|---|
| ALG-0001 | [Binary search](../SCRIPTS/02-algorithms-data-structures/binary-search/README.md) | Python | Passed locally |
| DATA-0001 | [JSON Lines validation](../SCRIPTS/03-file-data-processing/jsonl-validator/README.md) | Python | Passed locally |
| SEC-0001 | [SHA-256 file digest](../SCRIPTS/08-cybersecurity/sha256-file/README.md) | Python | Passed locally |
| DB-0001 | [SQLite transactions](../SCRIPTS/07-databases-storage/sqlite-transactions/README.md) | Python, SQL | Passed locally |
| MATH-0001 | [Online statistics](../SCRIPTS/12-data-science-mathematics/online-statistics/README.md) | Python | Passed locally |

Test command: `python -m unittest discover -s TESTS -p "test_*.py" -v`. See [review](../TODO/SPRINT-0001/REVIEW.md) for results and limitations. Completed sprints: 3. Open backlog tasks: 29. Known unresolved implementation defects: 0. Two prior actions applied with Sprint 0002 evidence; long-term effectiveness remains under review.

| New item | Usage and limitations | Runnable scripts |
|---|---|---|
| NET-0002 | [Loopback TCP](../SCRIPTS/05-networking-protocols/loopback-tcp/README.md) | 2 |
| AUTO-0002 | [Directory inventory](../SCRIPTS/09-automation-scripting/directory-inventory/README.md) | 1 |

[Latest review](../TODO/SPRINT-0002/REVIEW.md). Total runnable scripts before Sprint 0004: 13. Symlink verification gap: QA-0003.

## Sprint 0003 - individual beginner scripts

Folder: `SCRIPTS/01-programming-languages/python-fundamentals/`. Python; verified on Windows/Python 3.13.9 on 2026-11-05.

| ID | Script | Basic description | Usage arguments | Status |
|---|---|---|---|---|
| PY-0001 | [temperature.py](../SCRIPTS/01-programming-languages/python-fundamentals/temperature.py) | Variables, float conversion and arithmetic | `0` | Passed |
| PY-0002 | [grade.py](../SCRIPTS/01-programming-languages/python-fundamentals/grade.py) | if/elif/else and validation | `85` | Passed |
| PY-0003 | [list_summary.py](../SCRIPTS/01-programming-languages/python-fundamentals/list_summary.py) | Lists, for loops, accumulators and modulo | `1 2 3 4` | Passed |
| PY-0004 | [text_summary.py](../SCRIPTS/01-programming-languages/python-fundamentals/text_summary.py) | Strings, split, len and Unicode letters | `"Hello Python"` | Passed |
| PY-0005 | [word_counts.py](../SCRIPTS/01-programming-languages/python-fundamentals/word_counts.py) | Dictionary get, updates and sorted keys | `"Python python code"` | Passed |

Run with `python` and the linked file path from the repository root. [Guide](../SCRIPTS/01-programming-languages/python-fundamentals/README.md). Current totals: 13 runnable scripts, 12 utility implementations, 8 domains, 3 completed sprints. Latest tests: 43 passed, 0 failed, 1 skipped (QA-0003).

## Sprint 0004 - second Python fundamentals set

Folder: `SCRIPTS/01-programming-languages/python-fundamentals-2/`. Python; verified on Windows/Python 3.13.9 on 2026-11-06.

| ID | Script | Basic description | Status |
|---|---|---|---|
| PY-0006 | [unique_items.py](../SCRIPTS/01-programming-languages/python-fundamentals-2/unique_items.py) | Sets and order-preserving deduplication | Passed |
| PY-0007 | [tuple_coordinates.py](../SCRIPTS/01-programming-languages/python-fundamentals-2/tuple_coordinates.py) | Tuples and coordinate unpacking | Passed |
| PY-0008 | [function_arguments.py](../SCRIPTS/01-programming-languages/python-fundamentals-2/function_arguments.py) | Defaults and keyword arguments | Passed |
| PY-0009 | [safe_integer.py](../SCRIPTS/01-programming-languages/python-fundamentals-2/safe_integer.py) | Exceptions and integer conversion | Passed |
| PY-0010 | [list_comprehensions.py](../SCRIPTS/01-programming-languages/python-fundamentals-2/list_comprehensions.py) | Filtering and transforming lists | Passed |

Run with `python` and the linked file path from the repository root. [Guide](../SCRIPTS/01-programming-languages/python-fundamentals-2/README.md). Current totals: 18 runnable scripts, 17 utility and teaching implementations, 8 domains, 4 completed sprints. Latest tests: 63 passed, 0 failed, 1 skipped (QA-0003).

## Integrated maintenance improvements

Merged from `improve/jsonl-and-sha256` into `main` by owner authorization: DATA-0001 adds `--max-line-bytes` (default 1 MiB including newline); SEC-0001 adds `--check SHA256`. See their linked guides above and [maintenance record](../TODO/IMPROVEMENTS-0001.md). Latest branch suite: 52 passed, zero failed, one existing symlink skip (53 tests). No new runnable scripts.
