from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]

def test_scripts_syntax():
    for script in ('validate-live.sh','build-and-validate.sh','smoke-test-qemu.sh','smoke-test-uefi.sh'):
        subprocess.run(['bash','-n',str(ROOT/script)],check=True)

def test_missing_iso_fails():
    p=subprocess.run(['bash',str(ROOT/'validate-live.sh'),'/nonexistent/developer-os.iso'],capture_output=True,text=True)
    assert p.returncode != 0

def test_persistence_protocol():
    text=(ROOT/'PERSISTENCE_TEST.md').read_text()
    assert 'persistence.conf' in text and '/ union' in text and 'reinicio' in text
