# Personal toolchain build

This image includes Codex CLI 0.163.0, jadx 1.5.6, Ghidra 12.1.4, Gradle 8.14.3,
Java 21, Android SDK Platform 36 and Build Tools 36.0.0. Pinned ZIP downloads are
verified using published SHA-256 digests. npm verifies its package integrity.

REA (morluto/rea) 6.7.0 is installed with Node.js 24.22.0 LTS. Its local MCP server
and matching instructions are registered in the Live user's Codex configuration.
Ghidra is the default native provider. The pinned jadx-headless-mcp 0.7.1 JAR
provides REA Android analysis. Chromium provides its Chrome-family browser.
Tests exercise the MCP server, Codex registration, JavaScript inspection, an
actual native main function through Ghidra, and analysis of the signed test APK.
No external account or paid model request is needed for these local checks.

Android SDK terms were explicitly accepted by the owner on 2026-10-18 for this
personal environment. Keep automatic public release publishing disabled for this
personal SDK image. This is not a distribution permission grant for other users.

The live-build hook installs tools, prepares PATH/JAVA_HOME/ANDROID_HOME for the
terminal and desktop, adds launchers, and runs developer-doctor --strict plus
developer-smoke-test. The latter builds and signs an Android APK, decompiles it,
compiles Linux and Windows programs, and analyzes the Linux executable in Ghidra.
All work uses temporary directories and a disposable test signing key.

The installed build-time report is /usr/local/share/developer-os/toolchain-smoke.json.
QEMU also signs in to the disposable Live user and verifies tools inside the ISO.
No personal credentials or APK signing keys are baked into the image.

Codex is preinstalled with the official ChatGPT login method and normal approval
and sandbox settings. Start developer-codex login and complete your own browser
sign-in. No paid requests or account access are exercised in build tests.

Sources:
- https://learn.chatgpt.com/docs/codex/cli
- https://learn.chatgpt.com/docs/auth
- https://github.com/skylot/jadx/releases/tag/v1.5.6
- https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.1.4_build
- https://developer.android.com/studio#command-tools
- https://developer.android.com/tools/sdkmanager
- https://services.gradle.org/distributions/gradle-8.14.3-bin.zip.sha256
- https://github.com/morluto/rea
- https://nodejs.org/en/blog/release/v24.22.0

## Productivity and recovery edition

Adds the official VS Code package with Codex and Spanish language extensions,
uv/Ruff/pytest, Playwright with its bundled headless browser and a configured MCP,
ShellCheck, scrcpy 5.0.1, Podman rootless prerequisites, Restic, ccache, jq and SQLite.
The official OpenAI documentation MCP is configured without an API key.
VS Code is fetched from Microsoft's official HTTPS update metadata and its SHA256
is checked; its exact version and hash are recorded in productivity-lock.json.
Python and Playwright MCP versions are recorded alongside the build reports.

The Spanish dashboard launches tools in visible terminals. Offline examples cover
Python, web, Android and native Linux/Windows builds. The local guide explains
account login, backups, cache, containers and persistence. ccache is capped at
1 GiB per user. Restic recovery always targets a new directory; credentials are
not included in the default backup inputs. Users choose and protect the backup
password themselves.

USB encryption requires a user-selected, unmounted leaf partition on USB/removable
media, explicit confirmation of its path and interactive cryptsetup passphrases.
No physical disk is selected automatically. CI tests use an exclusively-created
new image file with a public disposable test-only key, never a user partition.
The image enables persistence-encryption=none,luks. Physical USB/hardware and
personal account login must still be checked by the owner.

Sources: code.visualstudio.com/docs/setup/linux; playwright.dev/python;
github.com/microsoft/playwright-mcp; docs.astral.sh; restic.net; ccache.dev;
docs.podman.io; github.com/Genymobile/scrcpy; Debian Live manual.
