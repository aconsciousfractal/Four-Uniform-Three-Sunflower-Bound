"""Exact small geometry behind pooling, slot capacity and positive controls."""
from itertools import combinations,product
from collections import Counter
import json
import audit_projection as A
from verify_component import Check,PAIRS,TRIPLES
from common import ROOT,need,load,emit

def sunflower(a,b,c):return a&b==a&c==b&c

def family_test(F):
 F=list(map(frozenset,F));need(len(F)==len(set(F)) and all(len(q)==4 for q in F),'simple quadruples')
 count=0
 for a,b,c in combinations(F,3):need(not sunflower(a,b,c),'positive control sunflower');count+=1
 return count

def lower54():
 def one(off):
  G=[tuple(range(off+3*i,off+3*i+3)) for i in range(3)]
  return [(*a,*b) for i,j in combinations(range(3),2) for a in combinations(G[i],2) for b in combinations(G[j],2)]
 F=one(0)+one(9);need(len(F)==54,'54');return family_test(F)

def main():
 P=tuple(map(frozenset,A.P));Q=tuple(frozenset((h,*p)) for h in(0,1) for p in combinations((2,3,4),2))+(frozenset((0,1,5)),frozenset((0,1,6)))
 records=[]
 for omit in combinations(range(10),2):
  M=tuple(t for i,t in enumerate(P) if i not in omit);S=set().union(*M)
  c1=[x for x in S if all(x in t for t in M)];c2=[p for p in combinations(sorted(S),2) if all(set(p)&t for t in M)];c3=[p for p in combinations(sorted(S),3) if all(set(p)&t for t in M)]
  need(not c1 and len(c3)==12 and len(c2)<=1,'P8 covers')
  records.append([list(omit),len(c2),len(c3),2*len(c3)+12*len(c2)])
 S=set().union(*Q);c2=[p for p in combinations(sorted(S),2) if all(set(p)&t for t in Q)];c3=[p for p in combinations(sorted(S),3) if all(set(p)&t for t in Q)]
 need(c2==[(0,1)] and len(c3)==11 and not any(all(x in t for t in Q) for x in S),'Q8 covers')
 for m,target in ((9,11),(10,10)):
  M=list(map(set,A.blocks(m)));covers=[t for t in combinations(range(6),3) if all(set(t)&b for b in M)];need(len(covers)==target,'P9/P10 triple covers')
  need(not any(all(set(p)&b for b in M) for p in combinations(range(6),2)),'no two-cover')
 # Pair+singleton affine inequality follows from the proved table plus h<=10.
 hbound=(10,10,8,5,4,2,1)
 need(all(5*h+9*b<=59 for b,h in enumerate(hbound)),'affine consequence')
 # Literal witnesses establishing that the six pure singleton categories form an intersecting family.
 witnesses=0
 for m in(9,10):
  M=list(map(set,A.blocks(m)))
  for y,z in combinations(range(6),2):
   T=next((T for T in M if not(T&{y,z})),None);need(T is not None,'pair avoidance')
   need(sunflower(frozenset(T|{6}),frozenset((y,7,8,9)),frozenset((z,10,11,12))),'literal empty-core witness');witnesses+=1
 # New slot obstruction is checked on one exact old-admissible projection only.
 e=load('controls/R99_TWO_SLOT.json');v=e['vector'];ns=v[:6];np=v[6:21];nt=v[21:];case=dict(id='P9_000',component=9,outside=9,r10=7,r9=7,interiors=[]);C=Check(case)
 ds=tuple(C.fix[y]+sum(n for n,U in zip(v,A.TYPES) if y in U) for y in range(6));need(list(ds)==e['degree_profile'],'projection degrees')
 marg=[sum(nt[k] for k,T in enumerate(TRIPLES) if set(p)<=set(T))+np[j] for j,p in enumerate(PAIRS)]
 for T,raw in zip(C.M,C.model['anchor_rows']):
  expected=(tuple(ds[y] for y in T),tuple(marg[PAIRS.index(p)] for p in combinations(T,2)),nt[TRIPLES.index(T)])
  allowed={(tuple(A.deg(r,i) for i in(1,2,3)),tuple(r[3+j]+r[6] for j in range(3)),r[6]) for r in raw}
  need(expected in allowed,'old exact projection fits each anchor')
 need(all(not C.cut(k,ns,np,nt) for k in range(2,7)),'old forcing rules must not reject the example')
 pair=PAIRS.index(tuple(e['pair']));U=[TRIPLES.index(tuple(t)) for t in e['extensions']];need(np[pair]==1 and all(nt[u]>=1 and pair in C.PF[u] for u in U),'three forced extension occurrences')
 merge=[]
 for u,w in combinations(U,2):
  h=set(C.SF[u])|set(C.SF[w]);p=set(C.PF[u])|set(C.PF[w]);d=2+sum(ns[y] for y in h)+sum(np[j] for j in p);merge.append(d);need(d>18,'extensions must be distinct')
 need(merge==e['merged_degree_bounds'],'exact 19/20/21')
 # A single external pair cannot contain the three distinct extension points.
 need(not any({7,8,9}<=set(p) for p in combinations(range(7,11),2)),'two-slot capacity')
 # Actual families: two singleton categories may coexist; no global candidate is asserted.
 H=[{v+10 for v in t} for t in P[2:]];positive=[]
 for m in(9,10):
  F=[{6,*t} for t in A.blocks(m)]+[{y,*t} for y in(0,1) for t in H]
  c=family_test(F);pure=[set(q) for q in F if 6 not in q];need(len(pure)==16 and all(a&b for a,b in combinations(pure,2)),'intersecting pooled positive control');positive.append({'members':len(F),'triples_tested':c,'pooled_members':16})
 count54=lower54()
 emit({'status':'PASS','P8_models_checked':45,'Q8_triple_covers':len(c3),'I8_pooling_uniform_cap':36,'P10_all13_required_singletons':48,'affine_pair_bound':'5h+9b<=59','literal_pooling_witnesses':witnesses,'R99_example_nonempty_traces':sum(v),'R99_example_merge_degrees':merge,'R99_example_status':'EXCLUDED_ONLY_THIS_PROJECTION','positive_families':positive,'lower54_triples':count54,'P8_cover_records':records})
if __name__=='__main__':main()
