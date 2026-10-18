import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class V34(unittest.TestCase):
    def test_workflow(self):
        subprocess.run([sys.executable, str(ROOT/'validate-workflow.py')], check=True, capture_output=True, timeout=15)
    def test_host_apt_not_gate(self):
        self.assertNotIn('check-build-inputs.py --apt', (ROOT/'.github/workflows/build-live-iso.yml').read_text())
    def test_artifact_integrity(self):
        self.assertIn('sha256sum -c iso.sha256', (ROOT/'.github/workflows/build-live-iso.yml').read_text())
    def test_failure_diagnostics(self):
        self.assertIn('build-diagnostics', (ROOT/'.github/workflows/build-live-iso.yml').read_text())
