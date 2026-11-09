# Python security research scanner specification

File: `projects/python-security-research/SPECIFICATION.md`

Folder: `projects/python-security-research`

Status: web scanner MVP delivered under Sprint 0007; PHP research scanner remains proposed and unimplemented.

## 1. Objectives and boundaries

The workspace will host two independent Python scanners. Scanner 1 observes web and API behavior through bounded HTTP requests. Scanner 2 studies PHP internals through source analysis and locally built, instrumented PHP binaries. Both systems produce evidence-backed hypotheses for manual validation; neither claims that a signal is an exploitable vulnerability or an eligible bounty report.

Permitted inputs must be explicit allowlists: target URLs or local services, paths, methods, test accounts, callback endpoints, PHP source trees, build artifacts and test duration. The default mode is dry-run or local-fixture mode. There is no unauthenticated Internet discovery, credential guessing, destructive payload, persistence action, shell command injection, real-money action or automatic report submission.

The CVE identifiers `CVE-2026-109618` and `CVE-2026-109619` are research intake labels only until their advisories, affected versions, patches and reproduction conditions are verified from primary sources. The scanner must not present unverified identifiers as confirmed facts.

## 2. Workspace architecture

`shared/` may provide:

- `scope.py`: exact host/path/account/callback allowlists and deny-by-default checks.
- `transport.py`: timeout, redirect, body-size, concurrency and request-budget enforcement for HTTP fixtures or explicitly permitted local targets.
- `evidence.py`: sanitized request/response excerpts, hashes, timestamps, test conditions and provenance.
- `finding_schema.py`: common identifiers, confidence, severity, status, references and manual-verification steps.
- `storage.py`: migrations and serialization helpers only; each scanner still owns a separate database file and migration history.
- `reports.py`: deterministic JSON/Markdown export with redaction and no secret-bearing raw payloads.

No shared module may make a vulnerability decision for both scanners. Scanner-specific logic consumes normalized observations and records why a detector fired.

## 3. Scanner 1 — web vulnerability scanner

Project folder: `web-vulnerability-scanner/`.

Owns `web_scanner.sqlite3`, detector modules, web fixtures, scanner-specific tests and reports. The initial detector interface should accept a baseline observation plus bounded test observations and return zero or more findings with evidence and confidence.

Planned modules:

1. `sqli`: compare controlled input responses, status/body/length/timing variance and database-error indicators without destructive statements.
2. `xss`: detect reflected markers and classify the observed output context; do not claim execution from reflection alone.
3. `idor_bola`: compare the same permitted resource request across two explicitly authorized accounts and record authorization deltas.
4. `ssrf`: use only an owner-controlled callback endpoint or local sink, with unique non-sensitive correlation tokens and strict target allowlists.
5. `path_traversal`: use harmless local fixtures and canonical-path comparisons; never read arbitrary host files.
6. `sensitive_disclosure`: check explicitly permitted files/endpoints for debug traces, exposed metadata and secret-like patterns, storing redacted matches only.
7. `cors`: compare preflight and simple responses for origin reflection, credential policy and allowed-method/header inconsistencies.
8. `authentication`: inspect session rotation, cookie flags, logout invalidation and access-control behavior using supplied accounts; no password attacks.
9. `file_upload`: use inert, non-executable fixture files to evaluate type, size, naming, storage and retrieval controls.
10. `misconfiguration`: inspect security headers, cookie attributes, unsafe methods, verbose errors and transport settings.

Each detector must have positive, negative and ambiguous fixtures, a request budget, a false-positive explanation and a manual verification checklist. Findings require observable evidence; a response difference alone is not proof of impact.

## 4. Scanner 2 — PHP vulnerability research scanner

Project folder: `php-vulnerability-research-scanner/`.

Owns `php_research.sqlite3`, source snapshots, build metadata, sanitizer logs, minimized local fixtures and research reports. Dynamic tests run only against locally built PHP versions under a process timeout and resource limit.

Planned modules:

1. `cve_2026_109618`: version/patch/source-intake analysis and a gated local reproduction harness after primary-source verification.
2. `cve_2026_109619`: the same evidence lifecycle, kept independent from the first CVE.
3. `request_initialization`: trace setup and partial initialization paths across controlled requests.
4. `allocation_failures`: inject deterministic allocator failures in a test build or harness and inspect error paths.
5. `cleanup_destruction`: exercise teardown and cleanup ordering under normal and failed requests.
6. `worker_lifecycle`: compare worker reuse, request isolation and reset behavior across repeated local requests.
7. `uaf_dangling`: use sanitizers and minimized local inputs to identify lifetime violations without exploit development.
8. `double_free_corruption`: use allocator/sanitizer diagnostics and stop on first memory-safety signal.
9. `partial_initialization`: test error handling and object state after deliberately controlled initialization failures.
10. `source_patch_compare`: compare verified vulnerable/fixed revisions and generate reviewable changed-code hypotheses.

The dynamic harness must record compiler flags, PHP commit/version, extensions, OS/runtime, sanitizer configuration, input hash, exit status and bounded logs. It must not generate weaponized payloads, bypass access controls or run against third-party systems.

## 5. Databases, reports and finding lifecycle

Each scanner has a separate SQLite database with migrations for `targets`, `runs`, `observations`, `findings`, `evidence`, `references`, `manual_reviews` and `report_history`. Database files are local artifacts and must never contain credentials, session cookies, raw authorization headers or unredacted secrets.

Every finding includes: stable ID, scanner/module, target fingerprint, run ID, timestamp, detector version, observation summary, sanitized evidence references, confidence (`low|medium|high`), severity (`informational|low|medium|high|critical`), affected scope, reproduction prerequisites, limitations, manual validation steps and reference status. Reports are deterministic JSON and Markdown exports. A finding may move from `signal` to `triage`, `confirmed`, `false_positive`, `accepted_risk` or `closed`; only a human may mark it confirmed.

## 6. Testing methodology

Use unit tests for parsers, scope checks, redaction, scoring and detector decision tables. Use local mock HTTP services and synthetic accounts for Scanner 1. Use temporary PHP source trees, locally compiled fixtures and sanitizer-enabled test binaries for Scanner 2. Add regression fixtures for every accepted signal and every known false positive. Test timeouts, size limits, rate limits, redirects, malformed responses, partial initialization, process crashes and cleanup.

The baseline acceptance gate is deterministic local execution with no external network dependency, no secrets, bounded runtime and complete evidence provenance. Missing PHP toolchains or sanitizer support are incomplete verification, never a pass.

## 7. Local LLM assistance

A local LLM may summarize sanitized findings, suggest false-positive questions and rank manual verification work. It receives structured observations, not credentials or raw secrets. Its output is advisory, stored with model/version/prompt metadata, and cannot change scope, execute tests or mark a finding confirmed.

## 8. Documentation and security requirements

Each implementation file must carry purpose, location, inputs/outputs, runtime/dependencies, usage and limits. Each project README must document setup, interfaces, tests, failure handling and limitations. Every report must state authorization scope, test conditions, evidence quality and unverified assumptions. The projects are research tooling, not production-ready scanners or proof of exploitability.
