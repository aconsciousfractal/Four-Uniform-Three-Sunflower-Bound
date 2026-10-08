"""Independent integer reconstruction of the mu42 component projections.
Bit-set intersections, t-before-p local generation, full-mask interior census.
This module does not import the discovery model or any numerical library.
"""
from itertools import combinations,product,permutations
from functools import lru_cache
from fractions import Fraction
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/"inputs"))
import audit43 as A
P=tuple(tuple(map(int,t)) for t in ('012','015','023','034','045','124','134','135','235','245'))
TYPES=tuple(t for k in (1,2,3) for t in combinations(range(6),k))
INTERNALS=tuple(combinations(range(6),4))
def bm(T):return sum(1<<v for v in T)
def need(ok,msg):
 if not ok:raise ValueError(msg)
def blocks(m):
 need(m in (9,10),'component');return P if m==10 else P[1:]
def deg(r,i):return 1+r[10+i]+sum(r[j] for j,p in enumerate(A.PAIR_LIST) if i in p)+sum(r[6:10])-r[6+i]
@lru_cache(None)
def rows(m,k,r10,r9,T):
 BB=tuple(bm(B) for B in blocks(m));R=bm(T)
 singles=tuple(sum(B&R==1<<v for B in BB) for v in T)
 doubles=tuple(sum(B&R==R^(1<<v) for B in BB) for v in T);result=[]
 for e in (0,1):
  ts=(e,*doubles)
  for tail in product(range(4),repeat=3):
   pp=singles+tail;domains=[];kk=[]
   for i in range(4):
    other=[j for j in range(4) if j!=i];alpha=tuple(pp[A.PAIR_LIST.index(tuple(sorted((i,j))))] for j in other)
    tau=tuple(ts[j] for j in other);kk.append(1+sum(alpha)+sum(tau))
    domains.append(tuple((s,d) for s,d in A.choices(alpha,tau,ts[i],r10,r9,18) if d>=4 and (i!=0 or s==k)))
   for vals in product(*domains):
    ss=tuple(t[0] for t in vals);ds=tuple(t[1] for t in vals)
    if sum(ds)<52 or any(ds[i]+ds[j]<20 for i,j in A.PAIR_LIST):continue
    if A.condition_global(pp,ts,ss,kk,ds,42):result.append(pp+ts+ss)
 result.sort();need(len(result)==len(set(result)),'row uniqueness');return tuple(result)

def catalog(m):
 M=blocks(m);fixed=[bm((6,*T)) for T in M];qq=[bm(Q) for Q in INTERNALS];bad=[]
 for k in (1,2,3):
  for inds in combinations(range(15),k):
   for cs in combinations(fixed,3-k):
    vals=tuple(qq[j] for j in inds)+cs;a,b,c=vals
    if a&b==a&c==b&c:bad.append(sum(1<<j for j in inds));break
 good={mask for mask in range(1<<15) if not any(mask&b==b for b in bad)}
 autos=[]
 for perm in permutations(range(6)):
  if {tuple(sorted(perm[v] for v in T)) for T in M}==set(M):autos.append(perm)
 maps=[[INTERNALS.index(tuple(sorted(p[v] for v in Q))) for Q in INTERNALS] for p in autos]
 covered=set();records=[]
 for mask in sorted(good,key=lambda x:(x.bit_count(),tuple(j for j in range(15) if x>>j&1))):
  if mask in covered:continue
  inds=[j for j in range(15) if mask>>j&1]
  orb={sum(1<<pm[j] for j in inds) for pm in maps};covered |=orb
  records.append({'id':f'P{m}_{len(records):03d}','interiors':[list(INTERNALS[j]) for j in inds],'orbit_size':len(orb)})
 need(covered==good,'full interior orbit coverage')
 return {'component':m,'internal_count':len(good),'automorphism_count':len(autos),'records':records}

def build(case):
 need(type(case) is dict and set(case)=={'id','component','outside','r10','r9','interiors'},'case fields')
 need(type(case['id']) is str,'case name')
 m,k,r10,r9=(case[v] for v in ('component','outside','r10','r9'))
 need(all(type(v) is int for v in (m,k,r10,r9)),'integer parameters')
 need((m,k,r10,r9) in ((10,8,7,7),(9,9,7,7)),'centre18 mu42 scope')
 M=blocks(m);ints=case['interiors']
 need(type(ints) is list and all(type(Q) is list and len(Q)==4 and all(type(v) is int and 0<=v<6 for v in Q) and sorted(set(Q))==Q for Q in ints),'internal member')
 need(len(ints)==len({tuple(Q) for Q in ints}),'simple internal family')
 I=tuple(bm(Q) for Q in ints);fixed=tuple(bm((6,*T)) for T in M)+I
 need(not any(a&b==a&c==b&c for a,b,c in combinations(fixed,3)),'sunflower in prescribed core')
 fy=[sum(v in T for T in M) for v in range(6)];iy=[sum(Q>>v&1 for Q in I) for v in range(6)]
 cap=[]
 for v in range(6):
  if fy[v]==5:cap.append(min(18,15+iy[v]))
  else:cap.append(max(d for d in range(4,19) if iy[v]>= {17:1,18:4,19:5,20:6}.get(d,0)))
 link=[tuple(Q^(1<<v) for Q in fixed if Q>>v&1) for v in range(6)]
 cl=[all(a&b for a,b in combinations(L,2)) for L in link];escape=[]
 for v in range(6):
  ec=0
  if fy[v]==4 and cl[v]:
   covers=[bm(T) for T in combinations([j for j in range(6) if j!=v],2) if all(bm(T)&B for B in link[v])]
   need(len(covers)<=1,'spine cover count')
   if covers:
    candidates=[covers[0]|(1<<7),covers[0]|(1<<8)]
    for n in (1,2):
     for extra in combinations(candidates,n):
      full=link[v]+extra
      if all(a&b for a,b in combinations(full,2)) and not any(a&b==a&c==b&c for a,b,c in combinations(full,3)):ec=max(ec,n)
  escape.append(ec)
 bounds=[];zero=set()
 for j,T in enumerate(TYPES):
  mask=bm(T);off=sum(mask&Q==mask for Q in fixed)
  hi={1:18,2:6,3:2}[len(T)]-off;need(hi>=0,'nonnegative codegree remainder')
  excluded=any(a&mask==a&b==b&mask for a,b in combinations(fixed,2))
  bounds.append((0,0 if excluded else hi))
  if excluded:zero.add(j)
 equal=[]
 def put(name,coef,rhs):equal.append((name,{j:int(c) for j,c in coef.items() if c},int(rhs)))
 sels=[]
 for v in range(6):
  ds=list(range(max(4,fy[v]+iy[v]),cap[v]+1));ids=list(range(len(bounds),len(bounds)+len(ds)))
  bounds.extend([(0,1)]*len(ids));select=dict(zip(ds,ids));sels.append(select)
  put(f'degree-choice:{v}',dict.fromkeys(ids,1),1)
  coeff={j:1 for j,T in enumerate(TYPES) if v in T};coeff.update({j:-d for d,j in select.items()})
  put(f'degree-tie:{v}',coeff,-fy[v]-iy[v])
 sizes=[]; all_anchor_rows=[]
 for pos,T in enumerate(M):
  mask=bm(T);features=[(1<<v,11+i) for i,v in enumerate(T)]+[(bm(ab),3+i) for i,ab in enumerate(combinations(T,2))]+[(mask,6)]
  bags={V:[j for j,Q in enumerate(TYPES) if bm(Q)&mask==V] for V,c in features}
  off={V:sum(Q&mask==V for Q in I) for V,c in features}
  live=[]
  for row in rows(m,k,r10,r9,T):
   valid=True
   for i,v in enumerate(T,1):
    d=deg(row,i);s=row[10+i];near=d-s
    if d>cap[v]:valid=False;break
    if s>=8 or d>=17:
     maximum=len(link[v])+(escape[v] if near<8 else 0)
     if not cl[v] or near<len(link[v]) or near>maximum:valid=False;break
   if not valid:continue
   if any(row[c]<off[V] or row[c]>off[V]+sum(bounds[j][1] for j in bags[V]) for V,c in features):continue
   live.append(row)
  ids=list(range(len(bounds),len(bounds)+len(live)));bounds.extend([(0,1)]*len(ids));sizes.append(len(live));all_anchor_rows.append(tuple(live))
  put(f'anchor:{pos}-choice',dict.fromkeys(ids,1),1)
  for V,c in features:
   coeff=dict.fromkeys(bags[V],1);coeff.update({j:-row[c] for j,row in zip(ids,live)})
   put(f'anchor:{pos}-trace:{V}',coeff,-off[V])
  for i,v in enumerate(T,1):
   for d,h in sels[v].items():
    coeff={h:-1};coeff.update({j:1 for j,row in zip(ids,live) if deg(row,i)==d})
    put(f'anchor:{pos}-degree:{v}:{d}',coeff,0)
 return dict(case=case,bounds=bounds,upper=[],equal=equal,quads=TYPES,zero=zero,objective=[0]*len(bounds),target=0,live_sizes=sizes,internal_degrees=iy,caps=cap,anchor_rows=all_anchor_rows)

def pair_rows(case):
    """Independent build of pair bounds from the full local point-link graph."""
    out=[]; M=tuple(frozenset(t) for t in blocks(case['component']))
    for y in range(6):
        edges=[B-{y} for B in M if y in B]
        covers=[]
        for a,b in combinations(sorted(set(range(6))-{y}),2):
            if all(a in e or b in e for e in edges):covers.append((a,b))
        need(len(covers)<=1, 'unique possible P5 cover')
        exclude=(None,) if not covers else covers[0]
        for a in exclude:
            js=[j for j,T in enumerate(TYPES) if len(T)==2 and y in T and (a is None or a not in T)]
            out.append((f'pair:{y}:{a}',dict.fromkeys(js,1),6))
            terms={TYPES.index((y,)):5}
            for j in js:terms[j]=9
            out.append((f'pair-singleton:{y}:{a}',terms,59))
    return out

def check(cert,data=None):
    need(type(cert) is dict and cert.get('schema')=='E20_F69_D18_COMPONENT_CERT_V1', 'certificate schema')
    data=build(cert['case']) if data is None else data
    data=dict(data);data['upper']=pair_rows(cert['case'])
    need(data['case']==cert['case'],'case identity')
    n=len(data['bounds'])
    for k,v in [('columns',n),('upper_rows',len(data['upper'])),('equal_rows',len(data['equal']))]:
        need(type(cert[k]) is int and cert[k]==v,'dimension '+k)
    need(type(cert['scale']) is int and cert['scale']>0,'scale')
    q=[0]*n;rhs=0;counts={}
    for name in ('upper','equal'):
        need(type(cert[name]) is list,'list');seen=set()
        for item in cert[name]:
            need(type(item) is list and len(item)==2,'record')
            i,w=item
            need(type(i) is int and i not in seen and 0<=i<len(data[name]),'row index')
            need(type(w) is int and w!=0 and (name!='upper' or w>0),'integer/sign')
            seen.add(i);label,a,b=data[name][i];rhs+=w*b
            for j,c in a.items():q[j]+=w*c
        counts[name]=len(seen)
    low=sum(min(c*l,c*u) for c,(l,u) in zip(q,data['bounds']));gap=rhs-low
    need(gap<0,'not a contradiction')
    for k,v in [('rhs',rhs),('box_min',low),('value',gap)]:need(type(cert[k]) is int and cert[k]==v,'exact '+k)
    return {'case':cert['case'],'status':'PASS','columns':n,'upper_terms':counts['upper'],'equal_terms':counts['equal'],'rhs':rhs,'box_min':low,'gap':gap,'live_sizes':data['live_sizes']}
