import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class IsoInspection(unittest.TestCase):
    def inspect(self, mode):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'image.iso').write_bytes(b'fixture')
            tool = root/'xorriso'
            tool.write_text('''#!/usr/bin/env python3
import os, sys
mode=os.environ['INSPECTION_FIXTURE']
if mode=='tool-error':
    print('fixture xorriso failure', file=sys.stderr); sys.exit(5)
if '-find' in sys.argv:
    assert '-print' not in sys.argv
    assert sys.argv[-3:]==['-exec','echo','--']
    if mode!='missing-kernel': print("'/live/vmlinuz-6.12-amd64'")
    print("'/live/initrd.img-6.12-amd64'")
    print("'/live/filesystem.squashfs'")
else:
    print('El Torito boot img : 1 BIOS y none', file=sys.stderr)
    if mode!='missing-uefi': print('El Torito boot img : 2 UEFI y none', file=sys.stderr)
''')
            tool.chmod(0o755)
            env={**os.environ,'PATH':str(root)+os.pathsep+os.environ['PATH'],'INSPECTION_FIXTURE':mode}
            return subprocess.run(['bash',str(ROOT/'inspect-iso-boot-files.sh'),str(root/'image.iso')],env=env,capture_output=True,text=True,timeout=10)

    def test_quoted_paths_and_stderr_boot_report(self):
        result=self.inspect('valid')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_missing_kernel_rejected(self):
        self.assertNotEqual(self.inspect('missing-kernel').returncode,0)

    def test_missing_uefi_rejected(self):
        self.assertNotEqual(self.inspect('missing-uefi').returncode,0)

    def test_tool_error_is_visible(self):
        result=self.inspect('tool-error')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('fixture xorriso failure',result.stderr)
