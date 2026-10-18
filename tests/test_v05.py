import ast,unittest,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BIN=ROOT/'config/includes.chroot/usr/local/bin'
class TestV05(unittest.TestCase):
 def test_python_scripts_parse(self):
  for name in ('developer-panel','developer-setup','developer-codex'):
   ast.parse((BIN/name).read_text())
 def test_setup_groups(self):
  spec=importlib.util.spec_from_loader('setup',loader=None)
  ns={'__name__':'not_main'}
  exec(compile((BIN/'developer-setup').read_text(),str(BIN/'developer-setup'),'exec'),ns)
  self.assertEqual(ns['missing_packages']('base',lambda pkg:pkg=='git'),['python3','python3-venv','cmake','ninja-build'])
 def test_panel_supervised_codex(self):
  s=(BIN/'developer-panel').read_text()
  self.assertIn('askyesno',s);self.assertIn('codex_task',s);self.assertIn("'--confirm'",s)
if __name__=='__main__':unittest.main()
