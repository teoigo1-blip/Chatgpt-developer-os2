import pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V38(unittest.TestCase):
 def test_prebuild_gate(self):
  self.assertIn('timeout 180s python3 -m unittest', (ROOT/'prebuild-gate.sh').read_text())
 def test_workflow_uses_gate(self):
  self.assertIn('./prebuild-gate.sh', (ROOT/'.github/workflows/build-live-iso.yml').read_text())
 def test_iso_filesystem_read(self):
  self.assertIn('xorriso -indev', (ROOT/'ci-build-iso.sh').read_text())
