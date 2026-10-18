#!/usr/bin/env bash
# Boots a live ISO in QEMU and checks evidence of Linux kernel startup.
# Does not establish graphical desktop functionality or USB persistence.
set -euo pipefail
if (( $# < 2 || $# > 3 )); then echo "Uso: $0 imagen.iso bios|uefi [segundos]" >&2; exit 2; fi
iso=$(realpath "$1")
mode=$2
seconds=${3:-120}
[[ -s "$iso" && "$seconds" =~ ^[0-9]+$ && "$seconds" -ge 20 ]] || { echo 'ISO o duración no válida' >&2; exit 2; }
[[ "$mode" == bios || "$mode" == uefi ]] || { echo 'Modo inválido' >&2; exit 2; }
for cmd in qemu-system-x86_64 timeout grep; do command -v "$cmd" >/dev/null || { echo "Falta $cmd" >&2; exit 2; }; done
args=(-m 2048 -smp 2 -boot d -cdrom "$iso" -nic none -display none -monitor none -serial stdio -no-reboot)
if [[ "$mode" == uefi ]]; then
 firmware=''
 for candidate in /usr/share/OVMF/OVMF_CODE_4M.fd /usr/share/OVMF/OVMF_CODE.fd /usr/share/ovmf/OVMF.fd; do
  if [[ -r "$candidate" ]]; then firmware=$candidate; break; fi
 done
 [[ -n "$firmware" ]] || { echo 'Firmware UEFI no encontrado' >&2; exit 2; }
 args+=(-drive "if=pflash,format=raw,readonly=on,file=$firmware")
fi
log=$(mktemp)
trap 'rm -f "$log"' EXIT
set +e
timeout --signal=TERM --kill-after=5s "${seconds}s" qemu-system-x86_64 "${args[@]}" >"$log" 2>&1
status=$?
set -e
if grep -Eiq '^\[[[:space:]]*[0-9]+\.[0-9]+\] Linux version [0-9]|^Linux version [0-9]|Run /init as init process|systemd\[[0-9]+\]' "$log"; then
 echo "OK: $mode: evidencia de arranque del kernel en consola serie"
 exit 0
fi
echo "SIN CONFIRMAR: $mode: no se encontró evidencia del kernel (QEMU exit=$status)" >&2
tail -n 25 "$log" >&2
exit 1
