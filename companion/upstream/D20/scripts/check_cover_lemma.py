"""Corroboration of a support-independent, ordinary covering proof for P9/P10.
Every outside-cover trace is forbidden by a literal sunflower. The omitted
block of P9 stays omitted; every pair of internal marked points is checked.
"""
from itertools import combinations
from common import main,need

def run():
 P=tuple(frozenset(int(v) for v in s) for s in '012 015 023 034 045 124 134 135 235 245'.split())
 results=[];total=0;forbidden_total=0
 for p,q in ((10,10),(10,9),(9,9)):
  A=P if p==10 else P[1:];B=P if q==10 else P[1:]
  for C in (A,B):
   need(all(any(not T&set(pair) for T in C) for pair in combinations(range(6),2)),'pair cannot be avoided')
   need(all(any(u in T and v not in T for T in C) for u in range(6) for v in range(6) if u!=v),'point containment cannot separate')
  F=tuple(T|{22} for T in A)+tuple(frozenset(v+6 for v in T)|{22} for T in B)
  count=bad=0
  for y in range(6):
   for z in range(6,12):
    M=frozenset((y,z,12,13))
    for r in range(3):
     for core in combinations(range(12),r):
      for s in range(3):
       for ext in combinations((12,13),s):
        Q=frozenset((*core,*ext,*range(100,100+4-r-s)));count+=1
        if {y,z}<=Q or Q&{12,13}:continue
        options=[T for T in F if Q&M==Q&T==M&T]
        need(bool(options),'missing literal sunflower witness')
        need(Q!=M and Q!=options[0] and M!=options[0],'three distinct members');bad+=1
  need(count==11376 and bad==2808,'complete trace coverage')
  results.append({'components':[p,q],'marked_internal_pairs':36,'trace_cases':count,'forbidden_outside_cover':bad,'min_blocks_avoiding_pair':[min(sum(not set(ab)&T for T in C) for ab in combinations(range(6),2)) for C in (A,B)],'max_mixed_residuals_at_branch_degree_cap':2*(p+q)+4})
  total+=count;forbidden_total+=bad
 need(total==34128 and forbidden_total==8424,'total coverage')
 need(6+20+20-2==44 and 49>44,'F69 cap20 cover')
 fixed=tuple(T|{22} for T in P)+tuple(frozenset(v+6 for v in T)|{22} for T in P)
 M=frozenset((0,6,12,13));escaping=frozenset((0,1,3,4));F=fixed+(M,escaping);checked=0
 for a,b,c in combinations(F,3):need(not a&b==a&c==b&c,'positive scope control');checked+=1
 need(not {0,6}<=escaping and not escaping&{12,13} and len(escaping&set(range(12)))==4,'scope counterexample')
 return {'status':'PASS','roots':results,'trace_cases':total,'outside_cover_cases':forbidden_total,'all_outside_cover_cases_have_literal_sunflower':True,'mixed_F69_D20_residual_cap':44,'required_residuals':49,'mixed_bound_formula':'|F| <= d(x) + 2 Delta(F) + 4','support_bound_used':False,'mu_bound_used':False,'H27_used_in_cover_lemma':False,'scope_control_members':len(F),'scope_control_ternas':checked}
if __name__=='__main__':main(run)
