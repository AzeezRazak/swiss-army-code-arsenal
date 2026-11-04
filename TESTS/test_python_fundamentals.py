# Purpose: verify beginner Python lessons and their public command-line behavior.
# Location: TESTS/test_python_fundamentals.py
# Input/output: synthetic values to unittest results; no persistent data changes.
# Requirements: Python 3.10+, standard library only.
# Usage: python -m unittest discover -s TESTS -p "test_*.py" -v
# Limits: subprocesses use the current interpreter; other runtimes unverified.
"""Boundary, reference and CLI tests for the five Sprint 0003 lessons."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

# Locate lessons independently of the shell's working directory.
BASE = Path(__file__).resolve().parents[1] / 'SCRIPTS/01-programming-languages/python-fundamentals'


def load(name):
    # Import a standalone file without executing its guarded main function.
    spec = importlib.util.spec_from_file_location(name, BASE / (name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FundamentalsTests(unittest.TestCase):
    def test_temperature_reference_points(self):
        for celsius, expected in [(0,32), (100,212), (-40,-40), (37,98.6)]:
            self.assertAlmostEqual(load('temperature').convert(celsius)['fahrenheit'], expected)

    def test_temperature_invalid(self):
        for value in [float('nan'), float('inf'), -float('inf'), 1.7e308, 'bad']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                load('temperature').convert(value)

    def test_grade_boundaries(self):
        # Check both sides of each branch threshold, including closed endpoints.
        for score, grade in [(0,'F'),(59.9,'F'),(60,'D'),(69.9,'D'),(70,'C'),
                             (79.9,'C'),(80,'B'),(89.9,'B'),(90,'A'),(100,'A')]:
            self.assertEqual(load('grade').classify(score)['grade'], grade)

    def test_grade_invalid(self):
        for score in [-1,101,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):
                load('grade').classify(score)

    def test_list_empty_and_signed(self):
        summarize=load('list_summary').summarize
        self.assertEqual(summarize([]),dict(count=0,sum=0,even=0,odd=0))
        values=[-3,-2,0,1,4]
        before=values.copy()
        self.assertEqual(summarize(values),dict(count=5,sum=0,even=3,odd=2))
        self.assertEqual(values,before)

    def test_list_references_and_iterator(self):
        values=list(range(-100,101))
        result=load('list_summary').summarize(iter(values))
        self.assertEqual(result['sum'],sum(values))
        self.assertEqual(result['count'],len(values))
        self.assertEqual(result['even']+result['odd'],len(values))

    def test_list_invalid(self):
        for value in [True,1.5,'2']:
            with self.assertRaises(ValueError):
                load('list_summary').summarize([value])

    def test_text_policies(self):
        summarize=load('text_summary').summarize
        self.assertEqual(summarize(''),dict(characters=0,words=0,letters=0))
        self.assertEqual(summarize('  Hi 42!\n'),dict(characters=9,words=2,letters=2))
        self.assertEqual(summarize(chr(233)+'!'),dict(characters=2,words=1,letters=1))
        # A combining accent is a separate code point, not a separate letter.
        self.assertEqual(summarize('e'+chr(0x301))['characters'],2)

    def test_word_counts(self):
        count=load('word_counts').count_words
        self.assertEqual(count(''),{})
        self.assertEqual(count('Python python CODE!'),{'code!':1,'python':2})
        self.assertEqual(count('Stra'+chr(223)+'e STRASSE'),{'strasse':2})
        self.assertEqual(list(count('z a z')),['a','z'])

    def test_text_type_errors(self):
        for name, function in [('text_summary','summarize'),('word_counts','count_words')]:
            with self.assertRaises(ValueError):
                getattr(load(name),function)(None)

    def test_documented_cli_examples(self):
        examples=[('temperature',['0'],{'celsius':0.0,'fahrenheit':32.0}),
                  ('grade',['85'],{'score':85.0,'grade':'B'}),
                  ('list_summary',['1','2','3','4'],dict(count=4,sum=10,even=2,odd=2)),
                  ('text_summary',['Hello Python'],dict(characters=12,words=2,letters=11)),
                  ('word_counts',['Python python code'],{'code':1,'python':2})]
        for name,args,expected in examples:
            with self.subTest(name=name):
                result=subprocess.run([sys.executable,str(BASE/(name+'.py')),*args],
                                      capture_output=True,text=True,timeout=5)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(json.loads(result.stdout),expected)
                self.assertEqual(result.stderr,'')

    def test_cli_rejects_bad_input(self):
        for name,args in [('temperature',['nan']),('grade',['101']),
                          ('list_summary',['1.2']),('text_summary',[]),('word_counts',[])]:
            # CLI errors must be non-success and keep stdout free of partial JSON.
            result=subprocess.run([sys.executable,str(BASE/(name+'.py')),*args],
                                  capture_output=True,text=True,timeout=5)
            self.assertEqual(result.returncode,2)
            self.assertEqual(result.stdout,'')
            self.assertIn('error:',result.stderr)


if __name__=='__main__':
    unittest.main()
