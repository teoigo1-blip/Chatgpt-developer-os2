#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(realpath "$0")")"
echo 'ChatGPT Developer OS — comprobación previa'
[ "$(uname -m)" = x86_64 ] || { echo 'Se requiere host Linux x86_64' >&2; exit 2; }
for x in lb debootstrap xorriso mksquashfs; do
  command -v "$x" >/dev/null || { echo "Falta $x (instalar live-build debootstrap xorriso squashfs-tools)" >&2; exit 2; }
done
[ -f config/package-lists/developer.list.chroot ] || exit 2
[ -f build.sh ] || exit 2
space=$(df -Pk . | awk 'NR==2{print $4}')
[ "$space" -ge 15728640 ] || { echo 'Se recomiendan al menos 15 GiB libres para construir' >&2; exit 2; }
echo 'Comprobación previa superada. La construcción aún no está verificada.'
