"""Producer with complete interior assignment on explicitly listed components.
Unassigned component interiors remain unrestricted. Existing base columns retain
exact order; incompatible row/degree selectors are set to zero, not deleted.
"""
from itertools import combinations
from collections import Counter,defaultdict
import model as B
matrix=B.matrix

def build(case):
    B.need(set(case)=={'id','mark','empty','marked','min_w','objective','assigned'},'assigned case fields')
    B.need(case['empty'] is False and case['marked'] is False and case['min_w']==0 and case['objective']=='cardinality','assigned stage')
    asg=case['assigned'];B.need(type(asg) is dict and set(asg)<={'0','1'},'components assigned')
    for key,vv in asg.items():
        B.need(type(vv) is list and len({tuple(q) for q in vv})==len(vv),'assigned uniqueness')
        B.need(all(type(q) is list and len(q)==4 and all(type(v) is int for v in q) and q==sorted(set(q)) and all(6*int(key)<=v<6*(int(key)+1) for v in q) for q in vv),'assigned members')
    plain={k:v for k,v in case.items() if k!='assigned'};data=B.build(plain)
    quads=data['quads'];qm=list(map(B.mask,quads));before=data['bounds'];box=list(before)
    chosen=sorted({tuple(q) for vv in asg.values() for q in vv}|(set() if case['mark'] is None else {tuple(case['mark'])}))
    ones={quads.index(q) for q in chosen};known=data['fixed']+tuple(B.mask(q) for q in chosen);zero=set(data['zero'])
    for j,q in enumerate(quads):
        if any(all(6*int(side)<=v<6*(int(side)+1) for v in q) and list(q) not in vv for side,vv in asg.items()):zero.add(j)
    for a,b in combinations(known,2):
        common=a&b
        zero.update(j for j,q in enumerate(qm) if q&a==common and q&b==common)
    B.need(not ones&zero,'contradictory assigned family')
    for j in range(len(quads)):box[j]=(1,1) if j in ones else (0,0) if j in zero else (0,1)
    internal={v:sum(v in q for q in asg[str(v//6)]) for v in range(12) if str(v//6) in asg}
    caps={v: min(19,15+i) if v in B.C5_POINTS else max(d for d in range(4,20) if {17:1,18:4,19:5}.get(d,0)<=i) for v,i in internal.items()}
    eq={name:(terms,rhs) for name,terms,rhs in data['equal']}
    for v,cap in caps.items():
        for d in range(sum(bool(f&(1<<v)) for f in data['fixed']),20):
            terms,_=eq['degree-tie:'+str(v)]
            # Negative terms of the degree tie are exactly the degree selectors.
            for j,c in terms.items():
                if j>=len(quads) and -c==d and d>cap:box[j]=(0,0)
    kept=[]
    for pos,T in enumerate(B.LINK):
        order=(22,*T);rm=B.mask(order);bucket=defaultdict(list);cnt=Counter(f&rm for f in data['fixed'])
        for j,q in enumerate(qm):bucket[q&rm].append(j)
        feats=[(1<<v,10+i) for i,v in enumerate(order)]
        feats += [(B.mask((order[a],order[b])),i) for i,(a,b) in enumerate(B.PAIRS)]
        feats += [(rm^(1<<v),6+i) for i,v in enumerate(order)]
        def limits(bb):return {i:(cnt[V]+sum(bb[j][0] for j in bucket[V]),cnt[V]+sum(bb[j][1] for j in bucket[V])) for V,i in feats}
        old,new=limits(before),limits(box)
        rows=[r for r in B.central_rows(T,False) if all(lo<=r[i]<=hi for i,(lo,hi) in old.items())]
        cols=list(eq['anchor:'+str(pos)+'-choice'][0]);B.need(len(rows)==len(cols),'base row order')
        live=0
        for j,r in zip(cols,rows):
            dd=B.deg(r);valid=all(lo<=r[i]<=hi for i,(lo,hi) in new.items())
            for i,v in enumerate(order):
                if v not in internal:continue
                if dd[i]>caps[v]:valid=False
                if r[10+i]>=8 and dd[i]-r[10+i]>(5 if v in B.C5_POINTS else 6)+internal[v]:valid=False
            if not valid:box[j]=(0,0)
            else:live+=1
        kept.append(live)
    up=list(data['upper'])
    for num,q in enumerate(chosen):
        # The marked anchor (if any) already has its H27 row in the base system.
        if case['mark'] is not None and list(q)==case['mark']:continue
        m=B.mask(q);up.append(('assigned-H27:'+str(num),{j:1 for j,z in enumerate(qm) if not z&m},27-sum(not f&m for f in data['fixed'])))
    data.update(case=case,bounds=box,upper=up,ones=ones,zero=zero,assigned_live=kept,assigned_degrees=internal,assigned_caps=caps)
    return data
