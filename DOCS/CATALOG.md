# Catalog

File: `DOCS/CATALOG.md`

Folder: `DOCS`


Seven implementations across seven domains; Python and SQL represented. Five fully verified locally; two new utilities verified with the Sprint 0002 platform limitations on 2026-11-04 (Windows, Python 3.13.9, SQLite 3.51.0). Latest suite: 31 passed, zero failed, one symlink integration test skipped (32 total). Each implementation has usage, setup, tests and limitations. No cross-platform verification or benchmarks performed.

| ID | Implementation | Language | Verification |
|---|---|---|---|
| ALG-0001 | [Binary search](../SCRIPTS/02-algorithms-data-structures/binary-search/README.md) | Python | Passed locally |
| DATA-0001 | [JSON Lines validation](../SCRIPTS/03-file-data-processing/jsonl-validator/README.md) | Python | Passed locally |
| SEC-0001 | [SHA-256 file digest](../SCRIPTS/08-cybersecurity/sha256-file/README.md) | Python | Passed locally |
| DB-0001 | [SQLite transactions](../SCRIPTS/07-databases-storage/sqlite-transactions/README.md) | Python, SQL | Passed locally |
| MATH-0001 | [Online statistics](../SCRIPTS/12-data-science-mathematics/online-statistics/README.md) | Python | Passed locally |

Test command: `python -m unittest discover -s TESTS -p "test_*.py" -v`. See [review](../TODO/SPRINT-0001/REVIEW.md) for results and limitations. Completed sprints: 2. Open backlog tasks: 24. Known unresolved implementation defects: 0. Two prior actions applied with Sprint 0002 evidence; long-term effectiveness remains under review.

| New item | Usage and limitations | Runnable scripts |
|---|---|---|
| NET-0002 | [Loopback TCP](../SCRIPTS/05-networking-protocols/loopback-tcp/README.md) | 2 |
| AUTO-0002 | [Directory inventory](../SCRIPTS/09-automation-scripting/directory-inventory/README.md) | 1 |

[Latest review](../TODO/SPRINT-0002/REVIEW.md). Total runnable scripts: 8. Symlink verification gap: QA-0003.
