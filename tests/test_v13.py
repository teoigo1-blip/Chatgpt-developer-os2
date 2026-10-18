import pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestV13(unittest.TestCase):
 def test_autostart(self):
  data=(ROOT/'config/includes.chroot/etc/xdg/autostart/developer-panel.desktop').read_text()
  self.assertIn('Exec=/usr/local/bin/developer-dashboard',data)
 def test_qemu_script(self):
  self.assertIn('qemu-system-x86_64',(ROOT/'smoke-test-qemu.sh').read_text())
 def test_boot_persistence(self):
  self.assertIn('boot=live components persistence',(ROOT/'build.sh').read_text())
if __name__=='__main__': unittest.main()
