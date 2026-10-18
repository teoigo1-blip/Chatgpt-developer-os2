#!/usr/bin/env bash
# Preserve QEMU output even when a boot check fails.
set -Eeuo pipefail
if (( $# != 3 )); then echo "Usage: $0 ISO bios|uefi TIMEOUT_SECONDS" >&2; exit 2; fi
iso=$(realpath -- "$1")
mode=$2
seconds=$3
[[ -f "$iso" && "$mode" =~ ^(bios|uefi)$ && "$seconds" =~ ^[0-9]+$ ]] || { echo "Invalid arguments" >&2; exit 2; }
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
mkdir -p "$root/dist/boot-evidence"
log="$root/dist/boot-evidence/${mode}.log"
set +e
"$root/qemu-serial-boot-check.sh" "$iso" "$mode" "$seconds" >"$log" 2>&1
status=$?
set -e
cat "$log"
printf 'mode=%s\nexit_code=%s\n' "$mode" "$status" >"$root/dist/boot-evidence/${mode}.status"
exit "$status"
