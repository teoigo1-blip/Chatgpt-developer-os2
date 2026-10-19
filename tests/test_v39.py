import os
from pathlib import Path
import unittest
import subprocess
R=Path(__file__).resolve().parents[1]
class TestV39(unittest.TestCase):
 def test_runner_guard(self):
  s=(R/'ci-runner-space.sh').read_text()
  self.assertIn('GITHUB_ACTIONS:-',s)
  self.assertIn('RUNNER_ENVIRONMENT:-',s)
 def test_workflow_cleanup_order(self):
  s=(R/'.github/workflows/build-live-iso.yml').read_text()
  self.assertLess(s.index('Reclaim space on ephemeral GitHub runner'),s.index('Install build prerequisites'))
 def test_no_bytecode_bundled(self):
  tracked=subprocess.run(['git','ls-files','--','config'],cwd=R,capture_output=True,text=True,check=True).stdout.splitlines()
  self.assertFalse([name for name in tracked if name.endswith('.pyc')])
 def test_no_iso_claim(self):
  self.assertFalse(list(R.glob('*.iso')))
