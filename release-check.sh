#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
python3 -m unittest discover -s tests -p 'test_*.py'
for script in *.sh config/includes.chroot/usr/local/bin/*; do
  if [[ -f "$script" ]] && head -c 2 "$script" | grep -q '#!'; then
    if head -n1 "$script" | grep -q bash; then bash -n "$script"; fi
  fi
done
if command -v lb >/dev/null 2>&1; then echo 'live-build: disponible'; else echo 'live-build: NO disponible (ISO sin construir)'; fi
