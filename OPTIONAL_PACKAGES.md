# Paquetes opcionales y compatibilidad Debian 13

Se han retirado del listado obligatorio los paquetes con disponibilidad dependiente del repositorio, la arquitectura o el modo de arranque: `grub-efi-amd64-signed`, `shim-signed`, `memtest86+`, `firmware-linux`, `firmware-linux-free`, `firmware-linux-nonfree`, `p7zip-full`. Se mantienen paquetes concretos de firmware para adaptadores comunes.

`openjdk-17-jdk` se sustituye por `default-jdk` para ajustarse al JDK predeterminado de Debian 13. Las compilaciones Android pueden requerir una versión específica de JDK y Android SDK instalada aparte.

**No se garantiza que todos los paquetes existan** en el espejo configurado por live-build: ejecutar `sudo apt update` y `./audit-packages.sh` en el anfitrión y validar después con una construcción real. Las imágenes de arranque firmadas para Secure Boot requieren tratamiento separado; no se afirma compatibilidad Secure Boot.
