# Sprint 0002 review

File: `TODO/SPRINT-0002/REVIEW.md`

Folder: `TODO/SPRINT-0002`


Completed 2026-11-04. Delivered 3 runnable scripts out of maximum 5; protocol.py is non-runnable support. No extra runtime dependencies.

| Item | Acceptance evidence | Limitations |
|---|---|---|
| NET-0002 | CLI request/reply, empty and 65,536-byte payloads, truncated header/body, oversize header, idle and accept timeouts, total trickle-byte deadline, parameter errors, clean exit | Windows only; local teaching protocol without authentication or TLS |
| AUTO-0002 | Empty/nested/Unicode trees, deterministic JSON, missing/file roots, content preservation, permission propagation, reparse classification, real junction non-traversal and linked-root rejection | Real symbolic-link test skipped (WinError 1314); permission errors injected; path-replacement races not prevented |

Verification: 32 discovered tests; 31 passed, zero failed, one skipped. All prior regressions passed. README examples passed. Documentation links and whitespace checks passed. Symlink integration verification is incomplete and tracked as QA-0003; junction verification is complete. No claim of all-platform or hostile-filesystem safety.

Commit 059f98e implements the tools. Subsequent closure commit has subject `docs: close sprint 0002 and plan bounded parser utilities`. Branch main; destination origin/main at https://github.com/AzeezRazak/swiss-army-code-arsenal. Push verification occurs after closure; inspect tracking state and final report for outcome.

RETRO-0001: error/deadline/resource contracts documented and linked to tests, with explicit unverified permissions/symlink cases. RETRO-0002: platform limits stated in both new READMEs. These actions are applied; broader long-term effectiveness still needs later evidence. License remains pending.

Progress: 7 utility implementations across 7 domains, 8 runnable scripts total, Python and SQL represented, 2 completed sprints. Counts exclude test and support modules.
