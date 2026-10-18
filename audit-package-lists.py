#!/usr/bin/env python3
"""Check Debian live-build package lists without network access."""
from pathlib import Path
from collections import defaultdict
import sys
root=Path(__file__).resolve().parent
seen=defaultdict(list)
errors=[]
for path in sorted((root/'config/package-lists').glob('*.list.chroot')):
    for n,line in enumerate(path.read_text().splitlines(),1):
        package=line.split('#',1)[0].strip()
        if not package: continue
        if len(package.split()) != 1 or any(c in package for c in ';|&$`'):
            errors.append(f'{path.name}:{n}: invalid package entry: {package}')
        else: seen[package].append(f'{path.name}:{n}')
for package,locations in sorted(seen.items()):
    if len(locations)>1: errors.append(f'duplicate {package}: {", ".join(locations)}')
print(f'Checked {len(seen)} unique package names across package lists')
for err in errors: print('ERROR:',err,file=sys.stderr)
sys.exit(1 if errors else 0)
