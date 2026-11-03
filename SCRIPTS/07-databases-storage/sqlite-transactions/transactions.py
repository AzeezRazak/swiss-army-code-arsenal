# ========================================================================
# Purpose: Demonstrate successful commit and atomic rollback in SQLite.
# Location: SCRIPTS/07-databases-storage/sqlite-transactions/transactions.py
# Input/output: Synthetic labels in a temporary database; outputs surviving labels as JSON.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/07-databases-storage/sqlite-transactions/transactions.py
# Limitations: Requires standard-library sqlite3; teaching example without concurrent writers.
# ========================================================================
"""Demonstrate commit and rollback in a temporary SQLite database."""
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory


def insert_batch(connection, labels):
    """Insert one atomic batch on an idle, non-autocommit connection.

    The caller owns the connection; an existing transaction is rejected.
    """
    # Avoid taking ownership of an existing transaction or using autocommit.
    if connection.in_transaction or connection.isolation_level is None:
        raise ValueError("requires an idle connection with transactions enabled")
    # Require legacy transaction semantics, including Python 3.12+ connections.
    if getattr(connection, "autocommit", -1) != -1:
        raise ValueError("requires legacy transaction control")
    # Commit the whole batch on success, or roll it back on an exception.
    with connection:
        # Bind each label as data rather than interpolating it into SQL.
        connection.executemany("INSERT INTO entries(label) VALUES (?)", ((x,) for x in labels))


def demonstrate():
    # Isolate the demonstration database and remove it after the connection closes.
    with TemporaryDirectory(prefix="arsenal-sqlite-") as directory:
        connection = sqlite3.connect(Path(directory) / "demo.db")
        try:
            connection.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))
            insert_batch(connection, ["alpha", "beta"])
            try:
                # The duplicate alpha forces gamma and the duplicate to roll back together.
                insert_batch(connection, ["gamma", "alpha"])
            # This expected constraint failure demonstrates rollback, not a retry.
            except sqlite3.IntegrityError:
                pass
            return [row[0] for row in connection.execute("SELECT label FROM entries ORDER BY id")]
        finally:
            # Release the database handle before temporary-directory cleanup.
            connection.close()


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    print(json.dumps(demonstrate()))
