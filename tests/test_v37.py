import pathlib, subprocess, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class V37(unittest.TestCase):
    def test_wrapper_syntax(self):
        subprocess.run(['bash','-n',str(ROOT/'ci-qemu-boot.sh')],check=True)
    def test_evidence_steps(self):
        s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
        self.assertIn('if: always()',s)
        self.assertIn('dist/boot-evidence/',s)
        self.assertIn('ci-qemu-boot.sh release.iso bios',s)
        self.assertIn('ci-qemu-boot.sh release.iso uefi',s)
    def test_wrapper_rejects_invalid_arguments(self):
        r=subprocess.run(['bash',str(ROOT/'ci-qemu-boot.sh')],capture_output=True)
        self.assertEqual(r.returncode,2)
