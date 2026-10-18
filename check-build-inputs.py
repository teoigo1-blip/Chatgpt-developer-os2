#!/usr/bin/env python3
"""Check local live-build inputs; optionally check package names using apt-cache."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--apt', action='store_true', help='Check package candidates against host APT (may differ from Debian target)')
args = parser.parse_args()
required = [root/'build.sh', root/'config/package-lists', root/'config/includes.chroot']
for p in required:
    if not p.exists():
        sys.exit(f'Missing required build input: {p.relative_to(root)}')
packages = {}
for manifest in sorted((root/'config/package-lists').glob('*.list.chroot')):
    for number, raw in enumerate(manifest.read_text().splitlines(), 1):
        name = raw.split('#', 1)[0].strip()
        if not name:
            continue
        if len(name.split()) != 1:
            sys.exit(f'Invalid package line: {manifest.name}:{number}')
        packages.setdefault(name, []).append(f'{manifest.name}:{number}')
if not packages:
    sys.exit('No packages found in .list.chroot manifests')
duplicates = {name: refs for name, refs in packages.items() if len(refs) > 1}
if duplicates:
    sys.exit(f'Duplicate packages: {duplicates}')
print(f'OK: {len(packages)} unique packages; live-build inputs exist')
if args.apt:
    if not shutil.which('apt-cache'):
        sys.exit('apt-cache not installed')
    missing = []
    for name in packages:
        result = subprocess.run(['apt-cache', 'policy', name], text=True, capture_output=True)
        if result.returncode != 0 or not any(line.strip().startswith('Candidate:') and '(none)' not in line for line in result.stdout.splitlines()):
            missing.append(name)
    if missing:
        print('WARNING: Host APT has no candidate for: ' + ', '.join(missing), file=sys.stderr)
        print('Host APT may differ from Debian trixie. This is diagnostic, not a definitive build failure.')
    else:
        print('Host APT candidates found for all manifest packages')
