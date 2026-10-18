from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class MixedTests(unittest.TestCase):
    def check_fixture(self, source, expected):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / 'fixture.py'
            fixture.write_text(source)
            result = subprocess.run([sys.executable, str(ROOT/'run-single-test.py'), str(fixture)], capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_plain_function_failure_is_not_ignored(self):
        self.check_fixture('def test_failure():\n    assert False\n', 1)

    def test_legacy_import_assertion_failure_is_not_ignored(self):
        self.check_fixture('assert False\n', 1)

    def test_legacy_import_assertion_passes(self):
        self.check_fixture('assert 2 + 2 == 4\n', 0)

    def test_unittest_failure_is_not_ignored(self):
        self.check_fixture('import unittest\nclass Check(unittest.TestCase):\n    def test_failure(self):\n        self.fail("regression")\n', 1)
