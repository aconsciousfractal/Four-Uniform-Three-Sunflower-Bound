"""Portable construction used for discovery, not trusted by the separate checker."""
from itertools import combinations
import pair_model as p
import marked_model as m

def build_finite_pilot(problem):
 stage=problem['stage']
 if stage=='interior_pair':return p.build(problem['pair'])
 case={'id':problem['id'],'mark':problem['mark']}
 if stage=='mixed_three':
  data=m.build(case,with_anchor=False)
  for j,T in enumerate(data['types']):
   if len(T)==4 and all(v<12 for v in T) and any(v<6 for v in T) and any(v>=6 for v in T):data['bounds'][j]=(0,0)
  return data
 if stage!='mixed_four':raise ValueError('unknown stage')
 data=p.build(dict(id=problem['id'],interiors_first=[],interiors_second=[]))
 mark=tuple(problem['mark']);M=frozenset(mark);j=data['types'].index(mark);data['bounds'][j]=(1,data['bounds'][j][1])
 cones=tuple(frozenset((22,*T)) for T in p.p.P[1:])+tuple(frozenset((22,*(v+6 for v in T))) for T in p.p.P[1:])
 for j,Q in enumerate(map(frozenset,data['types'])):
  if any(F&M==F&Q==M&Q for F in cones):data['bounds'][j]=(0,0)
 data['upper'].append((f'H27-mark:{mark}',{j:1 for j,Q in enumerate(data['types']) if not set(Q)&M},27-sum(not F&M for F in cones)))
 return data

from support_free import normalize
def build(problem):
 return normalize(build_finite_pilot(problem),problem)
