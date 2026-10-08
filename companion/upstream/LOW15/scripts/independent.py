"""Set-based independent reconstruction. No import of the primary model.
Categories are attached in a different order, by vertex subsets and path centres.
The local predicate uses t-before-p and partitions, from the inherited auditor.
"""
from itertools import combinations, permutations
from functools import lru_cache
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import audit43 as A
PAIRS=tuple(combinations(range(4),2))
def degree(r):
    return tuple(r[10+v]+1+sum(r[j] for j,e in enumerate(PAIRS) if v in e)
                 +sum(r[6+j] for j in range(4) if j!=v) for v in range(4))
def relabel_row(r,p):
    counts={frozenset(e):r[i] for i,e in enumerate(PAIRS)}
    counts.update({frozenset(set(range(4))-{i}):r[6+i] for i in range(4)})
    counts.update({frozenset((i,)):r[10+i] for i in range(4)})
    masks=[frozenset(e) for e in PAIRS]+[frozenset(set(range(4))-{i}) for i in range(4)]+[frozenset((i,)) for i in range(4)]
    return tuple(counts[frozenset(p[i] for i in T)] for T in masks)
@lru_cache(None)
def rows():
    return tuple(sorted(tuple(r) for r in A.enumerate_rows(mu=42,r10=7,r9=7,cap=15)
                        if min(degree(r))>=4))
@lru_cache(None)
def oriented():
    seen=set()
    for p in permutations(range(3,-1,-1)):
        for row in rows():seen.add(relabel_row(row,p))
    return tuple(sorted(seen))
def high_anchors():
    groups={}
    for r in rows():
        if sum(r)<=42:continue
        images={relabel_row(r,p) for p in permutations(range(4))};key=min(images)
        if key not in groups:groups[key]=[0,images]
        groups[key][0]+=1
    return [dict(id=i,row=list(r),ordered_count=v[0],orbit=[list(x) for x in sorted(v[1])])
            for i,(r,v) in enumerate(sorted(groups.items()))]
def canonical(F):
    ext=sorted(set().union(*map(set,F))-set(range(4)))
    answers=[]
    for p in permutations(ext):
        rename=dict(zip(ext,p))
        answers.append(tuple(sorted(tuple(sorted(rename.get(v,v) for v in q)) for q in F)))
    return min(answers)
def extensions(n,cat):
    root,m,kind=cat;r=1 if kind=='triple' else 2 if m==1 else 3
    for k in range(r+1):
        for old in combinations(range(4,n),r-k):
            V=tuple(old)+tuple(range(n,n+k))
            if kind=='triple' or m==1:yield (tuple(sorted(root+V)),),n+k
            elif m==3:yield tuple(sorted(tuple(sorted(root+e)) for e in combinations(V,2))),n+k
            else:
                for c in V:
                    yield tuple(sorted(tuple(sorted(root+(c,u))) for u in V if u!=c)),n+k

def census(r):
    big={i for i in range(4) if r[10+i]>=8}
    cats=[(p,r[k],'pair') for k,p in enumerate(PAIRS) if r[k]]+[(tuple(i for i in range(4) if i!=v),1,'triple') for v in range(4) if r[6+v]]
    if not big:raise ValueError('high-anchor domain must contain a large singleton')
    pivot=min(big);cats.sort(key=lambda c:(pivot not in c[0],c[2]!='triple',-c[1],tuple(reversed(c[0]))))
    nodes=[0]*(len(cats)+1);out=[]
    def rec(j,n,F):
        nodes[j]+=1
        if j==len(cats):out.append(F);return
        for extra,nn in extensions(n,cats[j]):
            ff=list(map(frozenset,F+extra))
            if len(set(ff))!=len(ff):continue
            if any(A&B=={v} for v in big for A,B in combinations(ff,2)):continue
            if any(A&B==B&C==C&A for A,B,C in combinations(ff,3)):continue
            rec(j+1,nn,tuple(sorted(F+extra)))
    rec(0,4,((0,1,2,3),))
    return tuple(sorted({canonical(F) for F in out})),nodes,len(out)

def trace_data(core):
    ff=tuple(frozenset(q) for q in core);vertices=sorted(set().union(*ff));base=set(range(4));cand=[];bounds=[]
    for k in range(1,5):
        for tt in combinations(vertices,k):
            T=frozenset(tt)
            if len(T&base)>1:continue
            allowed=True
            for a,b in combinations(ff,2):
                if T&a==T&b==a&b:allowed=False;break
            if not allowed:continue
            cap=(0,15,6,2,1)[k]-sum(T<=q for q in ff)
            if cap>0:cand.append(T);bounds.append(cap)
    return ff,vertices,tuple(cand),tuple(bounds)

def anchor_domain(core,base_row,Q):
    ff,vertices,cand,caps=trace_data(core);Q=list(Q);qs=frozenset(Q)
    feats=[frozenset((Q[a],Q[b])) for a,b in PAIRS]+[qs-{v} for v in Q]+[frozenset((v,)) for v in Q]
    lo=[sum(q&qs==T for q in ff) for T in feats]
    hi=[count+sum(c for U,c in zip(cand,caps) if U&qs==T) for T,count in zip(feats,lo)]
    d0=degree(base_row);live=[]
    for row in oriented():
        dd=degree(row)
        if any(dd[j]!=d0[v] for j,v in enumerate(Q) if v in range(4)):continue
        if any(dd[j]<sum(v in q for q in ff) for j,v in enumerate(Q)):continue
        if all(lo[j]<=row[j]<=hi[j] for j in range(14)):live.append(row)
    return tuple(feats),tuple(lo),tuple(hi),tuple(live)

def build(core,row):
    core=[list(q) for q in core];ff,vertices,cand,cap=trace_data(core)
    bounds=[(0,c) for c in cap];names=[['trace',sorted(U)] for U in cand];eq=[];up=[];sizes=[]
    for Q in core:
        feats,lo,hi,poss=anchor_domain(core,row,Q);qs=frozenset(Q);offset=len(bounds)
        sizes.append(len(poss));bounds.extend((0,1) for _ in poss)
        names.extend(['row',Q,list(p)] for p in poss)
        eq.append((f'choose:{Q}',dict.fromkeys(range(offset,offset+len(poss)),1),1))
        for j,T in enumerate(feats):
            terms={v:1 for v,U in enumerate(cand) if U&qs==T}
            for i,p in enumerate(poss):
                if p[j]:terms[offset+i]=-p[j]
            eq.append((f'trace:{Q}:{sum(1<<v for v in T)}',terms,-lo[j]))
    for k in range(1,4):
        for tt in combinations(vertices,k):
            T=frozenset(tt);co={v:1 for v,U in enumerate(cand) if T<=U}
            if co:up.append((f'cap:{tt}',co,(0,15,6,2)[k]-sum(T<=q for q in ff)))
    return dict(core=core,given=list(degree(row)),cand=[sum(1<<v for v in U) for U in cand],
                bounds=bounds,equal=eq,upper=up,varnames=names,live_sizes=sizes)
