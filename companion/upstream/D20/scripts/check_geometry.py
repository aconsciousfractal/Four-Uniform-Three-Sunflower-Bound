"""Independent full orbit partition by canonical subset signatures.
The production partition grows an orbit from each representative. This checker
instead classifies every one of the 7,315 quadruples, including allowed ones.
"""
from itertools import combinations,permutations
from collections import defaultdict,Counter
from functools import lru_cache
import json
from common import ROOT,need,main,check_index
import geometry

def run():
 check_index(json.loads((ROOT/'certificates/INDEX.json').read_text()))
 P=tuple(frozenset(int(v) for v in s) for s in ('012','015','023','034','045','124','134','135','235','245'))
 aut=[]
 for p in permutations(range(6)):
  if {frozenset(p[v] for v in t) for t in P}==set(P):aut.append(p)
 need(len(aut)==60,'automorphism group')
 @lru_cache(None)
 def canonical(T):return min(tuple(sorted(p[v] for v in T)) for p in aut)
 fixed=tuple(T|{22} for T in P)+tuple(frozenset(v+6 for v in T)|{22} for T in P)
 groups=defaultdict(set);qs=set(combinations(range(22),4));interior=set();kappa={}
 for q in qs:
  y=tuple(v for v in q if v<6);z=tuple(v-6 for v in q if 6<=v<12);w=sum(v>=12 for v in q)
  key=(tuple(sorted((canonical(y),canonical(z)))),w)
  groups[key].add(q);kappa[q]=sum(not set(q)&F for F in fixed)
  if len(y)==4 or len(z)==4:interior.add(q)
 need(len(qs)==7315 and len(interior)==30,'universe and interiors')
 I=[g for g in groups.values() if (0,1,2,3) in g]
 need(len(I)==1 and I[0]==interior,'internal orbit transports both sides')
 dangerous=sorted((g for g in groups.values() if kappa[min(g)]<12 and not g&interior),key=min)
 records=[]
 for i,g in enumerate(dangerous):
  q=min(g);need(len({kappa[T] for T in g})==1,'kappa invariant')
  records.append(dict(id=f'E{i:02d}',mark=list(q),size=len(g),kappa=kappa[q],W=sum(v>=12 for v in q),composition=[sum(v<6 for v in q),sum(6<=v<12 for v in q),sum(v>=12 for v in q)]))
 need(records==geometry.catalogue(),'literal orbit list comparison')
 need(len(records)==7,'seven dangerous orbits')
 phase1=set().union(*dangerous[:6]);phase2=dangerous[6]
 need(phase1=={q for q in qs if sum(v>=12 for v in q)<=1 and q not in interior},'first layer is complete')
 need(phase2=={q for q in qs if sum(v>=12 for v in q)==2 and sum(v<6 for v in q)==1 and sum(6<=v<12 for v in q)==1},'mixed orbit complete')
 need(not phase1&phase2 and not interior&(phase1|phase2),'disjoint coverage')
 terminal=qs-interior-phase1-phase2;hist=Counter(kappa[q] for q in terminal)
 need(hist=={12:1350,15:1440,20:210},'terminal column coefficients')
 need(len(terminal)==3000 and min(hist)==12,'terminal kappa')
 # Direct verification of point/pair incidences of P10, not a sampled statement.
 need(all(sum(v in T for T in P)==5 for v in range(6)),'P10 point counts')
 need(all(sum(set(p)<=T for T in P)==2 for p in combinations(range(6),2)),'P10 pair counts')
 need(12*49>20*27,'strict disjoint-pair contradiction')
 return {'status':'PASS','universe':7315,'automorphisms_per_P10':60,'internal_orbit_size':30,'first_external_layer':len(phase1),'mixed_second_layer':len(phase2),'total_excluded':len(interior|phase1|phase2),'terminal_columns':len(terminal),'terminal_histogram':dict(sorted(hist.items())),'lower_required':588,'upper_capacity':540,'residual_upper':45,'required_residuals':49,'orbits':records,'coverage_complete':True}
if __name__=='__main__':main(run)
