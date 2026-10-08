"""Remove unused finite-universe inequalities and check universal count boxes.
The support itself is not bounded in any of the50 certified cases.
"""
from itertools import combinations

def is_exterior_budget(name):return name=='W-degree' or name.startswith('yW-pairs:') or name.startswith('pairW-triples:')
def normalize(data,problem):
 result=dict(data)
 result['upper']=[row for row in data['upper'] if not is_exterior_budget(row[0])]
 # Count variables are finite even with unbounded exterior support: all traces
 # are nonempty because an explicit pair of prescribed disjoint members
 # forbids the empty trace in each branch of this proof.
 base=tuple(tuple(map(int,t)) for t in '015 023 034 045 124 134 135 235 245'.split())
 cones=tuple(frozenset((22,*T)) for T in base)+tuple(frozenset((22,*(v+6 for v in T))) for T in base)
 if problem['stage']=='interior_pair':
  pair=problem['pair'];fixed=cones+tuple(frozenset(T) for T in pair['interiors_first']+pair['interiors_second'])
 else:fixed=cones+(frozenset(problem['mark']),)
 if not any(not A&B for A,B in combinations(fixed,2)):raise ValueError('no witness excluding the empty trace')
 if data['bounds'][0]!=(0,0):raise ValueError('unbounded exterior-empty trace not excluded')
 for T,(lo,hi) in zip(data['types'],data['bounds'][:data['nz']]):
  if not T:continue
  universal={1:18,2:6,3:2,4:1}[len(T)]
  universal-=sum(set(T)<=C for C in cones)
  if not 0<=lo<=hi or hi not in (0,universal):raise ValueError('count bound tighter than its universal cap')
 return result
