# Purpose: verify Sprint 0006 offline security-research foundation utilities.
# Location: TESTS/test_security_foundations.py
# Input/output: synthetic JSON and temporary files to unittest results; no network access.
# Requirements: Python 3.10+, standard library only.
# Usage: python -m unittest TESTS.test_security_foundations -v
# Limits: tests exercise local functions and subprocesses only.
"""Boundary and CLI tests for reusable scanner-support utilities."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(relative, name):
    # Import each standalone script without executing its command-line entry point.
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SecurityFoundationTests(unittest.TestCase):
    def test_scope_allowlist(self):
        module = load("SCRIPTS/08-cybersecurity/scope-allowlist/validate_scope.py", "scope")
        self.assertEqual(module.validate_scope({"hosts": ["app.test", "app.test"], "paths": ["/api"], "callbacks": []})["hosts"], ["app.test"])
        with self.assertRaises(ValueError):
            module.validate_scope({"hosts": ["*.test"]})

    def test_finding_score(self):
        module = load("SCRIPTS/08-cybersecurity/finding-confidence/score_finding.py", "score")
        result = module.score_finding({"evidence": [{"quality": "strong"}, {"quality": "strong"}], "impact": "high"})
        self.assertEqual(result["confidence"], "high")
        self.assertFalse(result["confirmed"])

    def test_evidence_validation(self):
        module = load("SCRIPTS/03-file-data-processing/evidence-jsonl/validate_evidence.py", "evidence")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.jsonl"
            record = {"run_id": "r1", "timestamp": "2026-11-09T00:00:00Z", "module": "fixture", "summary": "redacted", "redacted": True}
            path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            self.assertEqual(module.validate_file(path), {"valid": 1, "lines": 1})

    def test_budget_plan(self):
        module = load("SCRIPTS/09-automation-scripting/request-budget-plan/build_rate_plan.py", "budget")
        plan = module.build_plan(5, 2, 2, 4096)
        self.assertEqual([batch["requests"] for batch in plan["batches"]], [2, 2, 1])
        with self.assertRaises(ValueError):
            module.build_plan(1, 0, 0, 1)

    def test_fixture_replay(self):
        module = load("SCRIPTS/20-testing-quality/fixture-replay/replay_fixture.py", "replay")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps({"observations": [{"baseline": {"status": 200, "body": "ok"}, "test": {"status": 200, "body": "changed"}}]}), encoding="utf-8")
            result = module.replay_fixture(path)
            self.assertTrue(result["results"][0]["length_changed"])

    def test_documented_cli_examples(self):
        commands = [
            ("SCRIPTS/08-cybersecurity/scope-allowlist/validate_scope.py", ['{"hosts":["app.test"],"paths":["/api"]}']),
            ("SCRIPTS/08-cybersecurity/finding-confidence/score_finding.py", ['{"evidence":[{"quality":"strong"}],"impact":"low"}']),
            ("SCRIPTS/09-automation-scripting/request-budget-plan/build_rate_plan.py", ["--requests", "2", "--interval", "1", "--concurrency", "1", "--body-bytes", "10"]),
        ]
        for script, args in commands:
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(ROOT / script), *args], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                json.loads(result.stdout)


if __name__ == "__main__":
    unittest.main()
