"""Reconstruct the entire mu42 domain, the small-degree rows, and exact charges."""
from pathlib import Path
from functools import lru_cache
from collections import Counter
from fractions import Fraction
import hashlib,json,time,argparse
import local43 as p,audit43 as a
import charge42 as c
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
 if not ok:raise ValueError(msg)
@lru_cache(None)
def nearby(pt):return tuple(1+sum(pt[j] for j in p.INC[i])+sum(pt[6:])-pt[6+i] for i in range(4))
def ds(r):return tuple(k+s for k,s in zip(nearby(r[:10]),r[10:]))
def summarize(rows):
 profiles=Counter();ns=Counter()
 for r in rows:
  d=ds(r);need(tuple(sorted(d))==d,'anchor degree ordering');profiles[d]+=1;ns[1+sum(r)]+=1
 rec={d:sum((Fraction(1,v) for v in d),Fraction()) for d in profiles}
 return {'rows':len(rows),'profiles':len(profiles),'min_degree':min(d[0] for d in profiles),'min_pair':min(d[0]+d[1] for d in profiles),'min_sum':min(map(sum,profiles)),'max_reciprocal':str(max(rec.values())),'min_reciprocal':str(min(rec.values())),'neighbourhoods':dict(sorted(ns.items())),'sha256':hashlib.sha256(b''.join(rows)).hexdigest()}
def run():
 start=time.monotonic();rp=sorted(bytes(r) for r in p.enumerate_rows(mu=42,r10=0,r9=0,cap_degree=20));ra=a.enumerate_rows(mu=42,r10=0,r9=0,cap=20)
 need(rp==ra,'full raw row lists differ');raw=summarize(rp);frozen=json.loads((ROOT/'data/RAW_DOMAIN42.json').read_text())
 for key in ('rows','profiles','min_degree','min_pair','min_sum','max_reciprocal','sha256'):need(raw[key]==frozen[key],('raw metadata mismatch',key))
 need(raw['rows']==980624 and raw['min_degree']==2 and raw['min_pair']==20,'raw hypotheses')
 degree2=[list(r) for r in rp if 2 in ds(r)];degree3=[list(r) for r in rp if 3 in ds(r)]
 expected=[0,0,0,3,3,3,1,0,0,0,1,10,10,10]
 need(degree2==[expected],'complete degree-two row universe')
 need(len(degree3)==4 and all(all(r[10+i]==2 for i,d in enumerate(ds(bytes(r))) if d==3) for r in degree3),'degree-three disjointness obligation')
 stages={}
 for minimum in (6,7):
  selected=[r for r in rp if all(s not in (9,10) or k>=minimum for s,k in zip(r[10:],nearby(r[:10])))]
  if minimum==7:
   rebuilt=a.enumerate_rows(mu=42,r10=7,r9=7,cap=20);need(selected==rebuilt,'direct r7 reconstruction mismatch')
  stages[str(minimum)]=summarize(selected)
 need(stages['6']['rows']==537483 and stages['7']['rows']==292565,'stage counts')
 used=[r for r in selected if min(ds(r))>=4];need(len(used)==292560,'small-degree deletion count')
 cert=json.loads((ROOT/'certificates/STAR_CHARGE42.json').read_text());charge=c.verify(cert,used)
 caps={str(cap):summarize([r for r in used if max(ds(r))<=cap]) for cap in (16,17,18,19,20)}
 return {'status':'PASS','mu':42,'raw':raw,'bootstrap_domains':stages,'degree2_rows':degree2,'degree3_rows':degree3,'charge':charge,'maximum_degree_subdomains':caps,'literal_comparisons':2,'seconds':time.monotonic()-start}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ar=ap.parse_args();need(not ar.output.exists(),'fresh output');res=run();ar.output.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res['charge'],indent=2))
