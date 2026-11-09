# Finding confidence scorer

File: `SCRIPTS/08-cybersecurity/finding-confidence/README.md`

Folder: `SCRIPTS/08-cybersecurity/finding-confidence`

`score_finding.py` converts bounded evidence-quality labels and an analyst-supplied impact label into deterministic triage metadata. It always emits `confirmed: false`; it does not test targets or establish exploitability.

Example: `python SCRIPTS/08-cybersecurity/finding-confidence/score_finding.py "{\"evidence\":[{\"kind\":\"response\",\"quality\":\"strong\"},{\"kind\":\"fixture\",\"quality\":\"strong\"}],\"impact\":\"high\"}"`
