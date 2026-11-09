# Evidence JSONL validator

File: `SCRIPTS/03-file-data-processing/evidence-jsonl/README.md`

Folder: `SCRIPTS/03-file-data-processing/evidence-jsonl`

`validate_evidence.py` checks bounded JSONL records for provenance fields, UTF-8 validity, line limits and explicit redaction. It rejects sensitive field names and never rewrites the evidence file.

Example: `python SCRIPTS/03-file-data-processing/evidence-jsonl/validate_evidence.py evidence.jsonl`
