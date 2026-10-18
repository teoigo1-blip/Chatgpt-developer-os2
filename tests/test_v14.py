from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_hybrid_boot():
    s=(ROOT/'build.sh').read_text()
    assert '--binary-images iso-hybrid' in s
    assert "--bootloaders 'grub-efi syslinux'" in s
def test_persistence_label():
    assert 'persistence-label=persistence' in (ROOT/'build.sh').read_text()
def test_compat_packages():
    s=(ROOT/'config/package-lists/boot-compat.list.chroot').read_text()
    for p in ['grub-efi-amd64-bin','syslinux-common','firmware-iwlwifi','firmware-realtek','firmware-amd-graphics']:
        assert p in s
