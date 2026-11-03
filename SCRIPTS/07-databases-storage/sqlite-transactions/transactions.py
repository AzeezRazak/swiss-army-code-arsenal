"""Demonstrate commit and rollback in a temporary SQLite database."""
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory


def insert_batch(connection, labels):
    """Insert one atomic batch on an idle, non-autocommit connection.

    The caller owns the connection; an existing transaction is rejected.
    """
    if connection.in_transaction or connection.isolation_level is None:
        raise ValueError("requires an idle connection with transactions enabled")
    if getattr(connection, "autocommit", -1) != -1:
        raise ValueError("requires legacy transaction control")
    with connection:
        connection.executemany("INSERT INTO entries(label) VALUES (?)", ((x,) for x in labels))


def demonstrate():
    with TemporaryDirectory(prefix="arsenal-sqlite-") as directory:
        connection = sqlite3.connect(Path(directory) / "demo.db")
        try:
            connection.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))
            insert_batch(connection, ["alpha", "beta"])
            try:
                insert_batch(connection, ["gamma", "alpha"])
            except sqlite3.IntegrityError:
                pass
            return [row[0] for row in connection.execute("SELECT label FROM entries ORDER BY id")]
        finally:
            connection.close()


if __name__ == "__main__":
    print(json.dumps(demonstrate()))
