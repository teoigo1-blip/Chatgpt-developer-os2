import ast, pathlib, subprocess, sys, tempfile, os
root=pathlib.Path(__file__).resolve().parents[1]
base=root/'config/includes.chroot/usr/local/bin'
for name in ('developer-agent','developer-tools'):
    ast.parse((base/name).read_text())
    result=subprocess.run([sys.executable,str(base/name),'--help'],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
with tempfile.TemporaryDirectory() as d:
    env={**os.environ,'HOME':d}
    agent=str(base/'developer-agent')
    for cmd in ('stop','status','resume'):
        r=subprocess.run([sys.executable,agent,cmd],env=env,capture_output=True,text=True)
        assert r.returncode==0,r.stderr
print('Pruebas v0.2: OK')
