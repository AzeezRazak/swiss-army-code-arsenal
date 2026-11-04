# Python fundamentals - first five lessons

File: `SCRIPTS/01-programming-languages/python-fundamentals/README.md`

Folder: `SCRIPTS/01-programming-languages/python-fundamentals`

Five small lessons, ordered from numeric values through dictionaries. Each file has a reusable function and a guarded CLI, with comments explaining the steps. Read the function first; argparse and JSON are the common command-line wrapper.

## Setup and error policy

Python 3.10+ and standard library only; no packages or installation. Tested on Windows/Python 3.13.9. Other versions/platforms unverified. Run examples from the repository root. Success prints JSON and exits 0; CLI input errors print to stderr and exit 2. Library functions raise ValueError for documented invalid values; unsupported object conversions may raise TypeError. None reads/writes files or uses network resources.

## PY-0001: Variables, float conversion and arithmetic

File: [SCRIPTS/01-programming-languages/python-fundamentals/temperature.py](temperature.py)

```powershell
python SCRIPTS/01-programming-languages/python-fundamentals/temperature.py 0
```

Expected JSON:

```json
{"celsius": 0.0, "fahrenheit": 32.0}
```

## PY-0002: if/elif/else and validation

File: [SCRIPTS/01-programming-languages/python-fundamentals/grade.py](grade.py)

```powershell
python SCRIPTS/01-programming-languages/python-fundamentals/grade.py 85
```

Expected JSON:

```json
{"score": 85.0, "grade": "B"}
```

## PY-0003: Lists, for loops, accumulators and modulo

File: [SCRIPTS/01-programming-languages/python-fundamentals/list_summary.py](list_summary.py)

```powershell
python SCRIPTS/01-programming-languages/python-fundamentals/list_summary.py 1 2 3 4
```

Expected JSON:

```json
{"count": 4, "sum": 10, "even": 2, "odd": 2}
```

## PY-0004: Strings, split, len and Unicode letters

File: [SCRIPTS/01-programming-languages/python-fundamentals/text_summary.py](text_summary.py)

```powershell
python SCRIPTS/01-programming-languages/python-fundamentals/text_summary.py "Hello Python"
```

Expected JSON:

```json
{"characters": 12, "words": 2, "letters": 11}
```

## PY-0005: Dictionary get, updates and sorted keys

File: [SCRIPTS/01-programming-languages/python-fundamentals/word_counts.py](word_counts.py)

```powershell
python SCRIPTS/01-programming-languages/python-fundamentals/word_counts.py "Python python code"
```

Expected JSON:

```json
{"code": 1, "python": 2}
```

## Exact policies and limits

- Temperature uses Celsius * 1.8 + 32. NaN, infinity and output overflow are rejected. It is an arithmetic lesson; it does not enforce physical absolute-zero constraints. Ordinary float rounding applies.
- Grades use A >= 90, B >= 80, C >= 70, D >= 60, otherwise F, for finite scores in [0,100]. This is an example scale, not an institutional grading rule.
- List summary accepts integers (not booleans in the function), including negatives and zero. Empty input produces all-zero counters. The function uses constant accumulator state; CLI inputs are retained as a list. Large integers may hit Python conversion limits.
- Text counts Unicode code points, whitespace-separated tokens and isalpha letters. Punctuation remains in tokens; combining marks are separate code points. It is not linguistic word segmentation.
- Word counts use casefold and whitespace splitting; punctuation remains attached and accents are not normalized. Empty text yields an empty dictionary. Keys are sorted for deterministic output.

Text and dictionary examples retain input/tokens in memory; dictionary storage grows with vocabulary. All examples are intended for small command-line inputs, not unbounded streams. No production readiness claim.

## Tests

`python -m unittest discover -s TESTS -p "test_*.py" -v`

[TESTS/test_python_fundamentals.py](../../../TESTS/test_python_fundamentals.py) covers reference temperatures, grade thresholds, empty/signed lists, invalid types, Unicode/text policies, dictionary case folding and all five CLI examples/error exits. Latest full suite: 43 passed, one existing symlink skip (QA-0003). See [Sprint 0003 review](../../../TODO/SPRINT-0003/REVIEW.md).
