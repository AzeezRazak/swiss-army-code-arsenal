# Tests

File: `TESTS/README.md`

Folder: `TESTS`


Run from the repository root:

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

Forty-four tests cover twelve utilities, including local loopback integration, deterministic reference comparisons and subprocess CLI checks. Latest Windows run: 43 passed, one real symlink test skipped due to WinError 1314. Real junction traversal checks passed. Fixtures use temporary directories; no external network or third-party packages.
