import pathlib,unittest
R=pathlib.Path(__file__).resolve().parents[1]
class TestV28(unittest.TestCase):
 def test_script_syntax(self):
  import subprocess
  self.assertEqual(subprocess.run(['bash','-n',str(R/'ci-build-iso.sh')]).returncode,0)
 def test_temp_build(self):
  s=(R/'ci-build-iso.sh').read_text();self.assertIn('mktemp -d',s);self.assertIn('cp -a',s)
 def test_sha(self):
  self.assertIn('sha256sum -c SHA256SUMS',(R/'ci-build-iso.sh').read_text())
 def test_workflow(self):
  s=(R/'.github/workflows/build-live-iso.yml').read_text();self.assertIn('sudo ./ci-build-iso.sh',s);self.assertIn('dist/build.log',s)
