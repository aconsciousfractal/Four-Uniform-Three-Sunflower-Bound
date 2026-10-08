"""Exact terminal certificate and small exhaustive tests of the ordinary lemmas."""
from common import *
from itertools import combinations
from collections import Counter
import copy
P=tuple(tuple(map(int,t)) for t in '012 015 023 034 045 124 134 135 235 245'.split())
M=P[1:];Y=frozenset(range(6));Z=frozenset(range(6,12));W=frozenset(range(12,22));S=Y|Z
CONES=tuple(frozenset((22,*T)) for T in M)+tuple(frozenset((22,*(v+6 for v in T))) for T in M)
def sf(a,b,c):return a&b==a&c==b&c

def terminal():
 cases={'internal':[],'mixed_four':[],'mixed_three':[],'mixed_two':[],'terminal':[]}
 for Q in combinations(range(22),4):
  q=frozenset(Q);A=q&Y;B=q&Z;s=len(A)+len(B)
  if s==4:kind='mixed_four' if A and B else 'internal'
  elif s==3 and A and B:kind='mixed_three'
  elif s==2 and A and B:kind='mixed_two'
  else:kind='terminal'
  cases[kind].append(Q)
 need({k:len(v) for k,v in cases.items()}=={'internal':30,'mixed_four':465,'mixed_three':1800,'mixed_two':1620,'terminal':3400},'partition')
 return cases

def verify_terminal(cert):
 need(cert['schema']=='E20_F69_R99_TERMINAL_V1','terminal schema')
 need(cert['cone_weights']==[1]*18,'all18 H27 constraints')
 special=[];transcounts=[];extrapairs=[]
 for shift in (0,6):
  m=tuple(frozenset(v+shift for v in t) for t in M);U=frozenset(range(shift,shift+6))
  ts={frozenset(T) for T in combinations(sorted(U),3) if all(set(T)&B for B in m)}
  extra=ts-set(m);need(len(ts)==11 and len(extra)==2,'11 transversal triples')
  A,B=sorted(extra,key=lambda t:tuple(sorted(t)));need(not A&B and A|B==U,'complementary exceptions')
  extrapairs.append([sorted(A),sorted(B)])
  special.extend(sorted(t) for t in m);transcounts.append(len(ts))
 need(cert['prescribed_triple_rows']==special and cert['exception_pairs']==extrapairs,'terminal rows')
 need(cert['per_prescribed_rhs']==1 and cert['per_exception_pair_rhs']==2,'triple capacities')
 T=terminal();hist=Counter();minimum=100
 for Q in T['terminal']:
  q=set(Q);k=sum(not q&C for C in CONES);hist[k]+=1
  coefficient=k+sum(set(t)<=q for t in special)+sum(any(set(t)<=q for t in pair) for pair in extrapairs)
  minimum=min(minimum,coefficient);need(coefficient>=10,'terminal column')
 rhs=18*27+len(special)+2*len(extrapairs)
 need(cert['rhs']==rhs==508 and cert['minimum_column']==minimum==10,'terminal arithmetic')
 need(cert['residual_target']==51 and cert['deficit_cap']==22,'correct target/deficit')
 need(10*51>rhs,'strict contradiction')
 return {'partition':{k:len(v) for k,v in T.items()},'kappa_histogram':dict(sorted(hist.items())),'terminal_rhs':rhs,'required_lhs':510,'deficit_bound':22,'disjoint_lower':488,'disjoint_upper':486,'transversal_counts':transcounts}

def cover_test():
 traces=[]
 for k in range(4):
  for U in combinations(range(12),k):
   if k==3 and not(set(U)<=Y or set(U)<=Z):continue
   for h in range(3):
    if k+h>4:continue
    for H in combinations((12,13),h):traces.append(frozenset(U+H+tuple(range(14,14+4-k-h))))
 need(len(traces)==436 and len(set(traces))==436,'canonical trace space')
 tested=sun=exceptions=0
 for y in Y:
  for z in Z:
   mark=frozenset((y,z,12,13))
   exceptions_allowed=[]
   for v,comp in ((y,Y),(z,Z)):
    edges=[C-{22,v} for C in CONES if v in C]
    covers=[frozenset(T) for T in combinations(sorted(comp-{v}),2) if all(set(T)&e for e in edges)]
    need(len(covers)<=1,'at most one P5 cover')
    exceptions_allowed.extend(c|{v} for c in covers)
   for Q in traces:
    tested+=1
    if {y,z}<=Q or Q&{12,13}:continue
    if any(sf(C,mark,Q) for C in CONES):sun+=1
    else:
     need(Q&S in exceptions_allowed and len(Q&S)==3,'unclassified cover exception');exceptions+=1
 need(tested==15696 and exceptions==36,'full coverage includingP5')
 return {'traces':tested,'sunflower_obstructions':sun,'P5_exceptions':exceptions,'residual_upper_if_mixed':2*18+4+2*2}

def complement_test():
 U=frozenset((0,1,2));V=frozenset((3,4,5));X=(12,13,14,15);D=CONES[9]
 families=[frozenset(A) for k in range(3) for A in combinations(X,k)];tested=violations=0
 for A in families:
  for B in families:
   tested+=1
   if len(A)+len(B)<=2:continue
   witnesses=[(U|{a},V|{b},D) for a in A for b in B if a!=b]
   need(witnesses and any(sf(*w) for w in witnesses),'complementary capacities');violations+=1
 return {'extension_patterns':tested,'overloads_refuted':violations}

def family_check(F):
 F=tuple(frozenset(Q) for Q in F);need(all(len(Q)==4 for Q in F) and len(set(F))==len(F),'simple4-family')
 count=0
 for A,B,C in combinations(F,3):need(not sf(A,B,C),'positive family has sunflower');count+=1
 return {'members':len(F),'support':len(set().union(*F)),'ternas':count}

def positives():
 tests=[]
 for A,B in [((12,),(12,)),((12,13),()),((),(12,13))]:
  F=CONES+tuple(frozenset((0,1,2,a)) for a in A)+tuple(frozenset((3,4,5,b)) for b in B)
  tests.append(family_check(F))
 # Both P5 exceptions can occur for one marked P5 point: the +2 term is not discarded.
 F=CONES+(frozenset((0,6,12,13)),frozenset((6,9,11,14)),frozenset((6,9,11,15)))
 tests.append(family_check(F))
 # Omitting an entire component-pool cap would not be justified; the input H27 stays explicit.
 D=[]
 for h in (0,9):
  groups=[tuple(range(h+3*i,h+3*i+3)) for i in range(3)]
  for A,B in combinations(groups,2):
   for a in combinations(A,2):
    for b in combinations(B,2):D.append(a+b)
 low=family_check(D);need(low['members']==54 and low['ternas']==24804,'54 witness')
 marked=[]
 for case in load('data/CASES.json'):
  prob=case['problem']
  if prob['stage']=='interior_pair':
   extra=prob['pair']['interiors_first']+prob['pair']['interiors_second']
  else:extra=[prob['mark']]
  marked.append(family_check(CONES+tuple(frozenset(Q) for Q in extra)))
 return {'sharp_complement_and_P5_families':tests,'marked_cores':len(marked),'marked_core_ternas':sum(x['ternas'] for x in marked),'lower54':low}

def run():
 c=load('data/TERMINAL.json');t=verify_terminal(c);mut=0
 for key,value in [('rhs',510),('residual_target',52),('per_exception_pair_rhs',1),('deficit_cap',18)]:
  m=copy.deepcopy(c);m[key]=value;rejected(lambda m=m:verify_terminal(m));mut+=1
 emit({'status':'PASS','terminal':t,'cover':cover_test(),'complement':complement_test(),'positive':positives(),'mutations_rejected':mut})
if __name__=='__main__':run()
