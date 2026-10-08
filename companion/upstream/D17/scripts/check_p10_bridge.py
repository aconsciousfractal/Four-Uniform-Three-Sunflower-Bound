"""Re-establish the mu42/centre17 reduction, then replay unchanged finite objects.
The source certificates keep their original mu43/centre18 headers: only the
combinatorial domain and universal contradiction rules are reused.
"""
from pathlib import Path
from itertools import product
import sys,json,gzip
from copy import deepcopy
from common import rejected
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'inherited_p10/scripts'))
sys.path.insert(0,str(ROOT/'inherited_p10/discovery'))
import verify_glue as C,build_glue as P
import projection as p,audit_projection as a

def main():
 case=dict(id='P10_000',component=10,outside=7,r10=7,r9=7,interiors=[])
 d=p.build(case);e=a.build(case)
 for k in ('bounds','equal','anchor_rows'):C.require(d[k]==e[k],'new component '+k)
 # Independent elementary enumeration under the NEW hypotheses.
 rows=[]
 for ee in (0,1):
  for ww in product(range(4),repeat=3):
   kk=(5+ee+ww[0]+ww[1],5+ee+ww[0]+ww[2],5+ee+ww[1]+ww[2])
   for ss in product(range(9),repeat=3):
    dd=tuple(k+s for k,s in zip(kk,ss))
    if max(dd)>15 or any(s==8 and k!=5 for k,s in zip(kk,ss)):continue
    if 17+ee+sum(ww)+sum(ss)<42:continue
    rows.append((ww,ee,ss,dd))
 rows=sorted(rows)
 C.require(rows==C.local_rows(),'same elementary inequalities, not a transferred threshold')
 expected=tuple(sorted((2,2,2)+w+(ee,1,1,1)+(7,)+s for w,ee,s,dd in rows))
 C.require(all(rr==expected for rr in d['anchor_rows']),'all ten current anchors exactly match')
 geo=C.fixed_geometry()
 C.require(not P.margins((13,15,15,15,15,15)),'degree13 incompatible')
 records=[];mutations=0
 for name,profile in C.PROFILE.items():
  aa,ma=P.projections(profile);bb,mb=C.independent_states(profile)
  C.require(aa==bb and ma==mb,'all41 coordinates match independently')
  cert=json.loads(gzip.decompress((ROOT/'inherited_p10/certificates'/f'{name}.json.gz').read_bytes()))
  rec=C.verify_certificate(cert,name,bb,mb)
  records.append(rec)
  bad=deepcopy(cert);bad["mu"]=42;rejected(lambda:C.verify_certificate(bad,name,bb,mb));mutations+=1
  bad=deepcopy(cert);bad["witnesses"].pop();rejected(lambda:C.verify_certificate(bad,name,bb,mb));mutations+=1
  bad=deepcopy(cert);bad["witnesses"][0]=["P",6];rejected(lambda:C.verify_certificate(bad,name,bb,mb));mutations+=1
 print(json.dumps(dict(status='PASS',current_mu=42,current_center_degree=17,current_degree_cap=17,elementary_rows=len(rows),full_anchor_rows=10*len(rows),unchanged_finite_domain_replayed=True,states=sum(r['states']for r in records),mutations_rejected=mutations,records=records,geometry=geo),sort_keys=True))
if __name__=='__main__':main()
