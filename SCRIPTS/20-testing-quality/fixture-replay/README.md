# Deterministic fixture replay

File: `SCRIPTS/20-testing-quality/fixture-replay/README.md`

Folder: `SCRIPTS/20-testing-quality/fixture-replay`

`replay_fixture.py` compares saved baseline/test HTTP observations using status, body length and SHA-256 differences. It reads local JSON only, rejects oversized data and never executes fixture code or contacts a URL.

Example fixture: `{\"observations\":[{\"id\":\"case-1\",\"baseline\":{\"status\":200,\"body\":\"ok\"},\"test\":{\"status\":200,\"body\":\"changed\"}}]}`
