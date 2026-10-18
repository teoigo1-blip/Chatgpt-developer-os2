# Primera ISO: pasos verificables

1. Descomprime el ZIP y sube **el contenido de la carpeta** a la raíz de un repositorio GitHub (incluye `.github/workflows/build-live-iso.yml`).
2. En GitHub abre **Actions → Build Live USB ISO → Run workflow**. Deja `publish_release` en `false`.
3. Espera a que finalice. Si falla, descarga el artefacto `build-diagnostics` y consulta `dist/build.log`; no des por construida la ISO.
4. Si termina correctamente, descarga el artefacto `chatgpt-developer-os-iso` y verifica `sha256sum -c iso.sha256` sobre `release.iso`.
5. Las pruebas QEMU comprueban indicadores de arranque, pero **no** sustituyen una prueba física de Wi-Fi, vídeo, teclado, almacenamiento y persistencia.
6. Para probar en USB utiliza una herramienta gráfica fiable, selecciona cuidadosamente el dispositivo y haz copia de seguridad: grabar la ISO borra el contenido de la unidad seleccionada.

La autenticación de Codex se hace mediante `codex login` con tu cuenta ChatGPT; no se almacenan contraseñas ni tokens en el repositorio.
