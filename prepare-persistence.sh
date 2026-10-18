#!/usr/bin/env bash
set -euo pipefail
# No toca discos ni particiones: crea exclusivamente un fichero de configuración.
TARGET="${1:-}"
if [[ -z "$TARGET" || ! -d "$TARGET" ]]; then
  echo "Uso: $0 /ruta/a/particion/persistence/montada" >&2; exit 2
fi
if [[ -e "$TARGET/persistence.conf" ]]; then
  echo "Ya existe persistence.conf; no se sobrescribe" >&2; exit 3
fi
printf '/ union\n' > "$TARGET/persistence.conf"
echo "Configuración creada. La partición debe ser ext4 con etiqueta persistence y el USB debe arrancar con persistence."
