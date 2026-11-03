# Read-only directory inventory (AUTO-0002)

inventory.py emits deterministic JSON metadata for descendants of a directory, sorted by relative POSIX-style path. Files include byte size; directories, links and other entries include type. The root itself is omitted. No file content is opened or modified. Python 3.10+ standard library only; no installation. Verified on Windows/Python 3.13.9 only.

## Usage

From the repository root:

```powershell
python SCRIPTS/09-automation-scripting/directory-inventory/inventory.py EXAMPLES
```

Output is an array with `path`, `type`, and file `size` fields. Empty directories produce `[]`. Non-ASCII names are JSON-escaped for console portability. Repeated runs on an unchanged tree produce the same output.

## Errors and limits

Missing paths, non-directory roots, linked/reparse-point roots, permission failures and filesystem errors print an error to stderr and exit 1, with no partial JSON output. Valid results exit 0; command syntax errors exit 2. Permission behavior is tested through an injected PermissionError; real ACL-denied traversal is not verified here.

Directory symlinks and Windows reparse points (including junctions) are listed as links, never intentionally traversed. Do not scan a tree being modified by untrusted actors: path replacement races are not prevented, and this is not a filesystem security boundary or atomic snapshot. File sizes may change during enumeration. Memory grows with the number of entries and sorting costs O(n log n); there is no entry limit. Use bounded, stable directories. This tool makes no network requests, but do not point it at network shares unless access is intended.

## Tests

`python -m unittest discover -s TESTS -p "test_*.py" -v`

[Tests](../../../TESTS/test_sprint2.py) cover empty/nested trees, Unicode, deterministic order, content preservation, missing/file roots, injected permissions, reparse classification and real Windows junction non-traversal. A real symlink test is included but skipped on this machine because Windows denies creation (WinError 1314). Symlink integration on a permitted environment and non-Windows execution remain incomplete; see [review](../../../TODO/SPRINT-0002/REVIEW.md).
