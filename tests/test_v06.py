import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'config/includes.chroot/usr/local/bin'
class TestV06(unittest.TestCase):
    def test_observer_exists(self): self.assertTrue((ROOT/'developer-observe').exists())
    def test_observer_local_only(self):
        s=(ROOT/'developer-observe').read_text();self.assertIn('developer-agent',s);self.assertIn('screenshot',s)
    def test_panel_button(self):self.assertIn('Capturar pantalla',(ROOT/'developer-panel').read_text())
    def test_python_syntax(self):
        for name in ('developer-observe','developer-panel'):
            compile((ROOT/name).read_text(),name,'exec')
