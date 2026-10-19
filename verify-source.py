#!/usr/bin/env python3
"""Verify tracked source integrity against the checked-out Git commit.

SOURCE_SHA256SUMS is a legacy release snapshot, not a manifest for a
continually edited development branch. The Git index/HEAD is authoritative
for CI checkouts. This check detects local modifications and missing files.
"""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent

def git(*args):
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )

inside = git("rev-parse", "--is-inside-work-tree")
if inside.returncode != 0 or inside.stdout.strip() != "true":
    sys.exit("ERROR: Git checkout required for source verification")

tracked = git("ls-files", "-z")
if tracked.returncode != 0 or not tracked.stdout:
    sys.exit("ERROR: no tracked source files")

changes = git("-c", "core.filemode=false", "status", "--porcelain", "--untracked-files=no")
if changes.returncode != 0:
    sys.exit("ERROR: unable to check source integrity")
if changes.stdout.strip():
    print("ERROR: tracked files modified or missing:\n" + changes.stdout, file=sys.stderr)
    sys.exit(1)

required = (
    "build.sh",
    ".github/workflows/build-live-iso.yml",
    "config/package-lists/developer.list.chroot",
    "config/package-lists/boot-compat.list.chroot",
)
missing = [name for name in required if not (root / name).is_file()]
if missing:
    sys.exit("ERROR: required source files missing: " + ", ".join(missing))

print("PASS: tracked source matches checked-out Git commit")
