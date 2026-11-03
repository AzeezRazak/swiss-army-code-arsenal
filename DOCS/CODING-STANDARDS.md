# Coding Standards

File: `DOCS/CODING-STANDARDS.md`

Folder: `DOCS`


Every meaningful implementation documents purpose, runtime versions, dependencies, setup, usage, input/output, errors, tests, limitations and security where relevant. Prefer idiomatic standard-library code with explicit interfaces, deterministic examples and actionable errors. Avoid unnecessary abstraction.

Use descriptive names and language-appropriate formatting. Validate boundary inputs; avoid destructive defaults. Keep language ports justified by educational or technical value. Any language comparison should discuss performance, memory management, typing, concurrency, errors, ecosystem, portability, security and maintainability with evidence.

## Required script comment block

Start all runnable scripts, support modules and tests with the language's comment syntax. Include purpose, repository-relative file location, inputs and outputs, runtime/dependencies, usage from the repository root and important limitations. SQL scripts use -- comments; preserve required shebangs or encoding declarations before the block.

## Explanatory comments

Explain what each meaningful line or small related block is doing in plain language. Cover algorithm updates, bounds, validation, error paths, parsing, filesystem/network/database effects, output format and cleanup. Explain why a non-obvious choice is needed. Simple related declarations can share one comment. Keep comments synchronized with code and do not claim behavior or guarantees that are not implemented.

## Document locations

Near the top of every document include `File: <repository-relative path>` and `Folder: <repository-relative parent>`. Root documents use `Folder: .`. Use forward slashes and relative Markdown links so locations remain valid after cloning. Sprint templates must carry their own location plus an instruction to set the generated file's actual location. Reports must name folder-qualified linked paths when referring to files.
