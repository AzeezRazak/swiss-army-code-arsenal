# SQLite transactions (DB-0001)

File: `SCRIPTS/07-databases-storage/sqlite-transactions/README.md`

Folder: `SCRIPTS/07-databases-storage/sqlite-transactions`


Create a fresh temporary file-backed database, commit alpha and beta, then attempt gamma followed by duplicate alpha. The unique constraint rejects the second batch and rolls back gamma. Print surviving labels as JSON and clean up the database. insert_batch requires an idle connection in legacy transaction mode with isolation_level enabled; incompatible modes raise ValueError, constraints raise sqlite3.IntegrityError. Uses parameterized SQL and closes connections before cleanup. This teaching example does not model concurrent writers, crash recovery or migrations. Unexpected filesystem/database failures propagate with nonzero exit.

## Requirements and setup

Python 3.10+ with standard-library modules only (SQLite support required for the database example). No installation or third-party packages. Verified on Windows with Python 3.13.9 and SQLite 3.51.0; other versions and operating systems are unverified. Run commands from the repository root.

## Usage

```powershell
python SCRIPTS/07-databases-storage/sqlite-transactions/transactions.py
```

Expected stdout:

```text
["alpha", "beta"]
```

File utilities read inputs without modifying them. Data fixtures are synthetic. No credentials or network access are used. For library use, load the standalone module or add its directory to your import path.

## Verification

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

See [acceptance tests](../../../TESTS/test_utilities.py) and [sprint review](../../../TODO/SPRINT-0001/REVIEW.md).
