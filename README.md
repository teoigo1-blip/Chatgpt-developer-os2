# ChatGPT Developer OS v4.2

Proyecto fuente Debian Live USB. **No contiene una ISO compilada**.

Esta versión añade una comprobación de salida limpia antes de compilar en GitHub Actions, conserva evidencia de validación y explica cómo ejecutar la primera compilación. Lee `GITHUB_FIRST_BUILD.md`.

Inicio de sesión Codex mediante el flujo oficial de Codex CLI, no API key. No implica control remoto oficial del escritorio por ChatGPT.

# ChatGPT Developer OS v3.8

Fuente para Debian 13 Live USB. Ejecuta `./prebuild-gate.sh` para validación estática y de tests. Sigue `GITHUB_BUILD.md` para construir ISO en GitHub Actions.

**No es una ISO ya construida.** El inicio de sesión oficial de Codex requiere instalar Codex CLI y autenticar al usuario; no concede control visual oficial de ChatGPT sobre el escritorio.


## v3.9: GitHub runner disk space

The workflow now reclaims space on **ephemeral GitHub-hosted runners only**, before installing live-build. `ci-runner-space.sh` refuses to run on a personal machine. Upload the repository to GitHub and manually run **Actions → Build Live USB ISO → Run workflow**. If it fails, download the `build-diagnostics` artifact and inspect the log. A passing local test suite is not proof of a bootable ISO.


## v4.0 — Primera compilación en GitHub
Ejecuta `./ci-local-check.sh` para validar localmente. Sigue `FIRST_ISO_STEPS.md` para lanzar el workflow en tu repositorio. **No se ha generado ni validado una ISO física aquí.**

## v4.1 — pruebas con límite individual
Las pruebas heredadas ahora se ejecutan en procesos separados con límite de 12 segundos por archivo. `run-tests-bounded.py` genera `test-results.json` e identifica el test que falla o se bloquea. GitHub Actions conserva el informe aunque falle el build. Esto NO equivale a construir ni arrancar la ISO.
