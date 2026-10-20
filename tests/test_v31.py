import pathlib
import subprocess
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class TestV31(unittest.TestCase):
    def test_shell_syntax(self):
        for name in ('ci-environment-check.sh', 'ci-build-iso.sh'):
            self.assertEqual(subprocess.run(['bash','-n',str(ROOT/name)]).returncode,0)
    def test_workflow_has_preflight(self):
        self.assertIn('run: ./ci-environment-check.sh', (ROOT/'.github/workflows/build-live-iso.yml').read_text())
    def test_build_logs_preserved(self):
        s=(ROOT/'ci-build-iso.sh').read_text()
        self.assertIn('Full log: $output_dir/build.log',s)
        self.assertIn('tail -n 100 "$output_dir/build.log"',s)
    def test_preflight_is_non_destructive(self):
        s=(ROOT/'ci-environment-check.sh').read_text()
        for token in ('mkfs.', 'dd if=', 'wipefs ', 'parted '): self.assertNotIn(token,s)
