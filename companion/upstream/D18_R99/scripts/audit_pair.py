"""Independent set/bitmask reconstruction of the two-component model.
Only Python standard library. Imports the separate inherited local auditor.
"""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from math import comb
import sys
UP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(UP/'inherited'))
import audit_projection as a
need=a.need
@lru_cache(None)
def local(ints):
 case={'id':'component','component':9,'outside':9,'r10':7,'r9':7,'interiors':[list(T) for T in ints]}
 ans=a.build(case);ans['upper']=a.pair_rows(case);return ans

def build(pair):
 ints=(tuple(tuple(Q) for Q in pair['interiors_first']),tuple(tuple(v-6 for v in Q) for Q in pair['interiors_second']))
 domains=[local(I) for I in ints]
 types=tuple(Q for r in range(5) for Q in combinations(range(12),r))
 tm=tuple(a.bm(Q) for Q in types);nz=len(types)
 cones=tuple(a.bm((22,*T)) for T in a.blocks(9))+tuple(a.bm((22,*(v+6 for v in T))) for T in a.blocks(9))
 marks=tuple(a.bm(Q) for Q in pair['interiors_first']+pair['interiors_second']);fixed=cones+marks
 bounds=[];masks=(63,4032)
 for Q,bits in zip(types,tm):
  if len(Q)==4 and any(bits&M==bits for M in masks):lo=hi=int(bits in marks)
  else:
   lo=0;hi=comb(10,4-len(Q))
   if len(Q) in (1,2,3):hi=min(hi,{1:18,2:6,3:2}[len(Q)]-sum(C&bits==bits for C in cones))
   if any(C&D==C&bits==D&bits for C,D in combinations(fixed,2)):hi=0
  need(lo<=hi and lo>=0,'count bound');bounds.append((lo,hi))
 rows={'equal':[],'upper':[]}
 for side,dom in enumerate(domains):
  offset=len(bounds);bounds.extend(dom['bounds'])
  for kind in rows:
   for name,co,rhs in dom[kind]:rows[kind].append((f's{side}/{name}',{j+offset:v for j,v in co.items()},rhs))
  for j,U in enumerate(a.TYPES):
   mask=a.bm(tuple(v+6*side for v in U));co={h:1 for h,bits in enumerate(tm) if bits&masks[side]==mask};co[offset+j]=-1
   rows['equal'].append((f'shared-trace:{side}:{U}',co,0))
  rows['upper'].append((f'pure-pool:{side}',{h:1 for h,bits in enumerate(tm) if (bits&masks[side]).bit_count()==1},27))
 for k in (1,2,3):
  for U in combinations(range(12),k):
   mask=a.bm(U);rows['upper'].append((f'cap:{U}',{h:1 for h,bits in enumerate(tm) if bits&mask==mask},{1:18,2:6,3:2}[k]-sum(C&mask==mask for C in cones)))
 for i,F in enumerate(fixed):rows['upper'].append((f'H27:{i}',{h:1 for h,bits in enumerate(tm) if bits&F==0},27-sum(F&C==0 for C in cones)))
 rows['upper'].append(('W-degree',{h:4-len(T) for h,T in enumerate(types) if len(T)<4},180))
 for y in range(12):rows['upper'].append((f'yW-pairs:{y}',{h:4-len(T) for h,T in enumerate(types) if y in T and len(T)<4},60))
 for U in combinations(range(12),2):
  mask=a.bm(U);rows['upper'].append((f'pairW-triples:{U}',{h:4-len(T) for h,(T,bits) in enumerate(zip(types,tm)) if mask&bits==mask and len(T)<4},20))
 return {'case':pair['id'],'bounds':bounds,**rows,'nz':nz,'types':types,'objective':[1]*nz+[0]*(len(bounds)-nz),'live':[d['live_sizes'] for d in domains],'pool':True}

def check(cert,data):
 need(type(cert) is dict and cert['case']==data['case'],'certificate case')
 n=len(data['bounds']);scale=cert['scale'];need(type(scale) is int and scale>0,'scale')
 need(cert['columns']==n and cert['upper_rows']==len(data['upper']) and cert['equal_rows']==len(data['equal']),'dimensions')
 lhs=[0]*n;rhs=0
 for kind in ('upper','equal'):
  used=set()
  for rec in cert[kind]:
   need(type(rec) is list and len(rec)==2,'record')
   i,w=rec;need(type(i) is int and 0<=i<len(data[kind]) and i not in used,'index')
   need(type(w) is int and w!=0 and (kind!='upper' or w>0),'weight')
   used.add(i);_,co,b=data[kind][i];rhs+=w*b
   for j,v in co.items():lhs[j]+=w*v
 if cert['mode']=='upper':
  res=[scale*c-v for c,v in zip(data['objective'],lhs)]
  box=sum(max(v*l,v*u) for v,(l,u) in zip(res,data['bounds']));value=rhs+box;need(value<51*scale,'bound is not below 51')
 elif cert['mode']=='infeasible':
  box=sum(min(v*l,v*u) for v,(l,u) in zip(lhs,data['bounds']));value=rhs-box;need(value<0,'nonnegative gap')
 else:raise ValueError('mode')
 need(all(type(cert[k]) is int and cert[k]==v for k,v in [('value',value),('rhs',rhs),('box',box)]),'arithmetic')
 return dict(case=data['case'],status='PASS',value=value,scale=scale,mode=cert['mode'],columns=n)
