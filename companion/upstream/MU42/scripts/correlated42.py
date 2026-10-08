"""Necessary external-family lower bounds, kept jointly across central anchors.
Exact finite implementation. Exact integer decisions; no outside-support cutoff.
"""
from itertools import combinations, product
from functools import lru_cache
import component42 as base

LEVELS=tuple(h for h in product((0,6,9,10),repeat=6)
             if sum(h) <= (20 if 10 in h else 22 if 9 in h else 1000000))
@lru_cache(None)
def compatible_H(A,lower):
    return sum(1<<i for i,h in enumerate(LEVELS) if all(v<=h[y] for y,v in zip(A,lower)))

@lru_cache(None)
def central(m,k,r10,r9):
    M=base.P if m==10 else base.P[1:]
    return base.base_rows(M,k,42,r10,r9)

def relations(m,k,r10,r9,mask):
    M=base.P if m==10 else base.P[1:]
    C=tuple(q for j,q in enumerate(base.QUADS) if mask>>j&1)
    F=tuple(T|{6} for T in M)+C
    links={y:tuple(sorted(tuple(sorted(Q-{y})) for Q in F if y in Q)) for y in range(6)}
    clean={y:all(set(u)&set(v) for u,v in combinations(links[y],2)) for y in range(6)}
    escape={y:base.escape_capacity(links[y]) if clean[y] else 0 for y in range(6)}
    ideg=[sum(y in Q for Q in C) for y in range(6)]
    fdeg=[sum(y in T for T in M) for y in range(6)]
    out=[]
    for A,raw in central(m,k,r10,r9):
        aset=frozenset(A)
        internal_s=tuple(sum(Q&aset=={v} for Q in C) for v in A)
        internal_w=tuple(sum(Q&aset==set(p) for Q in C) for p in combinations(A,2))
        internal_e=sum(aset<=Q for Q in C)
        rel={}
        for d,s,ks,w,e in raw:
            if e<internal_e or any(x<y for x,y in zip(w,internal_w)) or any(x<y for x,y in zip(s,internal_s)):continue
            low=[];okay=True
            for i,y in enumerate(A):
                if d[i]<len(links[y]) or (fdeg[y]==5 and d[i]-ideg[y]>15):okay=False;break
                if s[i]>=8 or d[i]>=17:
                    if not clean[y]:okay=False;break
                    mx=len(links[y])+(escape[y] if ks[i]<8 else 0)
                    if not len(links[y])<=ks[i]<=mx:okay=False;break
                elif ks[i]<sum(bool(set(T)&(aset-{y})) for T in links[y]):okay=False;break
                low.append({8:6,9:9,10:10}.get(s[i],0))
            if okay:rel.setdefault(d,set()).add(tuple(low))
        out.append((A,{d:tuple(sorted(ls)) for d,ls in rel.items()}))
    return out

def refine(prior):
    m,k,r10,r9=(prior[j] for j in ('central_size','outside_cap','r10','r9'))
    results=[];positive=[]
    for item in prior['survivors']:
        mask=item['internal_mask'];rels=relations(m,k,r10,r9,mask)
        # A distinct mask of all joint H lower vectors for each local degree triple.
        maps=[]
        for A,rel in rels:
            mapping={}
            for d,ls in rel.items():
                bit=0
                for lower in ls:bit |= compatible_H(A,lower)
                mapping[d]=bit
            maps.append((A,mapping))
        for record in item['colorings']:
            d=tuple(record['degrees']);allowed=(1<<len(LEVELS))-1
            for A,mp in maps:allowed &= mp.get(tuple(d[v] for v in A),0)
            entry={'internal_mask':mask,'degrees':list(d),'H_bits':hex(allowed),'H_count':allowed.bit_count()}
            results.append(entry)
            if allowed:positive.append(entry)
    return {'mu':42,'central_size':m,'outside_cap':k,'r10':r10,'r9':r9,'lower_levels':[0,6,9,10],
            'budget_vectors':len(LEVELS),'input_states':len(results),'open_states':len(positive),
            'states':results,'open':positive}
