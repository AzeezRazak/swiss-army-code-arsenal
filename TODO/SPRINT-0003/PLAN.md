# Sprint 0003 - Bounded parsing utilities

File: `TODO/SPRINT-0003/PLAN.md`

Folder: `TODO/SPRINT-0003`


PLANNED - AWAITING HUMAN AUTHORIZATION. Start/completion: not started/not completed. Review [Sprint 0002](../SPRINT-0002/REVIEW.md) and [lessons](../../DOCS/LESSONS-LEARNED.md) before execution.

## Script budget: 2/5

1. DATA-0002: Python CSV summary CLI.
2. COMP-0002: Python arithmetic expression interpreter CLI.

Tests, fixtures, docs and non-runnable support are excluded. No additional runnable scripts planned.

## Tasks and acceptance

DATA-0002: stream UTF-8 CSV with explicit header/row-width policy, summarize row count and missing cells per column, and output deterministic JSON. Document encoding, newline, duplicate header and malformed-row behavior. Tests cover quoted delimiters/newlines, empty input, duplicate headers and bad encoding. No source modification.

COMP-0002: tokenize and parse decimal arithmetic with parentheses and +, -, *, / without eval or exec. Define precedence and unary signs; bound input length and nesting. Tests cover precedence, invalid tokens, mismatched parentheses, zero division and resource bounds. Output result or clear nonzero error.

Requires Python standard library only. No external services or packages. Run all existing tests plus new CLI tests using `python -m unittest discover -s TESTS -p "test_*.py" -v`; execute documented examples. Record skips with IDs (RETRO-0003). QA-0003 symlink integration remains conditional on an available permitted environment; do not change system privileges automatically.

Finish with documented acceptance evidence, catalog, review, retrospective, authorized GitHub push and next plan. Stop before further execution. Risks: numeric rounding, parser recursion and malformed CSV; specify limits before implementation.
