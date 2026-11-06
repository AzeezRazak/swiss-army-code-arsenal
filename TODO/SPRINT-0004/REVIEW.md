# Sprint 0004 review

File: `TODO/SPRINT-0004/REVIEW.md`

Folder: `TODO/SPRINT-0004`

## Acceptance review

- PY-0006 passed: empty, repeated and Unicode strings preserve first occurrence order without mutating input.
- PY-0007 passed: finite 2D tuples return distance and midpoint; malformed, nonfinite, boolean and overflow values are rejected.
- PY-0008 passed: default and custom greeting options work; repeat counts are constrained to 1–10.
- PY-0009 passed: signed base-10 values and surrounding whitespace are accepted; fractions, internal whitespace and invalid tokens are rejected.
- PY-0010 passed: even integers are filtered and squared in order; empty, negative, duplicate and invalid-type cases are covered.
- Source purpose/usage/limits blocks, adjacent operation comments, README policies and tests are present.
- RETRO-0004 passed: all five README examples were executed by deterministic subprocess tests.

Full regression: 63 passed, 0 failed, 1 skipped (QA-0003, Windows symlink privilege limitation). Verification is limited to Windows/Python 3.13.9; no cross-platform or benchmark claim is made. No unresolved Sprint 0004 implementation defects.
