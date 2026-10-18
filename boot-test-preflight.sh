#!/usr/bin/env bash
set -euo pipefail
if (( $# != 1 )); then echo "Uso: $0 imagen.iso" >&2; exit 2; fi
iso=$(realpath "$1")
[[ -s "$iso" ]] || { echo "ISO inexistente o vacía" >&2; exit 2; }
command -v qemu-system-x86_64 >/dev/null || { echo "Falta QEMU" >&2; exit 2; }
firmware=''
for candidate in /usr/share/OVMF/OVMF_CODE_4M.fd /usr/share/OVMF/OVMF_CODE.fd /usr/share/ovmf/OVMF.fd; do
  if [[ -r "$candidate" ]]; then firmware="$candidate"; break; fi
done
[[ -n "$firmware" ]] || { echo "No se encuentra firmware UEFI OVMF" >&2; exit 2; }
printf 'BIOS: QEMU disponible\nUEFI: %s\nISO: %s\n' "$firmware" "$iso"
echo 'Esta prueba valida prerrequisitos, NO demuestra que el sistema arranque.'
