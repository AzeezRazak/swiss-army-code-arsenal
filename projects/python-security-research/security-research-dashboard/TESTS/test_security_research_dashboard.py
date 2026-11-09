# Purpose: Test scope persistence, scanner finding aggregation and dashboard exports.
# Location: projects/python-security-research/security-research-dashboard/TESTS/test_security_research_dashboard.py
# Input/output: temporary SQLite fixtures and HTTP requests; emits unittest results.
# Requirements: Python 3.10+, standard library only.
# Usage from root: python -m unittest projects/python-security-research/security-research-dashboard/TESTS/test_security_research_dashboard.py
# Limits: tests local behavior only; it never contacts a target or starts a public server.
"""Focused tests for the local security research dashboard."""
from __future__ import annotations

import importlib.util
import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("security_research_dashboard_app", APP_PATH)
app = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(app)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.scope_db = root / "dashboard.sqlite3"
        self.web_db = root / "web.sqlite3"
        self.php_db = root / "php.sqlite3"
        for database, module, finding in (
            (self.web_db, "xss", {"status": "signal", "severity": "high", "summary": "reflection"}),
            (self.php_db, "lifecycle", {"status": "review", "severity": "medium", "summary": "cleanup path"}),
        ):
            connection = sqlite3.connect(database)
            try:
                connection.execute("CREATE TABLE findings (id INTEGER PRIMARY KEY, module TEXT, finding_json TEXT NOT NULL)")
                connection.execute("INSERT INTO findings(module, finding_json) VALUES (?, ?)", (module, json.dumps(finding)))
                connection.commit()
            finally:
                connection.close()
        self.store = app.DashboardStore(self.scope_db, {"web": self.web_db, "php": self.php_db})

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scope_is_validated_and_persisted(self):
        saved = self.store.save_scope({"targets": ["https://example.test"], "methods": ["get"], "notes": "authorized"})
        self.assertEqual(saved["methods"], ["GET"])
        self.assertEqual(self.store.get_scope(), saved)
        with self.assertRaises(ValueError):
            self.store.save_scope({"methods": ["TRACE"]})

    def test_findings_and_exports_are_combined(self):
        findings = self.store.findings()
        self.assertEqual({item["scanner"] for item in findings}, {"web", "php"})
        content_type, body, filename = app.export_findings(findings, "csv")
        self.assertIn("text/csv", content_type)
        self.assertEqual(filename, "findings.csv")
        self.assertIn("xss", body)
        self.assertIn("lifecycle", body)

    def test_http_scope_and_summary_endpoints(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), app.make_handler(self.store))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            connection = HTTPConnection("127.0.0.1", server.server_port, timeout=3)
            connection.request("GET", "/api/summary")
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read())["total"], 2)
            payload = json.dumps({"targets": ["http://local.test"], "methods": ["HEAD"]})
            connection.request("POST", "/api/scope", payload, {"Content-Type": "application/json"})
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read())["methods"], ["HEAD"])
            connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
