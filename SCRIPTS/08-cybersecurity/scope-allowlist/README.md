# Scope allowlist validator

File: `SCRIPTS/08-cybersecurity/scope-allowlist/README.md`

Folder: `SCRIPTS/08-cybersecurity/scope-allowlist`

`validate_scope.py` validates exact hosts, paths and credential-free HTTP(S) callback URLs for local security-research fixtures. It rejects wildcards, unknown fields, empty policies and embedded credentials. It never performs network access.

Example: `python SCRIPTS/08-cybersecurity/scope-allowlist/validate_scope.py "{\"hosts\":[\"app.test\"],\"paths\":[\"/api\"]}"`
