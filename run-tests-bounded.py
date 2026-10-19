#!/usr/bin/env python3
"""Run legacy tests independently with time limits and honest result reporting."""
import argparse
import json
import pathlib
import subprocess
import sys
import time

root = pathlib.Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--timeout', type=int, default=12)
parser.add_argument('--output', default='test-results.json')
args = parser.parse_args()
results = []
for test in sorted((root / 'tests').glob('test_*.py')):
    started = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', test.name],
            cwd=root, capture_output=True, text=True, timeout=args.timeout)
        output = result.stdout + result.stderr
        # Older tests contain top-level assertions but no unittest.TestCase.
        # Execute those files directly instead of incorrectly reporting zero tests.
        if 'Ran 0 tests' in output:
            remaining = max(1, args.timeout - (time.monotonic() - started))
            direct = subprocess.run(
                [sys.executable, "-c", "import runpy,sys; ns=runpy.run_path(sys.argv[1]); [(v()) for k,v in ns.items() if k.startswith(\'test_\') and callable(v)]", str(test)], cwd=root,
                capture_output=True, text=True, timeout=remaining)
            output += '\nDirect script execution:\n' + direct.stdout + direct.stderr
            result = direct
        status = 'pass' if result.returncode == 0 else 'fail'
        detail = output[-4000:]
    except subprocess.TimeoutExpired:
        status = 'timeout'
        detail = f'Test exceeded {args.timeout} seconds'
    results.append({'file': test.name, 'status': status,
                    'seconds': round(time.monotonic() - started, 2), 'detail': detail})
    print(f'{test.name}: {status}', flush=True)
summary = {s: sum(r['status'] == s for r in results) for s in ('pass', 'fail', 'timeout')}
path = root / args.output
path.write_text(json.dumps({'summary': summary, 'results': results}, indent=2) + '\n')
print('Summary:', summary, 'Report:', path, flush=True)
sys.exit(1 if summary['fail'] or summary['timeout'] else 0)
