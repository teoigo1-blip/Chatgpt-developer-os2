import pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Version23(unittest.TestCase):
 def test_scripts_syntax(self):
  for name in ('build-environment.sh','build-and-validate-v23.sh'):
   self.assertEqual(subprocess.run(['bash','-n',str(ROOT/name)]).returncode,0)
 def test_python_syntax(self):
  import ast
  ast.parse((ROOT/'iso-artifact-report.py').read_text())
 def test_no_automatic_usb_writes(self):
  for name in ('build-environment.sh','build-and-validate-v23.sh','iso-artifact-report.py'):
   content=(ROOT/name).read_text()
   self.assertNotIn('mkfs.',content)
   self.assertNotIn('dd if=',content)
 def test_report_help(self):
  self.assertEqual(subprocess.run(['python3',str(ROOT/'iso-artifact-report.py'),'--help'],capture_output=True).returncode,0)
