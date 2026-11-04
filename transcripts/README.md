# Conversation and command transcripts

File: `transcripts/README.md`

Folder: `transcripts`

One file per local date, named YYYY-MM-DD.md, using Asia/Singapore time. Entries record the owner's messages, assistant actions/commands, observed results, failures/skips and commit references. These are activity records, not hidden reasoning or system/developer instructions.

## Dates

- [2026-11-04](2026-11-04.md): initialization, Sprints 0001/0002 and first GitHub publication.
- [2026-11-05](2026-11-05.md): standards, Sprint 0003, maintenance branch, project organization and transcript setup.

Historical entries were reconstructed from the conversation available on 2026-11-05. Date grouping follows supplied local-date context; exact message times are unavailable. Quoted user text is preserved where available. Attachment contents and long generated code payloads are summarized explicitly; this is not a complete raw transcript or exhaustive historical shell audit. No commands/results are invented to fill gaps.

## Recording standard going forward

Append one numbered entry per request, preserving order. Include:

1. Local date/time when actually known; otherwise say unavailable.
2. User message verbatim, with visible redactions if necessary.
3. Working directory and branch; purpose of the action.
4. Exact shell commands and relevant tool actions in order, including failures and retries. Keep multiline payloads intact when practical; explicitly label any omission or summary and link changed files or commits.
5. Observed exit status, concise output, test totals, skips, changed files and commit/push outcome. Distinguish planned actions from completed actions.

Never record credentials, authentication tokens, passwords, private keys or session cookies. Redact personal identifiers not necessary for the work and mark the redaction. Do not record hidden internal reasoning or confidential instructions. Keep existing history; append corrections rather than silently rewriting outcomes. Update the current day's file before the final response. A transcript cannot contain its own final commit hash until a later entry; reference the commit subject or add the hash subsequently.

## Ongoing project record maintenance

During every project interaction, update the dated transcript without requiring a separate reminder, including questions/decisions, implementation, reviews, tests, failures, commits and publication outcomes. Update affected project records (current state, backlog, catalog, decisions, sprint documents and usage guides) when facts change. Do not rewrite unaffected historical records merely to touch every file.

The owner authorized publishing these redacted project transcripts to the existing public repository on 2026-11-05. Include them with authorized project commits/pushes. This is a working practice for agents reading AGENTS.md, not a background recorder or scheduled automation. Activity performed outside the available session is not automatically observed; add it only when evidence is provided, with its source identified. Do not claim complete capture of unavailable sessions or external actions.
