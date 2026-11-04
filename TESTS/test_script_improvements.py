# Purpose: regression checks for bounded JSONL reads and SHA-256 verification.
# Location: TESTS/test_script_improvements.py
# Input/output: synthetic temporary files to unittest results.
# Requirements: Python 3.10+, standard library only.
# Usage: python -m unittest discover -s TESTS -p "test_*.py" -v
# Limits: uses local filesystem and interpreter; no external services.
"""Focused tests for the two-script improvement branch."""
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from test_utilities import load, cli


class ImprovementTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / 'data'

    def test_exact_line_boundaries(self):
        for data, limit, count in [(b'{}',2,1),(b'{}\n',3,1),(b'{}\r\n',4,1),(b'',1,0)]:
            self.path.write_bytes(data)
            self.assertEqual(load('jsonl').validate(self.path,limit),count)

    def test_overlong_line_number_and_no_mutation(self):
        data=b'{}\n"long"\n'
        self.path.write_bytes(data)
        with self.assertRaisesRegex(ValueError,'line 2: exceeds 3'):
            load('jsonl').validate(self.path,3)
        self.assertEqual(self.path.read_bytes(),data)

    def test_byte_not_character_limit(self):
        self.path.write_bytes(('"'+chr(233)+'"').encode('utf-8'))
        self.assertEqual(load('jsonl').validate(self.path,4),1)
        with self.assertRaises(ValueError):
            load('jsonl').validate(self.path,3)

    def test_reads_are_bounded(self):
        class BoundedReader(io.BytesIO):
            def readline(self, size=-1):
                # Fail if the validator ever requests an unlimited read.
                self.asserted_size = size
                if size != 5:
                    raise AssertionError(size)
                return super().readline(size)
        stream=BoundedReader(b'x'*10000)
        with patch('builtins.open',return_value=stream):
            with self.assertRaisesRegex(ValueError,'exceeds 4'):
                load('jsonl').validate(self.path,4)
        self.assertEqual(stream.asserted_size,5)

    def test_invalid_limit(self):
        for limit in [0,-1,True,1.5,10**100]:
            with self.assertRaises(ValueError):
                load('jsonl').validate(self.path,limit)

    def test_limit_cli(self):
        self.path.write_bytes(b'{}\n')
        self.assertEqual(cli('jsonl',self.path,'--max-line-bytes',3).returncode,0)
        result=cli('jsonl',self.path,'--max-line-bytes',2)
        self.assertEqual(result.returncode,1)
        self.assertEqual(result.stdout,'')

    def test_digest_match_and_mismatch(self):
        self.path.write_bytes(b'abc')
        digest='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
        for expected in [digest,digest.upper()]:
            result=cli('hash',self.path,'--check',expected)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(result.stdout.strip(),'OK')
        result=cli('hash',self.path,'--check','0'*64)
        self.assertEqual(result.returncode,1)
        self.assertEqual(result.stdout,'')
        self.assertIn('mismatch',result.stderr)

    def test_malformed_digest_rejected_before_io(self):
        for expected in ['abc','g'*64,'0'*63,'0'*65,' '+'0'*64]:
            result=cli('hash',self.path,'--check',expected)
            self.assertEqual(result.returncode,2)
            self.assertIn('64 hexadecimal',result.stderr)

    def test_missing_file_with_valid_digest(self):
        self.assertEqual(cli('hash',self.path,'--check','0'*64).returncode,1)


if __name__=='__main__':
    unittest.main()
