# Sprint 0004 - More Python fundamentals

File: `TODO/SPRINT-0004/PLAN.md`

Folder: `TODO/SPRINT-0004`

AUTHORIZED by owner message `execute next sprint` on 2026-11-06; completed. Python fundamentals remains the owner-selected focus. Read [previous review](../SPRINT-0003/REVIEW.md) and [lessons](../../DOCS/LESSONS-LEARNED.md) first.

## Script budget: 5/10 (minimum 5)

All planned scripts in `SCRIPTS/01-programming-languages/python-fundamentals-2/`.

- PY-0006: `unique_items.py` - Sets and order-preserving deduplication. Acceptance: Empty/repeated/Unicode tokens; retain first-occurrence order without mutating input.
- PY-0007: `tuple_coordinates.py` - Tuples and coordinate unpacking. Acceptance: Finite 2D coordinates; distance and midpoint; reject malformed/nonfinite/overflow input.
- PY-0008: `function_arguments.py` - Functions, defaults and keyword arguments. Acceptance: Format greetings with validated repeat count 1-10; default and custom options tested.
- PY-0009: `safe_integer.py` - Exceptions and integer conversion. Acceptance: Parse signed base-10 strings with explicit whitespace policy; reject decimal fractions and invalid tokens.
- PY-0010: `list_comprehensions.py` - Filtering and transforming lists. Acceptance: Return squares of even integers; empty/negative/duplicate cases and invalid types tested.

Python standard library only. Each script needs a purpose block, meaningful comments, a reusable function, documented CLI example and tests. No file mutation/network/packages. Define numerical and input-size limits before implementation. Run the full unittest discovery command and all five README examples. Apply RETRO-0004 by pairing examples with CLI tests. Report QA-0003 honestly if still unavailable.

Finish review/retrospective/catalog, commit and push to authorized origin/main, prepare next proposal and stop. No automatic execution. Start/completion: 2026-11-06 / 2026-11-06.
