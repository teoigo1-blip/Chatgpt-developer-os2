import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V25(unittest.TestCase):
 def test_shell(self):
  for p in ['boot-test-preflight.sh','boot-test-manual.sh','build.sh']:
   subprocess.run(['bash','-n',str(ROOT/p)],check=True)
 def test_workflow_integrity(self):
  s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
  self.assertIn('sha256sum release.iso > iso.sha256',s)
  self.assertIn('sha256sum -c iso.sha256',s)
 def test_manual_modes(self):
  s=(ROOT/'boot-test-manual.sh').read_text()
  self.assertIn('bios)',s)
  self.assertIn('uefi)',s)
  self.assertIn('readonly=on',s)
 def test_no_disk_writes(self):
  for p in ['boot-test-preflight.sh','boot-test-manual.sh']:
   s=(ROOT/p).read_text()
   self.assertNotIn('mkfs.',s)
   self.assertNotIn('dd if=',s)
