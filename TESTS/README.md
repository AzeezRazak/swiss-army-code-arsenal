# Tests

Run from the repository root:

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

Sixteen standard-library tests cover five utilities, including deterministic reference comparisons and subprocess CLI checks. Fixtures use temporary directories; no network or third-party packages.
