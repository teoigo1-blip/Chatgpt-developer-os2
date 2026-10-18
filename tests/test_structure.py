from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name in ('build.sh','README.md','config/package-lists/developer.list.chroot','config/includes.chroot/usr/local/bin/developer-doctor'):
    assert (root/name).is_file(), name
print('Estructura correcta')
