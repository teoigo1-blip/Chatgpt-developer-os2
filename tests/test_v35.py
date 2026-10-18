import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class DiagnosticsTests(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location("diagnostics",ROOT/"diagnose-build.py")
  self.mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.mod)
 def check(self, phrase, expected):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"build.log";path.write_text(phrase)
   self.assertIn(expected,[x["category"] for x in self.mod.diagnose(path)["findings"]])
 def test_missing_package(self): self.check("E: Unable to locate package fake-pkg", "missing_package")
 def test_network(self): self.check("Temporary failure resolving deb.debian.org", "network")
 def test_disk(self): self.check("No space left on device", "disk_space")
 def test_unknown(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"build.log";path.write_text("ok")
   self.assertEqual(self.mod.diagnose(path)["status"],"unclassified")
 def test_workflow(self):
  workflow=(ROOT/".github/workflows/build-live-iso.yml").read_text()
  self.assertIn("dist/build-diagnosis.json",workflow)
