# Python security research workspace

File: `projects/python-security-research/README.md`

Folder: `projects/python-security-research`

This workspace contains two independent, custom Python security-research projects:

- [Web vulnerability scanner](web-vulnerability-scanner/README.md): bounded HTTP/API detection for explicitly authorized web targets.
- [PHP vulnerability research scanner](php-vulnerability-research-scanner/README.md): static analysis and controlled testing of locally built PHP versions.
- [Security research dashboard](security-research-dashboard/README.md): local-only scope management, finding review and export UI for both scanners.

The projects may reuse general-purpose components for scope enforcement, request throttling, evidence normalization, database migrations and report serialization. Detection modules, databases, reports and project-specific tests remain separate. No commercial scanner, vulnerability-scanning CLI, paid API or hosted target is a dependency.

Both the web scanner MVP and PHP research scanner MVP have been delivered as local-fixture implementations. Work is limited to local laboratories, synthetic fixtures and assets/accounts/callback endpoints that the owner has explicitly permitted.

## Planned layout

```text
projects/python-security-research/
  shared/                         # future reusable safe infrastructure
  web-vulnerability-scanner/      # Scanner 1 code, DB, reports and tests
  php-vulnerability-research-scanner/ # Scanner 2 code, DB, reports and tests
  security-research-dashboard/    # local dashboard for scope, findings and exports
  docs/                           # research protocols and evidence policy
```

The shared layer must not contain vulnerability-specific detection logic. Each scanner owns its migrations, finding lifecycle, reports and acceptance tests; the dashboard reads those scanner databases without executing scans.
