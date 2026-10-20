#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY'
from pathlib import Path
p=Path('build.sh').read_text()
assert '--binary-images iso-hybrid' in p
assert '--bootappend-live' in p and 'persistence' in p
assert '--bootloaders' not in p  # Unsupported by the runner's live-build
assert '--image-name' not in p  # Unsupported by the runner's live-build
assert Path('prepare-persistence.sh').exists()
print('Configuración de arranque híbrido BIOS/UEFI: comprobación estática OK')
PY
