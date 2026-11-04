# SHA-256 file digest (SEC-0001)

File: `SCRIPTS/08-cybersecurity/sha256-file/README.md`

Folder: `SCRIPTS/08-cybersecurity/sha256-file`


Read binary data in 1 MiB chunks and print a lowercase SHA-256 digest. Empty files are supported. Read errors go to stderr with exit 1; success exits 0. The function accepts a positive integer chunk size. Memory is O(chunk size), time O(file size). Hashes help compare integrity but do not authenticate a sender; obtain expected digests through a trusted channel. Concurrent file modifications are not detected; use a stable regular file, not an endless device or pipe.

## Requirements and setup

Python 3.10+ with standard-library modules only. No installation or third-party packages. Verified on Windows with Python 3.13.9 ; other versions and operating systems are unverified. Run commands from the repository root.

## Usage

```powershell
python SCRIPTS/08-cybersecurity/sha256-file/sha256_file.py EXAMPLES/abc.txt
```

Expected stdout:

```text
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

File utilities read inputs without modifying them. Data fixtures are synthetic. No credentials or network access are used. For library use, load the standalone module or add its directory to your import path.

## Verification

```powershell
python -m unittest discover -s TESTS -p "test_*.py" -v
```

See [acceptance tests](../../../TESTS/test_utilities.py) and [sprint review](../../../TODO/SPRINT-0001/REVIEW.md).

## Verify an expected digest

```powershell
python SCRIPTS/08-cybersecurity/sha256-file/sha256_file.py EXAMPLES/abc.txt --check ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

A match prints `OK` and exits 0. A mismatch prints an error to stderr, leaves stdout empty and exits 1. Expected digests must be exactly 64 ASCII hexadecimal characters; uppercase is accepted. Malformed expected digests are rejected before file access with exit 2. Read errors remain exit 1. Omitting `--check` preserves digest-only output. Obtain the expected digest from a trusted source; comparison does not establish authenticity by itself.

Additional regression checks: [TESTS/test_script_improvements.py](../../../TESTS/test_script_improvements.py).
