import pathlib,unittest,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V19(unittest.TestCase):
 def test_no_duplicates(self):
  a=[x.strip() for x in (ROOT/'config/package-lists/developer.list.chroot').read_text().splitlines() if x.strip() and not x.startswith('#')]
  self.assertEqual(len(a),len(set(a)))
 def test_default_jdk(self):
  a=(ROOT/'config/package-lists/developer.list.chroot').read_text()
  self.assertIn('default-jdk',a)
  self.assertNotIn('openjdk-17-jdk',a)
 def test_scripts_syntax(self):
  for f in ['audit-packages.sh','build.sh','build-host-check.sh']:
   self.assertEqual(subprocess.run(['bash','-n',str(ROOT/f)]).returncode,0)
 def test_optional_documented(self):
  self.assertTrue((ROOT/'OPTIONAL_PACKAGES.md').is_file())
if __name__=='__main__':unittest.main()
