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
