# Sprint 0002 - Local networking and file inventory

Status: completed after user EXECUTE on 2026-11-04. Prerequisite: completed Sprint 0001. Review source: [Sprint 0001 retrospective](../SPRINT-0001/RETROSPECTIVE.md). Execution and review recorded alongside this plan.

## Script budget: 3/5

1. NET-0002: loopback TCP server.
2. NET-0002: loopback TCP client.
3. AUTO-0002: read-only directory inventory.

Tests, documentation, fixtures and non-runnable support modules are excluded. Additional runnable scripts must stay within five total; overflow goes to a later sprint.

## Proposed scope and acceptance

- NET-0002: Python loopback TCP request/reply example with length-prefixed messages, explicit maximum payload and finite timeouts. Deliver server/client CLI, README and local integration tests. Accept when normal exchanges, truncated frames, oversize declarations and idle-client timeout are tested; bind only to loopback by default and ensure clean shutdown.
- AUTO-0002: read-only Python directory inventory CLI producing deterministic JSON. Deliver script, README and temporary-tree tests. Accept when empty/nested trees, Unicode names and missing paths are covered; do not follow directory symlinks; document permission errors and avoid reading file contents.

Dependencies: Python 3 standard library and local loopback sockets. No packages, hosted CI or external requests. Risks: Windows socket timing and permission/symlink test availability; use bounded timeouts and report unavailable checks honestly. Scope excludes internet scanning, file mutation and other language ports.

Verification: extend `python -m unittest discover -s TESTS -p "test_*.py" -v`; all prior tests must remain passing. Run each new README example. Apply RETRO-0001 and RETRO-0002: every error/resource policy gets an executed test or explicit limitation; platform status remains explicit.

Finish with catalog, backlog, review, retrospective, local commits and a next proposal; stop before another sprint. Start/completion dates: 2026-11-04 / 2026-11-04.
