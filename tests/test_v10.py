import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / 'config/includes.chroot/usr/local/bin/developer-build'
CHECK = ROOT / 'config/includes.chroot/usr/local/bin/developer-check-build'

class BuildTests(unittest.TestCase):
    def test_help(self):
        r = subprocess.run(['python3', str(BUILD), '--help'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn('android', r.stdout)
    def test_no_execute_by_default(self):
        with tempfile.TemporaryDirectory() as d:
            pathlib.Path(d, 'CMakeLists.txt').write_text('cmake_minimum_required(VERSION 3.10)')
            r = subprocess.run(['python3', str(BUILD), 'linux', d], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            self.assertIn('Vista previa', r.stdout)
            self.assertFalse(pathlib.Path(d, 'build').exists())
    def test_diagnostics(self):
        r = subprocess.run(['python3', str(CHECK)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn('Codex CLI', r.stdout)

if __name__ == '__main__': unittest.main()
