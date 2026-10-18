#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
echo '=== Static source checks (no root/network required) ==='
python3 ./audit-package-lists.py
bash -n ./*.sh
python3 -m unittest discover -s tests -p 'test_*.py'
echo '=== Build tool availability ==='
missing=0
for tool in lb debootstrap xorriso mksquashfs; do
  if command -v "$tool" >/dev/null 2>&1; then echo "OK $tool"; else echo "MISSING $tool"; missing=1; fi
done
if (( missing )); then
  echo 'ISO build unavailable here. On Debian 13: sudo apt update && sudo apt install live-build debootstrap xorriso squashfs-tools'
  exit 3
fi
echo 'Build tools present. No ISO has been built or boot-tested by this check.'
