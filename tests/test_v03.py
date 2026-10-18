import ast, os, pathlib, subprocess, sys, tempfile
root=pathlib.Path(__file__).resolve().parents[1]
bin=root/'config/includes.chroot/usr/local/bin'
for name in ('developer-agent','developer-codex'):
    ast.parse((bin/name).read_text())
    r=subprocess.run([sys.executable,str(bin/name),'--help'],capture_output=True,text=True)
    assert r.returncode==0,r.stderr
with tempfile.TemporaryDirectory() as home:
    env={**os.environ,'HOME':home}
    agent=str(bin/'developer-agent')
    for action in ('stop','status','resume'):
        r=subprocess.run([sys.executable,agent,action],env=env,capture_output=True,text=True)
        assert r.returncode==0,r.stderr
    r=subprocess.run([sys.executable,agent,'move','10','20'],env={**env,'DISPLAY':''},capture_output=True,text=True)
    assert r.returncode!=0
    r=subprocess.run([sys.executable,str(bin/'developer-codex'),'--help'],env=env,capture_output=True,text=True)
    assert r.returncode==0
print('Pruebas v0.3: OK')
