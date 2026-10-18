#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
ISO="${1:?Uso: ./validate-live.sh ruta/a/imagen.iso}"
[[ -f "$ISO" ]] || { echo "ISO inexistente: $ISO" >&2; exit 2; }
ISO="$(realpath "$ISO")"
mkdir -p validation-reports
REPORT="validation-reports/validation-$(date -u +%Y%m%dT%H%M%SZ).txt"
{
 echo "ISO: $ISO"
 echo "SHA256: $(sha256sum "$ISO")"
 echo 'Chequeo estático:'
 ./verify-iso.sh "$ISO"
 echo 'IMPORTANTE: el arranque y la persistencia NO quedan verificados con el chequeo estático.'
} | tee "$REPORT"
cat <<EOF

Para probar visualmente BIOS:
  ./smoke-test-qemu.sh "$ISO"
Para probar visualmente UEFI:
  ./smoke-test-uefi.sh "$ISO"
Para comprobar persistencia, utiliza un USB de pruebas y sigue PERSISTENCE_TEST.md.
Informe: $REPORT
EOF
