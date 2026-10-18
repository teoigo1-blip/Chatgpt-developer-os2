# Dependencias de arranque del host

Los paquetes `grub-pc-bin`, `grub-efi-amd64-bin`, `isolinux`, `syslinux-common` y `mtools` pertenecen al **host que construye la ISO**, no a la lista de aplicaciones del sistema Live. `memtest86+`, `shim-signed` y `grub-efi-amd64-signed` no se incluyen por defecto: Secure Boot no está verificado. La ISO requiere pruebas BIOS y UEFI sin Secure Boot antes de distribuirse.

Paquetes recomendados en Ubuntu CI: `live-build debootstrap xorriso squashfs-tools syslinux-common isolinux grub-pc-bin grub-efi-amd64-bin mtools dosfstools qemu-system-x86 ovmf file`.
