import pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class V42(unittest.TestCase):
    def test_guide(self):
        self.assertIn('Run workflow',(ROOT/'GITHUB_FIRST_BUILD.md').read_text())
    def test_fresh_build_guard(self):
        self.assertIn('Ensure fresh build output',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
    def test_evidence(self):
        self.assertIn('source-validation',(ROOT/'.github/workflows/build-live-iso.yml').read_text())
