# Security research dashboard

File: `projects/python-security-research/security-research-dashboard/README.md`

Folder: `projects/python-security-research/security-research-dashboard`

This is a local-only sister application to the web and PHP scanners. It provides one browser dashboard to:

1. save an explicit scan scope (targets, methods, permitted account labels, callback URLs and notes);
2. view sanitized findings from both scanner SQLite databases; and
3. download JSON, CSV or Markdown exports for further analysis.

## Run

From the repository root:

`python projects/python-security-research/security-research-dashboard/app.py`

Open `http://127.0.0.1:8765`. The app binds to loopback by default, stores its scope in `dashboard.sqlite3`, and reads `web_scanner.sqlite3` and `php_research.sqlite3` from their sister project folders. Override paths with `--scope-db`, `--web-db` and `--php-db`.

The dashboard does not authenticate users, launch scans, contact targets, execute PHP, or store credentials. It is intended for the local owner on a trusted machine. Add authentication and a stronger deployment boundary before any non-local hosting.

## Tests

`python -m unittest TESTS.test_security_research_dashboard -v`
