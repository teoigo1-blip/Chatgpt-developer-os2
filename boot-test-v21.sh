#!/usr/bin/env bash
set -euo pipefail
if (( $# != 2 )); then echo "Uso: $0 bios|uefi /ruta/imagen.iso" >&2; exit 2; fi
mode=$1; iso=$(realpath -e "$2")
[[ -f "$iso" ]] || { echo 'ISO inexistente' >&2; exit 2; }
[[ "$mode" == bios || "$mode" == uefi ]] || { echo 'Modo inválido' >&2; exit 2; }
command -v qemu-system-x86_64 >/dev/null || { echo 'Instala qemu-system-x86' >&2; exit 3; }
args=(-machine q35 -m 2048 -smp 2 -boot d -cdrom "$iso" -display gtk -no-reboot)
if [[ "$mode" == uefi ]]; then
  firmware=''
  for path in /usr/share/OVMF/OVMF_CODE_4M.fd /usr/share/OVMF/OVMF_CODE.fd /usr/share/ovmf/OVMF.fd; do
    if [[ -f "$path" ]]; then firmware=$path; break; fi
  done
  [[ -n "$firmware" ]] || { echo 'Falta firmware OVMF (apt install ovmf)' >&2; exit 3; }
  args+=(-bios "$firmware")
fi
echo "Arranque interactivo $mode; comprueba escritorio y reinicio manualmente."
exec qemu-system-x86_64 "${args[@]}"
