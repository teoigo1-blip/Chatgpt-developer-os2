#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for f in .github/workflows/build-live-iso.yml ci-build-iso.sh build.sh config/package-lists/developer.list.chroot; do
  [[ -s "$f" ]] || { echo "Falta: $f" >&2; exit 1; }
done
bash -n build.sh ci-build-iso.sh qemu-serial-boot-check.sh
python3 check-build-inputs.py
python3 check-target-packages.py
printf 'Preparado para subir a GitHub. La ISO solo se generará cuando se ejecute el workflow.\n'
