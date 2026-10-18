import unittest
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
class Version36(unittest.TestCase):
 def test_source_integrity(self):
  subprocess.run(['python3',str(ROOT/'verify-source.py')],check=True,capture_output=True)
 def test_boot_script_syntax(self):
  subprocess.run(['bash','-n',str(ROOT/'qemu-serial-boot-check.sh')],check=True)
 def test_workflow_has_artifact_check(self):
  self.assertIn('Inspect generated artifact sizes',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
 def test_no_api_key_embedded(self):
  self.assertNotIn('OPENAI_API_KEY=',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
