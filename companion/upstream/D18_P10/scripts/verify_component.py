"""Exact replay of a local P9/P10 trace forest at mu42 and global cap18.
Independent set-based geometry; no numerical package, no producer import.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from itertools import combinations,permutations,product
import argparse,gzip,hashlib,json,time
from pathlib import Path
import audit_projection as A
need=A.need
PAIRS=tuple(combinations(range(6),2)); TRIPLES=tuple(combinations(range(6),3))
PI={p:i for i,p in enumerate(PAIRS)};TI={t:i for i,t in enumerate(TRIPLES)}
TP=tuple(tuple(PI[p] for p in combinations(t,2)) for t in TRIPLES)
YP=tuple(tuple(j for j,p in enumerate(PAIRS) if y in p) for y in range(6))
YT=tuple(tuple(j for j,t in enumerate(TRIPLES) if y in t) for y in range(6))
HBOUND=(20,10,8,5,4,2,1)
def sf(a,b,c):return a&b==a&c==b&c

class Check:
 def __init__(self,case):
  self.case=case;self.M=A.blocks(case['component']);self.I=tuple(map(frozenset,case['interiors']));self.fixed=tuple(frozenset((6,*t)) for t in self.M)+self.I
  self.FT=tuple(TI[t] for t in self.M);self.FP=tuple(TP[k] for k in self.FT);self.COMP=tuple(k for k in range(20) if k not in self.FT)
  self.fix=tuple(sum(y in q for q in self.fixed) for y in range(6));self.model=A.build(case);self.ub=tuple(b for a,b in self.model['bounds'][:41])
  self.SF=tuple(tuple(y for y in range(6) if any(sf(q,frozenset((*u,7)),frozenset((y,8,9,10))) for q in self.fixed)) for u in TRIPLES)
  self.PF=tuple(tuple(j for j,v in enumerate(PAIRS) if any(sf(q,frozenset((*u,7)),frozenset((*v,8,9))) for q in self.fixed)) for u in TRIPLES)
  self.TF=tuple(tuple(any(sf(q,frozenset((*u,7)),frozenset((*v,8))) for q in self.fixed) for v in TRIPLES) for u in TRIPLES)
  self.SM=tuple(sum(1<<y for y in s) for s in self.SF);self.PM=tuple(sum(1<<j for j in v) for v in self.PF)
  cov=[tuple(p for p in combinations(sorted(set(range(6))-{y}),2) if all(set(p)&(set(t)-{y}) for t in self.M if y in t)) for y in range(6)]
  need(all(len(c)<=1 for c in cov),'cover uniqueness')
  self.sub=tuple((YP[y],) if not cov[y] else tuple(tuple(j for j in YP[y] if a not in PAIRS[j]) for a in cov[y][0]) for y in range(6))
  self.components=lru_cache(maxsize=40000)(self._components)
 def domain(self,prefix,compare=False):
  allrows=[];pointdom=[set(range(4,19)) for y in range(6)];dsets=[]
  for t,raw in zip(self.M,self.model['anchor_rows']):
   rs=[]
   for r in raw:
    d=tuple(A.deg(r,i) for i in(1,2,3));e=r[6]-sum(set(t)<=q for q in self.I)
    m=tuple(r[3+j]+r[6]-sum(set(p)<=q for q in self.I) for j,p in enumerate(combinations(t,2)))
    need(e>=0 and min(m)>=0,'projected trace nonnegative');rs.append((d,m,e))
   rs=sorted(set(rs));allrows.append(rs);dd={d for d,m,e in rs};dsets.append(dd)
   for j,y in enumerate(t):pointdom[y]&={d[j] for d in dd}
  labelled=[]
  def rec(ds):
   y=len(ds)
   if y==6:labelled.append(tuple(ds));return
   for v in sorted(pointdom[y]):
    temp=ds+[v]
    if all(any(all(z[j]==temp[x] for j,x in enumerate(t) if x<=y) for z in vv) for t,vv in zip(self.M,dsets)):
     rec(temp)
  rec([])
  autos=[p for p in permutations(range(6)) if {tuple(sorted(p[y] for y in t)) for t in self.M}==set(self.M) and {tuple(sorted(p[y] for y in q)) for q in self.I}=={tuple(sorted(q)) for q in self.I}]
  canon=sorted({min(tuple(d[p[y]] for y in range(6)) for p in autos) for d in labelled})
  saved=json.loads(prefix.with_suffix('.profiles.json').read_text())
  for key,expected in [('case',self.case),('labelled',[list(x) for x in labelled]),('canonical',[list(x) for x in canon]),('autos',[list(x) for x in autos]),('row_counts',[len(t) for t in allrows])]:need(saved[key]==expected,'complete saved domain '+key)
  lines=[f'{len(self.M)} {len(self.I)}']+[' '.join(map(str,t)) for t in self.M]+[' '.join(map(str,sorted(q))) for q in self.I]
  lines+=[' '.join(map(str,self.ub)),str(len(canon))]+[' '.join(map(str,d)) for d in canon]
  for rr in allrows:
   lines.append(str(len(rr)));lines+=[' '.join(map(str,(*d,*m,e))) for d,m,e in rr]
  need(prefix.with_suffix('.domain.txt').read_text()=='\n'.join(lines)+'\n','literal complete domain text')
  if compare:
   import projection as P
   other=P.build(self.case)
   for key in ('anchor_rows','bounds','equal','caps','internal_degrees','quads','zero'):
    need(self.model[key]==other[key],'literal independent model '+key)
  return canon,allrows
 def _components(self,counts,sb,pb):
  ids=tuple(u for u,n in enumerate(counts) for _ in range(n));left=set(range(len(ids)));desc=[]
  while left:
   a=left.pop();group=[a];todo=[a]
   while todo:
    j=todo.pop();u=ids[j]
    new=[k for k in left if self.TF[u][ids[k]] or self.SM[u]&self.SM[ids[k]]&sb or self.PM[u]&self.PM[ids[k]]&pb]
    for k in new:left.remove(k);group.append(k);todo.append(k)
   types=tuple(ids[j] for j in group)
   if len(types)!=len(set(types)):return True,()
   ss=tuple(sorted({y for u in types for y in self.SF[u]}));pp=tuple(sorted({j for u in types for j in self.PF[u]}))
   inc=tuple(sum(y in TRIPLES[u] for u in types) for y in range(6));desc.append((len(types),ss,pp,inc))
  return False,tuple(desc)
 def cut(self,code,ns,np,nt):
  if code==2:return any((b:=sum(np[j] for j in sub))>6 or ns[y]>HBOUND[b] for y in range(6) for sub in self.sub[y])
  if code==3:return any(n>=2 and sum(ns[y] for y in self.SF[u])+sum(np[j] for j in self.PF[u])>6 for u,n in enumerate(nt))
  if code==7:
   t=sum(ns);h=max(ns)
   return h>=10 and t>20 or h>=9 and t>22 or h>=8 and t>36
  sb=sum(1<<y for y in range(6) if ns[y]>=3);pb=sum(1<<j for j in range(15) if np[j]>=2)
  du,cs=self.components(bytes(nt),sb,pb)
  if code==4:return du
  if du:return False
  if code==5:return any(n+sum(ns[y] for y in ss)+sum(np[j] for j in pp)>18 for n,ss,pp,inc in cs)
  if code==6:return any(inc[y]+(ns[y] if y in ss else 0)+sum(np[j] for j in pp if y in PAIRS[j])>6 for n,ss,pp,inc in cs for y in range(6))
  raise ValueError('unknown cut code')
 def verify(self,cid,profiles,allrows,prefix,override=None):
  ds=profiles[cid];options=[tuple((m,e) for d,m,e in rr if d==tuple(ds[y] for y in t)) for t,rr in zip(self.M,allrows)]
  binfile=prefix.parent/(prefix.name+'_'+str(cid)+'.bin');gz=Path(str(binfile)+'.gz')
  raw=gz.read_bytes() if gz.exists() else binfile.read_bytes();proof=gzip.decompress(raw) if gz.exists() else raw
  if override is not None:proof=override
  cur=joins=patterns=0;nt=[0]*20;mar=[-1]*15;used=[0]*15;reasons=[0]*10;base=[0]*6;start=time.monotonic()
  def complete(level,order):
   nonlocal cur
   need(cur<len(proof),'truncated proof');code=proof[cur];cur+=1;need(code<=8,'invalid/open code')
   if code:
    possible=[0]*15;extra=[0]*6
    for k in order[level:]:
     c=min(self.ub[21+k],*(mar[j]-used[j] for j in TP[k]));need(c>=0,'capacity')
     for j in TP[k]:possible[j]+=c
     for y in TRIPLES[k]:extra[y]+=c
    sr=[base[y]+sum(nt[k] for k in YT[y]) for y in range(6)]
    ns=[max(0,v) for v in sr];np=[max(0,mar[j]-used[j]-possible[j]) for j in range(15)]
    if code==1:valid=any(sr[y]+extra[y]<0 for y in range(6))
    elif code==8:valid=any(ns[y]>self.ub[y] for y in range(6)) or any(np[j]>self.ub[6+j] for j in range(15))
    else:valid=self.cut(code,ns,np,nt)
    need(valid,f'false cut case{cid} code{code} offset{cur-1} level{level}');reasons[code]+=1;return
   need(level<len(order),'unrefuted complete projection')
   k=order[level];c=min(self.ub[21+k],*(mar[j]-used[j] for j in TP[k]));need(c>=0,'branch cap')
   for e in range(c+1):
    nt[k]=e
    for j in TP[k]:used[j]+=e
    complete(level+1,order)
    for j in TP[k]:used[j]-=e
   nt[k]=0
  def join(rem):
   nonlocal joins,patterns
   joins+=1
   if not rem:
    patterns+=1
    for y in range(6):base[y]=ds[y]-self.fix[y]-sum(mar[j] for j in YP[y])
    order=sorted(self.COMP,key=lambda k:(min(mar[j]-used[j] for j in TP[k]),k));complete(0,order);return
   best=None;chosen=None
   for t in rem:
    pp=self.FP[t];live=[(m,e) for m,e in options[t] if e<=self.ub[21+self.FT[t]] and all((mar[j]<0 or mar[j]==v) and used[j]+e<=v for j,v in zip(pp,m))]
    if not live:return
    if best is None or len(live)<len(best):best=live;chosen=t
   pp=self.FP[chosen];fresh=[j for j in pp if mar[j]<0];rest=tuple(t for t in rem if t!=chosen)
   for m,e in best:
    for j,v in zip(pp,m):mar[j]=v;used[j]+=e
    nt[self.FT[chosen]]=e;join(rest);nt[self.FT[chosen]]=0
    for j in pp:used[j]-=e
    for j in fresh:mar[j]=-1
  join(tuple(range(len(self.M))));need(cur==len(proof),'trailing bytes')
  return dict(status='PASS',case=cid,profile=list(ds),joinnodes=joins,margin_patterns=patterns,projections=cur,reasons=reasons,certificate_sha256=hashlib.sha256(raw).hexdigest(),seconds=round(time.monotonic()-start,6))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('prefix',type=Path);ap.add_argument('--first',type=int,default=0);ap.add_argument('--last',type=int);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--compare',action='store_true');a=ap.parse_args()
 need(not a.output.exists(),'fresh output');saved=json.loads(a.prefix.with_suffix('.profiles.json').read_text());C=Check(saved['case']);profiles,rows=C.domain(a.prefix,a.compare);last=len(profiles) if a.last is None else a.last
 need(0<=a.first<=last<=len(profiles),'range');outs=[]
 with a.output.open('x') as out:
  for cid in range(a.first,last):
   r=C.verify(cid,profiles,rows,a.prefix);out.write(json.dumps(r)+'\n');out.flush();print(json.dumps(r),flush=True)
if __name__=='__main__':main()
