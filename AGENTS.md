# Swiss Army Code Arsenal operating rules

File: `AGENTS.md`

Folder: `.`


## Scope and authority

Work only in this repository and explicitly permitted development resources. Never inspect unrelated personal files, credentials, other repositories or production systems. No global configuration changes, system-wide dependency installs, paid APIs or infrastructure provisioning without separate authorization. Prefer project-local environments.

Initialization and planning are authorized. Sprint development requires fresh explicit human authorization. Do not start Sprint 0001 during initialization. Never automatically execute a future sprint, schedule unattended development, or create background execution loops. An open-ended roadmap is not an instruction to run indefinitely.

## Session recovery

Read this file, inspect Git status and branch, read TODO/CURRENT.md, inspect the current sprint, recent commits and incomplete tasks. Determine the currently authorized scope. An old instruction does not authorize a new sprint; clarify interrupted execution only when its authorization is unclear.

## Commands and lifecycle

PLAN prepares or revises a sprint without implementation. EXECUTE authorizes the current planned sprint. STATUS reports state only. REVIEW audits without new development. RETROSPECT evaluates history and proposes improvements. ROADMAP revisits coverage. PAUSE stops initiating work and preserves state. CONTINUE does not authorize a new sprint when no clearly authorized unfinished scope exists.

Before planning, review the roadmap, backlog, previous reviews, retrospectives, lessons, defects and coverage gaps. Select bounded tasks with measurable acceptance criteria. After authorization, implement, test, document and commit coherent units. Record passed, failed and skipped checks honestly. Review acceptance criteria, record defects, and retrospect with concrete actions, owner, target sprint and measurable verification. Prepare the next sprint and stop for authorization.

## Sprint size limit

From Sprint 0003 onward, each development sprint TODO must include at least five and at most ten runnable script deliverables in total, across all tasks. Count separate client/server scripts and language variants individually. Tests, documentation, fixtures and non-runnable support modules do not count. List the scripts and total in the sprint plan; defer additional scripts to a later sprint. The backlog is not subject to this per-sprint limit. Prioritize fundamental Python for Sprint 0003 and the next few proposals until the owner redirects the focus. Historical sprint sizes remain unchanged.

## Engineering quality

Favor useful, correct, reproducible implementations over file counts. Every meaningful implementation needs purpose, runtime requirements, dependencies, setup, usage, input/output, error handling, tests, limitations and relevant security notes. Keep small tools simple. Select languages for relevance rather than implementing every example in every language. Primary: Python, C, Rust, TypeScript, SQL, Bash. Secondary: C++, Go, Java, C#, Kotlin, Swift, PowerShell. Explore others when justified.

Tests are mandatory where feasible. Missing runtimes or hardware mean verification is incomplete, not passed. Use local mocks and simulations. Document actual failures and debugging evidence; do not repeat failing approaches without new evidence. A task is complete only when acceptance criteria pass. Do not label code production-ready without evidence.

## Source comments and document locations

Every script, support module and test file must start with a comment block stating purpose, repository-relative file location, inputs/outputs, runtime/dependencies, usage and important limits. Add clear adjacent comments explaining what each meaningful operation or small related block does; explain algorithm steps, validation, errors, I/O, side effects and cleanup. Keep comments accurate when code changes.

Every document, including sprint records and templates, must state its repository-relative file path and containing folder near the top. Root files use folder `.`. Templates identify their own location and require the generated document location to be filled in. Use repository-relative links in documents, and include folder-qualified file links in user-facing reports.

## Safety and source integrity

Security experiments use authorized local laboratories only. Finance examples default to offline data and paper trading; no real funds or live trades without separate authorization. Never commit secrets or private configuration. Respect third-party licenses and attribute sources; do not invent references or present unverified generated code as established fact.

## Git and reporting

Use conventional commits and preserve user changes. Before pushing inspect changes, check for secrets, run relevant checks, and verify the explicitly authorized remote and branch. No force-push or shared-history rewriting without approval. Missing or ambiguous remotes require the owner's destination. Failed pushes remain reported as failed, preserving local commits.

TODO is authoritative. Keep stable backlog identifiers, scope, dates, task status, evidence and pending decisions current. Maintain DOCS/DECISIONS.md and DOCS/LESSONS-LEARNED.md. Never relax authorization or workspace boundaries as a process improvement.

End a sprint with objective, deliverables, verification limitations, commit hashes/branch/push status, blockers, retrospective actions, meaningful coverage changes and next plan. End with: NEXT SPRINT PREPARED - AWAITING HUMAN AUTHORIZATION.

## Multi-language projects

When the owner requests a multi-language project, place it in `projects/<project-name>/` at the repository root. Keep all scripts, source, tests and configuration for that project inside its subfolder. Include a README describing language roles, setup, interfaces, usage, tests and limitations. Apply the same comment and document-location standards. Link project entries from DOCS/CATALOG.md and maintain management records in TODO. Creating the projects folder alone does not authorize project implementation.

## Dated transcripts

Maintain `transcripts/YYYY-MM-DD.md` using Asia/Singapore dates. Append the owner's messages, exact executed shell commands/tool actions, working directory/branch, and observed results including failures, retries, skips and commit/push outcomes. Record known timestamps only; do not invent them. Label historical reconstructions, summaries and omitted payloads explicitly. Redact credentials and unnecessary personal identifiers visibly. Never include hidden reasoning or confidential system/developer instructions. Keep File/Folder metadata and relative links; follow transcripts/README.md. Update the day's record before final reporting; do not claim unexecuted operations succeeded.

## Ongoing project record maintenance

During every project interaction, update the dated transcript without requiring a separate reminder, including questions/decisions, implementation, reviews, tests, failures, commits and publication outcomes. Update affected project records (current state, backlog, catalog, decisions, sprint documents and usage guides) when facts change. Do not rewrite unaffected historical records merely to touch every file.

The owner authorized publishing these redacted project transcripts to the existing public repository on 2026-11-05. Include them with authorized project commits/pushes. This is a working practice for agents reading AGENTS.md, not a background recorder or scheduled automation. Activity performed outside the available session is not automatically observed; add it only when evidence is provided, with its source identified. Do not claim complete capture of unavailable sessions or external actions.
