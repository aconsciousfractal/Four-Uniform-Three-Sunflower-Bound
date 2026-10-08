"""Exact producer. Anchor-row join, then capacities; not imported by checker."""
from itertools import combinations, product
from collections import defaultdict, Counter
from pathlib import Path
import gzip, json, hashlib, argparse, time
ROOT=Path(__file__).resolve().parents[1]
P=tuple(tuple(map(int,t)) for t in '012 015 023 034 045 124 134 135 235 245'.split())
PAIRS=tuple(combinations(range(6),2));PID={p:i for i,p in enumerate(PAIRS)}
TRIPLES=tuple(combinations(range(6),3));OTHER=tuple(t for t in TRIPLES if t not in P)
SUBSETS=tuple(t for k in (1,2,3) for t in combinations(range(6),k))
PP=tuple(tuple(PID[p] for p in combinations(t,2)) for t in P)
CP=tuple(tuple(PID[p] for p in combinations(t,2)) for t in OTHER)
PROFILES={'ALL15':(15,)*6,'ONE14':(14,15,15,15,15,15)}
def require(test,message):
    if not test:raise ValueError(message)

def rows(ds,T):
    out=[]
    for e in (0,1):
        for w in product(range(4),repeat=3):
            inc=(w[0]+w[1],w[0]+w[2],w[1]+w[2])
            s=tuple(ds[v]-5-e-inc[i] for i,v in enumerate(T))
            if not all(0<=a<=8 for a in s):continue
            if any(a==8 and 5+e+inc[i]!=5 for i,a in enumerate(s)):continue
            if 18+e+sum(w)+sum(s)<43:continue
            out.append((e,tuple(a+e for a in w)))
    return out

def margins(ds):
    opts=tuple(rows(ds,T) for T in P)
    def visit(i,m,e):
        if i==len(P):yield tuple(m),tuple(e);return
        for bit,values in opts[i]:
            if any(m[j]!=-1 and m[j]!=v for j,v in zip(PP[i],values)):continue
            new=m.copy()
            for j,v in zip(PP[i],values):new[j]=v
            yield from visit(i+1,new,e+[bit])
    return list(visit(0,[-1]*15,[]))

def projections(ds):
    out=[];mm=margins(ds)
    for m,e in mm:
        cap=list(m)
        for b,inds in zip(e,PP):
            for j in inds:cap[j]-=b
        if min(cap)<0:continue
        def visit(i,chosen):
            if i<len(OTHER):
                inds=CP[i]
                for q in range(min(2,*(cap[j] for j in inds))+1):
                    for j in inds:cap[j]-=q
                    visit(i+1,chosen+[q])
                    for j in inds:cap[j]+=q
            else:
                n=dict(zip(P+OTHER,e+tuple(chosen)));n.update(dict(zip(PAIRS,cap)))
                for y in range(6):
                    n[y,]=ds[y]-5-sum(c for U,c in n.items() if len(U)>1 and y in U)
                    if n[y,]<0:return
                out.append(tuple(n[U] for U in SUBSETS))
        visit(0,[])
    require(len(out)==len(set(out)),'duplicate projection')
    return sorted(out),len(mm)

def label_groups(n):
    tt=[T for T in TRIPLES for _ in range(n[T])];parent=list(range(len(tt)))
    def find(i):
        while parent[i]!=i:i=parent[i]
        return i
    def join(i,j):parent[find(i)]=find(j)
    for i,U in enumerate(tt):
        for j,V in enumerate(tt[:i]):
            if len(set(U)&set(V))==2 and not(U in P and V in P):join(i,j)
    for y in range(6):
        ids=[i for i,T in enumerate(tt) if y in T]
        if n[y,]>=3:
            for i in ids[1:]:join(ids[0],i)
    groups=defaultdict(list)
    for i in range(len(tt)):groups[find(i)].append(i)
    return tt,sorted((tuple(ids) for ids in groups.values()),key=lambda a:a[0])

def costs(n,tt,ids):
    ys={y for i in ids for y in tt[i]}
    pairs={U for U in PAIRS if n[U] and any(set(U)<=set(tt[i]) for i in ids)}
    total=len(ids)+sum(n[y,] for y in ys)+sum(n[U] for U in pairs)
    incident=tuple((n[y,] if y in ys else 0)+sum(y in tt[i] for i in ids)+sum(n[U] for U in pairs if y in U) for y in range(6))
    return total,incident

def refutation(vector):
    n=dict(zip(SUBSETS,vector))
    for y in range(6):
        b=sum(n[U] for U in PAIRS if y in U)
        if b>6:return ['P',y]
    tt,groups=label_groups(n)
    for ids in groups:
        if len({tt[i] for i in ids})<len(ids):return ['S',ids[0]]
    for ids in groups:
        total,incident=costs(n,tt,ids)
        if total>20:return ['D',ids[0]]
    for ids in groups:
        total,incident=costs(n,tt,ids)
        for y,q in enumerate(incident):
            if q>6:return ['C',ids[0],y]
    raise ValueError(('OPEN projection',vector))

def build(outdir):
    outdir.mkdir(parents=True,exist_ok=True);summary={}
    require(not margins((13,15,15,15,15,15)),'ONE13 unexpectedly survived')
    for name,ds in PROFILES.items():
        states,nm=projections(ds);witnesses=[refutation(v) for v in states]
        blob={'schema':'E20_P10_LITERAL_GLUE_V1','profile':list(ds),'label':name,
              'mu':43,'center_degree':18,'outside_degree_cap':20,'pair_codegree_cap':6,
              'triple_codegree_cap':2,'subsets':[list(U) for U in SUBSETS],
              'margin_patterns':nm,'state_count':len(states),
              'domain_sha256':hashlib.sha256(bytes(a for v in states for a in v)).hexdigest(),
              'witnesses':witnesses}
        raw=(json.dumps(blob,separators=(',',':'))+'\n').encode()
        (outdir/(name+'.json.gz')).write_bytes(gzip.compress(raw,mtime=0))
        counts=dict(sorted(Counter(w[0] for w in witnesses).items()))
        summary[name]={'margins':nm,'states':len(states),'reasons':counts,'nonempty_members_range':[min(map(sum,states)),max(map(sum,states))],'open':0}
    return summary
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'certificates');a=ap.parse_args()
    print(json.dumps(build(a.out),indent=2))
