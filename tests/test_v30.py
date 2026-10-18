import pathlib
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class TestV30(unittest.TestCase):
    def test_iso_inspector_syntax(self):
        import subprocess
        subprocess.run(['bash','-n',str(ROOT/'inspect-iso-boot-files.sh')],check=True)
    def test_checks_kernel_and_initrd(self):
        s=(ROOT/'inspect-iso-boot-files.sh').read_text()
        self.assertIn('/live/vmlinuz',s)
        self.assertIn('/live/initrd',s)
        self.assertIn('-report_el_torito',s)
    def test_workflow_enforces_inspection(self):
        s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
        self.assertIn('./inspect-iso-boot-files.sh "${images[0]}"',s)
