import pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
BIN=ROOT/'config/includes.chroot/usr/local/bin'
class V09(unittest.TestCase):
 def test_browser_official(self):
  self.assertIn('https://chatgpt.com/',(BIN/'developer-chatgpt').read_text())
 def test_no_api_integration(self):
  for n in ('developer-vision','developer-loop'):
   self.assertIn('deshabilitado',(BIN/n).read_text())
 def test_login_panel(self):
  p=(BIN/'developer-panel').read_text()
  self.assertIn('codex_login',p)
  self.assertIn('developer-chatgpt',p)
 def test_codex_uses_official_login(self):
  self.assertIn("[codex,'login']",(BIN/'developer-codex').read_text())
if __name__=='__main__': unittest.main()
