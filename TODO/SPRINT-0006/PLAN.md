# Sprint 0006 - Security research foundations proposal

File: `TODO/SPRINT-0006/PLAN.md`

Folder: `TODO/SPRINT-0006`

Status: proposed; awaiting fresh owner authorization. This plan supersedes the generic Python-fundamentals proposal because the owner redirected the focus to the two security-research projects. It is planning-only until explicitly authorized.

## Objective

Create five small, offline Python utilities in existing `SCRIPTS/` domains. They are reusable concepts inspired by the two scanner specifications, not scanner implementations and not network attack tools. Scanner code remains inside `projects/python-security-research/` and requires a later bounded sprint.

## Script budget: 5/10

1. `SCRIPTS/08-cybersecurity/scope-allowlist/validate_scope.py` — validate URL, host, path, account and callback allowlist records; reject wildcard or malformed scope by default.
2. `SCRIPTS/08-cybersecurity/finding-confidence/score_finding.py` — calculate deterministic confidence/severity labels from structured evidence quality; never claim exploitability.
3. `SCRIPTS/03-file-data-processing/evidence-jsonl/validate_evidence.py` — validate bounded sanitized evidence JSONL records, required provenance fields and secret-redaction markers without changing input.
4. `SCRIPTS/09-automation-scripting/request-budget-plan/build_rate_plan.py` — produce an offline request schedule from count, interval, concurrency and body-size limits; never send requests.
5. `SCRIPTS/20-testing-quality/fixture-replay/replay_fixture.py` — replay saved HTTP observations against a local detector interface or fixture adapter; no live network access and deterministic output.

## Acceptance criteria

- Five scripts only, each with a purpose/location/input-output/runtime/usage/limits comment block and README.
- Standard library only; no Burp Suite, Nuclei, sqlmap, external scanning CLI, live target, callback service or paid API.
- Unit tests cover valid, boundary, malformed, secret-bearing and resource-limit inputs.
- CLI examples are paired with subprocess tests; all filesystem fixtures use temporary directories.
- Full test discovery passes, with missing tools or environment limitations reported honestly.
- Update backlog, catalog only after delivery, current state, decisions, lessons and the dated transcript.

## Deferred work

Do not implement either scanner, detector modules, live HTTP transport, PHP builds, CVE reproductions, exploit payloads, database migrations or dashboard code in Sprint 0006. Those require separate plans, explicit authorization, local lab prerequisites and primary-source CVE verification.

NEXT SPRINT PREPARED - AWAITING HUMAN AUTHORIZATION.
