# Purpose: verify the single-command PHP research scanner and its local analysis modules.
# Location: TESTS/test_php_scanner.py
# Input/output: temporary source trees/logs/SQLite/report fixtures to unittest results.
# Requirements: Python 3.10+, standard library only; no PHP toolchain or network.
# Usage: python -m unittest TESTS.test_php_scanner -v
# Limits: all inputs are inert local fixtures; no source or log content is executed.
"""Positive, negative and integration tests for the PHP research MVP."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / "projects/python-security-research/php-vulnerability-research-scanner"


def load(name):
    # Import a research module without invoking the scanner command-line entry point.
    sys.path.insert(0, str(BASE))
    try:
        spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


class PHPResearchTests(unittest.TestCase):
    def test_cve_intake_stays_unconfirmed(self):
        result = load("cve_intake").analyze({"references": [{"id": "CVE-2026-109618", "source": "pending-primary-source"}]})
        self.assertFalse(result[0]["confirmed"])
        with self.assertRaises(ValueError):
            load("cve_intake").analyze({"references": [{"id": "not-cve"}]})

    def test_patch_compare(self):
        with tempfile.TemporaryDirectory() as directory:
            before = Path(directory) / "before"
            after = Path(directory) / "after"
            before.mkdir()
            after.mkdir()
            (before / "zend.c").write_text("old", encoding="utf-8")
            (after / "zend.c").write_text("new", encoding="utf-8")
            result = load("patch_compare").analyze(before, after)
            self.assertEqual(result[0]["evidence"]["modified"], ["zend.c"])

    def test_lifecycle_and_sanitizer(self):
        lifecycle = load("lifecycle_analyzer").analyze("request_start\ninitialize_error\n")
        self.assertEqual(lifecycle[0]["status"], "signal")
        sanitizer = load("sanitizer_parser").analyze("ERROR: AddressSanitizer: use-after-free")
        self.assertEqual(sanitizer[0]["evidence"]["signal"], "use-after-free")

    def test_source_risk_analyzer_flags_local_flow_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "index.php"
            source.write_text("<?php\n$name = $_GET['name'];\neval($name);\n", encoding="utf-8")
            result = load("source_risk_analyzer").analyze(directory)
            self.assertEqual(result[0]["evidence"]["category"], "dynamic-code")
            self.assertFalse(result[0]["confirmed"])

    def test_build_manifest_redacts_policy_by_rejection(self):
        module = load("build_manifest")
        result = module.analyze({"php_version": "8.x", "compiler": "clang", "commit": "abc", "flags": ["-O1"], "extensions": ["core"]})
        self.assertEqual(result[0]["module"], "build-manifest")
        with self.assertRaises(ValueError):
            module.analyze({"php_version": "8.x", "compiler": "clang", "commit": "abc", "flags": [], "extensions": [], "token": "secret"})

    def test_single_entry_point_runs_all_modules(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = root / "before"
            after = root / "after"
            before.mkdir()
            after.mkdir()
            (before / "engine.c").write_text("old", encoding="utf-8")
            (after / "engine.c").write_text("new", encoding="utf-8")
            lifecycle = root / "lifecycle.log"
            sanitizer = root / "sanitizer.log"
            lifecycle.write_text("request_start\ninitialize\ncleanup\nrequest_end\n", encoding="utf-8")
            sanitizer.write_text("no sanitizer errors", encoding="utf-8")
            bundle = root / "bundle.json"
            bundle.write_text(json.dumps({"cve_intake": {"references": [{"id": "CVE-2026-109619"}]}, "before_source": str(before), "after_source": str(after), "lifecycle_log": str(lifecycle), "sanitizer_log": str(sanitizer), "build_manifest": {"php_version": "8.x", "compiler": "clang", "commit": "abc", "flags": [], "extensions": []}}), encoding="utf-8")
            database = root / "research.sqlite3"
            report = root / "report.json"
            result = subprocess.run([sys.executable, str(BASE / "php_research_scanner.py"), str(bundle), "--database", str(database), "--report", str(report)], capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["scanner"], "php-research-scanner")
            self.assertEqual(len(payload["findings"]), 5)


if __name__ == "__main__":
    unittest.main()
