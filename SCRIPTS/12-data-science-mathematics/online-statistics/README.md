# Online statistics (MATH-0001)

Consume a numeric iterable once with Welford updates; return count, mean, population variance and sample variance. Empty and nonfinite inputs or overflowing intermediate arithmetic raise ValueError; invalid conversions can raise TypeError/ValueError/OverflowError. A singleton has population variance 0 and sample variance None (JSON null). CLI errors exit 2. Function uses O(n) time and O(1) state; CLI arguments are held in memory. Floating-point rounding remains possible, especially for large offsets; this is not arbitrary-precision statistics.

## Requirements and setup

Python 3.10+ with standard-library modules only (SQLite support required for the database example). No installation or third-party packages. Verified on Windows with Python 3.13.9 and SQLite 3.51.0; other versions and operating systems are unverified. Run commands from the repository root.

## Usage

```powershell
python SCRIPTS/12-data-science-mathematics/online-statistics/online_stats.py 1 2 3 4
```

Expected stdout:

```text
{"count": 4, "mean": 2.5, "population_variance": 1.25, "sample_variance": 1.6666666666666667}
```

File utilities read inputs without modifying them. Data fixtures are synthetic. No credentials or network access are used. For library use, load the standalone module or add its directory to your import path.

## Verification

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

See [acceptance tests](../../../TESTS/test_utilities.py) and [sprint review](../../../TODO/SPRINT-0001/REVIEW.md).
