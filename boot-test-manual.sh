#!/usr/bin/env bash
set -euo pipefail
if (( $# != 2 )); then echo "Uso: $0 bios|uefi /ruta/imagen.iso" >&2; exit 2; fi
mode=$1
iso=$(realpath "$2")
[[ -s "$iso" ]] || { echo 'ISO no encontrada' >&2; exit 2; }
command -v qemu-system-x86_64 >/dev/null || exit 2
args=(-m 3072 -smp 2 -boot d -cdrom "$iso" -nic user -display gtk)
case "$mode" in
 bios) ;;
 uefi)
  firmware=''
  for candidate in /usr/share/OVMF/OVMF_CODE_4M.fd /usr/share/OVMF/OVMF_CODE.fd /usr/share/ovmf/OVMF.fd; do
   [[ -r "$candidate" ]] && { firmware="$candidate"; break; }
  done
  [[ -n "$firmware" ]] || { echo 'Falta OVMF' >&2; exit 2; }
  args+=(-drive "if=pflash,format=raw,readonly=on,file=$firmware")
  ;;
 *) echo 'Modo inválido' >&2; exit 2 ;;
esac
printf 'Prueba manual %s: comprueba arranque, inicio de sesión, XFCE, Codex y red.\n' "$mode"
exec qemu-system-x86_64 "${args[@]}"
