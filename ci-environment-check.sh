#!/usr/bin/env bash
# Preflight for a real Debian Live ISO build; no disk writes or installs.
set -euo pipefail
failed=0
for tool in lb debootstrap xorriso mksquashfs grub-mkimage; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'OK: %s\n' "$tool"
  else
    printf 'MISSING: %s\n' "$tool" >&2
    failed=1
  fi
done
if [[ $(uname -m) != x86_64 ]]; then
  echo 'ERROR: build host must be x86_64' >&2
  failed=1
fi
available_kib=$(df -Pk . | awk 'NR==2 {print $4}')
if [[ ! "$available_kib" =~ ^[0-9]+$ ]] || (( available_kib < 15728640 )); then
  echo 'ERROR: at least 15 GiB free disk space recommended for building' >&2
  failed=1
else
  printf 'OK: free space %s KiB\n' "$available_kib"
fi
exit "$failed"
