#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
[[ $(uname -s) == Linux ]] || { echo 'Requiere Linux' >&2; exit 2; }
[[ $(uname -m) == x86_64 ]] || { echo 'Requiere host x86_64' >&2; exit 2; }
failed=0
for tool in lb debootstrap xorriso mksquashfs sha256sum file; do
  if command -v "$tool" >/dev/null; then echo "OK: $tool"; else echo "FALTA: $tool"; failed=1; fi
done
if [[ $failed -ne 0 ]]; then
  echo 'Debian 13: sudo apt update && sudo apt install live-build debootstrap xorriso squashfs-tools' >&2
  exit 3
fi
./verify-boot-config.sh
printf 'Herramientas de construcción presentes; esto no garantiza un arranque correcto.\n'
