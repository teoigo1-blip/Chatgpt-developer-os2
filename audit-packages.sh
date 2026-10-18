#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
command -v apt-cache >/dev/null || { echo 'Falta apt-cache' >&2; exit 2; }
if ! find /var/lib/apt/lists -maxdepth 1 -type f -name '*Packages*' 2>/dev/null | grep -q .; then
  echo 'SIN INDICES APT: sudo apt update en un anfitrión Debian 13 con red.' >&2
  exit 3
fi
missing=0; checked=0
while IFS= read -r pkg; do
  [[ -z "$pkg" || "$pkg" == \#* ]] && continue
  checked=$((checked+1))
  candidate=$(apt-cache policy "$pkg" | sed -n 's/^  Candidate: //p' | head -n 1)
  if [[ -z "$candidate" || "$candidate" == '(none)' ]]; then
    echo "SIN CANDIDATO LOCAL: $pkg"; missing=$((missing+1))
  fi
done < <(sed 's/[[:space:]]*#.*$//' config/package-lists/*.list.chroot | awk 'NF {print $1}' | sort -u)
echo "Comprobados: $checked; sin candidato local: $missing"
echo 'Auditoría del índice APT local, no prueba de compilación live-build.'
((missing == 0))
