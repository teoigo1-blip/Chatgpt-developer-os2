#!/usr/bin/env python3
"""Save a real VM framebuffer via QMP before the bounded boot test ends."""
import json
from pathlib import Path
import socket
import sys
import time

address, destination, seconds = sys.argv[1], Path(sys.argv[2]).resolve(), int(sys.argv[3])
serial_input=Path(sys.argv[4]) if len(sys.argv)>4 else None
time.sleep(15)
destination.parent.mkdir(parents=True, exist_ok=True)
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
    connection.settimeout(8)
    connection.connect(address)
    stream=connection.makefile('rwb')
    json.loads(stream.readline())
    def command(name, arguments=None):
        request={'execute':name}
        if arguments is not None: request['arguments']=arguments
        stream.write((json.dumps(request)+'\n').encode()); stream.flush()
        while True:
            response=json.loads(stream.readline())
            if 'error' in response: raise RuntimeError(response['error'])
            if 'return' in response: return response['return']
    command('qmp_capabilities')
    command('screendump',{'filename':str(destination.with_name(destination.stem+'-menu.ppm'))})
    command('send-key',{'keys':[{'type':'qcode','data':'ret'}]})
    print('Selected the default Live system menu entry with Enter.')
    if serial_input is not None:
        time.sleep(100)
        with serial_input.open('w',buffering=1) as terminal:
            terminal.write('user\n'); time.sleep(5)
            terminal.write('live\n'); time.sleep(5)
            terminal.write(". /etc/profile.d/developer-toolchain.sh; developer-doctor --json; if developer-doctor --strict; then printf '\\nGUEST_TOOLCHECK_OK\\n'; else printf '\\nGUEST_TOOLCHECK_FAILED\\n'; fi; codex --version; jadx --version; sdkmanager --version; cat /usr/local/share/developer-os/toolchain-smoke.json; cat /usr/local/share/developer-os/enhancement-smoke.json; if developer-container-test; then echo GUEST_CONTAINER_OK; else echo GUEST_CONTAINER_FAILED; fi; DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority developer-dashboard >/tmp/developer-dashboard.log 2>&1 &\n")
        time.sleep(max(1,seconds-140))
    else:
        time.sleep(max(1, seconds - 30))
    status=command('query-status')
    command('screendump',{'filename':str(destination)})
    destination.with_suffix('.json').write_text(json.dumps({'vm_status':status,'framebuffer':destination.name,'observation':'Framebuffer only; no automated desktop functionality claim.'},indent=2)+'\n')
print('VM framebuffer saved:',destination)
