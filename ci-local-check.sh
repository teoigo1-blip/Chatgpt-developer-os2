#!/usr/bin/env bash
# Fast, non-root validation before uploading to GitHub Actions.
set -Eeuo pipefail
cd "$(dirname "$(realpath "$0")")"
for script in *.sh; do bash -n "$script"; done
python3 -m compileall -q -f -x '/\.git/' .
python3 check-build-inputs.py
python3 validate-workflow.py
python3 -m unittest discover -s tests -p 'test_*.py' -q
printf '\nLocal static checks passed. This does NOT verify an ISO boot.\n'
