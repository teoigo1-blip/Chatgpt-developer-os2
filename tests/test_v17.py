from pathlib import Path
import configparser
import subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_welcome_shell_syntax():
    p=ROOT/'config/includes.chroot/usr/local/bin/developer-welcome'
    assert subprocess.run(['bash','-n',str(p)]).returncode==0
    assert 'codex' in p.read_text().lower()
def test_autostart_not_duplicate():
    p=ROOT/'config/includes.chroot/etc/xdg/autostart'
    assert (p/'developer-welcome.desktop').exists()
    active=[]
    for desktop in p.glob('developer-*.desktop'):
        entry=configparser.ConfigParser(interpolation=None)
        entry.read(desktop)
        values=entry['Desktop Entry']
        if not values.getboolean('Hidden',fallback=False):active.append(values['Exec'])
    assert active==['/usr/local/bin/developer-dashboard']
def test_audit_syntax():
    assert subprocess.run(['bash','-n',str(ROOT/'audit-packages.sh')]).returncode==0
def test_no_usb_writes_in_new_scripts():
    for p in [ROOT/'audit-packages.sh',ROOT/'config/includes.chroot/usr/local/bin/developer-welcome']:
        s=p.read_text()
        assert 'mkfs.' not in s and 'dd if=' not in s
