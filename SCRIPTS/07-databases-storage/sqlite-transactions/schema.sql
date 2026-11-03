-- Purpose: define the table used to demonstrate SQLite commit and rollback.
-- Location: SCRIPTS/07-databases-storage/sqlite-transactions/schema.sql
-- Input: fresh SQLite database. Output: empty entries table.
-- Usage: loaded by transactions.py; requires SQLite, no external dependencies.
-- Limit: initialization only; rerunning against the same table raises an error.
CREATE TABLE entries (
    -- SQLite assigns an integer row identifier when the insert omits it.
    id INTEGER PRIMARY KEY,
    -- Reject missing or duplicate labels to exercise atomic batch rollback.
    label TEXT NOT NULL UNIQUE
);
