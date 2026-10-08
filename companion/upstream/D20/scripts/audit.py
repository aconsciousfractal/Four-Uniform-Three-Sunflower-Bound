"""Independent set/partition reconstruction and exact verification.
Imports only the declared upstream anchor predicate and Python standard library.
It never imports the discovery constructor or a numerical solver.
"""
from pathlib import Path
from itertools import combinations,product
from collections import Counter,defaultdict
from functools import lru_cache
from fractions import Fraction
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'sources'))
import audit43 as U
BASE=tuple(tuple(int(a) for a in s) for s in '012 015 023 034 045 124 134 135 235 245'.split())
CONES=BASE+tuple(tuple(a+6 for a in T) for T in BASE)
PAIRS=tuple(combinations(range(4),2))

def require(ok,msg):
    if not ok:raise ValueError(msg)
def code(S):return sum(2**v for v in S)
def degrees(r):
    return tuple(r[10+i]+1+sum(r[j] for j,(a,b) in enumerate(PAIRS) if i in (a,b))+sum(r[6:10])-r[6+i] for i in range(4))

def vertex_choices(i,p,t,cap):
    other=tuple(j for j in range(4) if j!=i)
    alpha=tuple(p[PAIRS.index(tuple(sorted((i,j))))] for j in other)
    tau=tuple(t[j] for j in other)
    return U.choices(alpha,tau,t[i],7,7,cap)

def finish(p,t,options):
    if any(not o for o in options):return []
    kk=tuple(1+sum(p[j] for j,ab in enumerate(PAIRS) if i in ab)+sum(t)-t[i] for i in range(4))
    out=[];maxs=[max(s for s,d in c) for c in options];req=41-sum(p)-sum(t)
    def rec(i,ss,ds):
        if i==4:
            if min(ds)>=4 and sum(ds)>=52 and all(ds[a]+ds[b]>=20 for a,b in PAIRS) and U.condition_global(p,t,ss,kk,ds,42):out.append(p+t+tuple(ss))
            return
        for s,d in options[i]:
            if sum(ss)+s+sum(maxs[i+1:])>=req:rec(i+1,ss+[s],ds+[d])
    rec(0,[],[])
    return out

@lru_cache(None)
def central(T,empty):
    T=tuple(sorted(T));R=frozenset(T);M=tuple(map(frozenset,CONES))
    aa=tuple(sum(Q&R=={a} for Q in M) for a in T)
    tt=tuple(sum(Q&R==R-{a} for Q in M) for a in T)
    sx=sum(not Q&R for Q in M);out=[]
    for e in (0,1):
        t=(e,*tt)
        for tail in product(range(4),repeat=3):
            p=aa+tail;options=[]
            for i in range(4):
                cap=15 if empty and i else 20
                cc=[]
                for s,d in vertex_choices(i,p,t,cap):
                    if d<4 or i==0 and s!=sx:continue
                    if i and empty and s>=8 and d-s!=5:continue
                    cc.append((s,d))
                options.append(cc)
            out.extend(finish(p,t,options))
    out.sort();require(len(out)==len(set(out)),'duplicate central rows');return tuple(out)

def marked_rows(order,limits,empty):
    out=[]
    for t in product(*(range(limits[6+i][0],min(1,limits[6+i][1])+1) for i in range(4))):
        for p in product(*(range(limits[i][0],min(3,limits[i][1])+1) for i in range(6))):
            options=[]
            for i,v in enumerate(order):
                cap=15 if empty and v<12 else 20
                lo,hi=limits[10+i]
                options.append(tuple((s,d) for s,d in vertex_choices(i,p,t,cap) if d>=4 and lo<=s<=hi))
            out.extend(finish(p,t,options))
    out.sort();require(len(out)==len(set(out)),'duplicate marked rows');return tuple(out)


def build(case):
    require(type(case) is dict and set(case)=={'id','mark','empty','marked','min_w','objective'},'case fields')
    require(type(case['id']) is str and type(case['empty']) is bool and type(case['marked']) is bool,'case types')
    require(type(case['min_w']) is int and case['min_w'] in (0,2) and (not case['min_w'] or case['empty']),'stage')
    require(case['objective'] in ('cardinality','deficit'),'objective')
    qs=tuple(combinations(range(22),4));Q=tuple(map(frozenset,qs));n=len(qs)
    mark=case['mark']; require(mark is None or type(mark) is list and len(mark)==4 and all(type(v) is int for v in mark) and tuple(mark) in qs,'marker')
    require(not case['marked'] or mark is not None,'missing marked member')
    f=tuple(frozenset((22,*T)) for T in CONES)
    ones=set() if mark is None else {qs.index(tuple(mark))};known=f+tuple(Q[j] for j in sorted(ones));forbidden=set()
    for j,q in enumerate(Q):
        if any(q&a==q&b==a&b for a,b in combinations(known,2)):forbidden.add(j)
        if case['empty'] and (q<=set(range(6)) or q<=set(range(6,12))):forbidden.add(j)
        if case['min_w'] and len(q&set(range(12,22)))<case['min_w']:forbidden.add(j)
    require(not ones&forbidden,'chosen forbidden')
    box=[(1,1) if j in ones else (0,0) if j in forbidden else (0,1) for j in range(n)]
    up=[];eq=[]
    def emit(dest,label,a,b):dest.append((label,{int(j):int(v) for j,v in a.items() if v},int(b)))
    sub=defaultdict(list)
    for j,q in enumerate(qs):
        for size in (1,2,3):
            for T in combinations(q,size):sub[T].append(j)
    offset={T:sum(set(T)<=a for a in f) for T in sub}
    for T,js in sorted(sub.items()):
        c=({1:20,2:6,3:2}[len(T)])
        if len(T)==1 and case['empty'] and T[0]<12:c=15
        emit(up,'cap:'+str(T),dict.fromkeys(js,1),c-offset[T])
        if len(T)==1 and T[0]<12:emit(up,'min:'+str(T),dict.fromkeys(js,-1),offset[T]-4)
    for i,a in enumerate(known):emit(up,'H27:'+str(i),{j:1 for j,q in enumerate(Q) if not q&a},27-sum(not a&b for b in f))
    degrees_select={}
    for v in range(22):
        vals=tuple(range(5,16 if case['empty'] else 21)) if v<12 else (0,*range(4,21))
        js=list(range(len(box),len(box)+len(vals)));box.extend([(0,1)]*len(js));sel=dict(zip(vals,js));degrees_select[v]=sel
        emit(eq,'degree-choice:'+str(v),dict.fromkeys(js,1),1)
        a=dict.fromkeys(sub[v,],1);a.update({j:-d for d,j in sel.items()});emit(eq,'degree-tie:'+str(v),a,-offset[v,])
    emit(up,'unused-cap',{degrees_select[v][0]:1 for v in range(12,22)},7)
    for v in range(12):
        S=set(range(0,6)) if v<6 else set(range(6,12))
        a={j:d for d,j in degrees_select[v].items()};a.update({j:-1 for j,q in enumerate(Q) if v in q and q<=S})
        emit(up,'C5-internal:'+str(v),a,15)
    if case['empty']:emit(up,'W-incidences',{j:-len(q&set(range(12,22))) for j,q in enumerate(Q)},-76)
    if case['min_w']:emit(up,'W-two-minimum',{j:-len(q&set(range(12,22))) for j,q in enumerate(Q)},-49*case['min_w'])
    raw=[];live=[];extra=[]
    def attach(order,rows,label,is_central):
        R=frozenset(order);buckets=defaultdict(list);cnt=Counter(a&R for a in f)
        for j,q in enumerate(Q):buckets[q&R].append(j)
        feats=[(frozenset((v,)),10+i) for i,v in enumerate(order)]
        feats += [(frozenset((order[a],order[b])),i) for i,(a,b) in enumerate(PAIRS)]
        feats += [(R-{v},6+i) for i,v in enumerate(order)]
        ranges={i:(cnt[T]+sum(box[j][0] for j in buckets[T]),cnt[T]+sum(box[j][1] for j in buckets[T])) for T,i in feats}
        if rows is None:rows=marked_rows(order,ranges,case['empty'])
        kept=tuple(r for r in rows if all(low<=r[i]<=high for i,(low,high) in ranges.items()))
        ids=list(range(len(box),len(box)+len(kept)));box.extend([(0,1)]*len(ids))
        emit(eq,label+'-choice',dict.fromkeys(ids,1),1)
        for T,i in feats:
            if is_central and 22 in T:continue
            a=dict.fromkeys(buckets[T],1);a.update({j:-r[i] for j,r in zip(ids,kept)})
            emit(eq,label+'-trace:'+str(code(T)),a,-cnt[T])
        dd=tuple(map(degrees,kept))
        for i,v in enumerate(order):
            if is_central and v==22:continue
            for d,h in degrees_select[v].items():
                a={h:-1};a.update({j:1 for j,D in zip(ids,dd) if D[i]==d});emit(eq,label+'-degree:'+str(v)+':'+str(d),a,0)
        return len(rows),len(kept)
    for pos,T in enumerate(CONES):
        a,b=attach((22,*T),central(T,case['empty']),'anchor:'+str(pos),True);raw.append(a);live.append(b)
    if case['marked']:extra=attach(tuple(mark),None,'marked',False)
    kappa=tuple(sum(not q&t for t in f) for q in Q)
    if case['objective']=='deficit':emit(eq,'residual49',dict.fromkeys(range(n),1),49)
    obj=[max(0,12-k) if case['objective']=='deficit' else 1 for k in kappa]+[0]*(len(box)-n)
    return dict(case=case,bounds=box,upper=up,equal=eq,quads=qs,fixed=tuple(map(code,f)),zero=forbidden,ones=ones,
                raw_sizes=raw,live_sizes=live,extra_size=extra,objective=obj,target=48 if case['objective']=='deficit' else 49)

def verify(cert,data=None):
    require(type(cert) is dict and cert.get('schema')=='E20_F69_D20_LINEAR_V1','schema')
    require(cert.get('mode') in ('upper','infeasible'),'mode')
    d=build(cert['case']) if data is None else data
    require(cert['case']==d['case'],'bound to case')
    for name,val in (('target',d['target']),('columns',len(d['bounds'])),('upper_rows',len(d['upper'])),('equal_rows',len(d['equal']))):
        require(type(cert.get(name)) is int and cert[name]==val,'dimensions '+name)
    scale=cert.get('scale');require(type(scale) is int and scale>0,'scale')
    coeff=[0]*len(d['bounds']);rhs=0
    for key,rows in (('upper',d['upper']),('equal',d['equal'])):
        require(type(cert.get(key)) is list,'multiplier list');seen=set()
        for x in cert[key]:
            require(type(x) is list and len(x)==2,'record');i,w=x
            require(type(i) is int and 0<=i<len(rows) and i not in seen,'index')
            require(type(w) is int and w!=0 and (key!='upper' or w>0),'coefficient')
            seen.add(i);_,r,b=rows[i];rhs+=w*b
            for j,v in r.items():coeff[j]+=w*v
    if cert['mode']=='upper':
        r=[scale*c-q for c,q in zip(d['objective'],coeff)]
        value=rhs+sum(max(a*l,a*u) for a,(l,u) in zip(r,d['bounds']));require(value<scale*d['target'],'not below target')
    else:
        value=rhs-sum(min(a*l,a*u) for a,(l,u) in zip(coeff,d['bounds']));require(value<0,'nonnegative gap')
    require(type(cert.get('value')) is int and cert['value']==value,'value mismatch')
    return {'status':'PASS','id':cert['case']['id'],'mode':cert['mode'],'value':value,'scale':scale,'ratio':str(Fraction(value,scale)),
            'columns':len(coeff),'upper_rows':len(d['upper']),'equal_rows':len(d['equal']),'raw_sizes':d['raw_sizes'],'live_sizes':d['live_sizes'],'extra_size':d['extra_size']}
