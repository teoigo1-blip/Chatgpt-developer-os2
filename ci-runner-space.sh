#!/usr/bin/env bash
# GitHub-hosted Ubuntu runner only. Never run cleanup on a personal computer.
set -Eeuo pipefail
if [[ "${GITHUB_ACTIONS:-}" != "true" || "${RUNNER_ENVIRONMENT:-}" != "github-hosted" ]]; then
  echo 'Refusing runner cleanup outside a GitHub-hosted Actions runner' >&2
  exit 2
fi
printf 'Free space before cleanup:\n'; df -h .
# Remove known large, unrelated preinstalled SDKs from ephemeral runner only.
for path in /usr/local/lib/android /usr/share/dotnet /opt/hostedtoolcache; do
  if [[ -d "$path" ]]; then sudo rm -rf -- "$path"; fi
done
sudo apt-get clean
printf 'Free space after cleanup:\n'; df -h .
