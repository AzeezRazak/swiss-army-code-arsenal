# Sprint 0007 - Web scanner MVP proposal

File: `TODO/SPRINT-0007/PLAN.md`

Folder: `TODO/SPRINT-0007`

Status: proposed; awaiting fresh authorization. This sprint implements only local-fixture web scanner foundations and four detector modules. It does not contact live targets.

## Script budget: 5/10

1. `projects/python-security-research/web-vulnerability-scanner/http_observer.py` — bounded fixture/allowlisted HTTP observation adapter.
2. `projects/python-security-research/web-vulnerability-scanner/sqli_detector.py` — controlled response-difference and database-error signal detector.
3. `projects/python-security-research/web-vulnerability-scanner/xss_detector.py` — reflection and output-context classifier.
4. `projects/python-security-research/web-vulnerability-scanner/idor_detector.py` — two-permitted-account response comparison.
5. `projects/python-security-research/web-vulnerability-scanner/misconfiguration_detector.py` — headers, cookies and unsafe-method policy checks.

All inputs use local JSON fixtures or an explicitly configured local mock. Use the Sprint 0006 scope/evidence/rate/fixture utilities. No SSRF callback, file upload, path traversal, authentication attack, live bounty target or exploit payload is included. Acceptance requires positive, negative and ambiguous fixtures, redacted evidence and deterministic tests.

NEXT SPRINT PREPARED - AWAITING HUMAN AUTHORIZATION.
