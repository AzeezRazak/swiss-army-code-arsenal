# Sprint 0008 - PHP research MVP proposal

File: `TODO/SPRINT-0008/PLAN.md`

Folder: `TODO/SPRINT-0008`

Status: AUTHORIZED by owner request `php scanner?` on 2026-11-09; completed. This sprint implemented local source/log analysis only; it did not build PHP, reproduce unverified CVEs or execute memory-safety experiments automatically.

## Script budget: 5/10

1. `projects/python-security-research/php-vulnerability-research-scanner/cve_intake.py` — verify and record primary-source metadata while keeping supplied CVE labels unconfirmed until verified.
2. `projects/python-security-research/php-vulnerability-research-scanner/patch_compare.py` — compare two local source trees and produce bounded changed-file reports.
3. `projects/python-security-research/php-vulnerability-research-scanner/lifecycle_analyzer.py` — classify setup, cleanup and partial-initialization events from synthetic logs.
4. `projects/python-security-research/php-vulnerability-research-scanner/sanitizer_parser.py` — parse local sanitizer logs for UAF/double-free signals without executing log content.
5. `projects/python-security-research/php-vulnerability-research-scanner/build_manifest.py` — record local compiler, commit, flags and extension metadata with secret redaction.

Use temporary source trees and synthetic logs. No exploit generation, third-party source access, arbitrary command execution, automatic CVE confirmation or external network dependency. Acceptance requires malformed-log, missing-source, redaction and bounded-input tests.

NEXT SPRINT PREPARED - AWAITING HUMAN AUTHORIZATION.
