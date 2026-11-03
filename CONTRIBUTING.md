# Contributing

File: `CONTRIBUTING.md`

Folder: `.`


Use the [operating rules](AGENTS.md) and an explicitly authorized sprint. Select a backlog item, define acceptance criteria, and keep changes inside its scope. Do not start development during planning.

Each implementation must document purpose, language/runtime, dependencies, setup, commands, input/output, error behavior, tests, limitations and relevant security considerations. Prefer standard libraries and isolated dependencies. Use synthetic fixtures and local mocks.

Run appropriate checks and record exact commands, outcomes and skipped checks in the sprint execution log. Update the catalog only for delivered implementations; mark verification separately. Review changed files for secrets and license issues, then create coherent conventional commits. Push only to the owner's authorized destination.

Add unresolved work to the backlog. Record concrete retrospective actions and verify their effectiveness in later sprints. See [testing standards](DOCS/TESTING-STANDARDS.md).

Before review, confirm every changed script has a purpose/location/input/output/setup/usage/limits comment block, clear comments for meaningful operations, and every document has File and Folder metadata.
