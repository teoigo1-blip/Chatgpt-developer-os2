#!/usr/bin/env python3
"""Extract actionable diagnostics from a failed live-build log; no network/disk mutation."""
import argparse
import json
import re
from pathlib import Path

PATTERNS = [
 ("missing_package", re.compile(r"(?:Unable to locate package|Package .+ has no installation candidate|E: Unable to locate package)\s*([^\n]*)", re.I), "Check Debian trixie package names and configured archive areas."),
 ("dependency_conflict", re.compile(r"(?:unmet dependencies|held broken packages|Unable to correct problems)[^\n]*", re.I), "Review conflicting packages in config/package-lists."),
 ("network", re.compile(r"(?:Temporary failure resolving|Could not resolve|Failed to fetch|Connection timed out)[^\n]*", re.I), "Retry when Debian mirrors and DNS are reachable."),
 ("disk_space", re.compile(r"(?:No space left on device|not enough free space)[^\n]*", re.I), "Free disk space; build host needs at least 15 GiB available."),
 ("permission", re.compile(r"(?:Permission denied|Operation not permitted)[^\n]*", re.I), "Run the image build as root on a suitable Linux host."),
]

def diagnose(log):
 text=Path(log).read_text(encoding="utf-8", errors="replace")
 findings=[]
 for kind, pattern, advice in PATTERNS:
  match=pattern.search(text)
  if match:
   findings.append({"category":kind,"evidence":match.group(0)[:250],"advice":advice})
 return {"log":str(log),"findings":findings,"status":"issues_found" if findings else "unclassified"}

if __name__ == "__main__":
 p=argparse.ArgumentParser();p.add_argument("log");p.add_argument("--output")
 a=p.parse_args(); result=diagnose(a.log); rendered=json.dumps(result,ensure_ascii=False,indent=2)
 if a.output: Path(a.output).write_text(rendered+"\n",encoding="utf-8")
 print(rendered)
