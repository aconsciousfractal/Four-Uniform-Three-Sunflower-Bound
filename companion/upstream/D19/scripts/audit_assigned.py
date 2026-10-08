"""Separate set-based reconstruction of complete assignments; no solver imports."""
from itertools import combinations
from collections import Counter,defaultdict
import copy
import audit as B
require=B.require

def build(case):
    require(type(case) is dict and set(case)=={'id','mark','empty','marked','min_w','objective','assigned'},'assigned case fields')
    require(case['empty'] is False and case['marked'] is False and case['min_w']==0 and case['objective']=='cardinality','assigned stage')
    assignments=case['assigned'];require(type(assignments) is dict and set(assignments)<={'0','1'},'assigned component indices')
    supports=(set(range(6)),set(range(6,12)))
    for key,vv in assignments.items():
        require(type(vv) is list and all(type(q) is list and len(q)==4 and all(type(v) is int for v in q) and q==sorted(set(q)) and set(q)<=supports[int(key)] for q in vv),'assignment format')
        require(len(vv)==len({tuple(q) for q in vv}),'assignment duplicates')
    d=B.build({k:v for k,v in case.items() if k!='assigned'});qs=d['quads'];Q=list(map(frozenset,qs));old=d['bounds'];box=list(old)
    chosen=sorted(set(tuple(q) for vv in assignments.values() for q in vv)|(set() if case['mark'] is None else {tuple(case['mark'])}))
    ones={qs.index(q) for q in chosen};fixed=tuple(frozenset((22,*T)) for T in B.CONES);known=fixed+tuple(map(frozenset,chosen));zero=set(d['zero'])
    for j,q in enumerate(Q):
        if any(q<=supports[int(side)] and sorted(q) not in vv for side,vv in assignments.items()):zero.add(j)
        if any(q&a==q&b==a&b for a,b in combinations(known,2)):zero.add(j)
    require(not ones&zero,'selected forbidden')
    for j in range(len(qs)):box[j]=(1,1) if j in ones else (0,0) if j in zero else (0,1)
    internal={v:sum(v in q for q in vv) for side,vv in assignments.items() for v in sorted(supports[int(side)])}
    caps={}
    for v,I in internal.items():
        cap=19
        while (max(0,cap-15) if v not in (6,7,8) else 5 if cap==19 else 4 if cap==18 else 1 if cap==17 else 0)>I:cap-=1
        caps[v]=cap
        _,coeffs,_=next(r for r in d['equal'] if r[0]=='degree-tie:'+str(v))
        for j,c in coeffs.items():
            if j>=len(qs) and -c>cap:box[j]=(0,0)
    active=[]
    for pos,T in enumerate(B.CONES):
        order=(22,*T);R=frozenset(order);cnt=Counter(f&R for f in fixed);buckets=defaultdict(list)
        for j,q in enumerate(Q):buckets[q&R].append(j)
        features=[(frozenset((v,)),10+i) for i,v in enumerate(order)]
        features.extend((frozenset((order[a],order[b])),i) for i,(a,b) in enumerate(B.PAIRS))
        features.extend((R-{v},6+i) for i,v in enumerate(order))
        def ranges(bb):return {i:(cnt[V]+sum(bb[j][0] for j in buckets[V]),cnt[V]+sum(bb[j][1] for j in buckets[V])) for V,i in features}
        initial=ranges(old);current=ranges(box)
        rr=[r for r in B.central(T,False) if all(lo<=r[i]<=hi for i,(lo,hi) in initial.items())]
        _,choices,_=next(r for r in d['equal'] if r[0]=='anchor:'+str(pos)+'-choice')
        require(len(rr)==len(choices),'base columns')
        count=0
        for j,r in zip(choices,rr):
            bad=any(r[i]<lo or r[i]>hi for i,(lo,hi) in current.items())
            for i,v in enumerate(order):
                if v not in internal:continue
                degree=B.degrees(r)[i]
                if degree>caps[v]:bad=True
                if r[10+i]>=8 and degree-r[10+i]>internal[v]+(6 if v in (6,7,8) else 5):bad=True
            if bad:box[j]=(0,0)
            else:count+=1
        active.append(count)
    up=list(d['upper'])
    for i,q in enumerate(chosen):
        if case['mark'] is not None and list(q)==case['mark']:continue
        s=frozenset(q);up.append(('assigned-H27:'+str(i),{j:1 for j,q in enumerate(Q) if not q&s},27-sum(not f&s for f in fixed)))
    d.update(case=case,bounds=box,upper=up,ones=ones,zero=zero,assigned_live=active,assigned_degrees=internal,assigned_caps=caps)
    return d

def verify(cert,data=None):
    require(type(cert) is dict and cert.get('schema')=='E20_F69_D19_ASSIGNED_V1','assigned certificate schema')
    d=build(cert['case']) if data is None else data
    forwarded=copy.deepcopy(cert);forwarded['schema']='E20_F69_D19_LINEAR_V2'
    out=B.verify(forwarded,d)
    out.update(assigned_live=d['assigned_live'],assigned_caps=d['assigned_caps'],assigned_degrees=d['assigned_degrees'])
    return out
