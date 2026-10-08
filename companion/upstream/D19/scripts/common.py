"""Receipt utilities. Mathematical checks use explicit exceptions, also with -O."""
from pathlib import Path
import argparse,json,time,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def main(run):
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=a.output.resolve()
    need(not p.exists(),'receipt must be new');need(ROOT not in p.parents,'receipt outside immutable package');need(p.parent.exists(),'output directory exists')
    t=time.monotonic();out=run();out['seconds']=time.monotonic()-t;dump(p,out);print(json.dumps(out,ensure_ascii=False),flush=True)
