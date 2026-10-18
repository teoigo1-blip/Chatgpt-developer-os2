import pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestV29(unittest.TestCase):
 def test_manual_publish_off(self):
  s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
  self.assertIn('default: false',s)
  self.assertIn('needs: iso',s)
 def test_release_integrity(self):
  s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
  self.assertIn('sha256sum -c iso.sha256',s)
  self.assertIn('gh release create',s)
  self.assertIn('--prerelease',s)
 def test_no_overwrite(self):
  s=(ROOT/'.github/workflows/build-live-iso.yml').read_text()
  self.assertIn('gh release view',s)
  self.assertIn('refusing overwrite',s)
