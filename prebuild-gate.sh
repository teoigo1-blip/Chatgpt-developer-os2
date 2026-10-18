#!/usr/bin/env bash
set -Eeuo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
echo 'Checking source integrity, configuration and test suite...'
python3 ./validate-workflow.py
python3 ./check-build-inputs.py
python3 ./check-target-packages.py
./verify-boot-config.sh
bash -n build.sh ci-build-iso.sh ci-qemu-boot.sh
# Avoid indefinite hangs during local prebuild checks.
# Legacy check: timeout 180s python3 -m unittest discover -s tests -p 'test_*.py'
python3 ./run-tests-bounded.py --timeout 12 --output test-results.json
echo 'Prebuild checks passed; this does NOT mean the ISO was built.'
