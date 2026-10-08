"""Mask-based necessary models on exact traces. No solver is imported."""
from common import *
from functools import lru_cache
@lru_cache(32)
def possible_masks(n):
    return tuple(mask(vs)for k in (1,2,3,4)for vs in combinations(range(n),k)if sum(v<4 for v in vs)<=1)
def trace_data(core):
    ff=tuple(mask(q)for q in core);n=max(max(q)for q in core)+1;cv=[];caps=[]
    pairs=tuple((a,b,a&b)for a,b in combinations(ff,2))
    for u in possible_masks(n):
        if any(a&u==c and b&u==c for a,b,c in pairs):continue
        cap={1:16,2:6,3:2,4:1}[u.bit_count()]-sum(f&u==u for f in ff)
        if cap>0:cv.append(u);caps.append(cap)
    return ff,n,tuple(cv),tuple(caps)
def anchor_data(core,row,q,td=None):
    ff,n,cv,caps=td if td else trace_data(core);qm=mask(q)
    feats=tuple(mask((q[i],q[j]))for i,j in PAIRS)+tuple(qm^(1<<v)for v in q)+tuple(1<<v for v in q)
    low=tuple(sum(f&qm==t for f in ff)for t in feats)
    high=tuple(l+sum(c for u,c in zip(cv,caps)if u&qm==t)for t,l in zip(feats,low))
    fd={v:sum(v in f for f in core)for v in q}
    bits=row_index().choose(tuple(q),degree(row),fd,low,high)
    ids=tuple(row_index().indices(bits));rows=tuple(row_index().rows[i]for i in ids)
    return feats,low,high,rows

def build(core,row,case):
    ff,n,cv,caps=trace_data(core);bounds=[(0,c)for c in caps];names=[['trace',u]for u in cv];eq=[];up=[];sizes=[]
    def add(dest,label,co,rhs):dest.append((label,{j:v for j,v in co.items()if v},rhs))
    for q in core:
        fs,lo,hi,rr=anchor_data(core,row,q,(ff,n,cv,caps));at=len(bounds)
        bounds.extend([(0,1)]*len(rr));names.extend([['anchor',q,list(r)]for r in rr]);sizes.append(len(rr))
        add(eq,'choice:'+str(q),dict.fromkeys(range(at,at+len(rr)),1),1)
        qm=mask(q)
        for i,t in enumerate(fs):
            co={j:1 for j,u in enumerate(cv)if u&qm==t};co.update({at+j:-r[i]for j,r in enumerate(rr)if r[i]})
            add(eq,'trace:'+str(q)+':'+str(t),co,-lo[i])
    for k in (1,2,3):
        for vs in combinations(range(n),k):
            t=mask(vs);co={j:1 for j,u in enumerate(cv)if u&t==t}
            if co:add(up,'cap:'+str(vs),co,{1:16,2:6,3:2}[k]-sum(f&t==t for f in ff))
    if case['shared_degrees']:
        sels={};given=degree(row)
        for v in range(n):
            opts=[given[v]]if v<4 else range(max(8,sum(v in q for q in core)),17)
            ids={d:len(bounds)+i for i,d in enumerate(opts)};bounds.extend([(0,1)]*len(ids));names.extend([['degree',v,d]for d in ids]);sels[v]=ids
            add(eq,'global_degree:'+str(v),dict.fromkeys(ids.values(),1),1)
        for q in core:
            for pos,v in enumerate(q):
                by={d:{}for d in sels[v]}
                for j,name in enumerate(names):
                    if name[0]=='anchor' and name[1]==q:
                        d=degree(name[2])[pos]
                        if d not in by:bounds[j]=(0,0)
                        else:by[d][j]=1
                for d,co in by.items():co[sels[v][d]]=-1;add(eq,f'degdist:{q}:{v}:{d}',co,0)
    if case['total69']:
        require(any(not a&b for a,b in combinations(ff,2)),'empty trace needs a fixed disjoint pair')
        add(eq,'total_F69',dict.fromkeys(range(len(cv)),1),69-len(core))
    if case['h27_cuts']:
        for pos,cl in enumerate(load('data/H27_CUTS.json')):
            validate_clique(core,cv,cl)
            add(up,'H27_clique:'+str(pos),{j:1 for j in cl if j>=0},27-sum(j<0 for j in cl))
    return dict(core=core,row=row,bounds=bounds,varnames=names,equal=eq,upper=up,sizes=sizes)

def validate_clique(core,cv,cl):
    require(len(cl)==len(set(cl)),'repeated cut node');ff=tuple(mask(q)for q in core)
    require(all(type(i)is int and -len(core)<=i<len(cv) for i in cl),'cut node bounds')
    for i,j in combinations(cl,2):
        if i<0 and j<0:require(bool(ff[-i-1]&ff[-j-1]),'nonintersecting fixed cut nodes')
        elif i<0 or j<0:
            a,b=(i,j)if i<0 else (j,i);require(bool(ff[-a-1]&cv[b]),'trace does not meet fixed cut node')
        else:
            u,v=cv[i],cv[j]
            require(bool(u&v)or any(not(a&(u|v))for a in ff),'unsupported trace-pool intersection')

def verify_certificate(m,c):
    require(type(c)is dict and c['columns']==len(m['bounds'])and c['upper_rows']==len(m['upper'])and c['equal_rows']==len(m['equal']),'certificate dimensions')
    require(type(c['scale'])is int and c['scale']>0,'positive scale')
    lhs=[0]*len(m['bounds']);rhs=0
    for field,rows,positive in [('y',m['upper'],True),('eta',m['equal'],False)]:
        seen=set()
        for i,w in c[field]:
            require(type(i)is int and type(w)is int and 0<=i<len(rows)and i not in seen and w!=0 and (not positive or w>0),'invalid multiplier')
            seen.add(i);_,co,b=rows[i];rhs+=w*b
            for j,v in co.items():lhs[j]+=w*v
    low=sum(min(w*l,w*u)for w,(l,u)in zip(lhs,m['bounds']))
    require((rhs,low,rhs-low)==(c['H'],c['L'],c['gap']),'arithmetic mismatch')
    require(rhs<low,'not a refutation')
    return dict(id=c['label'],columns=len(lhs),upper_rows=len(m['upper']),equal_rows=len(m['equal']),H=rhs,L=low,gap=rhs-low,used_upper=len(c['y']),used_equal=len(c['eta']))
