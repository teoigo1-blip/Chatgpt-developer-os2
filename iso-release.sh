#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
if (( $# != 1 )); then echo "Uso: $0 /ruta/imagen.iso" >&2; exit 2; fi
iso=$(realpath -e "$1")
[[ -f "$iso" && "$iso" == *.iso ]] || { echo 'Se requiere una ISO existente' >&2; exit 2; }
./verify-iso.sh "$iso"
./release-check.sh
printf '\nResultado: comprobaciones estáticas superadas.\n'
printf 'No implica arranque BIOS/UEFI ni persistencia funcional.\n'
printf 'Para pruebas manuales: ./boot-test-v21.sh bios "%s"\n' "$iso"
printf 'Para UEFI: ./boot-test-v21.sh uefi "%s"\n' "$iso"
