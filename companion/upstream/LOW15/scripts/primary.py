"""Exact primary census of high-anchor cores and the necessary trace systems.
No cutoff; only standard-library arithmetic. The core support is not bounded
in advance: fresh labels are introduced at every category attachment.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from functools import lru_cache
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent / 'inputs'))
import local43 as L
PAIRS = tuple(combinations(range(4), 2))
PERMS = tuple(permutations(range(4)))

def degree(r):
    return tuple(1+r[10+i]+sum(r[j] for j,p in enumerate(PAIRS) if i in p)
                 +sum(r[6:10])-r[6+i] for i in range(4))

def relabel_row(r,p):
    return (tuple(r[PAIRS.index(tuple(sorted((p[i],p[j]))))] for i,j in PAIRS)
            +tuple(r[6+p[i]] for i in range(4))+tuple(r[10+p[i]] for i in range(4)))

@lru_cache(None)
def rows():
    return tuple(sorted(tuple(r) for r in L.enumerate_rows(mu=42,r10=7,r9=7,cap_degree=15)
                        if min(degree(r)) >= 4))

@lru_cache(None)
def oriented():
    return tuple(sorted({relabel_row(r,p) for r in rows() for p in PERMS}))

def high_anchors():
    groups={}
    for r in rows():
        if 1+sum(r)<44: continue
        c=min(relabel_row(r,p) for p in PERMS)
        groups.setdefault(c,[]).append(r)
    return [dict(id=i,row=list(r),ordered_count=len(rr),
                 orbit=[list(s) for s in sorted({relabel_row(r,p) for p in PERMS})])
            for i,(r,rr) in enumerate(sorted(groups.items()))]

def mask(vs): return sum(1<<v for v in vs)
def sf(A,B,C): return A&B==A&C==B&C

def canonical(core):
    n=max(max(q) for q in core)+1
    return min(tuple(sorted(tuple(sorted(v if v<4 else 4+p[v-4] for v in q)) for q in core))
               for p in permutations(range(n-4)))

def category_extensions(n,m,edges,root):
    seen=set()
    for fresh in range(m+1):
        new=set(range(n,n+fresh))
        for f in permutations(range(n+fresh),m):
            if not new<=set(f): continue
            if [x for x in f if x>=n]!=sorted(x for x in f if x>=n): continue
            blocks=tuple(sorted(tuple(sorted(root|{4+f[v] for v in e})) for e in edges))
            if blocks in seen: continue
            seen.add(blocks)
            yield tuple(map(frozenset,blocks)),n+fresh

def census(row):
    big={i for i,s in enumerate(row[10:]) if s>=8}
    R=frozenset(range(4)); cats=[]
    for j,p in enumerate(row[:6]):
        if not p:continue
        edges={1:((0,1),),2:((0,1),(0,2)),3:((0,1),(0,2),(1,2))}[p]
        cats.append((2 if p==1 else 3,edges,frozenset(PAIRS[j]),('pair',j)))
    for j,t in enumerate(row[6:10]):
        if t:cats.append((1,((0,),),R-{j},('triple',j)))
    cats.sort(key=lambda c:(-len(c[1]),-len(c[2]&big),-len(c[2]),c[3]))
    nodes=[0]*(len(cats)+1); complete=[]
    def visit(k,n,F):
        nodes[k]+=1
        if k==len(cats):
            complete.append(tuple(sorted(tuple(sorted(A)) for A in F)));return
        m,e,root,_=cats[k]
        for extra,nn in category_extensions(n,m,e,root):
            ff=list(F)
            for A in extra:
                if A in ff:break
                if any(len(A&B)==1 and (A&B)<=big for B in ff):break
                if any(sf(A,B,C) for B,C in combinations(ff,2)):break
                ff.append(A)
            else:visit(k+1,nn,tuple(ff))
    visit(0,0,(R,))
    return tuple(sorted({canonical(c) for c in complete})),nodes,len(complete)

def trace_data(core):
    core=tuple(tuple(q) for q in core)
    F=tuple(mask(q) for q in core); n=max(max(q) for q in core)+1
    pairs=tuple((a,b,a&b) for a,b in combinations(F,2)); cand=[]; caps=[]
    for k in (1,2,3,4):
        for T in combinations(range(n),k):
            u=mask(T)
            if (u&15).bit_count()>=2:continue
            if any(a&u==c and b&u==c for a,b,c in pairs):continue
            cap={1:15,2:6,3:2,4:1}[k]-sum(f&u==u for f in F)
            if cap>0:cand.append(u);caps.append(cap)
    return F,n,tuple(cand),tuple(caps)

def anchor_domain(core,row,Q):
    F,n,cand,caps=trace_data(core);Q=tuple(Q);qm=mask(Q)
    features=(tuple(mask((Q[i],Q[j])) for i,j in PAIRS)
              +tuple(qm^(1<<v) for v in Q)+tuple(1<<v for v in Q))
    lows=tuple(sum(f&qm==T for f in F) for T in features)
    ups=tuple(lo+sum(c for U,c in zip(cand,caps) if U&qm==T) for T,lo in zip(features,lows))
    given=degree(row); fixeddeg={v:sum(v in q for q in core) for v in Q};live=[]
    for r in oriented():
        d=degree(r)
        if any(d[i]!=given[v] for i,v in enumerate(Q) if v<4):continue
        if any(d[i]<fixeddeg[v] for i,v in enumerate(Q)):continue
        if any(v<lo or v>hi for v,lo,hi in zip(r,lows,ups)):continue
        live.append(r)
    return features,lows,ups,tuple(live)

def build(core,row):
    core=[list(q) for q in core];F,n,cand,caps=trace_data(core)
    bounds=[(0,c) for c in caps]; eq=[];up=[]
    names=[['trace',[v for v in range(n) if U>>v&1]] for U in cand];sizes=[]
    for Q in core:
        features,lows,ups,live=anchor_domain(core,row,Q);qm=mask(Q);at=len(bounds)
        bounds.extend([(0,1)]*len(live));names.extend([['row',Q,list(r)] for r in live]);sizes.append(len(live))
        eq.append((f'choose:{Q}',{at+j:1 for j in range(len(live))},1))
        for i,T in enumerate(features):
            co={j:1 for j,U in enumerate(cand) if U&qm==T}
            co.update({at+j:-r[i] for j,r in enumerate(live) if r[i]})
            eq.append((f'trace:{Q}:{T}',co,-lows[i]))
    for k in (1,2,3):
        for T in combinations(range(n),k):
            tm=mask(T);co={j:1 for j,U in enumerate(cand) if U&tm==tm}
            rhs={1:15,2:6,3:2}[k]-sum(f&tm==tm for f in F)
            if co:up.append((f'cap:{T}',co,rhs))
    return dict(core=core,given=list(degree(row)),cand=list(cand),bounds=bounds,
                equal=eq,upper=up,varnames=names,live_sizes=sizes)
