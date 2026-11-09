# Sprint 0009 - security-research support utilities proposal

File: `TODO/SPRINT-0009/PLAN.md`

Folder: `TODO/SPRINT-0009`

Status: PROPOSED; planning only. This sprint is not authorized for implementation. It intentionally pauses expansion of the web scanner, PHP scanner and dashboard while extracting reusable offline utilities for other Swiss folders.

## Objective

Turn proven ideas from the [web vulnerability scanner](../../projects/python-security-research/web-vulnerability-scanner/README.md), [PHP research scanner](../../projects/python-security-research/php-vulnerability-research-scanner/README.md) and [security research dashboard](../../projects/python-security-research/security-research-dashboard/README.md) into small, reusable Python scripts in the existing domain folders. The scripts must operate on local fixtures or explicitly supplied files, never discover targets, execute payloads or contact external services.

## Script budget: 5/10

1. `SCRIPTS/03-file-data-processing/finding-export/export_findings.py` — convert sanitized finding JSON into deterministic JSON, CSV and Markdown reports. Inspired by the dashboard export endpoints. Acceptance: stable ordering, CSV quoting, empty input, malformed records and redaction of request/response bodies are tested.
2. `SCRIPTS/08-cybersecurity/scope-policy/lint_scope.py` — validate a scope document containing targets, methods, accounts and callback labels before a tool consumes it. Inspired by scanner scope controls and the dashboard scope form. Acceptance: deny-by-default behavior, unsupported methods, wildcard targets, duplicate entries, bounds and valid local fixtures are tested.
3. `SCRIPTS/20-testing-quality/finding-regression/compare_findings.py` — compare two saved finding reports and classify added, removed and changed findings using stable finding keys. Inspired by scanner evidence persistence and report review. Acceptance: deterministic comparison, severity/status changes, missing fields, duplicate keys and bounded input are tested without modifying source reports.
4. `SCRIPTS/09-automation-scripting/evidence-bundle/build_evidence_bundle.py` — assemble sanitized reports, manifests and test-condition metadata into a reproducible local evidence bundle. Inspired by scanner report storage and PHP build manifests. Acceptance: required files, path confinement, size limits, secret-pattern rejection, deterministic manifest output and missing-input errors are tested.
5. `SCRIPTS/21-software-architecture/project-contracts/check_project_contract.py` — inspect a selected project folder for required README/source comment/test conventions and emit a machine-readable compliance report. Inspired by the scanner project contracts and dashboard separation boundaries. Acceptance: pass/fail checks for required files, location metadata, usage sections, test references and ignored unrelated files are covered; it must not rewrite files.

## Shared implementation requirements

- Python standard library only unless a later plan authorizes a dependency.
- Each script has its own CLI, README usage, bounded input policy, error contract and focused tests.
- Every source and test file begins with the repository-relative purpose/location/input-output/runtime/usage/limits comment block.
- Use temporary fixtures and local files only. Do not run a scanner, launch PHP, contact a target, invoke a shell command from input, or upload evidence.
- Preserve sanitized data: reject or redact cookies, authorization headers, credentials, raw bodies and likely secrets.
- Do not create a shared runtime module until repeated behavior is demonstrated by tests.

## Acceptance criteria

- Exactly five runnable scripts are implemented if this sprint is later authorized.
- Each script has focused unit tests and documentation; tests are added to the repository suite.
- Full discovery reports passed, failed and skipped tests honestly, including the existing QA-0003 platform limitation.
- `git diff --check` passes; no secrets or generated databases are committed.
- Sprint review records deliverables, limitations, coverage changes and any deferred work.

## Deferred work

Live HTTP scanning, PHP toolchain execution, authentication for the dashboard, remote hosting, external CVE verification and additional scanner detectors remain deferred. The five script ideas below the sprint budget are not authorized by this plan.

NEXT SPRINT PREPARED - AWAITING HUMAN AUTHORIZATION.
