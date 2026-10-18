import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V33(unittest.TestCase):
 def test_preflight_syntax(self):
  subprocess.run(['bash','-n',str(ROOT/'github-preflight.sh')],check=True)
 def test_workflow_timeout(self):
  self.assertIn("timeout 180s python3 -m unittest",(ROOT/'.github/workflows/build-live-iso.yml').read_text())
 def test_workflow_reports(self):
  self.assertIn('test -s iso-artifact.json',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
 def test_android_guide(self):
  self.assertIn('Actions > Build Live USB ISO',(ROOT/'GITHUB_BUILD.md').read_text())
