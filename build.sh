#!/usr/bin/env bash
set -euo pipefail
if [ "$(id -u)" -ne 0 ]; then echo 'Ejecuta con sudo.' >&2; exit 1; fi
if ! command -v lb >/dev/null; then echo 'Falta live-build: apt install live-build' >&2; exit 1; fi
cd "$(dirname "$(realpath "$0")")"
# Preserve the checked-in config/ tree (including package lists and desktop files).
# --purge may remove configuration; never use it here.
lb clean
lb config \
  --mode debian \
  --distribution trixie \
  --architectures amd64 \
  --binary-images iso-hybrid \
  --debian-installer none \
  --archive-areas 'main contrib non-free non-free-firmware' \
  --bootloaders 'grub-efi syslinux' \
  --bootappend-live 'boot=live components persistence persistence-label=persistence locales=es_ES.UTF-8 keyboard-layouts=es console=tty0 console=ttyS0,115200n8' \
  --iso-application 'ChatGPT Developer OS' \
  --iso-publisher 'Community build' \
  --image-name chatgpt-developer-os
lb build
printf '\nISO generadas:\n'
find . -maxdepth 1 -name '*.iso' -type f -printf '%f (%s bytes)\n'
