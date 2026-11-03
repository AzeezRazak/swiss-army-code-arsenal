# ========================================================================
# Purpose: Verify the five Sprint 0001 utilities using synthetic data.
# Location: TESTS/test_utilities.py
# Input/output: Temporary fixtures and subprocesses; unittest pass/fail report.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python -m unittest discover -s TESTS -p "test_*.py" -v
# Limitations: No external services; temporary databases/files are cleaned up.
# ========================================================================
"""Acceptance tests for Sprint 0001; fixtures stay in temporary directories."""
import hashlib
import importlib.util
from pathlib import Path
import random
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import unittest

# Resolve fixtures/modules relative to the repository rather than the shell cwd.
ROOT = Path(__file__).resolve().parents[1]
PATHS = {
    "search": "SCRIPTS/02-algorithms-data-structures/binary-search/binary_search.py",
    "jsonl": "SCRIPTS/03-file-data-processing/jsonl-validator/validate_jsonl.py",
    "hash": "SCRIPTS/08-cybersecurity/sha256-file/sha256_file.py",
    "db": "SCRIPTS/07-databases-storage/sqlite-transactions/transactions.py",
    "stats": "SCRIPTS/12-data-science-mathematics/online-statistics/online_stats.py",
}


def load(key):
    # Load standalone scripts by path without requiring installed packages.
    spec = importlib.util.spec_from_file_location(key, ROOT / PATHS[key])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cli(key, *args):
    return subprocess.run([sys.executable, str(ROOT / PATHS[key]), *map(str, args)],
                          capture_output=True, text=True, timeout=15)


class SearchTests(unittest.TestCase):
    def test_boundaries(self):
        search = load("search").first_index
        for values, target, expected in [([], 1, -1), ([1], 1, 0), ([1], 0, -1),
                ([1, 2, 2, 3], 2, 1), ([1, 2, 3], 3, 2), ([1, 2, 3], 4, -1)]:
            with self.subTest(values=values, target=target):
                self.assertEqual(search(values, target), expected)

    def test_against_linear_reference(self):
        # Seed randomized inputs so a regression is reproducible.
        rng = random.Random(42)
        search = load("search").first_index
        for _ in range(200):
            values = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(100)))
            target = rng.randrange(-25, 26)
            self.assertEqual(search(values, target), values.index(target) if target in values else -1)

    def test_cli_sorted_validation(self):
        self.assertEqual(cli("search", 2, 1, 2, 2, 3).stdout.strip(), "1")
        self.assertEqual(cli("search", 2, 3, 1).returncode, 2)


class FileTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "input"

    def test_jsonl_valid_and_empty(self):
        validate = load("jsonl").validate
        for data, count in [(b"", 0), (b'{}\n[1]\r\ntrue\nnull', 4)]:
            self.path.write_bytes(data)
            self.assertEqual(validate(self.path), count)
            self.assertEqual(self.path.read_bytes(), data)

    def test_jsonl_rejects_invalid_input(self):
        validate = load("jsonl").validate
        for bad in [b'{', b'\xff', b'', b'NaN', b'Infinity', b'\xef\xbb\xbf{}']:
            with self.subTest(bad=bad):
                data = b'{}\n' + bad + b'\n'
                self.path.write_bytes(data)
                with self.assertRaisesRegex(ValueError, "line 2"):
                    validate(self.path)
                self.assertEqual(self.path.read_bytes(), data)

    def test_jsonl_cli_error_and_missing(self):
        self.path.write_bytes(b'{}\n{')
        result = cli("jsonl", self.path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 2", result.stderr)
        self.assertEqual(cli("jsonl", self.path.with_name("missing")).returncode, 1)

    def test_hash_known_vectors(self):
        digest = load("hash").digest_file
        for data, expected in [(b'', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
                (b'abc', 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')]:
            self.path.write_bytes(data)
            self.assertEqual(digest(self.path, 1), expected)

    def test_hash_binary_multiple_chunks(self):
        data = bytes(range(256)) * 10000
        self.path.write_bytes(data)
        self.assertEqual(load("hash").digest_file(self.path), hashlib.sha256(data).hexdigest())
        self.assertEqual(self.path.read_bytes(), data)

    def test_hash_bad_chunk_and_missing(self):
        for size in [0, -1, 1.5, True]:
            with self.assertRaises(ValueError):
                load("hash").digest_file(self.path, size)
        self.assertEqual(cli("hash", self.path).returncode, 1)
        self.assertEqual(cli("hash", Path(self.directory.name)).returncode, 1)


class DatabaseTests(unittest.TestCase):
    def test_commit_and_rollback_persist(self):
        module = load("db")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.db"
            connection = sqlite3.connect(path)
            try:
                connection.executescript((ROOT / PATHS['db']).with_name('schema.sql').read_text())
                module.insert_batch(connection, ['alpha', 'beta'])
                with self.assertRaises(sqlite3.IntegrityError):
                    module.insert_batch(connection, ['gamma', 'alpha'])
                self.assertFalse(connection.in_transaction)
            finally:
                # Release the database handle before temporary-directory cleanup.
                connection.close()
            connection = sqlite3.connect(path)
            try:
                self.assertEqual(connection.execute('SELECT label FROM entries ORDER BY id').fetchall(), [('alpha',), ('beta',)])
            finally:
                # Release the database handle before temporary-directory cleanup.
                connection.close()

    def test_reject_active_or_autocommit(self):
        connection = sqlite3.connect(':memory:')
        try:
            connection.execute('BEGIN')
            with self.assertRaises(ValueError):
                load('db').insert_batch(connection, [])
            connection.rollback()
            connection.isolation_level = None
            with self.assertRaises(ValueError):
                load('db').insert_batch(connection, [])
        finally:
            # Release the database handle before temporary-directory cleanup.
            connection.close()

    def test_repeatable_demo(self):
        self.assertEqual(load('db').demonstrate(), ['alpha', 'beta'])
        self.assertEqual(load('db').demonstrate(), ['alpha', 'beta'])
        self.assertEqual(cli('db').stdout.strip(), '["alpha", "beta"]')


class StatisticsTests(unittest.TestCase):
    def test_reference_values(self):
        # Keep numerical reference comparisons reproducible across runs.
        rng = random.Random(7)
        for values in [[1, 2, 3, 4], [-5, -2, 0, 7], [5] * 20,
                       [rng.uniform(-100, 100) for _ in range(1000)]]:
            result = load('stats').summarize(iter(values))
            self.assertEqual(result['count'], len(values))
            self.assertAlmostEqual(result['mean'], statistics.mean(values), places=9)
            self.assertAlmostEqual(result['population_variance'], statistics.pvariance(values), places=9)
            self.assertAlmostEqual(result['sample_variance'], statistics.variance(values), places=9)

    def test_singleton(self):
        self.assertEqual(load('stats').summarize([7]), {'count': 1, 'mean': 7.0,
                         'population_variance': 0.0, 'sample_variance': None})

    def test_reject_invalid_or_overflow(self):
        for values in [[], [float('nan')], [float('inf')], [-float('inf')], [1e308, -1e308]]:
            with self.assertRaises(ValueError):
                load('stats').summarize(values)
        self.assertEqual(cli('stats', 'nan').returncode, 2)

    def test_cli_example(self):
        result = cli('stats', 1, 2, 3, 4)
        self.assertEqual(result.returncode, 0)
        self.assertIn('"mean": 2.5', result.stdout)


# Run the test suite only when this module is executed directly.
if __name__ == '__main__':
    unittest.main()
