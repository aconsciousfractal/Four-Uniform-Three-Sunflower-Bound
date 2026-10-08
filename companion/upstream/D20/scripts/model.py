"""Necessary F69/P10+P10 anchor model. Exact integer coefficients.
Discovery constructor, not by itself a proof of its mathematical premises.
All variables/rows have deterministic order. No finite-family solution is
asserted by feasibility of this relaxation.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter, defaultdict
from functools import lru_cache
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'sources'))
import local43 as L
P=tuple(tuple(sorted(t)) for t in L.P)
LINK=P+tuple(tuple(v+6 for v in t) for t in P)
PAIRS=tuple(combinations(range(4),2))

def need(ok,msg):
    if not ok: raise ValueError(msg)
def mask(q): return sum(1<<v for v in q)
def sf(a,b,c): return a&b==a&c==b&c

def deg(r):
    return tuple(1+r[10+i]+sum(r[j] for j in L.INC[i])+sum(r[6:10])-r[6+i] for i in range(4))

def good(p,t,s,k):
    ds=tuple(sv+kv for sv,kv in zip(s,k))
    return (min(ds)>=4 and max(ds)<=20 and sum(ds)>=52
        and all(ds[i]+ds[j]>=20 for i,j in PAIRS)
        and sum(d>=19 for d in ds)<=2
        and 1+sum(p)+sum(t)+sum(s)>=42
        and sum(p)+sum(t)<=(12,14,17,19,22)[sum(v<8 for v in s)]
        and L.equality_consistent(p,t,s,k))

@lru_cache(None)
def central_rows(A,empty):
    A=tuple(A); aa=frozenset(A); LL=tuple(map(frozenset,LINK))
    alpha=tuple(sum(T&aa=={v} for T in LL) for v in A)
    tau=tuple(sum(T&aa==aa-{v} for T in LL) for v in A)
    s0=sum(not T&aa for T in LL); out=[]
    for tail in product(range(4),repeat=3):
        p=alpha+tail
        for e in (0,1):
            t=(e,*tau);k=tuple(1+sum(p[j] for j in L.INC[i])+sum(t)-t[i] for i in range(4))
            if s0 not in L.local_s_candidates(0,p,t,17,7,7):continue
            cap=15 if empty else 20
            opts=[tuple(s for s in L.local_s_candidates(i,p,t,17,7,7)
                if 4<=s+k[i]<=cap and (not empty or s<8 or k[i]==5)) for i in (1,2,3)]
            for v in product(*opts):
                s=(s0,*v)
                if good(p,t,s,k):out.append(p+t+s)
    return tuple(sorted(set(out)))

def general_rows(order,limits,empty):
    out=[]
    for p in product(*(range(limits[i][0],min(3,limits[i][1])+1) for i in range(6))):
        for t in product(*(range(limits[6+i][0],min(1,limits[6+i][1])+1) for i in range(4))):
            k=tuple(1+sum(p[j] for j in L.INC[i])+sum(t)-t[i] for i in range(4))
            opts=[]
            for i,v in enumerate(order):
                cap=15 if empty and v<12 else 20
                lo,hi=limits[10+i]
                opts.append(tuple(s for s in L.local_s_candidates(i,p,t,17,7,7) if lo<=s<=hi and 4<=s+k[i]<=cap))
            if any(not o for o in opts) or 1+sum(p)+sum(t)+sum(o[-1] for o in opts)<42:continue
            for s in product(*opts):
                if good(p,t,s,k):out.append(p+t+s)
    return tuple(sorted(set(out)))


def build(case):
    need(set(case)=={'id','mark','empty','marked','min_w','objective'},'case fields')
    need(type(case['id']) is str and type(case['empty']) is bool and type(case['marked']) is bool,'types')
    need(case['min_w'] in (0,2) and (case['min_w']==0 or case['empty']),'min_w premise')
    need(case['objective'] in ('cardinality','deficit'),'objective')
    x=22;quads=tuple(combinations(range(x),4));qm=tuple(map(mask,quads));nz=len(quads)
    fixed=tuple(mask((x,*t)) for t in LINK); mark=case['mark']
    need(mark is None or type(mark) is list and tuple(mark) in quads,'mark')
    need(not case['marked'] or mark is not None,'marked anchor exists')
    ones=set() if mark is None else {quads.index(tuple(mark))}
    selected=fixed+tuple(qm[j] for j in sorted(ones)); zero=set()
    for a,b in combinations(selected,2):
        c=a&b
        zero.update(j for j,q in enumerate(qm) if q&a==c and q&b==c)
    if case['empty']:zero.update(j for j,q in enumerate(quads) if q[-1]<6 or q[0]>=6 and q[-1]<12)
    if case['min_w']:zero.update(j for j,q in enumerate(quads) if sum(v>=12 for v in q)<case['min_w'])
    need(not ones&zero,'literal forbidden mark')
    bd=[(1,1) if j in ones else (0,0) if j in zero else (0,1) for j in range(nz)]
    up=[];eq=[];sub=defaultdict(list)
    def row(dest,name,t,rhs):dest.append((name,{int(j):int(v) for j,v in t.items() if v},int(rhs)))
    for j,q in enumerate(quads):
        for size in (1,2,3):
            for U in combinations(q,size):sub[U].append(j)
    off={U:sum(f&mask(U)==mask(U) for f in fixed) for U in sub}
    for U,ids in sorted(sub.items()):
        cap=(15 if case['empty'] and U[0]<12 else 20) if len(U)==1 else {2:6,3:2}[len(U)]
        row(up,'cap:'+str(U),dict.fromkeys(ids,1),cap-off[U])
        if len(U)==1 and U[0]<12:row(up,'min:'+str(U),dict.fromkeys(ids,-1),off[U]-4)
    for i,R in enumerate(selected):
        row(up,'H27:'+str(i),{j:1 for j,q in enumerate(qm) if not R&q},27-sum(not R&f for f in fixed))
    sels={}
    for v in range(x):
        cap=15 if case['empty'] and v<12 else 20
        ds=tuple(range(5,cap+1)) if v<12 else (0,*range(4,21)) # each component point has five fixed members
        sel={d:len(bd)+h for h,d in enumerate(ds)};bd.extend([(0,1)]*len(sel));sels[v]=sel
        row(eq,'degree-choice:'+str(v),dict.fromkeys(sel.values(),1),1)
        terms=dict.fromkeys(sub[v,],1);terms.update({h:-d for d,h in sel.items()})
        row(eq,'degree-tie:'+str(v),terms,-off[v,])
    row(up,'unused-cap',{sels[v][0]:1 for v in range(12,22)},7) # support >=16 out of 23
    # Hereditary empty-C5 theorem: delete all internal members through v.
    for v in range(12):
        side=v//6
        ids=[j for j,q in enumerate(quads) if v in q and all(u//6==side for u in q)]
        terms={h:d for d,h in sels[v].items()};terms.update({j:-1 for j in ids})
        row(up,'C5-internal:'+str(v),terms,15)
    if case['empty']:
        row(up,'W-incidences',{j:-sum(v>=12 for v in q) for j,q in enumerate(quads)},-(276-20-12*15))
    if case['min_w']:
        row(up,'W-two-minimum',{j:-sum(v>=12 for v in q) for j,q in enumerate(quads)},-case['min_w']*49)
    raw=[];live=[];extra=[]
    def attach(order,rows,label,central):
        R=mask(order);buckets=defaultdict(list);cnt=Counter(f&R for f in fixed)
        for j,q in enumerate(qm):buckets[q&R].append(j)
        feat=[(1<<v,10+i) for i,v in enumerate(order)]
        feat += [(mask((order[a],order[b])),i) for i,(a,b) in enumerate(PAIRS)]
        feat += [(R^(1<<v),6+i) for i,v in enumerate(order)]
        limits={i:(cnt[T]+sum(bd[j][0] for j in buckets[T]),cnt[T]+sum(bd[j][1] for j in buckets[T])) for T,i in feat}
        if rows is None:rows=general_rows(order,limits,case['empty'])
        rr=tuple(r for r in rows if all(lo<=r[i]<=hi for i,(lo,hi) in limits.items()))
        cols=list(range(len(bd),len(bd)+len(rr)));bd.extend([(0,1)]*len(cols))
        row(eq,label+'-choice',dict.fromkeys(cols,1),1)
        for T,i in feat:
            if central and T&(1<<x):continue
            terms=dict.fromkeys(buckets[T],1);terms.update({j:-r[i] for j,r in zip(cols,rr)})
            row(eq,label+'-trace:'+str(T),terms,-cnt[T])
        dd=tuple(map(deg,rr))
        for i,v in enumerate(order):
            if central and v==x:continue
            for d,h in sels[v].items():
                terms={h:-1};terms.update({j:1 for j,dg in zip(cols,dd) if dg[i]==d})
                row(eq,label+'-degree:'+str(v)+':'+str(d),terms,0)
        return len(rows),len(rr)
    for i,T in enumerate(LINK):
        r,l=attach((x,*T),central_rows(T,case['empty']),'anchor:'+str(i),True);raw.append(r);live.append(l)
    if case['marked']:extra=attach(tuple(mark),None,'marked',False)
    kappa=[sum(not q&f for f in fixed) for q in qm]
    if case['objective']=='deficit':row(eq,'residual49',dict.fromkeys(range(nz),1),49)
    obj=[max(0,12-c) if case['objective']=='deficit' else 1 for c in kappa]+[0]*(len(bd)-nz)
    return dict(case=case,bounds=bd,upper=up,equal=eq,quads=quads,fixed=fixed,zero=zero,ones=ones,
                raw_sizes=raw,live_sizes=live,extra_size=extra,objective=obj,target=48 if case['objective']=='deficit' else 49)


def matrix(rows,n):
    import numpy as np
    from scipy.sparse import coo_matrix
    ii=[];jj=[];vv=[]
    for i,(_,r,b) in enumerate(rows):
        for j,v in r.items():ii.append(i);jj.append(j);vv.append(v)
    return coo_matrix((np.asarray(vv,float),(ii,jj)),shape=(len(rows),n)).tocsr(),np.array([b for _,_,b in rows],float)
