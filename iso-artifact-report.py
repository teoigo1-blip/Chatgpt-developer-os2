#!/usr/bin/env python3
"""Read-only ISO artifact report; not a boot test."""
import argparse, hashlib, json, pathlib, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('iso',type=pathlib.Path)
p.add_argument('--output',type=pathlib.Path)
a=p.parse_args()
if not a.iso.is_file(): p.error('No existe la ISO')
if a.iso.stat().st_size < 100_000_000: p.error('ISO demasiado pequeña')
h=hashlib.sha256()
with a.iso.open('rb') as stream:
 for chunk in iter(lambda: stream.read(1024*1024),b''): h.update(chunk)
report={'iso':str(a.iso.resolve()),'bytes':a.iso.stat().st_size,'sha256':h.hexdigest(),'boot_tested':False}
if subprocess.run(['which','xorriso'],capture_output=True).returncode==0:
 r=subprocess.run(['xorriso','-indev',str(a.iso),'-report_el_torito','plain'],capture_output=True,text=True)
 report['el_torito_report']=r.stdout[-12000:]
 report['el_torito_check_exit_code']=r.returncode
else: report['el_torito_report']='xorriso no instalado'
output=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
if a.output:
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(output)
else: print(output,end='')
