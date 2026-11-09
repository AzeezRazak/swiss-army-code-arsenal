# Purpose: Serve a local dashboard for scan scope, findings and report exports.
# Location: projects/python-security-research/security-research-dashboard/app.py
# Input/output: local scanner SQLite databases and dashboard scope data to localhost HTTP responses.
# Requirements: Python 3.10+, standard library only; no network calls beyond 127.0.0.1.
# Usage from root: python projects/python-security-research/security-research-dashboard/app.py
# Limits: binds to loopback by default; no authentication, live scanning or credential storage.
"""Local-only dashboard for the web and PHP research scanner outputs."""
from __future__ import annotations

import argparse
import csv
import io
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sqlite3
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = Path(__file__).resolve().parent / "static"
DEFAULT_DATABASES = {
    "web": PROJECT_ROOT / "web-vulnerability-scanner" / "web_scanner.sqlite3",
    "php": PROJECT_ROOT / "php-vulnerability-research-scanner" / "php_research.sqlite3",
}


def _bounded_strings(value, field):
    # Keep the personal scope policy small and human-readable before storing it.
    if not isinstance(value, list) or len(value) > 100 or any(not isinstance(item, str) or len(item) > 512 for item in value):
        raise ValueError(f"{field} must contain at most 100 short strings")
    return [item.strip() for item in value if item.strip()]


def validate_scope(scope):
    """Validate the dashboard's non-executing scan-scope record."""
    if not isinstance(scope, dict):
        raise ValueError("scope must be an object")
    methods = [item.upper() for item in _bounded_strings(scope.get("methods", []), "methods")]
    if any(method not in {"GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"} for method in methods):
        raise ValueError("methods contains an unsupported HTTP method")
    notes = scope.get("notes", "")
    if not isinstance(notes, str) or len(notes) > 4_000:
        raise ValueError("notes must be at most 4000 characters")
    return {"targets": _bounded_strings(scope.get("targets", []), "targets"), "methods": methods, "accounts": _bounded_strings(scope.get("accounts", []), "accounts"), "callbacks": _bounded_strings(scope.get("callbacks", []), "callbacks"), "notes": notes.strip()}


class DashboardStore:
    """Read scanner findings and persist the dashboard-owned scope record."""

    def __init__(self, scope_database, scanner_databases=None):
        self.scope_database = Path(scope_database)
        self.scanner_databases = scanner_databases or DEFAULT_DATABASES
        self.scope_database.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.scope_database)
        try:
            connection.execute("CREATE TABLE IF NOT EXISTS scope (id INTEGER PRIMARY KEY CHECK (id = 1), scope_json TEXT NOT NULL)")
            if connection.execute("SELECT 1 FROM scope WHERE id = 1").fetchone() is None:
                connection.execute("INSERT INTO scope(id, scope_json) VALUES (1, ?)", (json.dumps(validate_scope({})),))
            connection.commit()
        finally:
            connection.close()

    def get_scope(self):
        # Return the last locally saved policy without performing any scan.
        connection = sqlite3.connect(self.scope_database)
        try:
            raw = connection.execute("SELECT scope_json FROM scope WHERE id = 1").fetchone()[0]
        finally:
            connection.close()
        return json.loads(raw)

    def save_scope(self, scope):
        # Validate before replacing the single dashboard scope record.
        normalized = validate_scope(scope)
        connection = sqlite3.connect(self.scope_database)
        try:
            connection.execute("UPDATE scope SET scope_json = ? WHERE id = 1", (json.dumps(normalized, sort_keys=True),))
            connection.commit()
        finally:
            connection.close()
        return normalized

    def findings(self, scanner="all"):
        # Read only the existing scanner-owned findings tables; missing databases are empty.
        scanners = self.scanner_databases.keys() if scanner == "all" else [scanner]
        if scanner not in {"all", *self.scanner_databases}:
            raise ValueError("scanner must be web, php or all")
        result = []
        for name in scanners:
            database = Path(self.scanner_databases[name])
            if not database.is_file():
                continue
            connection = sqlite3.connect(database)
            try:
                rows = connection.execute("SELECT id, module, finding_json FROM findings ORDER BY id").fetchall()
            finally:
                connection.close()
            for record_id, module, raw in rows:
                finding = json.loads(raw)
                finding.update({"record_id": record_id, "module": module, "scanner": name})
                result.append(finding)
        return result


def export_findings(findings, output_format):
    """Serialize findings as JSON, CSV or Markdown for downstream analysis."""
    if output_format == "json":
        return "application/json", json.dumps(findings, indent=2, sort_keys=True) + "\n", "findings.json"
    columns = ["scanner", "module", "status", "confidence", "severity", "summary"]
    if output_format == "csv":
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=columns)
        writer.writeheader()
        writer.writerows({column: finding.get(column, "") for column in columns} for finding in findings)
        return "text/csv; charset=utf-8", buffer.getvalue(), "findings.csv"
    if output_format == "markdown":
        lines = ["# Scanner findings", "", "| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
        for finding in findings:
            values = [str(finding.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
            lines.append("| " + " | ".join(values) + " |")
        return "text/markdown; charset=utf-8", "\n".join(lines) + "\n", "findings.md"
    raise ValueError("format must be json, csv or markdown")


def make_handler(store):
    """Create a request handler closed over one dashboard store."""
    class Handler(BaseHTTPRequestHandler):
        def _send(self, body, content_type="application/json", status=HTTPStatus.OK, disposition=None):
            # Send bounded local responses with an optional browser download filename.
            data = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            if disposition:
                self.send_header("Content-Disposition", f"attachment; filename=\"{disposition}\"")
            self.end_headers()
            self.wfile.write(data)

        def _json(self, payload, status=HTTPStatus.OK):
            self._send(json.dumps(payload, sort_keys=True), status=status)

        def do_GET(self):
            # Route dashboard data and static assets without exposing arbitrary filesystem paths.
            parsed = urlparse(self.path)
            if parsed.path == "/":
                self._send((STATIC_ROOT / "index.html").read_text(encoding="utf-8"), "text/html; charset=utf-8")
                return
            if parsed.path.startswith("/static/"):
                asset = STATIC_ROOT / parsed.path.removeprefix("/static/")
                if asset.is_file() and asset.parent == STATIC_ROOT:
                    content_type = "text/css; charset=utf-8" if asset.suffix == ".css" else "text/javascript; charset=utf-8"
                    self._send(asset.read_text(encoding="utf-8"), content_type)
                    return
                self._json({"error": "asset not found"}, HTTPStatus.NOT_FOUND)
                return
            query = parse_qs(parsed.query)
            try:
                if parsed.path == "/api/scope":
                    self._json(store.get_scope())
                elif parsed.path == "/api/summary":
                    findings = store.findings("all")
                    self._json({"total": len(findings), "web": sum(item["scanner"] == "web" for item in findings), "php": sum(item["scanner"] == "php" for item in findings), "signals": sum(item.get("status") == "signal" for item in findings), "high": sum(item.get("severity") in {"high", "critical"} for item in findings)})
                elif parsed.path == "/api/findings":
                    self._json(store.findings(query.get("scanner", ["all"])[0]))
                elif parsed.path == "/api/export":
                    content_type, body, filename = export_findings(store.findings(query.get("scanner", ["all"])[0]), query.get("format", ["json"])[0])
                    self._send(body, content_type, disposition=filename)
                else:
                    self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            except (OSError, ValueError, json.JSONDecodeError) as error:
                self._json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

        def do_POST(self):
            # Accept only the dashboard scope policy; scanning remains outside this web app.
            if urlparse(self.path).path != "/api/scope":
                self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 64 * 1024:
                    raise ValueError("request is too large")
                scope = json.loads(self.rfile.read(length).decode("utf-8"))
                self._json(store.save_scope(scope))
            except (ValueError, UnicodeError, json.JSONDecodeError) as error:
                self._json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

        def log_message(self, format_string, *args):
            # Keep local dashboard logs concise and free of request headers or payloads.
            print(f"dashboard: {self.command} {self.path}")

    return Handler


def main():
    # Bind to loopback only so the personal dashboard is not exposed on the LAN.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--scope-db", default=str(Path(__file__).with_name("dashboard.sqlite3")))
    parser.add_argument("--web-db", default=str(DEFAULT_DATABASES["web"]))
    parser.add_argument("--php-db", default=str(DEFAULT_DATABASES["php"]))
    args = parser.parse_args()
    store = DashboardStore(args.scope_db, {"web": args.web_db, "php": args.php_db})
    server = ThreadingHTTPServer((args.host, args.port), make_handler(store))
    print(f"Security research dashboard: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
