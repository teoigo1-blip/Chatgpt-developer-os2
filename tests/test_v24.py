import pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class BuildWorkflowTests(unittest.TestCase):
 def test_workflow_exists(self): self.assertTrue((ROOT/'.github/workflows/build-live-iso.yml').is_file())
 def test_manual_trigger(self): self.assertIn('workflow_dispatch:',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
 def test_no_usb_flash(self):
  workflow=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
  self.assertNotIn('dd if=',workflow)
  self.assertNotIn('mkfs.',workflow)
 def test_artifact(self): self.assertIn('actions/upload-artifact@v4',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
 def test_guidance(self): self.assertIn('No acredita',(ROOT/'GITHUB_BUILD.md').read_text())
