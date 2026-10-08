"""Exact orbit partition for P10+P10 with ten free exterior labels."""
from itertools import combinations,permutations,product
from math import comb
P=tuple(tuple(int(v) for v in s) for s in '012 015 023 034 045 124 134 135 235 245'.split())
Y=frozenset(range(6));Z=frozenset(range(6,12));W=frozenset(range(12,22))
L=tuple(frozenset(t) for t in P)+tuple(frozenset(v+6 for v in t) for t in P)
AUT=tuple(p for p in permutations(range(6)) if {tuple(sorted(p[v] for v in t)) for t in P}==set(P))

def orbit(q):
 q=frozenset(q);a=q&Y;b={v-6 for v in q&Z};w=len(q&W)
 aa={tuple(sorted(p[v] for v in a)) for p in AUT};bb={tuple(sorted(p[v] for v in b)) for p in AUT}
 return {tuple(sorted((*u,*(v+6 for v in z),*e))) for left,right in ((aa,bb),(bb,aa)) for u in left for z in right for e in combinations(W,w)}

def kappa(q):return sum(not set(q)&T for T in L)

def catalogue():
 allq=set(combinations(range(22),4));bad={q for q in allq if kappa(q)<12 and not(set(q)<=Y or set(q)<=Z)}
 out=[]
 while bad:
  mark=min(bad);orb=orbit(mark)
  if not orb<=bad:raise ValueError('orbit not contained')
  kval={kappa(q) for q in orb}
  if len(kval)!=1:raise ValueError('nonconstant kappa')
  out.append(dict(id=f'E{len(out):02d}',mark=list(mark),size=len(orb),kappa=kval.pop(),W=sum(v>=12 for v in mark),composition=[len(set(mark)&Y),len(set(mark)&Z),len(set(mark)&W)]));bad-=orb
 return out
if __name__=='__main__':
 import json
 print(json.dumps(catalogue(),indent=2))
