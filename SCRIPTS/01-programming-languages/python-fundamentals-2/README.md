# Python fundamentals - second five lessons

File: `SCRIPTS/01-programming-languages/python-fundamentals-2/README.md`

Folder: `SCRIPTS/01-programming-languages/python-fundamentals-2`

Five standard-library-only lessons extending the first Python fundamentals set. Each reusable function validates inputs and each CLI prints deterministic JSON. Tested on Windows/Python 3.13.9; other runtimes and platforms are unverified.

## Setup and error policy

Run from the repository root with Python 3.10+. No packages, file mutation or network access are required. Successful commands exit 0; invalid CLI input prints a diagnostic to stderr and exits 2. Functions raise `ValueError` for documented invalid values.

## Examples

```powershell
python SCRIPTS/01-programming-languages/python-fundamentals-2/unique_items.py red blue red
python SCRIPTS/01-programming-languages/python-fundamentals-2/tuple_coordinates.py 0 0 3 4
python SCRIPTS/01-programming-languages/python-fundamentals-2/function_arguments.py Ada --repeat 2 --punctuation '?'
python SCRIPTS/01-programming-languages/python-fundamentals-2/safe_integer.py '-42'
python SCRIPTS/01-programming-languages/python-fundamentals-2/list_comprehensions.py -3 -2 0 3 4
```

Expected results are respectively `['red', 'blue']`, distance `5.0` with midpoint `[1.5, 2.0]`, two `Hello, Ada?` greetings, `{"value": -42}`, and `[4, 0, 16]`.

## Policies and limits

- `unique_items` accepts at most 100,000 strings and retains exact Unicode values in first-seen order.
- `tuple_coordinates` requires two 2D real-number points. Coordinates, distance and midpoint must be finite; booleans, malformed tuples and float overflow are rejected.
- `function_arguments` trims a nonempty name, permits repeat counts 1–10 and requires one non-whitespace punctuation character.
- `safe_integer` permits surrounding whitespace, accepts an optional sign and ASCII decimal digits, rejects fractions/internal whitespace, and limits input to 1,000 digits.
- `list_comprehensions` accepts at most 100,000 integers, rejects booleans and returns squares of even values in input order.

These are teaching contracts, not universal parsing or formatting rules. Values are retained in memory and are not intended for unbounded input.

## Tests

`python -m unittest discover -s TESTS -p "test_*.py" -v`

[TESTS/test_python_fundamentals2.py](../../../TESTS/test_python_fundamentals2.py) covers boundary cases, invalid values, non-mutation, and all five documented CLI examples.
