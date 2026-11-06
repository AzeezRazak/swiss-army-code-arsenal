# Decisions

File: `DOCS/DECISIONS.md`

Folder: `DOCS`


## DEC-0001 - Repository root (2026-11-04)

Use the owner-selected Swiss directory directly, avoiding a redundant nested repository. Inspection found an empty folder without Git configuration.

## DEC-0002 - Initial sprint size

Propose five offline Python/SQL implementations to validate testing and documentation discipline before expanding runtimes. Broad simultaneous language bootstrapping was deferred to keep the first sprint verifiable.

## DEC-0003 - Explicit pending choices

Owner chose local-only Git and supplied an email. Use repository-local author azeezshahrizal with the supplied email; license remains pending. No remote or push configured.

## DEC-0004 - Domain discoverability

Provide one concise scope README per requested domain. This preserves the requested architecture in Git without falsely counting empty categories as implemented coverage.

## DEC-0005 - Public GitHub publication (2026-11-04)

The owner superseded local-only operation by explicitly requesting a new public repository and push. Created AzeezRazak/swiss-army-code-arsenal, configured origin and published main with upstream tracking. All 16 tests passed before publication. License remains undecided; historical local-only sprint records describe the state at sprint completion. Sprint 0002 remains unauthorized.

## DEC-0006 - Bounded Sprint 0002 interfaces

Keep the network example as two runnable scripts plus a non-runnable framing module; inventory is the third script (3/5). Use fixed loopback addresses, single exchanges, maximum payload and absolute receive deadlines. Inventory rejects linked roots and lists links without traversal; path races remain documented limitations.

## DEC-0007 - Explanatory source and document locations

Owner requested purpose blocks, clear comments explaining operations, and file locations in documents. Applied to all existing Python/SQL source and tests, and all tracked Markdown documents plus the license placeholder. Persisted requirements in operating/coding standards, contribution guidance and sprint templates. No new runnable scripts or sprint execution. Validation: unchanged Python ASTs; 31 tests passed, one existing symlink skip; file locations, links and whitespace checked.

## DEC-0008 - Fundamental Python and revised sprint size

On 2026-11-05 the owner authorized revising/executing Sprint 0003 around fundamental Python and replaced the prior cap with minimum five/maximum ten runnable scripts per future development sprint. Deliver five focused lessons now; prioritize Python fundamentals in the next few proposals. Deferred DATA-0002 and COMP-0002. Historical sprint sizes are unchanged.

## DEC-0009 - Sprint 0004 execution

On 2026-11-06 the owner authorized `execute next sprint`. Sprint 0004 delivered five standard-library Python fundamentals scripts, with paired CLI tests and explicit input limits. DATA-0002 and COMP-0002 remain deferred while the owner-selected Python focus continues.
