"""Discovery model, R99 F69, matching both P9 component projections."""
import sys,math
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from collections import defaultdict
UP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(UP/'inherited'))
import projection as p
S=(frozenset(range(6)),frozenset(range(6,12)))
TYPES=tuple(T for k in range(5) for T in combinations(range(12),k))
MASKS=tuple(sum(1<<v for v in T) for T in TYPES)
@lru_cache(None)
def local_model(ints):
 case={'id':'component','component':9,'outside':9,'r10':7,'r9':7,'interiors':[list(q) for q in ints]}
 d=p.build(case);d['upper']=p.pair_constraints(d,9)
 return d

def build(pair,mark=None,pool=True):
 ints=[tuple(tuple(q) for q in pair['interiors_first']),tuple(tuple(v-6 for v in q) for q in pair['interiors_second'])]
 local=[local_model(t) for t in ints]
 L=tuple(p.P[1:])+tuple(tuple(v+6 for v in T) for T in p.P[1:])
 cones=tuple(frozenset((22,*T)) for T in L)
 internals=tuple(frozenset(q) for q in pair['interiors_first']+pair['interiors_second'])
 # A pure internal singleton marker can be included. Global mark use actual23 geometry later.
 fixed=cones+internals
 sets=tuple(map(frozenset,TYPES));nz=len(TYPES)
 bad=[];bounds=[]
 for T in sets:
  if len(T)==4 and any(T<=B for B in S):
   b=(1,1) if T in internals else (0,0)
  else:
   impossible=any(a&b==a&T==b&T for a,b in combinations(fixed,2))
   hi=math.comb(10,4-len(T))
   if len(T) in (1,2,3):hi=min(hi,{1:18,2:6,3:2}[len(T)]-sum(T<=C for C in cones))
   b=(0,0 if impossible else hi)
  bounds.append(b)
  if b==(0,0):bad.append(len(bounds)-1)
 eq=[];up=[]
 def add(rows,label,c,r):rows.append((label,{i:v for i,v in c.items() if v},r))
 for side,d in enumerate(local):
  start=len(bounds);bounds.extend(d['bounds'])
  for typ in ('equal','upper'):
   for label,coef,rhs in d[typ]:add(eq if typ=='equal' else up,f's{side}/{label}',{j+start:v for j,v in coef.items()},rhs)
  for j,U in enumerate(p.U):
   target=frozenset(v+6*side for v in U)
   terms={h:1 for h,T in enumerate(sets) if T&S[side]==target};terms[j+start]=-1
   add(eq,f'shared-trace:{side}:{U}',terms,0)
  if pool:add(up,f'pure-pool:{side}',{h:1 for h,T in enumerate(sets) if len(T&S[side])==1},27)
 # Universal incidences on subsets of12 old points, no centre.
 for k in (1,2,3):
  for U in combinations(range(12),k):
   U=frozenset(U)
   add(up,f'cap:{tuple(sorted(U))}',{h:1 for h,T in enumerate(sets) if U<=T},{1:18,2:6,3:2}[k]-sum(U<=F for F in cones))
 # H27 around all known true anchors. Interiors stay among count variables.
 for k,F in enumerate(fixed):
  add(up,f'H27:{k}',{h:1 for h,T in enumerate(sets) if not T&F},27-sum(not F&C for C in cones))
 # Uniformly aggregate the ten exterior labels; the total is an upper bound.
 add(up,'W-degree',{h:4-len(T) for h,T in enumerate(sets)},180)
 for y in range(12):
  add(up,f'yW-pairs:{y}',{h:4-len(T) for h,T in enumerate(sets) if y in T},60)
 for U in combinations(range(12),2):
  add(up,f'pairW-triples:{U}',{h:4-len(T) for h,T in enumerate(sets) if set(U)<=T},20)
 return {'case':pair['id'],'bounds':bounds,'equal':eq,'upper':up,'nz':nz,'types':TYPES,'objective':[1]*nz+[0]*(len(bounds)-nz),'live':[d['live_sizes'] for d in local],'pool':pool}
