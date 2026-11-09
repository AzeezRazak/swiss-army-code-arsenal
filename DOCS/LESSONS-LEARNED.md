# Lessons learned

File: `DOCS/LESSONS-LEARNED.md`

Folder: `DOCS`


## LESSON-0001 - Explicit contracts support meaningful tests

Source: Sprint 0001. Observation/evidence: 16 tests and five CLI examples passed; tests explicitly exercise first-duplicate search, blank JSON lines, rollback boundaries and singleton variance. Ambiguous edge behavior would make acceptance hard to assess. Improvement: specify invalid-input and resource policies before each new implementation. Action: RETRO-0001 assigned to Codex for Sprint 0002; completion requires executed error-path tests linked in review. Effectiveness: pending future verification.

## LESSON-0002 - Verification scope must stay visible

Source: Sprint 0001. Evidence: checks ran on Windows/Python 3.13.9 only. Root cause of limited portability evidence: a single available execution environment. Action RETRO-0002: Codex must retain explicit platform limitations in Sprint 0002 READMEs and review. No claim of cross-platform verification. Outcome: initial documentation records the limitation; future effectiveness is pending.

## LESSON-0003 - Platform-dependent filesystem verification

Source: Sprint 0002. Real symbolic-link creation failed with WinError 1314; a real junction integration test passed. Cause: Windows privilege constraints. Action: preserve the symlink skip, track QA-0003, and validate available native reparse behavior. Owner Codex; target Sprint 0003 reporting (RETRO-0003). Junction outcome verified; cross-platform symlink behavior still incomplete. Prior RETRO-0001/0002 actions applied through documented contracts, timeout/error tests and explicit platform limits.

## LESSON-0004 - Beginner lessons need explicit policies

Source Sprint 0003: tests verify every grading threshold and explain whitespace/casefold behavior. These choices are teaching contracts, not universal domain rules. Action RETRO-0004: Codex, Sprint 0004, pair each documented example with a deterministic CLI test; completion requires five verified examples. Outcome: all five Sprint 0004 examples passed as subprocess tests. Effectiveness confirmed for this sprint; continue the practice in Sprint 0005.
## LESSON-0005 - Resource policies belong beside file examples

Source Sprint 0005: the text-file lesson rejects symlinks, non-files, invalid UTF-8 and inputs over 1 MiB, with a temporary-file test for valid and missing paths. Observation/evidence: the initial full suite exposed two test defects before the corrected 71-test run passed. Action RETRO-0006: keep filesystem examples isolated in temporary directories and run focused tests before the full suite. Owner Codex; target Sprint 0006.
