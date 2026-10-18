import ast,json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1]; b=root/'config/includes.chroot/usr/local/bin'
for name in ('developer-plan','developer-panel'):ast.parse((b/name).read_text())
plan=b/'developer-plan'
r=subprocess.run([sys.executable,str(plan),str(root/'examples/plan-demo.json')],capture_output=True,text=True)
assert r.returncode==0,r.stderr
assert 'preview' in r.stdout
with tempfile.TemporaryDirectory() as tmp:
    bad=pathlib.Path(tmp)/'bad.json';bad.write_text(json.dumps({'steps':[{'action':'shell','command':'rm -rf /'}]}))
    r=subprocess.run([sys.executable,str(plan),str(bad)],capture_output=True,text=True)
    assert r.returncode!=0
print('Pruebas v0.4: OK')
