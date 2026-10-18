# Construcción real de la ISO en GitHub Actions (v2.4)

1. Sube **el contenido** de este proyecto a un repositorio de GitHub (incluyendo `.github/workflows/build-live-iso.yml`).
2. Abre **Actions → Build Live USB ISO → Run workflow**.
3. Cuando termine correctamente, descarga el artefacto `chatgpt-developer-os-iso`: contiene `release.iso`, `iso.sha256` e `iso-artifact.json`.
4. Comprueba el SHA-256 antes de escribir el USB. **No escribas el USB sin seleccionar y verificar expresamente el dispositivo correcto.**

La ejecución de Actions compila y hace validaciones estáticas. **No acredita** un arranque BIOS/UEFI ni persistencia funcional. Si falla, revisa el registro de la tarea; Debian 13 y el host Ubuntu pueden requerir ajustes de paquetes y bootloaders. La ISO no se ha generado aquí.

### v2.7
El flujo verifica la integridad de los manifiestos antes de compilar y carga diagnósticos si falla. La verificación de paquetes del host Ubuntu es solo orientativa. Si falla la ISO, revisar el registro de GitHub Actions; no se debe interpretar como ISO validada.

### v2.9 — Publicación opcional

En **Actions → Build Live USB ISO → Run workflow**, deja `publish_release=false` para recibir el ZIP del artefacto durante 30 días. Para crear una versión descargable en **Releases**, marca `publish_release=true` e introduce un tag nuevo como `v2.9-iso1`. Solo se publica si la construcción, SHA-256 y ambas comprobaciones QEMU finalizan correctamente. No reemplaza versiones existentes y se marca como *pre-release*. El repositorio debe permitir escribir Releases con `GITHUB_TOKEN`.

**Importante:** QEMU solo comprueba evidencia de inicio del núcleo en consola serie; no certifica interfaz gráfica, persistencia USB ni compatibilidad con hardware real.

## Ejecución desde Android (sin PC)
1. Crea un repositorio GitHub y sube el **contenido** del ZIP, incluyendo `.github/workflows/build-live-iso.yml` (la carpeta `.github` puede estar oculta en gestores de archivos).
2. En GitHub abre **Actions > Build Live USB ISO > Run workflow**. Deja `publish_release` desactivado.
3. Revisa el resultado del trabajo `iso`. Si pasa, descarga el artifact `chatgpt-developer-os-iso` desde la ejecución.
4. Si falla, descarga `build-diagnostics` y comparte `build.log` para corregir errores reales.
5. El artifact de Actions no es una ISO verificada en hardware físico; no grabes el USB sin comprobar el archivo SHA-256.

La compilación necesita conexión a Internet, espacio suficiente y puede superar los límites del runner. No se ha ejecutado desde este entorno.


### v3.4 — Validación y ejecución
Se eliminó la comprobación bloqueante de candidatos APT en Ubuntu: el sistema destino es Debian 13 (trixie), por lo que el APT del runner Ubuntu no determina disponibilidad en Debian. Se añadió `validate-workflow.py` como comprobación estructural local.

**Desde Android:** crea un repositorio, sube los archivos descomprimidos (incluida `.github`), abre Actions, habilita los workflows si GitHub lo solicita y ejecuta **Build Live USB ISO → Run workflow**. Descarga el artefacto solo si la ejecución acaba correctamente. Para publicar un release, activa expresamente la opción correspondiente.

La ejecución remota NO se ha iniciado desde esta conversación. Si falla, comparte el log de GitHub Actions para corregir el error concreto.

### v3.8 — Ejecutar de verdad la compilación
La compilación solo se ejecuta cuando subes este proyecto a un repositorio GitHub y pulsas **Actions → Build Live USB ISO → Run workflow**. Desde Android, lo más fiable es importar los archivos con una herramienta Git compatible o subirlos desde el navegador en modo escritorio; **comprueba que `.github/workflows/build-live-iso.yml` existe en el repositorio**. Un ZIP adjunto a un issue no sirve para activar Actions.

El workflow ejecuta `prebuild-gate.sh` antes de descargar y construir la imagen. Si falla, abre el trabajo y comparte el error exacto. No afirmamos haber construido una ISO sin un run de Actions completado.
