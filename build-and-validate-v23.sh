#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
./build-environment.sh
if (( EUID != 0 )); then echo 'Ejecuta con sudo para construir la ISO' >&2; exit 2; fi
./build-and-validate.sh
mapfile -t isos < <(find . -maxdepth 1 -type f -name '*.iso' -print)
if (( ${#isos[@]} != 1 )); then echo 'Se esperaba exactamente una ISO' >&2; exit 3; fi
./iso-artifact-report.py "${isos[0]}" --output build-reports/iso-artifact.json
printf 'Informe: %s/build-reports/iso-artifact.json\n' "$PWD"
