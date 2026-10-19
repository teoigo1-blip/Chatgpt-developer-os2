#!/usr/bin/env bash
# Inspect ISO contents independently of the build configuration.
set -euo pipefail
if [[ $# -ne 1 || ! -s $1 ]]; then echo "Usage: $0 image.iso" >&2; exit 2; fi
iso=$(realpath -- "$1")
for cmd in xorriso grep python3; do command -v "$cmd" >/dev/null || { echo "Missing $cmd" >&2; exit 2; }; done
listing=$(mktemp); boot=$(mktemp); errors=$(mktemp)
trap 'rm -f -- "$listing" "$boot" "$errors"' EXIT
if ! xorriso -indev "$iso" -find / -type f -exec echo -- >"$listing" 2>"$errors"; then
 cat "$errors" >&2; exit 2
fi
# xorriso quotes paths; decode them rather than relying on shell find output.
python3 - "$listing" <<'PY'
from pathlib import Path
import re, shlex, sys
paths = [p for line in Path(sys.argv[1]).read_text().splitlines() for p in shlex.split(line)]
for pattern, label in ((r'/live/vmlinuz[^/]*', 'kernel'), (r'/live/initrd[^/]*', 'initrd'), (r'/live/filesystem[^/]*\.squashfs', 'root filesystem')):
    if not any(re.fullmatch(pattern, p) for p in paths):
        raise SystemExit('FAIL: missing ' + label)
PY
if ! xorriso -indev "$iso" -report_el_torito plain >"$boot" 2>&1; then
 cat "$boot" >&2; exit 2
fi
grep -Eq 'El Torito boot img[[:space:]]*:[[:space:]]*[0-9]+[[:space:]]+BIOS' "$boot" || { cat "$boot" >&2; echo 'FAIL: no BIOS boot image' >&2; exit 1; }
grep -Eq 'El Torito boot img[[:space:]]*:[[:space:]]*[0-9]+[[:space:]]+UEFI' "$boot" || { cat "$boot" >&2; echo 'FAIL: no UEFI boot image' >&2; exit 1; }
printf 'OK: kernel and initrd found; El Torito report available\n'
cat "$boot"
