import json
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'config/includes.chroot/usr/local/bin/developer-usb-persistence'

class PersistenceGuards(unittest.TestCase):
    def setUp(self):self.ns=runpy.run_path(str(SCRIPT))
    def test_internal_disks_and_mounted_partitions_are_excluded(self):
        disks={'blockdevices':[
          {'path':'/dev/sda','tran':'sata','rm':False,'children':[{'path':'/dev/sda2','type':'part','mountpoints':[]}]},
          {'path':'/dev/sdb','tran':'usb','rm':True,'children':[
            {'path':'/dev/sdb1','type':'part','mountpoints':['/run/live/medium']},
            {'path':'/dev/sdb2','type':'part','mountpoints':[],'size':123},
            {'path':'/dev/sdb3','type':'part','mountpoints':[],'children':[{'type':'crypt'}]}]}]}
        with patch('subprocess.check_output',return_value=json.dumps(disks)):
            self.assertEqual([p['path'] for p in self.ns['inventory']()],['/dev/sdb2'])
    def test_zero_cancels_before_any_format(self):
        safe=[{'path':'/dev/sdb2','size':1024**3,'fstype':None}]
        self.ns['main'].__globals__['inventory']=lambda:safe
        with patch.object(sys,'argv',['developer-usb-persistence']),patch('os.geteuid',return_value=0,create=True),patch('builtins.input',return_value='0'),patch('subprocess.run') as run:
            with self.assertRaises(SystemExit):self.ns['main']()
            run.assert_not_called()
    def test_existing_test_image_cannot_be_overwritten(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'existing.img';f.write_bytes(b'keep')
            with patch.object(sys,'argv',['developer-usb-persistence','--test-image',str(f)]),patch('os.geteuid',return_value=0,create=True),patch('subprocess.run') as run:
                with self.assertRaises(FileExistsError):self.ns['main']()
                self.assertEqual(f.read_bytes(),b'keep');run.assert_not_called()

if __name__=='__main__':unittest.main()
