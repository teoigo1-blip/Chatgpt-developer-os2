#!/usr/bin/env bash
# Inspect ISO contents independently of the build configuration.
set -euo pipefail
if [[ $# -ne 1 || ! -s $1 ]]; then echo "Usage: $0 image.iso" >&2; exit 2; fi
iso=$(realpath -- "$1")
for cmd in xorriso grep; do command -v "$cmd" >/dev/null || { echo "Missing $cmd" >&2; exit 2; }; done
listing=$(mktemp); boot=$(mktemp)
trap 'rm -f -- "$listing" "$boot"' EXIT
xorriso -indev "$iso" -find / -type f -print >"$listing" 2>/dev/null
xorriso -indev "$iso" -report_el_torito plain >"$boot" 2>/dev/null
if ! grep -Eq '^/live/vmlinuz[^/]*$' "$listing"; then echo 'FAIL: missing /live/vmlinuz' >&2; exit 1; fi
if ! grep -Eq '^/live/initrd[^/]*$' "$listing"; then echo 'FAIL: missing /live/initrd' >&2; exit 1; fi
if ! grep -Eiq 'El Torito|BIOS|UEFI|EFI' "$boot"; then echo 'FAIL: no El Torito boot evidence' >&2; exit 1; fi
printf 'OK: kernel and initrd found; El Torito report available\n'
cat "$boot"
