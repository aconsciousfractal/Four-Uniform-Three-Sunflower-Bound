"""Independent exact verifier: binary pair masks, reverse triple recursion,
literal sunflower witnesses and graph connected components. No producer import.
All comparisons are integers; every generated state consumes one proof record.
"""
from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import argparse, gzip, hashlib, json, time
ROOT=Path(__file__).resolve().parents[1]
P=tuple(tuple(map(int,t)) for t in ('012','015','023','034','045','124','134','135','235','245'))
POINTS=tuple(range(6));PAIR=tuple(combinations(POINTS,2));TRIPLE=tuple(combinations(POINTS,3))
SUB=tuple(U for k in (1,2,3) for U in combinations(POINTS,k))
COMP=tuple(T for T in TRIPLE if T not in P)
PAIR_INDEX={U:i for i,U in enumerate(PAIR)}
PROFILE={'ALL15':(15,15,15,15,15,15),'ONE14':(14,15,15,15,15,15)}

def require(ok,message):
    if not ok:raise ValueError(message)

def sunflower(A,B,C):
    return A!=B and A!=C and B!=C and A&B==A&C==B&C

CONES=tuple(frozenset((6,*T)) for T in P)
# The following finite incidence witnesses use two distinct exterior placeholders.
TRIPLE_FORCE={(U,V):any(sunflower(A,frozenset((*U,7)),frozenset((*V,8))) for A in CONES) for U in TRIPLE for V in TRIPLE}
SINGLE_FORCE={U:frozenset(y for y in POINTS if any(sunflower(A,frozenset((*U,7)),frozenset((y,8,9,10))) for A in CONES)) for U in TRIPLE}
PAIR_FORCE={(U,V):any(sunflower(A,frozenset((*U,7)),frozenset((*V,8,9))) for A in CONES) for U in TRIPLE for V in PAIR if set(V)<=set(U)}

def local_rows():
    """Rebuild the ten rows from only the elementary bounds in PROOF section 2."""
    out=[]
    for ss in product(range(9),repeat=3):
        for ww in product(range(4),repeat=3):
            for e in (0,1):
                kk=(5+e+ww[0]+ww[1],5+e+ww[0]+ww[2],5+e+ww[1]+ww[2])
                dd=tuple(a+b for a,b in zip(ss,kk))
                if max(dd)>15:continue
                if any(s==8 and k!=5 for s,k in zip(ss,kk)):continue
                if 18+e+sum(ss)+sum(ww)<43:continue
                out.append((ww,e,ss,dd))
    require(len(out)==10,'ten elementary anchor rows')
    return sorted(out)

def fixed_geometry():
    require(len(P)==10 and len(set(P))==10,'P10 simple')
    require(all(sum(v in T for T in P)==5 for v in POINTS),'P10 degree')
    require(all(sum(set(U)<=set(T) for T in P)==2 for U in PAIR),'P10 pair incidence')
    for y in POINTS:
        edges=[set(T)-{y} for T in P if y in T]
        vv=set().union(*edges)
        require(len(vv)==5 and all(sum(v in e for e in edges)==2 for v in vv),'cycle degrees')
        reached={min(vv)}
        for _ in range(5):
            for e in edges:
                if reached&e:reached|=e
        require(reached==vv,'C5 connected')
        require(not any(all(set(t)&e for e in edges) for t in combinations(vv,2)),'C5 cover >=3')
    autos=[p for p in permutations(POINTS) if {tuple(sorted(p[v] for v in T)) for T in P}==set(P)]
    require(len(autos)==60 and {p[0] for p in autos}==set(POINTS),'normalization transitivity')
    require(all(SINGLE_FORCE[U]==frozenset(U) for U in TRIPLE),'literal singleton witnesses')
    require(all(PAIR_FORCE.values()),'literal pair-family witnesses')
    rows=local_rows()
    require({d for _,_,_,d in rows}==set(permutations((13,15,15)))|set(permutations((14,15,15)))|{(15,15,15)},'degree profiles')
    require(all(sum(d<15 for d in row[3])<=1 for row in rows),'one low per anchor')
    # ONE13: block 012 forces residual degree of pair 12 to 3; block 124
    # has three degree-15 vertices and forces that same residual degree <=2.
    low=[r for r in rows if r[3]==(13,15,15)]
    high=[r for r in rows if r[3]==(15,15,15)]
    require(len(low)==1 and low[0][0][2]+low[0][1]==3,'ONE13 first anchor')
    require((0,1,2) in P and (1,2,4) in P and all(r[0][0]+r[1]<=2 for r in high),'ONE13 second anchor')
    return {'automorphisms':60,'elementary_rows':len(rows),'ONE13':'EXCLUDED_BY_SHARED_PAIR_12','single_witnesses':120,'pair_witnesses':60}

def independent_states(profile):
    """Binary weak-pair masks, not a join of anchor rows."""
    one14=profile[0]==14
    choices=tuple(i for i,U in enumerate(PAIR) if not(one14 and 0 in U))
    states=[];patterns=0
    for bits in range(1<<len(choices)):
        m=[1 if one14 and 0 in U else 2 for U in PAIR]
        for k,j in enumerate(choices):m[j]=2-((bits>>k)&1)
        pcount=[];good=True
        for T in P:
            mm=[m[PAIR_INDEX[U]] for U in combinations(T,2)]
            if one14 and 0 in T:
                U=tuple(v for v in T if v!=0)
                if m[PAIR_INDEX[U]]!=2:good=False;break
                pcount.append(0)
            elif sorted(mm)==[2,2,2]:pcount.append(1)
            elif sorted(mm)==[1,2,2]:pcount.append(0)
            else:good=False;break
        if not good:continue
        patterns+=1
        budget=m.copy();n={T:c for T,c in zip(P,pcount)}
        for T,c in zip(P,pcount):
            for U in combinations(T,2):budget[PAIR_INDEX[U]]-=c
        if min(budget)<0:continue
        reverse=tuple(reversed(COMP))
        def complete(i):
            if i==len(reverse):
                nn=dict(n)
                nn.update((U,budget[j]) for j,U in enumerate(PAIR))
                for y in POINTS:
                    remaining=profile[y]-5-sum(c for U,c in nn.items() if len(U)>=2 and y in U)
                    if remaining<0:return
                    nn[y,]=remaining
                states.append(tuple(nn[U] for U in SUB));return
            T=reverse[i];ids=[PAIR_INDEX[U] for U in combinations(T,2)]
            maximum=min(2,*(budget[j] for j in ids))
            for c in reversed(range(maximum+1)):
                n[T]=c
                for j in ids:budget[j]-=c
                complete(i+1)
                for j in ids:budget[j]+=c
            del n[T]
        complete(0)
    require(len(states)==len(set(states)),'duplicate independent state')
    return sorted(states),patterns

def components(n):
    tt=[T for T in TRIPLE for _ in range(n[T])]
    graph=[set() for T in tt]
    for i,U in enumerate(tt):
        for j in range(i):
            V=tt[j]
            if TRIPLE_FORCE[U,V] or any(n[y,]>=3 for y in SINGLE_FORCE[U]&SINGLE_FORCE[V]):
                graph[i].add(j);graph[j].add(i)
    remaining=set(range(len(tt)));out=[]
    while remaining:
        first=min(remaining);visited={first};queue=[first]
        while queue:
            i=queue.pop()
            for j in graph[i]-visited:visited.add(j);queue.append(j)
        remaining-=visited;out.append(tuple(sorted(visited)))
    return tt,out

def lower_counts(n,tt,C):
    singles=set().union(*(SINGLE_FORCE[tt[i]] for i in C))
    pairs={U for U in PAIR if n[U]>0 and any(set(U)<=set(tt[i]) and PAIR_FORCE[tt[i],U] for i in C)}
    degree=len(C)+sum(n[y,] for y in singles)+sum(n[U] for U in pairs)
    codegrees=[]
    for y in POINTS:
        codegrees.append((n[y,] if y in singles else 0)+sum(y in tt[i] for i in C)+sum(n[U] for U in pairs if y in U))
    return degree,codegrees

def verify_record(vector,record):
    require(type(record) is list and record and type(record[0]) is str,'witness format')
    n=dict(zip(SUB,vector));kind=record[0]
    if kind=='P':
        require(len(record)==2 and type(record[1]) is int and 0<=record[1]<6,'pair-trace witness')
        y=record[1];b=sum(c for U,c in n.items() if len(U)==2 and y in U)
        require(b>6,'false pair-trace witness');return kind,b
    require(kind in ('S','D','C'),'unknown witness type')
    require(len(record)==(3 if kind=='C' else 2) and type(record[1]) is int,'class witness format')
    tt,classes=components(n);available={C[0]:C for C in classes}
    require(record[1] in available,'unknown equality component');C=available[record[1]]
    if kind=='S':
        require(len({tt[i] for i in C})<len(C),'false duplicate-set witness');return kind,len(C)
    degree,codegrees=lower_counts(n,tt,C)
    if kind=='D':require(degree>20,'false exterior-degree witness');return kind,degree
    require(type(record[2]) is int and 0<=record[2]<6,'codegree witness point')
    value=codegrees[record[2]];require(value>6,'false codegree witness');return kind,value

def verify_certificate(cert,name,states=None,patterns=None):
    require(type(cert) is dict,'certificate object')
    expected={'schema':'E20_P10_LITERAL_GLUE_V1','profile':list(PROFILE[name]),'label':name,'mu':43,
              'center_degree':18,'outside_degree_cap':20,'pair_codegree_cap':6,'triple_codegree_cap':2,
              'subsets':[list(U) for U in SUB]}
    require(set(cert)==set(expected)|{'margin_patterns','state_count','domain_sha256','witnesses'},'certificate fields')
    for key,value in expected.items():require(cert[key]==value,'contract mismatch: '+key)
    if states is None:states,patterns=independent_states(PROFILE[name])
    require(type(cert['state_count']) is int and cert['state_count']==len(states),'state count')
    require(type(cert['margin_patterns']) is int and cert['margin_patterns']==patterns,'margin count')
    require(type(cert['witnesses']) is list and len(cert['witnesses'])==len(states),'complete witness coverage')
    # Digest is identity information only; every independently generated state is checked.
    digest=hashlib.sha256(bytes(v for state in states for v in state)).hexdigest()
    require(cert['domain_sha256']==digest,'domain serialization identity')
    cnt=Counter();ranges={}
    for v,w in zip(states,cert['witnesses']):
        k,q=verify_record(v,w);cnt[k]+=1
        if k not in ranges:ranges[k]=[q,q]
        else:ranges[k]=[min(q,ranges[k][0]),max(q,ranges[k][1])]
    return {'status':'PASS','profile':name,'margins':patterns,'states':len(states),'reasons':dict(sorted(cnt.items())),
            'witness_value_ranges':ranges,'nonempty_members_range':[min(map(sum,states)),max(map(sum,states))],
            'open':0,'domain_sha256':digest}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);a=ap.parse_args();start=time.monotonic()
    geo=fixed_geometry();out={'status':'PASS','geometry':geo,'certificates':[]}
    for name in PROFILE:
        path=ROOT/'certificates'/(name+'.json.gz');cert=json.loads(gzip.decompress(path.read_bytes()))
        out['certificates'].append(verify_certificate(cert,name))
    out['seconds']=time.monotonic()-start
    if a.output:
        require(not a.output.exists(),'refuse to overwrite output');a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
