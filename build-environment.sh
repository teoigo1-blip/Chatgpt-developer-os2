#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
missing=0
for command in lb debootstrap xorriso mksquashfs; do
  if command -v "$command" >/dev/null 2>&1; then
    printf 'OK %-16s %s\n' "$command" "$(command -v "$command")"
  else
    printf 'FALTA %s\n' "$command" >&2
    missing=1
  fi
done
if [[ "$(uname -m)" != x86_64 ]]; then echo 'Requiere host Linux x86_64' >&2; missing=1; fi
if [[ "$(uname -s)" != Linux ]]; then echo 'Requiere Linux' >&2; missing=1; fi
free_kib=$(df -Pk . | awk 'NR==2 {print $4}')
if (( free_kib < 15728640 )); then echo 'Se recomiendan al menos 15 GiB libres' >&2; missing=1; fi
if (( missing )); then
  echo 'En Debian 13: sudo apt update && sudo apt install live-build debootstrap xorriso squashfs-tools' >&2
  exit 1
fi
