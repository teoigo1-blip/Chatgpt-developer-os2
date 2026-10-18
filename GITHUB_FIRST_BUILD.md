# Primera compilación real (desde Android o PC)

1. Crea un repositorio **privado** nuevo en GitHub.
2. Sube **el contenido de esta carpeta**, incluida `.github/workflows/build-live-iso.yml` (no subas solo el ZIP).
   - En Android, la web de GitHub puede ocultar carpetas que empiezan por punto; una opción más fiable es usar Termux con `git` y `unzip`, o GitHub Desktop en un PC.
3. En GitHub abre **Actions** → **Build Live USB ISO** → **Run workflow**. Deja `publish_release=false`.
4. Si el trabajo acaba en verde, descarga el artefacto `chatgpt-developer-os-iso` desde el resultado de Actions. Comprueba `sha256sum -c iso.sha256` en un entorno Linux.
5. Si falla, descarga `build-diagnostics`, `boot-evidence` o `source-validation` y comparte el log para corregir **el error real**.

No se puede ejecutar GitHub Actions sin un repositorio y la autorización de su propietario. La prueba QEMU no equivale a una prueba en hardware real; persistencia y escritorio siguen pendientes de comprobar.
