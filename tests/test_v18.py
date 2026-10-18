import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V18(unittest.TestCase):
    def test_shell_syntax(self):
        for name in ('audit-packages.sh','build-host-check.sh','build-and-validate.sh'):
            self.assertEqual(subprocess.run(['bash','-n',str(ROOT/name)]).returncode,0)
    def test_build_guide(self):
        self.assertIn('sudo ./build-and-validate.sh',(ROOT/'BUILD_GUIDE.md').read_text())
    def test_no_usb_write(self):
        for name in ('audit-packages.sh','build-host-check.sh'):
            data=(ROOT/name).read_text()
            self.assertNotIn('mkfs.',data)
            self.assertNotIn('dd if=',data)
    def test_host_check_used(self):
        self.assertIn('./build-host-check.sh',(ROOT/'build-and-validate.sh').read_text())
