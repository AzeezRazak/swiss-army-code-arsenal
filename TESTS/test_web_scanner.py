# Purpose: verify the local-fixture web scanner MVP, storage and redaction behavior.
# Location: TESTS/test_web_scanner.py
# Input/output: synthetic JSON fixtures, temporary SQLite/report files and subprocess results.
# Requirements: Python 3.10+, standard library only; no network access.
# Usage: python -m unittest TESTS.test_web_scanner -v
# Limits: all observations are inert local fixtures; no live target verification is claimed.
"""Positive, negative, ambiguous and CLI tests for the web scanner MVP."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / "projects/python-security-research/web-vulnerability-scanner"


def load(name):
    # Add the project directory so detector scripts can import sibling support modules.
    sys.path.insert(0, str(BASE))
    try:
        spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def observation(body="ok", status=200, headers=None, cookies=None, url="http://app.test/item"):
    return {"status": status, "headers": headers or {}, "body": body, "cookies": cookies or [], "url": url}


class WebScannerTests(unittest.TestCase):
    def test_observer_bounds_and_normalizes(self):
        module = load("observation")
        result = module.normalize_observation(observation(headers={"Content-Type": "text/plain"}))
        self.assertEqual(result["headers"], {"content-type": "text/plain"})
        with self.assertRaises(ValueError):
            module.normalize_observation(observation(body="x" * 70_000))

    def test_sqli_positive_and_negative(self):
        module = load("sqli_detector")
        positive = {"baseline": observation(), "tests": [observation("sqlite error: near input", 500)]}
        self.assertEqual(module.detect(positive)[0]["confidence"], "high")
        self.assertEqual(module.detect({"baseline": observation("same"), "tests": [observation("same")] }), [])

    def test_xss_reflection_context(self):
        module = load("xss_detector")
        result = module.detect({"marker": "MARK", "observations": [observation("<p>MARK</p>")]})
        self.assertEqual(result[0]["evidence"]["context"], "html-text")
        self.assertEqual(module.detect({"marker": "MARK", "observations": [observation("clean")]}), [])

    def test_idor_comparison(self):
        module = load("idor_detector")
        fixture = {"resource": "/api/order/1", "account_a": observation("order"), "account_b": observation("order")}
        self.assertEqual(module.detect(fixture)[0]["id"], "idor-1")
        fixture["account_b"] = observation("forbidden", 403)
        self.assertEqual(module.detect(fixture), [])

    def test_misconfiguration_and_cookie_redaction(self):
        module = load("misconfiguration_detector")
        findings = module.detect(observation(headers={}, cookies=[{"name": "sid", "secure": False, "httponly": False, "samesite": ""}], url="https://app.test"))
        self.assertTrue(any(item["id"] == "misconfig-hsts" for item in findings))
        with tempfile.TemporaryDirectory() as directory:
            storage = load("web_storage")
            payload = storage.save_findings(Path(directory) / "db.sqlite3", Path(directory) / "report.json", "test", [{"evidence": {"token": "secret", "ok": True}}])
            self.assertEqual(payload["findings"][0]["evidence"]["token"], "[REDACTED]")

    def test_detector_cli_writes_database_and_report(self):
        fixture = {"marker": "MARK", "observations": [observation("MARK")]}
        with tempfile.TemporaryDirectory() as directory:
            fixture_path = Path(directory) / "xss.json"
            database = Path(directory) / "scanner.sqlite3"
            report = Path(directory) / "report.json"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")
            result = subprocess.run([sys.executable, str(BASE / "xss_detector.py"), str(fixture_path), "--database", str(database), "--report", str(report)], capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(database.exists())
            self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["findings"][0]["status"], "signal")

    def test_single_entry_point_runs_all_detectors(self):
        fixture = {
            "sqli": {"baseline": observation(), "tests": [observation("sqlite error", 500)]},
            "xss": {"marker": "MARK", "observations": [observation("<p>MARK</p>")]},
            "idor": {"resource": "/api/order/1", "account_a": observation("order"), "account_b": observation("order")},
            "misconfiguration": observation(url="https://app.test"),
        }
        with tempfile.TemporaryDirectory() as directory:
            fixture_path = Path(directory) / "scan.json"
            database = Path(directory) / "scanner.sqlite3"
            report = Path(directory) / "web_scan.json"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")
            result = subprocess.run([sys.executable, str(BASE / "http_observer.py"), str(fixture_path), "--database", str(database), "--report", str(report)], capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["module"], "web-scanner")
            self.assertGreaterEqual(len(payload["findings"]), 4)


if __name__ == "__main__":
    unittest.main()
