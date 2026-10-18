import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V22(unittest.TestCase):
    def test_package_lists(self):
        self.assertEqual(subprocess.run(['python3',str(ROOT/'audit-package-lists.py')],capture_output=True).returncode,0)
    def test_shell_syntax(self):
        scripts=list(ROOT.glob('*.sh'))
        self.assertEqual(subprocess.run(['bash','-n',*map(str,scripts)],capture_output=True).returncode,0)
    def test_no_automatic_disk_writes_in_readiness(self):
        data=(ROOT/'build-readiness.sh').read_text()
        self.assertNotIn('dd if=',data)
        self.assertNotIn('mkfs.',data)
    def test_readiness_uses_tests(self):
        self.assertIn('unittest discover', (ROOT/'build-readiness.sh').read_text())
