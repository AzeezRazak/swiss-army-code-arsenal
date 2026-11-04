# Sprint 0003 - Fundamental Python

File: `TODO/SPRINT-0003/PLAN.md`

Folder: `TODO/SPRINT-0003`

Authorized by the owner's EXECUTE on 2026-11-05, with revised focus and 5-10 script limit. Start/completion: 2026-11-05 / 2026-11-05. Status: complete. Five runnable scripts; no support scripts. The previous DATA-0002 and COMP-0002 proposal is deferred to the backlog.

## Script budget: 5/10 (minimum 5)

All deliverables are in `SCRIPTS/01-programming-languages/python-fundamentals/`:

- PY-0001: `temperature.py` - Variables and arithmetic. Convert Celsius to Fahrenheit.
- PY-0002: `grade.py` - Conditionals. Classify a numeric score using an explicit example grading scale.
- PY-0003: `list_summary.py` - Loops and lists. Count even and odd integers and calculate their sum.
- PY-0004: `text_summary.py` - Strings. Count characters, whitespace-separated words and alphabetic characters.
- PY-0005: `word_counts.py` - Dictionaries. Count whitespace-separated words after case folding.

## Acceptance

Each script has a reusable function, clear comments and CLI documentation. Test normal and boundary inputs, invalid inputs and subprocess exit/output. Temperature rejects nonfinite/overflow values; grades define every threshold; list totals support empty and signed inputs; text uses Unicode code points and whitespace tokens; dictionary counts casefold and preserve punctuation. All five documented examples must pass; previous regressions remain passing or explicitly skipped with QA-0003 recorded.

Python standard library only. No files modified by lesson CLIs, no network or packages. Run `python -m unittest discover -s TESTS -p "test_*.py" -v`. Complete review/retrospective/catalog, commit and push to authorized origin/main; prepare but do not execute the next sprint. Risks: floating-point rounding and simple tokenization are documented rather than hidden.
