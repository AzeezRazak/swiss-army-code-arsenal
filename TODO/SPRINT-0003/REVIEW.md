# Sprint 0003 review

File: `TODO/SPRINT-0003/REVIEW.md`

Folder: `TODO/SPRINT-0003`

Completed 2026-11-05: five runnable scripts, within the new 5-10 range.

| ID | Acceptance evidence |
|---|---|
| PY-0001 | Freezing/boiling/negative/fractional values; nonfinite/overflow rejection |
| PY-0002 | Both sides of every grade threshold; endpoints and invalid scores |
| PY-0003 | Empty/signed data, iterator use, reference totals and nonmutation |
| PY-0004 | Empty/whitespace/Unicode text, code-point policy and invalid type |
| PY-0005 | Repeated/casefolded tokens, punctuation, empty input and sorted keys |

All five documented CLI examples and invalid CLI cases executed. Full suite: 43 passed, 0 failed, 1 existing real symlink skip (QA-0003, Windows privilege limitation). No new failures or skipped beginner checks. Windows/Python 3.13.9 only; other runtimes unverified. Examples intentionally use simple tokenization and floating-point arithmetic with documented limits.

Source comments, file/folder headers and catalog entries included. Existing eight runnable scripts plus five new ones: thirteen runnable scripts; twelve utility implementations across eight domains. Three completed sprints. Branch main, authorized destination origin/main. Implementation and closure commit hashes are available in Git history under the Sprint 0003 commit subjects; publication outcome is verified after pushing and reported to the owner.

License remains undecided. CSV and interpreter work deferred by owner direction, not failed acceptance. No Sprint 0004 implementation authorized.

Implementation and sprint records: commit `1b05a68`. Publication targets the authorized origin/main; verify current synchronization with Git tracking state.
