#!/usr/bin/env python3
"""Auditoría de un artefacto ISO; no demuestra arranque real."""
import argparse, hashlib, json, pathlib, subprocess, sys
p=argparse.ArgumentParser(); p.add_argument('iso'); p.add_argument('--report'); args=p.parse_args()
iso=pathlib.Path(args.iso)
if not iso.is_file(): p.error('No existe el archivo ISO')
size=iso.stat().st_size
h=hashlib.sha256()
with iso.open('rb') as f:
    for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
report={'file':str(iso),'bytes':size,'sha256':h.hexdigest(),'size_plausible':size>=100*1024*1024,'boot_tested':False}
try:
    result=subprocess.run(['xorriso','-indev',str(iso),'-report_el_torito','plain'],capture_output=True,text=True,timeout=60)
    report['el_torito_exit_code']=result.returncode
    report['el_torito_report']=(result.stdout+result.stderr)[-8000:]
except (FileNotFoundError,subprocess.TimeoutExpired): report['el_torito_report']='xorriso no disponible o timeout'
print(json.dumps(report,ensure_ascii=False,indent=2))
if args.report: pathlib.Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['size_plausible'] else 2)
