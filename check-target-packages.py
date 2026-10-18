#!/usr/bin/env python3
"""Check Debian target manifests without mistaking Ubuntu APT for Debian APT."""
from pathlib import Path
import sys
root = Path(__file__).resolve().parent
lists = root/'config/package-lists'
errors=[]
packages=[]
for manifest in sorted(lists.glob('*.list.chroot')):
    for lineno, line in enumerate(manifest.read_text().splitlines(), 1):
        name=line.split('#',1)[0].strip()
        if not name: continue
        if any(c.isspace() for c in name): errors.append(f'{manifest.name}:{lineno}: multiple tokens')
        packages.append(name)
for name in ('grub-pc-bin','grub-efi-amd64-bin','isolinux','syslinux-common','memtest86+','shim-signed'):
    if name in packages: errors.append(f'{name}: host boot package must not be installed inside live image')
if len(packages)!=len(set(packages)): errors.append('duplicate package names')
if errors:
    print('\n'.join(errors),file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(packages)} packages; boot tooling separated from live chroot')
