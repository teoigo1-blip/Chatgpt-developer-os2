#!/usr/bin/env python3
"""Save a real VM framebuffer via QMP before the bounded boot test ends."""
import json
from pathlib import Path
import socket
import sys
import time

address, destination, seconds = sys.argv[1], Path(sys.argv[2]).resolve(), int(sys.argv[3])
time.sleep(max(1, seconds - 15))
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
    status=command('query-status')
    command('screendump',{'filename':str(destination)})
    destination.with_suffix('.json').write_text(json.dumps({'vm_status':status,'framebuffer':destination.name,'observation':'Framebuffer only; no automated desktop functionality claim.'},indent=2)+'\n')
print('VM framebuffer saved:',destination)
