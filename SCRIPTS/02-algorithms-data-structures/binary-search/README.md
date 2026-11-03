# Binary search (ALG-0001)

Return the first index matching a target, or -1 when absent. The function requires an ascending random-access sequence with a total ordering. Unsorted input and NaN are outside its contract; incompatible comparisons raise TypeError. The integer CLI validates ascending order and exits 2 on bad input. Function: O(log n) time and O(1) extra space; CLI validation is O(n).

## Requirements and setup

Python 3.10+ with standard-library modules only (SQLite support required for the database example). No installation or third-party packages. Verified on Windows with Python 3.13.9 and SQLite 3.51.0; other versions and operating systems are unverified. Run commands from the repository root.

## Usage

```powershell
python SCRIPTS/02-algorithms-data-structures/binary-search/binary_search.py 2 1 2 2 3
```

Expected stdout:

```text
1
```

File utilities read inputs without modifying them. Data fixtures are synthetic. No credentials or network access are used. For library use, load the standalone module or add its directory to your import path.

## Verification

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

See [acceptance tests](../../../TESTS/test_utilities.py) and [sprint review](../../../TODO/SPRINT-0001/REVIEW.md).
