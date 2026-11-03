# Sprint 0001 - Offline foundations

Status: completed on 2026-11-04 following explicit user EXECUTE authorization.

## Goal and scope

Deliver five independently usable Python/SQL examples: ALG-0001 binary search, DATA-0001 JSON Lines validation, SEC-0001 file hashing, DB-0001 SQLite rollback, and MATH-0001 online statistics. Use Python's standard library and SQLite through sqlite3. Avoid dependency installation unless a verified prerequisite requires approval.

## Deliverables and acceptance

Every item must meet its [backlog criteria](../BACKLOG.md), include an implementation README with setup, usage, error cases and limitations, and meaningful unittest coverage. Tests must operate on synthetic data and temporary files. Add working examples and catalog entries with honest verification status.

Executed verification command: `python -m unittest discover -s TESTS -p "test_*.py" -v`. During execution confirm the actual Python version and sqlite3 availability, record commands and outcomes, and run documented CLI examples. No third-party network access or credentials required.

## Dependencies and risks

Requires human sprint authorization and a working Python 3 runtime. Floating-point comparison needs tolerances; hashing does not provide authentication; binary search assumes sorted input; JSON validation must bound memory to one line; SQLite examples must isolate temporary databases. Document any unresolved portability checks.

## Exclusions and finish condition

No web service, hosted CI, dependency framework, GPU, real financial operation or additional language port in this sprint. Done means all five task criteria and documentation checks pass, review/retrospective are recorded, and the next bounded plan is prepared. Failed criteria remain incomplete. Stop before any next sprint execution.
