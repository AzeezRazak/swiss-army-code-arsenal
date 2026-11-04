# Two-script improvements

File: `TODO/IMPROVEMENTS-0001.md`

Folder: `TODO`

Authorized by owner on 2026-11-05: improve two existing scripts and publish on a separate branch. This bounded maintenance task is not a new development sprint; no new runnable scripts added. Sprint 0004 remains unstarted.

Branch: improve/jsonl-and-sha256. Destination: origin/improve/jsonl-and-sha256 at the existing public repository. Main is not changed or merged.

- [x] SCRIPTS/03-file-data-processing/jsonl-validator/validate_jsonl.py: configurable default 1 MiB physical-line limit, bounded reads, one-based overlimit diagnostics.
- [x] SCRIPTS/08-cybersecurity/sha256-file/sha256_file.py: --check expected digest, strict hex validation, case normalization, explicit match/mismatch exit behavior.
- [x] Update each folder's README usage and compatibility notes; preserve purpose blocks and explanatory comments.
- [x] Add TESTS/test_script_improvements.py with nine regression tests covering byte/newline boundaries, bounded reads, invalid limits, digest matches/mismatches, malformed digests and missing files.

Verification: `python -m unittest discover -s TESTS -p "test_*.py" -q` ran 53 tests in 5.737 seconds on Windows/Python 3.13.9: 52 passed, zero failed, one existing symlink skip (QA-0003). Original regression tests remain passing. No dependencies installed. Documentation links and Git whitespace checked before commit. Publication outcome is checked after push via upstream tracking and reported to owner.

Limitations: JSONL default now rejects lines over 1 MiB; callers can raise the limit deliberately. Neither utility is a defense against unlimited-duration device streams. SHA-256 verification still requires a trusted expected digest and stable input file. Cross-platform verification is not claimed.

## Integration into main

Owner authorized pushing to main on 2026-11-05. Fast-forwarded main to implementation commit 2a82225 after fetching origin. Re-ran all 53 tests: 52 passed, zero failed, one existing symlink skip. Improvement branch retained.
