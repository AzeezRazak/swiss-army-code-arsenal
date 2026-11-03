# ========================================================================
# Purpose: Verify local TCP framing and read-only inventory contracts.
# Location: TESTS/test_sprint2.py
# Input/output: Loopback sockets and temporary trees; unittest pass/fail/skip report.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python -m unittest discover -s TESTS -p "test_*.py" -v
# Limitations: Real symlink checks may skip when OS privileges are unavailable.
# ========================================================================
"""Loopback integration and synthetic filesystem acceptance checks."""
import importlib.util
import json
import os
from pathlib import Path
import queue
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

# Resolve fixtures/modules relative to the repository rather than the shell cwd.
ROOT = Path(__file__).resolve().parents[1]
NET = ROOT / "SCRIPTS/05-networking-protocols/loopback-tcp"
AUTO = ROOT / "SCRIPTS/09-automation-scripting/directory-inventory/inventory.py"
spec = importlib.util.spec_from_file_location("inventory", AUTO)
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)
sys.path.insert(0, str(NET))
import protocol


class NetworkTests(unittest.TestCase):
    def start_server(self, timeout=2):
        process = subprocess.Popen([sys.executable, str(NET / 'server.py'), '--timeout', str(timeout)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        def cleanup():
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=5)
        # Ensure a failed assertion cannot leave a server subprocess running.
        self.addCleanup(cleanup)
        lines = queue.Queue()
        threading.Thread(target=lambda: lines.put(process.stdout.readline()), daemon=True).start()
        # Bound readiness waiting so a broken server cannot hang the suite.
        line = lines.get(timeout=5)
        self.assertTrue(line.startswith('PORT '), line)
        return process, int(line.split()[1])

    def finish(self, process, success):
        _, error = process.communicate(timeout=5)
        self.assertEqual(process.returncode, 0 if success else 1, error)
        return error

    def test_client_server_cli(self):
        process, port = self.start_server()
        result = subprocess.run([sys.executable, str(NET/'client.py'), str(port), 'hello'],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'hello')
        self.finish(process, True)

    def test_empty_and_maximum_frame(self):
        for payload in [b'', bytes(range(256))*256]:
            with self.subTest(size=len(payload)):
                process, port = self.start_server()
                with socket.create_connection(('127.0.0.1', port), timeout=2) as connection:
                    protocol.send_frame(connection, payload, 2)
                    self.assertEqual(protocol.receive_frame(connection, 2), payload)
                self.finish(process, True)

    def test_truncated_header_and_body(self):
        for payload in [b'\x00', struct.pack('!I', 5)+b'ab']:
            process, port = self.start_server()
            with socket.create_connection(('127.0.0.1', port), timeout=2) as connection:
                connection.sendall(payload)
                # Signal EOF after a partial frame while allowing the server to report failure.
                connection.shutdown(socket.SHUT_WR)
            self.assertIn('truncated', self.finish(process, False))

    def test_oversize_header(self):
        process, port = self.start_server()
        with socket.create_connection(('127.0.0.1', port), timeout=2) as connection:
            connection.sendall(struct.pack('!I', protocol.MAX_PAYLOAD+1))
        self.assertIn('exceeds', self.finish(process, False))

    def test_idle_client_timeout(self):
        process, port = self.start_server(0.4)
        with socket.create_connection(('127.0.0.1', port), timeout=2):
            self.finish(process, False)

    def test_accept_timeout(self):
        process, _ = self.start_server(0.4)
        self.finish(process, False)

    def test_total_frame_deadline(self):
        # Create local connected sockets to isolate the trickle-byte deadline test.
        left, right = socket.socketpair()
        self.addCleanup(left.close)
        self.addCleanup(right.close)
        def trickle():
            try:
                for byte in struct.pack('!I', 3)+b'abc':
                    right.send(bytes([byte]))
                    time.sleep(0.08)
            except OSError:
                pass
        sender = threading.Thread(target=trickle, daemon=True)
        sender.start()
        with self.assertRaises(TimeoutError):
            protocol.receive_frame(left, 0.2)
        sender.join(timeout=2)

    def test_parameter_validation(self):
        for script, args in [('server.py', ['--timeout', 'nan']),
                             ('server.py', ['--port', '-1']),
                             ('client.py', ['0', 'hi']),
                             ('client.py', ['12345', 'hi', '--timeout', '0'])]:
            result = subprocess.run([sys.executable, str(NET/script), *args],
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 1)
            self.assertIn('error:', result.stderr)

    def test_send_size_limit(self):
        with self.assertRaises(ValueError):
            protocol.send_frame(None, b'x'*(protocol.MAX_PAYLOAD+1), 1)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_empty(self):
        self.assertEqual(inv.inventory(self.root), [])

    def test_nested_unicode_sorted_and_readonly(self):
        (self.root/'z').mkdir()
        name = 'caf'+chr(233)+'.txt'
        (self.root/'z'/name).write_bytes(b'hello')
        (self.root/'a').write_bytes(b'')
        expected = [{'path':'a','type':'file','size':0}, {'path':'z','type':'directory'},
                    {'path':'z/'+name,'type':'file','size':5}]
        self.assertEqual(inv.inventory(self.root), expected)
        self.assertEqual(inv.inventory(self.root), expected)
        self.assertEqual((self.root/'z'/name).read_bytes(), b'hello')
        result = subprocess.run([sys.executable, str(AUTO), str(self.root)],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), expected)

    def test_missing_and_file_root(self):
        for path in [self.root/'missing', self.root/'file']:
            if path.name=='file':
                path.touch()
            result = subprocess.run([sys.executable, str(AUTO), str(path)],
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, '')

    def test_permission_error_propagates(self):
        with patch.object(inv.os, 'scandir', side_effect=PermissionError('denied')):
            with self.assertRaises(PermissionError):
                inv.inventory(self.root)

    def test_directory_symlink_not_followed(self):
        (self.root/'target').mkdir()
        (self.root/'target'/'file').write_bytes(b'x')
        try:
            (self.root/'link').symlink_to(self.root/'target', target_is_directory=True)
        except OSError as error:
            # Report the missing platform capability explicitly rather than claiming a pass.
            self.skipTest('OS disallows symlink creation: '+str(error))
        rows = inv.inventory(self.root)
        self.assertIn({'path':'link','type':'link'}, rows)
        self.assertFalse(any(row['path'].startswith('link/') for row in rows))
        with self.assertRaises(ValueError):
            inv.inventory(self.root/'link')

    @unittest.skipUnless(os.name == 'nt', 'Windows junction test')
    def test_directory_junction_not_followed(self):
        target = self.root/'target'
        target.mkdir()
        (target/'file').write_bytes(b'x')
        environment = dict(os.environ, ARSENAL_TEST_ROOT=str(self.root))
        result = subprocess.run(['powershell', '-NoProfile', '-Command',
            "New-Item -ItemType Junction -Path (Join-Path $env:ARSENAL_TEST_ROOT 'link') -Target (Join-Path $env:ARSENAL_TEST_ROOT 'target') | Out-Null"],
            env=environment, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = inv.inventory(self.root)
        self.assertIn({'path':'link','type':'link'}, rows)
        self.assertFalse(any(row['path'].startswith('link/') for row in rows))
        with self.assertRaises(ValueError):
            inv.inventory(self.root/'link')

    def test_reparse_attribute_classification(self):
        class Info:
            st_mode = 0
            st_file_attributes = 0x400
        self.assertTrue(inv.is_link(Info()))


# Run the test suite only when this module is executed directly.
if __name__ == '__main__':
    unittest.main()
