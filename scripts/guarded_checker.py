"""Run one packaged checker with a Python-level filesystem boundary."""
from pathlib import Path
import runpy,sys,os
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve();script=(ROOT/sys.argv[2]).resolve()
if not script.is_relative_to(ROOT):raise ValueError('Checker escapes package')
allowed=[ROOT,OUT,Path(sys.prefix).resolve(),Path(sys.base_prefix).resolve(),Path(sys.exec_prefix).resolve()]
def audit(event,args):
 if event not in ('open','os.listdir','os.scandir'):return
 value=args[0]
 if value is None or isinstance(value,int):return
 p=Path(os.fsdecode(value)).resolve()
 if not any(p.is_relative_to(base) for base in allowed):
  raise PermissionError('Filesystem access outside package, receipts and interpreter: '+str(p))
sys.addaudithook(audit)
sys.argv=[str(script),*sys.argv[3:]]
sys.path.insert(0,str(script.parent))
runpy.run_path(str(script),run_name='__main__')

