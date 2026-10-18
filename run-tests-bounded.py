#!/usr/bin/env python3
"""Run legacy tests independently so a hung test cannot stall the whole build."""
import argparse, json, pathlib, subprocess, sys, time, os, tempfile
root=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser(); p.add_argument('--timeout',type=int,default=12); p.add_argument('--output',default='test-results.json'); args=p.parse_args()
results=[]
for test in sorted((root/'tests').glob('test_*.py')):
    started=time.monotonic()
    try:
        with tempfile.TemporaryDirectory(prefix='developer-os-test-cache-') as cache:
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1', 'PYTHONPYCACHEPREFIX':cache}
            r=subprocess.run([sys.executable,str(root/'run-single-test.py'),str(test)],cwd=root,env=env,capture_output=True,text=True,timeout=args.timeout)
        status='pass' if r.returncode==0 else 'fail'; detail=(r.stdout+r.stderr)[-2500:]
    except subprocess.TimeoutExpired as e:
        status='timeout'; detail='Test exceeded %s seconds'%args.timeout
    results.append({'file':test.name,'status':status,'seconds':round(time.monotonic()-started,2),'detail':detail})
    print(f'{test.name}: {status}',flush=True)
summary={s:sum(r['status']==s for r in results) for s in ('pass','fail','timeout')}
path=root/args.output; path.write_text(json.dumps({'summary':summary,'results':results},indent=2)+'\n')
print('Summary:',summary,'Report:',path,flush=True)
sys.exit(1 if summary['fail'] or summary['timeout'] else 0)
