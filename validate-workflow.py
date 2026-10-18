#!/usr/bin/env python3
"""Offline structural validation for the GitHub Actions ISO workflow."""
from pathlib import Path
import sys
root = Path(__file__).resolve().parent
p = root / '.github/workflows/build-live-iso.yml'
s = p.read_text()
required = ['workflow_dispatch:', 'runs-on: ubuntu-24.04', 'sudo ./ci-build-iso.sh', 'ci-qemu-boot.sh release.iso bios', 'ci-qemu-boot.sh release.iso uefi', 'sha256sum -c iso.sha256', 'actions/upload-artifact@v4', 'if: failure()']
missing = [x for x in required if x not in s]
if missing:
    sys.exit('Missing required workflow checks: ' + ', '.join(missing))
if 'check-build-inputs.py --apt' in s:
    sys.exit('Ubuntu host APT must not be used as Debian trixie package gate')
print('Workflow structure OK (static only; not a GitHub Actions run)')
