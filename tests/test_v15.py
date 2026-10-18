from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
def test_audit_script_parses(): ast.parse((ROOT/'iso-inspect.py').read_text())
def test_build_validation_uses_pipefail(): assert 'pipefail' in (ROOT/'build-and-validate.sh').read_text()
def test_build_validation_checks_dependencies():
    assert './build-host-check.sh' in (ROOT/'build-and-validate.sh').read_text()
    host_check=(ROOT/'build-host-check.sh').read_text()
    assert 'debootstrap' in host_check
    assert 'exit 3' in host_check
def test_iso_audit_does_not_claim_boot(): assert "'boot_tested':False" in (ROOT/'iso-inspect.py').read_text()
