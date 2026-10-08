"""One marked quadruple, two complete P9 trace systems, anonymised exterior."""
import math,sys
from pathlib import Path
from itertools import combinations,product
from collections import Counter
from functools import lru_cache
import pair_model as pm
p=pm.p

def build(case,with_anchor=False):
 # Mark is actual canonical0..12; 13..21 stay anonymous.
 mark=tuple(case['mark']);core=max(12,1+max(mark));nw=22-core
 if core>14 or len(mark)!=4 or any(v<0 or v>=core for v in mark):raise ValueError('mark/core')
 types=tuple(T for k in range(5) for T in combinations(range(core),k));sets=tuple(map(frozenset,types));nz=len(types)
 M=p.P[1:];L=tuple(M)+tuple(tuple(v+6 for v in T) for T in M);cones=tuple(frozenset((22,*T)) for T in L)
 sm=frozenset(mark);fixed=cones+(sm,)
 caps={v:16 if v%6<3 else 15 for v in range(12)};caps.update({v:18 for v in range(12,core)})
 local=pm.local_model(())
 bounds=[];zero=[]
 for j,T in enumerate(sets):
  if len(T)==4 and any(T<=S for S in pm.S):bb=(0,0)
  else:
   forbidden=any(a&b==a&T==b&T for a,b in combinations(fixed,2))
   hi=math.comb(nw,4-len(T))
   if len(T) in (1,2,3):hi=min(hi,{1:18,2:6,3:2}[len(T)]-sum(T<=C for C in cones))
   bb=(0,0 if forbidden else hi)
  if T==sm:
   if bb[1]<1:raise ValueError('self-forbidden mark')
   bb=(1,1)
  bounds.append(bb)
  if bb[1]==0:zero.append(j)
 equal=[];upper=[]
 def add(rows,label,co,r):rows.append((label,{j:v for j,v in co.items() if v},r))
 sels={}
 for side in (0,1):
  start=len(bounds);bounds.extend(local['bounds'])
  for kind in ('equal','upper'):
   for label,co,rhs in local[kind]:add(equal if kind=='equal' else upper,f's{side}/{label}',{j+start:v for j,v in co.items()},rhs)
  for j,U in enumerate(p.U):
   target=frozenset(v+6*side for v in U);co={h:1 for h,T in enumerate(sets) if T&pm.S[side]==target};co[start+j]=-1
   add(equal,f'shared-trace:{side}:{U}',co,0)
  add(upper,f'pure-pool:{side}',{h:1 for h,T in enumerate(sets) if len(T&pm.S[side])==1},27)
  # reconstruct selectors exact order in local data
  at=start+41
  fy=[sum(v in T for T in M) for v in range(6)]
  for v in range(6):
   ds=list(range(max(4,fy[v]),local['caps'][v]+1));sels[v+6*side]=dict(zip(ds,range(at,at+len(ds))));at+=len(ds)
 for v in range(12,core):
  cols=list(range(len(bounds),len(bounds)+15));bounds.extend([(0,1)]*15);sels[v]=dict(zip(range(4,19),cols))
  add(equal,f'ext-degree-choice:{v}',dict.fromkeys(cols,1),1)
  co={j:1 for j,T in enumerate(sets) if v in T};co.update({idx:-d for d,idx in sels[v].items()});add(equal,f'ext-degree-tie:{v}',co,0)
 for k in (1,2,3):
  for U in combinations(range(core),k):
   mask=frozenset(U)
   add(upper,f'cap:{U}',{h:1 for h,T in enumerate(sets) if mask<=T},caps[U[0]] if k==1 else {2:6,3:2}[k])
   # subtract cone offset, all other fixed quads are variables
   label,co,r=upper[-1];upper[-1]=(label,co,r-sum(mask<=F for F in cones))
 for i,F in enumerate(fixed):add(upper,f'H27:{i}',{h:1 for h,T in enumerate(sets) if not T&F},27-sum(not F&C for C in cones))
 add(upper,'W-degree',{h:4-len(T) for h,T in enumerate(sets)},18*nw)
 for y in range(core):add(upper,f'yW-pairs:{y}',{h:4-len(T) for h,T in enumerate(sets) if y in T},6*nw)
 for U in combinations(range(core),2):add(upper,f'pairW-triples:{U}',{h:4-len(T) for h,T in enumerate(sets) if set(U)<=T},2*nw)
 live=[]
 if with_anchor:raise ValueError('Full marked-anchor pilot is not part of this model')
 return dict(case=case['id'],bounds=bounds,equal=equal,upper=upper,nz=nz,types=types,objective=[1]*nz+[0]*(len(bounds)-nz),live=live,mark=mark,with_anchor=with_anchor)
