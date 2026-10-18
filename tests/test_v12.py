import pathlib, subprocess, tempfile, unittest, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestV12(unittest.TestCase):
 def test_scripts_syntax(self):
  for p in (ROOT/'prepare-persistence.sh',ROOT/'config/includes.chroot/usr/local/bin/developer-codex-install'):
   self.assertEqual(subprocess.run(['bash','-n',str(p)]).returncode,0)
 def test_persistence_creation(self):
  with tempfile.TemporaryDirectory() as d:
   r=subprocess.run(['bash',str(ROOT/'prepare-persistence.sh'),d],capture_output=True)
   self.assertEqual(r.returncode,0)
   self.assertEqual((pathlib.Path(d)/'persistence.conf').read_text(),'/ union\n')
   self.assertNotEqual(subprocess.run(['bash',str(ROOT/'prepare-persistence.sh'),d],capture_output=True).returncode,0)
 def test_codex_no_install_without_flag(self):
  p=subprocess.run(['bash',str(ROOT/'config/includes.chroot/usr/local/bin/developer-codex-install')],capture_output=True,text=True)
  self.assertEqual(p.returncode,0) if shutil.which('npm') else self.assertNotEqual(p.returncode,0)
