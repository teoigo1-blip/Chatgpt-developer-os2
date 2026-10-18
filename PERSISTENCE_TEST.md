# Protocolo de validación Live USB v1.6

## Arranque

1. Generar ISO en Debian/Ubuntu x86-64 con `sudo ./build-and-validate.sh`.
2. Ejecutar `./validate-live.sh ./imagen.iso` y conservar el informe.
3. Ejecutar `./smoke-test-qemu.sh ./imagen.iso` y confirmar manualmente el escritorio XFCE; cerrar QEMU.
4. Ejecutar `./smoke-test-uefi.sh ./imagen.iso` y confirmar manualmente el escritorio XFCE; cerrar QEMU.
5. Repetir BIOS y UEFI en hardware real compatible, si está disponible.

## Persistencia en USB de pruebas

**Atención:** nunca preparar particiones sin identificar y confirmar el dispositivo de destino; hacer copia de seguridad. El proceso de grabación puede borrar datos.

1. Grabar la ISO en un USB dedicado mediante una herramienta confiable, identificando el dispositivo por modelo y capacidad.
2. Preparar una partición `ext4` con etiqueta `persistence` en espacio libre del USB (consultar `prepare-persistence.sh` y verificar su comportamiento antes de usarlo).
3. En la raíz de esa partición, crear `persistence.conf` con la línea `/ union`.
4. Arrancar con la opción de persistencia habilitada.
5. Crear `~/prueba-persistencia.txt` con contenido único y reiniciar completamente.
6. Verificar que el archivo y el contenido permanecen tras el reinicio.
7. Probar desconexión segura, Wi-Fi, audio, almacenamiento y arranque sin tocar discos internos.

Registrar **aprobado/no probado/fallido** para cada comprobación. No declarar el USB validado hasta completar pruebas reales.
