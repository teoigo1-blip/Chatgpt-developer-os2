# Construcción de la ISO (Debian 13, x86_64)

Este ZIP contiene el **código fuente**, no una ISO construida. Necesitas un equipo Linux x86_64, conexión a Internet, permisos de administrador y espacio libre suficiente (recomendado: 20 GiB o más).

```bash
sudo apt update
sudo apt install live-build debootstrap xorriso squashfs-tools
./build-host-check.sh
./audit-packages.sh  # opcional; requiere índices APT y puede detectar paquetes obsoletos
sudo ./build-and-validate.sh
```

Si `audit-packages.sh` detecta paquetes sin candidato, revisar los repositorios de Debian 13 y las listas en `config/package-lists/` **antes** de compilar. La disponibilidad en el anfitrión no garantiza la del chroot.

Al finalizar correctamente, `build-and-validate.sh` verifica la estructura de la ISO y calcula SHA-256. Después ejecutar las pruebas de BIOS/UEFI mediante QEMU y el protocolo `PERSISTENCE_TEST.md`. **No escribir en USB ni formatear discos automáticamente.**

Codex CLI se instala por separado y requiere inicio de sesión oficial con ChatGPT. No se incluyen tokens ni claves.
