#!/usr/bin/env bash
# Build an ISO in a fresh temporary working directory, leaving source intact.
set -Eeuo pipefail
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
output_dir=${1:-"$source_dir/dist"}
mkdir -p -- "$output_dir"
output_dir=$(realpath "$output_dir")
command -v lb >/dev/null || { echo "ERROR: install live-build" >&2; exit 1; }
command -v xorriso >/dev/null || { echo "ERROR: install xorriso" >&2; exit 1; }
if (( EUID != 0 )); then echo "ERROR: run as root (sudo)" >&2; exit 1; fi
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cp -a -- "$source_dir/config" "$source_dir/build.sh" "$work/"
cd "$work"
if ! ./build.sh 2>&1 | tee "$output_dir/build.log"; then
  echo "ERROR: ISO build failed. Last 100 log lines:" >&2
  tail -n 100 "$output_dir/build.log" >&2 || true
  echo "Full log: $output_dir/build.log" >&2
  exit 1
fi
mapfile -d '' images < <(find "$work" -maxdepth 1 -type f -name '*.iso' -print0)
if (( ${#images[@]} != 1 )); then echo "ERROR: expected exactly one ISO, got ${#images[@]}" >&2; exit 1; fi
image=${images[0]}
if (( $(stat -c %s "$image") < 100000000 )); then echo "ERROR: suspiciously small ISO" >&2; exit 1; fi
cp -- "$image" "$output_dir/chatgpt-developer-os-amd64.iso"
(cd "$output_dir" && sha256sum chatgpt-developer-os-amd64.iso > SHA256SUMS && sha256sum -c SHA256SUMS)
file "$output_dir/chatgpt-developer-os-amd64.iso"
# Check that xorriso can read the produced ISO filesystem before publishing.
xorriso -indev "$output_dir/chatgpt-developer-os-amd64.iso" -find / -maxdepth 1 -type d >/dev/null
echo "ISO created at $output_dir/chatgpt-developer-os-amd64.iso"
