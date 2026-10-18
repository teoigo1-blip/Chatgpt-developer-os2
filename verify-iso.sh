#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
if (( $# != 1 )); then echo "Uso: $0 /ruta/imagen.iso" >&2; exit 2; fi
iso="$(realpath "$1")"
[[ -f "$iso" ]] || { echo "ISO inexistente: $iso" >&2; exit 2; }
command -v xorriso >/dev/null || { echo 'Falta xorriso' >&2; exit 2; }
command -v file >/dev/null || { echo 'Falta file' >&2; exit 2; }
size=$(stat -c%s "$iso")
(( size >= 104857600 )) || { echo 'ISO sospechosamente pequeña' >&2; exit 2; }
file "$iso"
file --mime-type "$iso" | grep -Eq 'application/(x-iso9660-image|octet-stream)' || { echo 'Formato ISO no reconocido' >&2; exit 2; }
report="${iso%.iso}.boot-report.txt"
xorriso -indev "$iso" -report_el_torito plain >"$report" 2>&1 || { cat "$report" >&2; exit 2; }
grep -Eiq 'El Torito|boot' "$report" || { echo 'No se detecta información de arranque' >&2; exit 2; }
sha256sum "$iso" >"${iso}.sha256"
echo "Verificación estática correcta: $iso"
echo 'Pendiente: arranque real BIOS/UEFI y persistencia.'
