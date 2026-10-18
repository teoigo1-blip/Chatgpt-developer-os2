import pathlib, subprocess, unittest
R=pathlib.Path(__file__).resolve().parents[1]
class V32(unittest.TestCase):
    def test_manifest_separates_host_boot_tools(self):
        self.assertEqual(subprocess.run(['python3',str(R/'check-target-packages.py')],capture_output=True).returncode,0)
    def test_ci_runs_target_check(self):
        self.assertIn('python3 ./check-target-packages.py',(R/'.github/workflows/build-live-iso.yml').read_text())
    def test_boot_package_manifest_is_firmware_only(self):
        s=(R/'config/package-lists/boot-compat.list.chroot').read_text()
        self.assertNotIn('memtest86+',s)
        self.assertIn('firmware-iwlwifi',s)
