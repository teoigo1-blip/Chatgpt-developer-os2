#!/usr/bin/env bash
set -euo pipefail
ISO="${1:?Uso: smoke-test-uefi.sh archivo.iso}"
[[ -f "$ISO" ]] || { echo 'ISO no encontrada' >&2; exit 2; }
command -v qemu-system-x86_64 >/dev/null || { echo 'Instala qemu-system-x86' >&2; exit 3; }
OVMF="$(find /usr/share/OVMF /usr/share/ovmf -name 'OVMF_CODE*.fd' 2>/dev/null | head -1 || true)"
[[ -n "$OVMF" ]] || { echo 'Instala ovmf para probar UEFI' >&2; exit 4; }
qemu-system-x86_64 -m 2048 -smp 2 -machine q35 -drive "if=pflash,format=raw,readonly=on,file=$OVMF" -cdrom "$ISO" -boot d
