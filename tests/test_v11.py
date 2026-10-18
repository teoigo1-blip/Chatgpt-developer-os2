import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V11(unittest.TestCase):
 def test_scripts_syntax(self):
  for n in ('preflight.sh','verify-iso.sh','build.sh'):
   subprocess.run(['bash','-n',str(ROOT/n)],check=True)
 def test_guide_syntax(self):
  subprocess.run(['python3','-m','py_compile',str(ROOT/'config/includes.chroot/usr/local/bin/developer-install-guide')],check=True)
 def test_no_automatic_disk_write(self):
  for n in ('preflight.sh','verify-iso.sh'):
   s=(ROOT/n).read_text()
   self.assertNotIn('dd if=',s)
   self.assertNotIn('mkfs.',s)
if __name__=='__main__': unittest.main()
