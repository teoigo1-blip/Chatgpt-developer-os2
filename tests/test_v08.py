import pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
BIN=ROOT/'config/includes.chroot/usr/local/bin'
class DeprecatedVisualApi(unittest.TestCase):
 def test_visual_api_disabled(self):
  self.assertIn('deshabilitado',(BIN/'developer-vision').read_text())
  self.assertIn('deshabilitado',(BIN/'developer-loop').read_text())
