import pathlib,subprocess,unittest
R=pathlib.Path(__file__).resolve().parents[1]
class TestV41(unittest.TestCase):
 def test_runner_syntax(self):
  self.assertEqual(subprocess.run(['python3','-m','py_compile',str(R/'run-tests-bounded.py')]).returncode,0)
 def test_runner_report(self):
  s=(R/'run-tests-bounded.py').read_text();self.assertIn('TimeoutExpired',s);self.assertIn('json.dumps',s)
 def test_ci_artifact(self):
  self.assertIn('unit-test-report',(R/'.github/workflows/build-live-iso.yml').read_text())
