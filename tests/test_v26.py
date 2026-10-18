import pathlib, unittest, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestV26(unittest.TestCase):
 def test_bash_syntax(self):
  for file in ('build.sh','qemu-serial-boot-check.sh'):
   self.assertEqual(subprocess.run(['bash','-n',str(ROOT/file)]).returncode,0)
 def test_workflow_runs_real_boot(self):
  s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
  self.assertIn('qemu-serial-boot-check.sh release.iso bios',s)
  self.assertIn('qemu-serial-boot-check.sh release.iso uefi',s)
 def test_serial_console_configured(self):
  self.assertIn('console=ttyS0,115200n8',(ROOT/'build.sh').read_text())
 def test_no_usb_write(self):
  s=(ROOT/'qemu-serial-boot-check.sh').read_text()
  self.assertNotIn('mkfs.',s)
  self.assertNotIn('dd if=',s)
