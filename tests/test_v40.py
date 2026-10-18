import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class V40Tests(unittest.TestCase):
    def test_shell_syntax(self):
        p = subprocess.run(['bash','-n',str(ROOT/'ci-local-check.sh')], capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr.decode())
    def test_checklist(self):
        guide=(ROOT/'FIRST_ISO_STEPS.md').read_text()
        self.assertIn('build-diagnostics', guide)
        self.assertIn('sha256sum -c iso.sha256', guide)
    def test_no_automatic_usb_format(self):
        script=(ROOT/'ci-local-check.sh').read_text()
        self.assertNotIn('mkfs.', script)
        self.assertNotIn('dd if=', script)
