#!/usr/bin/env python3
"""Validate the source tree against the shipped SHA256 manifest."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
entries=(root/'SOURCE_SHA256SUMS').read_text().splitlines()
fail=[]
for line in entries:
    expected, relative=line.split('  ',1)
    path=root/relative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
        fail.append(relative)
if fail:
    print('Mismatch or missing:', ', '.join(fail), file=sys.stderr)
    sys.exit(1)
print(f'OK: {len(entries)} source files verified')
