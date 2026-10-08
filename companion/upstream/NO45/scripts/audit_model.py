"""Set-based second construction. Shares row indexing, not model assembly."""
from common import *
from collections import Counter,defaultdict

def trace_sets(core):
    F=tuple(frozenset(q)for q in core);vertices=range(1+max(v for q in core for v in q));ts=[];bs=[]
    for size in range(1,5):
        for vs in combinations(vertices,size):
            U=frozenset(vs)
            if len(U&frozenset(range(4)))>1:continue
            if any(U&A==U&B==A&B for A,B in combinations(F,2)):continue
            b={1:16,2:6,3:2,4:1}[size]-sum(U<=A for A in F)
            if b>0:ts.append(U);bs.append(b)
    return F,tuple(ts),tuple(bs)
def bounds_for_anchor(core,row,Q,F,ts,bs):
    A=frozenset(Q);features=tuple(frozenset((Q[i],Q[j]))for i,j in PAIRS)+tuple(A-{v}for v in Q)+tuple(frozenset((v,))for v in Q)
    count=Counter(B&A for B in F);addition=Counter()
    for U,b in zip(ts,bs):addition[U&A]+=b
    low=tuple(count[T]for T in features);high=tuple(count[T]+addition[T]for T in features)
    fixed={v:sum(v in B for B in F)for v in Q}
    bits=row_index().choose(tuple(Q),degree(row),fixed,low,high)
    rr=tuple(row_index().rows[i]for i in row_index().indices(bits))
    return features,low,high,rr

def build(core,row,case):
    F,ts,bs=trace_sets(core);nv=1+max(v for Q in core for v in Q)
    bounds=[(0,b)for b in bs];names=[['trace',mask(U)]for U in ts];up=[];eq=[];sizes=[]
    def emit(dest,label,terms,rhs):dest.append((label,{j:int(v)for j,v in terms.items()if v},int(rhs)))
    for Q in core:
        A=frozenset(Q);feats,lo,hi,rr=bounds_for_anchor(core,row,Q,F,ts,bs)
        columns=list(range(len(bounds),len(bounds)+len(rr)));bounds.extend([(0,1)]*len(rr));names.extend([['anchor',Q,list(r)]for r in rr]);sizes.append(len(rr))
        emit(eq,'choice:'+str(Q),dict.fromkeys(columns,1),1)
        for p,T in enumerate(feats):
            co={j:1 for j,U in enumerate(ts)if U&A==T}
            for j,r in zip(columns,rr):
                if r[p]:co[j]=-r[p]
            emit(eq,'trace:'+str(Q)+':'+str(mask(T)),co,-lo[p])
    for size in (1,2,3):
        for vs in combinations(range(nv),size):
            T=frozenset(vs);terms={j:1 for j,U in enumerate(ts)if T<=U}
            if terms:emit(up,'cap:'+str(vs),terms,{1:16,2:6,3:2}[size]-sum(T<=B for B in F))
    if case['shared_degrees']:
        sels={};given=degree(row)
        for v in range(nv):
            ds=([given[v]]if v<4 else list(range(max(8,sum(v in Q for Q in core)),17)))
            cols=list(range(len(bounds),len(bounds)+len(ds)));sels[v]=dict(zip(ds,cols));bounds.extend([(0,1)]*len(cols));names.extend([['degree',v,d]for d in ds])
            emit(eq,'global_degree:'+str(v),dict.fromkeys(cols,1),1)
        anchors=defaultdict(list)
        for j,t in enumerate(names):
            if t[0]=='anchor':anchors[tuple(t[1])].append((j,degree(t[2])))
        for Q in core:
            for p,v in enumerate(Q):
                for j,ds in anchors[tuple(Q)]:
                    if ds[p] not in sels[v]:bounds[j]=(0,0)
                for d,h in sels[v].items():
                    terms={j:1 for j,ds in anchors[tuple(Q)]if ds[p]==d};terms[h]=-1
                    emit(eq,f'degdist:{Q}:{v}:{d}',terms,0)
    if case['total69']:
        require(any(not A&B for A,B in combinations(F,2)),'auditor missing disjoint fixed pair')
        emit(eq,'total_F69',dict.fromkeys(range(len(ts)),1),69-len(F))
    if case['h27_cuts']:
        for ci,cl in enumerate(load('data/H27_CUTS.json')):
            require(len(cl)==len(set(cl))and all(-len(F)<=i<len(ts)for i in cl),'auditor cut labels')
            for i,j in combinations(cl,2):
                if i<0 and j<0:ok=bool(F[-i-1]&F[-j-1])
                elif i<0 or j<0:
                    a,b=(i,j)if i<0 else (j,i);ok=bool(F[-a-1]&ts[b])
                else:ok=bool(ts[i]&ts[j])or any(not A&(ts[i]|ts[j])for A in F)
                require(ok,'auditor invalid pool')
            emit(up,'H27_clique:'+str(ci),{i:1 for i in cl if i>=0},27-sum(i<0 for i in cl))
    return dict(core=core,row=row,bounds=bounds,varnames=names,equal=eq,upper=up,sizes=sizes)
