"""Exact labelled coverage for P10 + P9, without exchanging unequal components."""
from itertools import combinations, permutations
P=tuple(tuple(map(int,s)) for s in '012 015 023 034 045 124 134 135 235 245'.split())
P9=P[1:]
Y=frozenset(range(6));Z=frozenset(range(6,12));W=frozenset(range(12,22))
LINK=tuple(frozenset(T) for T in P)+tuple(frozenset(v+6 for v in T) for T in P9)

def automorphisms(C):
    ss=set(C)
    return tuple(p for p in permutations(range(6)) if {tuple(sorted(p[v] for v in T)) for T in C}==ss)
AUT10=automorphisms(P);AUT9=automorphisms(P9)

def orbit(q):
    q=frozenset(q);a=q&Y;b={v-6 for v in q&Z};w=len(q&W)
    aa={tuple(sorted(p[v] for v in a)) for p in AUT10}
    bb={tuple(sorted(p[v] for v in b)) for p in AUT9}
    return {tuple(sorted((*u,*(v+6 for v in z),*e))) for u in aa for z in bb for e in combinations(sorted(W),w)}

def kappa(q):return sum(not set(q)&T for T in LINK)

def catalogue(kind):
    if kind not in ('internal','external'):raise ValueError('catalogue kind')
    allq=set(combinations(range(22),4))
    ints={q for q in allq if set(q)<=Y or set(q)<=Z}
    bad=ints if kind=='internal' else {q for q in allq-ints if len(set(q)&W)<=1}
    out=[]
    while bad:
        mark=min(bad);o=orbit(mark)
        if not o<=bad:raise ValueError('overlap or wrong orbit')
        ks={kappa(q) for q in o}
        if len(ks)!=1:raise ValueError('kappa not invariant')
        out.append(dict(id=('I' if kind=='internal' else 'E')+f'{len(out):02}',mark=list(mark),size=len(o),kappa=ks.pop(),W=len(set(mark)&W)))
        bad-=o
    return out
if __name__=='__main__':
    import json
    print(json.dumps({'automorphism_orders':[len(AUT10),len(AUT9)],'internals':catalogue('internal'),'external':catalogue('external')},indent=2))
