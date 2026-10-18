#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
if (( EUID != 0 )); then echo 'Ejecuta con sudo' >&2; exit 2; fi
LOGDIR="${LOGDIR:-$PWD/build-reports}"
mkdir -p "$LOGDIR"
log="$LOGDIR/build-$(date -u +%Y%m%dT%H%M%SZ).log"
./build-host-check.sh | tee "$LOGDIR/preflight.txt"
# No aceptar ISO preexistentes como resultado de la nueva compilación.
mapfile -t existing < <(find . -maxdepth 1 -type f -name '*.iso' -print)
if (( ${#existing[@]} )); then
  printf 'Hay ISO anteriores. Muévelas fuera del directorio antes de compilar:\n' >&2
  printf '%s\n' "${existing[@]}" >&2
  exit 3
fi
set +e
./build.sh 2>&1 | tee "$log"
status=${PIPESTATUS[0]}
set -e
if (( status != 0 )); then echo "Compilación fallida: $log" >&2; exit "$status"; fi
mapfile -t isos < <(find . -maxdepth 1 -type f -name '*.iso' -print)
if (( ${#isos[@]} != 1 )); then echo 'No se ha generado exactamente una ISO' >&2; exit 4; fi
./verify-iso.sh "${isos[0]}" | tee "$LOGDIR/iso-check.txt"
echo "ISO generada: ${isos[0]}"
echo 'Pendiente prueba de arranque BIOS/UEFI y persistencia.'
