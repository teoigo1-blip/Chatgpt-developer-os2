import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestV21(unittest.TestCase):
    def test_scripts_syntax(self):
        for name in ('iso-release.sh','boot-test-v21.sh'):
            self.assertEqual(subprocess.run(['bash','-n',str(ROOT/name)]).returncode,0)
    def test_invalid_mode(self):
        p=subprocess.run([str(ROOT/'boot-test-v21.sh'),'other',str(ROOT/'README.md')],capture_output=True)
        self.assertNotEqual(p.returncode,0)
    def test_no_iso(self):
        p=subprocess.run([str(ROOT/'iso-release.sh'),'/tmp/no-such-v21.iso'],capture_output=True)
        self.assertNotEqual(p.returncode,0)
    def test_no_disk_writes(self):
        for name in ('iso-release.sh','boot-test-v21.sh'):
            content=(ROOT/name).read_text()
            self.assertNotIn('mkfs.',content)
            self.assertNotIn('dd if=',content)
