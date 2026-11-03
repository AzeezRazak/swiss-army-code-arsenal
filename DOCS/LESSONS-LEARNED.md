# Lessons learned

File: `DOCS/LESSONS-LEARNED.md`

Folder: `DOCS`


## LESSON-0001 - Explicit contracts support meaningful tests

Source: Sprint 0001. Observation/evidence: 16 tests and five CLI examples passed; tests explicitly exercise first-duplicate search, blank JSON lines, rollback boundaries and singleton variance. Ambiguous edge behavior would make acceptance hard to assess. Improvement: specify invalid-input and resource policies before each new implementation. Action: RETRO-0001 assigned to Codex for Sprint 0002; completion requires executed error-path tests linked in review. Effectiveness: pending future verification.

## LESSON-0002 - Verification scope must stay visible

Source: Sprint 0001. Evidence: checks ran on Windows/Python 3.13.9 only. Root cause of limited portability evidence: a single available execution environment. Action RETRO-0002: Codex must retain explicit platform limitations in Sprint 0002 READMEs and review. No claim of cross-platform verification. Outcome: initial documentation records the limitation; future effectiveness is pending.

## LESSON-0003 - Platform-dependent filesystem verification

Source: Sprint 0002. Real symbolic-link creation failed with WinError 1314; a real junction integration test passed. Cause: Windows privilege constraints. Action: preserve the symlink skip, track QA-0003, and validate available native reparse behavior. Owner Codex; target Sprint 0003 reporting (RETRO-0003). Junction outcome verified; cross-platform symlink behavior still incomplete. Prior RETRO-0001/0002 actions applied through documented contracts, timeout/error tests and explicit platform limits.
