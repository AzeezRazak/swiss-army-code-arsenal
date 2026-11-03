# Catalog

Five implementations across five domains; Python and SQL represented. All five verified locally on 2026-11-04 (Windows, Python 3.13.9, SQLite 3.51.0). Sixteen tests passed; zero failed/skipped. Each implementation has usage, setup, tests and limitations. No cross-platform verification or benchmarks performed.

| ID | Implementation | Language | Verification |
|---|---|---|---|
| ALG-0001 | [Binary search](../SCRIPTS/02-algorithms-data-structures/binary-search/README.md) | Python | Passed locally |
| DATA-0001 | [JSON Lines validation](../SCRIPTS/03-file-data-processing/jsonl-validator/README.md) | Python | Passed locally |
| SEC-0001 | [SHA-256 file digest](../SCRIPTS/08-cybersecurity/sha256-file/README.md) | Python | Passed locally |
| DB-0001 | [SQLite transactions](../SCRIPTS/07-databases-storage/sqlite-transactions/README.md) | Python, SQL | Passed locally |
| MATH-0001 | [Online statistics](../SCRIPTS/12-data-science-mathematics/online-statistics/README.md) | Python | Passed locally |

Test command: `python -m unittest discover -s TESTS -p "test_*.py" -v`. See [review](../TODO/SPRINT-0001/REVIEW.md) for results and limitations. Completed sprints: 1. Open backlog tasks: 23. Known unresolved implementation defects: 0. Verified historical corrective actions: 0.
