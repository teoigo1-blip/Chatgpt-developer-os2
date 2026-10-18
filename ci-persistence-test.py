#!/usr/bin/env python3
"""Boot twice with a NEW disposable encrypted disk; prove a user's file survives."""
import argparse,json,os,re,selectors,shutil,subprocess,tempfile,time
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('iso',type=Path);p.add_argument('--output',type=Path,default=Path('dist/persistence-evidence'));a=p.parse_args()
    iso=a.iso.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    root=Path(__file__).resolve().parent;key='developer-os-disposable-test-only';token='DEVOS_REBOOT_PERSISTENCE_2026'
    with tempfile.TemporaryDirectory(prefix='devos-persistence-ci-') as tmp:
        tmp=Path(tmp);image=tmp/'disposable.img'
        helper=root/'config/includes.chroot/usr/local/bin/developer-usb-persistence'
        subprocess.run(['sudo','python3',str(helper),'--test-image',str(image)],check=True)
        subprocess.run(['sudo','chown',str(os.getuid())+':'+str(os.getgid()),str(image)],check=True)
        for name in ('vmlinuz','initrd.img'):
            subprocess.run(['xorriso','-osirrox','on','-indev',str(iso),'-extract','/live/'+name,str(tmp/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for phase in ('write','read'):
            cmd=['qemu-system-x86_64','-m','4096','-smp','2','-display','none','-monitor','none','-serial','stdio','-nic','none','-no-reboot','-cdrom',str(iso),'-kernel',str(tmp/'vmlinuz'),'-initrd',str(tmp/'initrd.img'),'-append','boot=live components persistence persistence-encryption=luks persistence-label=persistence locales=es_ES.UTF-8 console=ttyS0,115200n8','-drive','file='+str(image)+',format=raw,if=virtio']
            process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            selector=selectors.DefaultSelector();selector.register(process.stdout,selectors.EVENT_READ)
            started=time.monotonic();transcript='';unlocked=False;user=False;password=False;sent=False;password_time=0
            def send(text):process.stdin.write((text+'\n').encode());process.stdin.flush()
            try:
                while time.monotonic()-started<600 and process.poll() is None:
                    events=selector.select(1)
                    if events:
                        chunk=os.read(process.stdout.fileno(),65536).decode(errors='replace');transcript+=chunk
                        tail=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',transcript[-1800:]).replace('\r','')
                        if not unlocked and re.search(r'(?i)(passphrase|unlock.*disk|contraseña.*disco|frase.*contraseña)',tail):send(key);unlocked=True
                        if not user and re.search(r'(?im)^.*login:\s*$',tail):send('user');user=True
                        elif user and not password and re.search(r'(?im)^(password|contraseña|contrasena):\s*$',tail):send('live');password=True;password_time=time.monotonic()
                    if password and not sent and time.monotonic()-password_time>8:
                        if phase=='write':body="mkdir -p ~/Projects; printf '%s\\n' '"+token+"' > ~/Projects/.persistence-proof; sync"
                        else:body="test \"$(cat ~/Projects/.persistence-proof)\" = '"+token+"'"
                        marker='PERSIST_'+phase.upper()+'_OK'
                        send("if grep -q /dev/mapper /proc/mounts && { "+body+"; }; then printf '\\n"+marker+"\\n'; else echo PERSIST_FAILED; fi; sync; sudo poweroff")
                        sent=True
                if process.poll() is None:process.terminate()
                try:remaining=process.communicate(timeout=15)[0];transcript+=remaining.decode(errors='replace')
                except subprocess.TimeoutExpired:process.kill();process.communicate()
            finally:
                if process.poll() is None:process.kill();process.wait()
                selector.close();(out/(phase+'.log')).write_text(transcript)
            marker='PERSIST_'+phase.upper()+'_OK'
            if not re.search(r'(?m)^'+marker+r'\r?$',transcript):
                print(transcript[-12000:]);raise SystemExit('Encrypted persistence boot failed: '+phase)
            print(marker,flush=True)
    report={'encrypted_persistence_reboot_passed':True,'write_then_read':True,'physical_usb_tested':False,'personal_password_tested':False,'test_key':'public disposable key, not included in ISO configuration'}
    (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
