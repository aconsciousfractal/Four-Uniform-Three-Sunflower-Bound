"""Independent standard-library audit of every rooted empty-C5 R16 case.
The certificate has one byte per labelled degree-six star. 0..n-1 names a
vertex with insufficient completion capacity; 32+pair_index names an overused
pair; 128+vertex names an overfull degree. No solver and no producer import.
"""
from itertools import combinations,permutations,product
from collections import Counter
from pathlib import Path
import hashlib,json,sys,time,argparse
from math import comb
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
 if not ok:raise ValueError(message)
def canonical_cases():
 edges={frozenset((i,(i+1)%5)) for i in range(5)}
 group=[p for p in permutations(range(5)) if {frozenset((p[i],p[(i+1)%5])) for i in range(5)}==edges]
 patterns=sorted({min(tuple(t[p[i]] for i in range(5)) for p in group) for t in product(range(3,6),repeat=5)})
 require(len(group)==10,'cycle automorphism coverage')
 out=[]
 for p in patterns:
  remaining=48-5-sum(p);tails=[]
  for a in range(remaining//2+1):
   for b in range((remaining-2*a)//3+1):
    for c in range((remaining-2*a-3*b)//4+1):
     for d in range((remaining-2*a-3*b-4*c)//5+1):
      r=remaining-2*a-3*b-4*c-5*d
      if r<=0 or r%6:continue
      e=r//6;full=(5,*p,*((2,)*a+(3,)*b+(4,)*c+(5,)*d+(6,)*e));cnt=Counter(full)
      if 2*cnt[2]+3*cnt[3]>16:continue
      if sum(w*cnt[k] for k,w in ((2,2),(3,5),(4,10),(5,16),(6,24)))<128:continue
      tails.append(tuple(full[6:]))
  for ext in sorted(tails):out.append((5,*p,*ext))
 return patterns,out

def audit(proof_path,progress=False):
 start=time.monotonic();patterns,cases=canonical_cases();blob=Path(proof_path).read_bytes();pos=0;reports=[]
 expected_bytes=sum(10*comb(len(d)-2,6) for d in cases)
 require(len(blob)==expected_bytes,'certificate length does not match the complete root universe')
 for cid,degree in enumerate(cases):
  n=len(degree);center=0;z=next(i for i in range(6,n) if degree[i]==6)
  pairs=list(combinations(range(n),2));pi={p:i for i,p in enumerate(pairs)}
  pairmask=[(1<<a)|(1<<b) for a,b in pairs]
  capacities=[max(0,min(2,degree[a]+degree[b]-6)) for a,b in pairs]
  base=tuple((1<<0)|(1<<i)|(1<<(i%5+1)) for i in range(1,6));pool=[i for i in range(1,n) if i!=z]
  # Candidate catalogue for each potential deficient vertex; no degree-six star
  # has yet been selected when this catalogue is made.
  candidates=[[] for _ in range(n)]
  for t in combinations(range(n),3):
   m=sum(1<<v for v in t)
   if m&63==m or sum(degree[v] for v in t)<11:continue
   ps=tuple(pi[u] for u in combinations(t,2))
   for v in t:candidates[v].append((t,m,ps))
  counts=Counter()
  for six in combinations(pool,6):
   for two in combinations(six[1:],2):
    tri=(six[0],*two);other=tuple(v for v in six if v not in tri)
    fixed=base+tuple((1<<z)|(1<<a)|(1<<b) for T in (tri,other) for a,b in combinations(T,2))
    require(pos<len(blob),'truncated certificate');code=blob[pos];pos+=1;counts['roots']+=1
    if 32<=code<32+len(pairs):
     p=code-32;require(sum((f&pairmask[p])==pairmask[p] for f in fixed)>capacities[p],('false pair witness',cid,pos-1,p));counts['pair']+=1
    elif 128<=code<128+n:
     v=code-128;require(sum(bool(f&(1<<v)) for f in fixed)>degree[v],('false degree witness',cid,pos-1,v));counts['degree']+=1
    elif code<n:
     v=code;fixed_set=set(fixed);used=[sum(bool(f&(1<<u)) for f in fixed) for u in range(n)]
     need=degree[v]-used[v];require(need>0,('nondeficient vertex',cid,pos-1,v))
     cd=[sum(f&m==m for f in fixed) for m in pairmask]
     disjoint=[sum(not(f&g) for g in fixed) for f in fixed]
     agreements=tuple((a,b,(a&b)) for a,b in combinations(fixed,2));available=0
     for t,m,ps in candidates[v]:
      if m in fixed_set:continue
      if any(used[u]>=degree[u] for u in t):continue
      if any(cd[p]>=capacities[p] for p in ps):continue
      # A sunflower has no point of multiplicity exactly two.
      if any(((a&b&~m)|(a&m&~b)|(b&m&~a))==0 for a,b,ab in agreements):continue
      lost=[j for j,f in enumerate(fixed) if not m&f]
      if len(lost)>7 or any(disjoint[j]>=7 for j in lost):continue
      available+=1
      require(available<need,('capacity witness admits enough triples',cid,pos-1,v,available,need))
     counts['capacity']+=1
    else:raise ValueError(('unsupported or OPEN certificate byte',cid,pos-1,code))
  reports.append({'case':cid,'n':n,**counts})
  if progress and cid%50==0:print('verified cases',cid+1,'roots',pos,flush=True)
 require(pos==len(blob),'unconsumed trailing certificate data')
 total=Counter()
 for r in reports:
  for k in ('roots','pair','degree','capacity'):total[k]+=r.get(k,0)
 return {'status':'PASS','scope':'R16 with degree-five C5 point and exactly five triples on its six-point closed support; degree-six existence is imported','patterns':len(patterns),'cases':len(cases),'case_degrees_sha256':hashlib.sha256(json.dumps(cases,separators=(',',':')).encode()).hexdigest(),'support_counts':dict(Counter(map(len,cases))),'certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),'totals':dict(total),'reports':reports,'seconds':time.monotonic()-start}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=ROOT/'certificates/C5_EMPTY_R16.bin');ap.add_argument('--output',type=Path);ap.add_argument('--progress',action='store_true');a=ap.parse_args()
 out=audit(a.certificate,a.progress);print(json.dumps({k:v for k,v in out.items() if k!='reports'},indent=2),flush=True)
 if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
