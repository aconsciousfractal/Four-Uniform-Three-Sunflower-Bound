"""Finite necessary projection on one isolated P10/P9, at mu=42.
All nonempty traces are shared across the anchors; the exterior support and
number of exterior-disjoint members are not bounded. Discovery constructor.
"""
from itertools import product,combinations,permutations
from functools import lru_cache
from collections import Counter
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import local43 as L
P=tuple(tuple(sorted(T)) for T in L.P)
U=tuple(T for n in (1,2,3) for T in combinations(range(6),n))
QUADS=tuple(combinations(range(6),4))
def sf(A,B,C):return A&B==A&C==B&C
def degrees(r):return tuple(1+r[10+i]+sum(r[j] for j in L.INC[i])+sum(r[6:10])-r[6+i] for i in range(4))
def models(m):return P if m==10 else P[1:] if m==9 else ()
@lru_cache(None)
def raw_rows(m,k,r10,r9,T):
 M=models(m);A=frozenset(T)
 alpha=tuple(sum(frozenset(B)&A=={v} for B in M) for v in T)
 tau=tuple(sum(frozenset(B)&A==A-{v} for B in M) for v in T)
 result=[]
 for p_tail in product(range(4),repeat=3):
  p=alpha+p_tail
  for e in (0,1):
   t=(e,*tau);kk=tuple(1+sum(p[j] for j in L.INC[i])+sum(t)-t[i] for i in range(4))
   if k not in L.local_s_candidates(0,p,t,17,r10,r9):continue
   options=[tuple(s for s in L.local_s_candidates(i,p,t,17,r10,r9) if s+kk[i]>=2) for i in (1,2,3)]
   for tail in product(*options):
    ss=(k,*tail);ds=tuple(a+b for a,b in zip(ss,kk))
    if min(ds)<4 or max(ds)>18 or sum(ds)<52 or any(ds[i]+ds[j]<20 for i,j in L.PAIRS):continue
    if 1+sum(p)+sum(t)+sum(ss)<42:continue
    if sum(d>=19 for d in ds)>2:continue
    if sum(p)+sum(t)>(12,14,17,19,22)[sum(s<8 for s in ss)]:continue
    if not L.equality_consistent(p,t,ss,kk):continue
    result.append(p+t+ss)
 return tuple(sorted(set(result)))

def catalog(m):
 M=models(m);fixed=[frozenset((6,*T)) for T in M];all_int=[]
 def rec(start,chosen,F):
  all_int.append(tuple(chosen))
  for i in range(start,15):
   Q=frozenset(QUADS[i])
   if any(sf(Q,A,B) for A,B in combinations(F,2)):continue
   rec(i+1,chosen+[i],F+[Q])
 rec(0,[],fixed)
 autos=[p for p in permutations(range(6)) if {tuple(sorted(p[v] for v in T)) for T in M}==set(M)]
 images=[[QUADS.index(tuple(sorted(p[v] for v in Q))) for Q in QUADS] for p in autos]
 seen=set();records=[]
 for inds in sorted(all_int,key=lambda t:(len(t),t)):
  if inds in seen:continue
  orbit={tuple(sorted(pm[j] for j in inds)) for pm in images};seen.update(orbit)
  records.append({'id':f'P{m}_{len(records):03d}','interiors':[list(QUADS[j]) for j in inds],'orbit_size':len(orbit)})
 if seen!=set(all_int):raise ValueError('Internal catalogue coverage')
 return {'component':m,'internal_count':len(all_int),'automorphism_count':len(autos),'records':records}

def build(case):
 if set(case)!={'id','component','outside','r10','r9','interiors'}:raise ValueError('case fields')
 m,k,r10,r9=(case[a] for a in ('component','outside','r10','r9'))
 if m not in (9,10) or k!=18-m or (r10,r9)!=(7,7):raise ValueError('scope')
 M=models(m);I=tuple(frozenset(Q) for Q in case['interiors']);fixed=tuple(frozenset((6,*T)) for T in M)+I
 if len(I)!=len(set(I)) or any(len(Q)!=4 or not Q<=set(range(6)) for Q in I):raise ValueError('interior validity')
 if any(sf(A,B,C) for A,B,C in combinations(fixed,3)):raise ValueError('sunflower in fixed members')
 fy=[sum(v in T for T in M) for v in range(6)];iy=[sum(v in Q for Q in I) for v in range(6)]
 caps=[min(18,15+iy[v]) if fy[v]==5 else 18 for v in range(6)]
 # E17/E18/C1: a P5 in a separated component needs an internal completion.
 for v in range(6):
  if fy[v]==4:
   caps[v]=max(d for d in range(4,19) if {17:1,18:4,19:5,20:6}.get(d,0)<=iy[v])
 links=[tuple(Q-{v} for Q in fixed if v in Q) for v in range(6)]
 clean=[all(A&B for A,B in combinations(T,2)) for T in links]
 esc=[]
 for v in range(6):
  if fy[v]==5 or not clean[v]:esc.append(0);continue
  covers=[frozenset(ab) for ab in combinations(set(range(6))-{v},2) if all(set(ab)&Q for Q in links[v])]
  if len(covers)>1:raise ValueError('multiple two-covers of the spine')
  extra=0
  if covers:
   candidates=[covers[0]|{z} for z in (7,8)]
   for size in (1,2):
    for ext in combinations(candidates,size):
     FF=links[v]+ext
     if all(A&B for A,B in combinations(FF,2)) and not any(sf(A,B,C) for A,B,C in combinations(FF,3)):extra=max(extra,size)
  esc.append(extra)
 bounds=[];zero=set()
 for j,T in enumerate(U):
  S=frozenset(T);off=sum(S<=Q for Q in fixed)
  hi={1:18,2:6,3:2}[len(T)]-off
  bad=any(A&B==A&S==B&S for A,B in combinations(fixed,2))
  if hi<0:raise ValueError('negative residual cap')
  bounds.append((0,0 if bad else hi))
  if bad:zero.add(j)
 eq=[]
 def put(name,terms,rhs):eq.append((name,{j:int(w) for j,w in terms.items() if w},int(rhs)))
 sels=[]
 for v in range(6):
  ds=range(max(4,fy[v]+iy[v]),caps[v]+1);ids=list(range(len(bounds),len(bounds)+len(ds)))
  bounds.extend([(0,1)]*len(ids));sel=dict(zip(ds,ids));sels.append(sel)
  put(f'degree-choice:{v}',dict.fromkeys(ids,1),1)
  terms={j:1 for j,T in enumerate(U) if v in T};terms.update({j:-d for d,j in sel.items()})
  put(f'degree-tie:{v}',terms,-fy[v]-iy[v])
 sizes=[]; all_anchor_rows=[]
 for pos,T in enumerate(M):
  A=frozenset(T);features=[(frozenset((v,)),11+i) for i,v in enumerate(T)]
  features += [(frozenset(ab),3+i) for i,ab in enumerate(combinations(T,2))]+[(A,6)]
  buckets={V:[j for j,Q in enumerate(U) if frozenset(Q)&A==V] for V,_ in features}
  off={V:sum(Q&A==V for Q in I) for V,_ in features}
  live=[]
  for row in raw_rows(m,k,r10,r9,T):
   ds=degrees(row);okay=True
   for i,v in enumerate(T,1):
    if ds[i]>caps[v]:okay=False;break
    ki=ds[i]-row[10+i]
    if row[10+i]>=8 or ds[i]>=17:
     if not clean[v] or not len(links[v])<=ki<=len(links[v])+(esc[v] if ki<8 else 0):okay=False;break
   if not okay:continue
   if any(not off[V]<=row[c]<=off[V]+sum(bounds[j][1] for j in buckets[V]) for V,c in features):continue
   live.append(row)
  cols=list(range(len(bounds),len(bounds)+len(live)));bounds.extend([(0,1)]*len(cols));sizes.append(len(live));all_anchor_rows.append(tuple(live))
  put(f'anchor:{pos}-choice',dict.fromkeys(cols,1),1)
  for V,c in features:
   terms=dict.fromkeys(buckets[V],1);terms.update({j:-r[c] for j,r in zip(cols,live)})
   put(f'anchor:{pos}-trace:{sum(1<<v for v in V)}',terms,-off[V])
  DD=[degrees(r) for r in live]
  for i,v in enumerate(T,1):
   for d,h in sels[v].items():
    terms={h:-1};terms.update({j:1 for j,ds in zip(cols,DD) if ds[i]==d})
    put(f'anchor:{pos}-degree:{v}:{d}',terms,0)
 return dict(case=case,bounds=bounds,upper=[],equal=eq,quads=U,zero=zero,objective=[0]*len(bounds),target=0,live_sizes=sizes,internal_degrees=iy,caps=caps,anchor_rows=all_anchor_rows)

def matrix(rows,n):
 import numpy as np
 from scipy.sparse import coo_matrix
 ii=[];jj=[];vv=[]
 for i,(_,terms,_) in enumerate(rows):
  for j,v in terms.items():ii.append(i);jj.append(j);vv.append(v)
 return coo_matrix((np.asarray(vv,dtype=float),(ii,jj)),shape=(len(rows),n)).tocsr(),np.array([rhs for _,_,rhs in rows],dtype=float)

def pair_constraints(data,comp):
 ups=[];M=models(comp)
 for y in range(6):
  st=[set(T)-{y} for T in M if y in T]
  cov=[set(p) for p in combinations([v for v in range(6) if v!=y],2) if all(set(p)&E for E in st)]
  exclusions=[None] if not cov else sorted(cov[0])
  for ex in exclusions:
   ids=[j for j,T in enumerate(U) if len(T)==2 and y in T and (ex is None or ex not in T)]
   h=U.index((y,))
   ups.extend([(f'pair:{y}:{ex}',dict.fromkeys(ids,1),6),(f'pair-singleton:{y}:{ex}',{h:5,**dict.fromkeys(ids,9)},59)])
 return ups

