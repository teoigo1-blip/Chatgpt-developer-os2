#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
ISO="${1:-}"
if [[ -z "$ISO" || ! -f "$ISO" ]]; then echo "Uso: $0 /ruta/imagen.iso" >&2; exit 2; fi
command -v qemu-system-x86_64 >/dev/null || { echo 'Instala qemu-system-x86' >&2; exit 2; }
echo 'Arranque de prueba BIOS en QEMU. Comprueba manualmente escritorio, red y panel. Cierra QEMU para finalizar.'
exec qemu-system-x86_64 -m 3072 -smp 2 -boot d -cdrom "$ISO" -nic user -display gtk
