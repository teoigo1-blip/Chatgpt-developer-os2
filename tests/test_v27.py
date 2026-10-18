import subprocess
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class V27Tests(unittest.TestCase):
    def test_no_purge_config(self):
        script = (ROOT/'build.sh').read_text()
        self.assertNotIn('lb clean --purge || true', script)
        self.assertIn('lb clean\n', script)
    def test_manifest_validation(self):
        r = subprocess.run(['python3', str(ROOT/'check-build-inputs.py')], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
    def test_workflow_diagnostics(self):
        flow = (ROOT/'.github/workflows/build-live-iso.yml').read_text()
        self.assertIn('check-build-inputs.py', flow)
        self.assertIn('if: failure()', flow)
