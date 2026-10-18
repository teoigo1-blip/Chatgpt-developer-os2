import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V20(unittest.TestCase):
    def test_shell_syntax(self):
        for name in ('build-and-validate.sh','verify-iso.sh','release-check.sh'):
            self.assertEqual(subprocess.run(['bash','-n',str(ROOT/name)]).returncode,0)
    def test_verify_requires_argument(self):
        p=subprocess.run(['bash',str(ROOT/'verify-iso.sh')],capture_output=True)
        self.assertEqual(p.returncode,2)
    def test_verify_missing_iso(self):
        p=subprocess.run(['bash',str(ROOT/'verify-iso.sh'),'/tmp/nonexistent-developer-os-v20.iso'],capture_output=True)
        self.assertEqual(p.returncode,2)
    def test_stale_iso_guard(self):
        self.assertIn('ISO anteriores',(ROOT/'build-and-validate.sh').read_text())
    def test_no_disk_writes(self):
        for name in ('verify-iso.sh','release-check.sh'):
            t=(ROOT/name).read_text()
            self.assertNotIn('mkfs.',t)
            self.assertNotIn('dd if=',t)
