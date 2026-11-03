# Testing Standards

Use unit tests for algorithms; integration checks for local services and databases; property checks for parsers where useful; compilation checks for compiled code; controlled fuzzing for security-sensitive boundaries; benchmarks for measured performance claims. External integrations use local mocks. Hardware uses simulation where possible.

Cover normal inputs, boundaries, invalid inputs and error behavior. Isolate filesystem tests in temporary directories. Record exact commands, runtime versions and passed/failed/skipped outcomes. Missing tools or hardware mean incomplete verification. Do not claim unrun tests passed. CI should run the same commands locally documented, with minimum permissions and no unnecessary secrets.
