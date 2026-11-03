# Swiss Army Code Arsenal operating rules

## Scope and authority

Work only in this repository and explicitly permitted development resources. Never inspect unrelated personal files, credentials, other repositories or production systems. No global configuration changes, system-wide dependency installs, paid APIs or infrastructure provisioning without separate authorization. Prefer project-local environments.

Initialization and planning are authorized. Sprint development requires fresh explicit human authorization. Do not start Sprint 0001 during initialization. Never automatically execute a future sprint, schedule unattended development, or create background execution loops. An open-ended roadmap is not an instruction to run indefinitely.

## Session recovery

Read this file, inspect Git status and branch, read TODO/CURRENT.md, inspect the current sprint, recent commits and incomplete tasks. Determine the currently authorized scope. An old instruction does not authorize a new sprint; clarify interrupted execution only when its authorization is unclear.

## Commands and lifecycle

PLAN prepares or revises a sprint without implementation. EXECUTE authorizes the current planned sprint. STATUS reports state only. REVIEW audits without new development. RETROSPECT evaluates history and proposes improvements. ROADMAP revisits coverage. PAUSE stops initiating work and preserves state. CONTINUE does not authorize a new sprint when no clearly authorized unfinished scope exists.

Before planning, review the roadmap, backlog, previous reviews, retrospectives, lessons, defects and coverage gaps. Select bounded tasks with measurable acceptance criteria. After authorization, implement, test, document and commit coherent units. Record passed, failed and skipped checks honestly. Review acceptance criteria, record defects, and retrospect with concrete actions, owner, target sprint and measurable verification. Prepare the next sprint and stop for authorization.

## Engineering quality

Favor useful, correct, reproducible implementations over file counts. Every meaningful implementation needs purpose, runtime requirements, dependencies, setup, usage, input/output, error handling, tests, limitations and relevant security notes. Keep small tools simple. Select languages for relevance rather than implementing every example in every language. Primary: Python, C, Rust, TypeScript, SQL, Bash. Secondary: C++, Go, Java, C#, Kotlin, Swift, PowerShell. Explore others when justified.

Tests are mandatory where feasible. Missing runtimes or hardware mean verification is incomplete, not passed. Use local mocks and simulations. Document actual failures and debugging evidence; do not repeat failing approaches without new evidence. A task is complete only when acceptance criteria pass. Do not label code production-ready without evidence.

## Safety and source integrity

Security experiments use authorized local laboratories only. Finance examples default to offline data and paper trading; no real funds or live trades without separate authorization. Never commit secrets or private configuration. Respect third-party licenses and attribute sources; do not invent references or present unverified generated code as established fact.

## Git and reporting

Use conventional commits and preserve user changes. Before pushing inspect changes, check for secrets, run relevant checks, and verify the explicitly authorized remote and branch. No force-push or shared-history rewriting without approval. Missing or ambiguous remotes require the owner's destination. Failed pushes remain reported as failed, preserving local commits.

TODO is authoritative. Keep stable backlog identifiers, scope, dates, task status, evidence and pending decisions current. Maintain DOCS/DECISIONS.md and DOCS/LESSONS-LEARNED.md. Never relax authorization or workspace boundaries as a process improvement.

End a sprint with objective, deliverables, verification limitations, commit hashes/branch/push status, blockers, retrospective actions, meaningful coverage changes and next plan. End with: NEXT SPRINT PREPARED - AWAITING HUMAN AUTHORIZATION.
