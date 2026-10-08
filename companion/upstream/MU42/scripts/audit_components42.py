"""Independent exact replay of the P10/P9 necessary-state reductions at mu42.
No import of component43.py/local43.py. Internal families are checked by
forbidden-mask enumeration; degree assignments by constraint backtracking.
Only the independently rebuilt local predicate in audit43.py is shared.
"""
from itertools import combinations,permutations,product
from pathlib import Path
from functools import lru_cache
import json,argparse,time,hashlib
from audit43 import choices,condition_global,PAIR_LIST,require,P_BITS,Q_BITS
ROOT=Path(__file__).resolve().parents[1]
P=tuple(frozenset(i for i in range(6) if b>>i&1) for b in P_BITS)
QUADS=tuple(frozenset(q) for q in combinations(range(6),4))

def sf(A,B,C):return A&B==A&C==B&C

def full_internal_masks(M):
    cone=tuple(A|{6} for A in M)
    forbidden=[]
    for k in (1,2,3):
        for J in combinations(range(15),k):
            q=tuple(QUADS[j] for j in J)
            if any(sf(*(q+f)) for f in combinations(cone,3-k)):forbidden.append(sum(1<<j for j in J))
    return [m for m in range(1<<15) if not any(m&bad==bad for bad in forbidden)]

def verify_small_inputs():
    # Cross-family 3-cover counts and the absence of a P5 spine inside Q8.
    autos=[p for p in permutations(range(6)) if {frozenset(p[i] for i in A) for A in P}==set(P)]
    block_orbit={frozenset(p[i] for i in P[0]) for p in autos}
    require(len(autos)==60 and block_orbit==set(P),'P10 automorphisms/omission transport')
    counts={}
    for m,M in ((10,P),(9,P[1:])):
        twocovers=[T for T in combinations(range(6),2) if all(set(T)&A for A in M)]
        threes=[T for T in combinations(range(6),3) if all(set(T)&A for A in M)]
        require(not twocovers,'unexpected 2-cover')
        require(len(threes)==(10 if m==10 else 11),'triple cover count')
        require(all(any(not(A&set(T)) for A in M) for T in combinations(range(6),2)),'pair avoidance')
        counts[m]={'three_covers':len(threes),'two_covers':0}
    Q=[frozenset(i for i in range(7) if b>>i&1) for b in Q_BITS]
    for x in range(7):
        edges={tuple(sorted(A-{x})) for A in Q if x in A}
        for order in permutations([i for i in range(7) if i!=x],5):
            require(not all(tuple(sorted(order[j:j+2])) in edges for j in range(4)),'Q8 contains P5 spine')
    return {'P10_automorphisms':60,'P10_block_orbit':10,'covers':counts,'Q8_P5_spines':0}

def base(M,kcap,r10,r9,mu=42):
    ans=[]
    for A in M:
        ordered=tuple(sorted(A));first=tuple(sum(B&A=={u} for B in M) for u in ordered)
        tau=tuple(sum(B&A==A-{u} for B in M) for u in ordered)
        rs=[]
        for e in (0,1):
            t=(e,*tau)
            for w in product(range(4),repeat=3):
                p=first+w;K=[];C=[]
                for i in range(4):
                    others=[j for j in range(4) if j!=i]
                    alpha=tuple(p[PAIR_LIST.index(tuple(sorted((i,j))))] for j in others)
                    pair=tuple(t[j] for j in others);K.append(1+sum(alpha)+sum(pair))
                    if i:C.append(choices(alpha,pair,t[i],r10,r9,20))
                for triples in product(*C):
                    s=(kcap,*(u[0] for u in triples));d=(kcap+K[0],*(u[1] for u in triples))
                    if min(d)<2 or any(d[i]+d[j]<20 for i,j in PAIR_LIST):continue
                    if not condition_global(p,t,s,K,d,mu):continue
                    rs.append((d[1:],s[1:],tuple(K[1:]),w,e))
        ans.append((ordered,rs))
    return ans

def escape(I):
    # The fixed complete x-link excludes new triples containing x=6.
    pts=set().union(*I)-{6}
    covers=[frozenset(T) for T in combinations(pts,2) if all(set(T)&A for A in I)]
    require(len(covers)<=1,'more than one P5/C5 two-cover')
    if not covers:return 0
    extras=[covers[0]|{z} for z in (7,8)]
    best=0
    for size in (1,2):
        for add in combinations(extras,size):
            family=tuple(I)+add
            if all(A&B for A,B in combinations(family,2)) and not any(sf(A,B,C) for A,B,C in combinations(family,3)):best=size
    return best

def degree_solutions(relations):
    domains=[set(range(2,21)) for _ in range(6)]
    for pts,relation in relations:
        for i,y in enumerate(pts):domains[y]&={v[i] for v in relation}
    if any(not d for d in domains):return []
    order=sorted(range(6),key=lambda y:len(domains[y]));assignment={};out=[]
    def rec(pos):
        if pos==6:
            d=tuple(assignment[i] for i in range(6));lower=[0]*6
            for pts,rel in relations:
                local=rel[tuple(d[i] for i in pts)]
                for i,y in enumerate(pts):lower[y]=max(lower[y],local[i])
            out.append((d,tuple(lower)));return
        y=order[pos]
        for v in sorted(domains[y]):
            assignment[y]=v
            valid=True
            for pts,rel in relations:
                if y not in pts:continue
                if not any(all(assignment[z]==key[i] for i,z in enumerate(pts) if z in assignment) for key in rel):valid=False;break
            if valid:rec(pos+1)
            del assignment[y]
    rec(0);return out

def run(m,kcap,r10,r9,mu=42):
    require(mu==42 and m in (9,10) and 0<=kcap<=7,"component interface scope")
    M=P if m==10 else P[1:]
    internal_masks=full_internal_masks(M);require(len(internal_masks)==(292 if m==10 else 373),'internal family count')
    B=base(M,kcap,r10,r9,mu)
    pre=0;survivors=[];decisions=[]
    for mask in internal_masks:
        C=[QUADS[i] for i in range(15) if mask>>i&1]
        family=tuple(A|{6} for A in M)+tuple(C)
        I={y:tuple(A-{y} for A in family if y in A) for y in range(6)}
        clean={y:all(A&B for A,B in combinations(I[y],2)) for y in range(6)}
        extra={y:escape(I[y]) if clean[y] else 0 for y in range(6)}
        rels=[]
        for pts,raw in B:
            A=frozenset(pts);internal_s=[sum(Q&A=={u} for Q in C) for u in pts]
            internal_p=[sum(Q&A==set(pair) for Q in C) for pair in combinations(pts,2)]
            internal_t=sum(A<=Q for Q in C);rel={}
            for d,s,k,w,e in raw:
                if e<internal_t or any(x<y for x,y in zip(w,internal_p)) or any(x<y for x,y in zip(s,internal_s)):continue
                valid=True;lb=[]
                for i,y in enumerate(pts):
                    if d[i]<len(I[y]):valid=False;break
                    if sum(y in T for T in M)==5 and d[i]-sum(y in Q for Q in C)>15:valid=False;break
                    if s[i]>=8 or d[i]>=17:
                        if not clean[y]:valid=False;break
                        maximum=len(I[y])+(extra[y] if k[i]<8 else 0)
                        if not len(I[y])<=k[i]<=maximum:valid=False;break
                    elif k[i]<sum(bool(T&(A-{y})) for T in I[y]):valid=False;break
                    lb.append({8:6,9:9,10:10}.get(s[i],0))
                if valid:
                    value=tuple(lb)
                    if d in rel:value=tuple(min(x,y) for x,y in zip(value,rel[d]))
                    rel[d]=value
            if not rel:break
            rels.append((pts,rel))
        if len(rels)!=len(M):decisions.append((mask,0,0));continue
        candidates=degree_solutions(rels);pre+=len(candidates);good=[]
        for d,lb in candidates:
            cap=20 if max(lb)>=10 else 22 if max(lb)>=9 else None
            if cap is not None and sum(lb)>cap:continue
            good.append({'degrees':d,'external_lower':lb,'external_cap':cap})
        decisions.append((mask,len(candidates),len(good)))
        if good:survivors.append({'internal_mask':mask,'colorings':sorted(good,key=lambda x:x['degrees'])})
    return {'mu':mu,'central_size':m,'outside_cap':kcap,'r10':r10,'r9':r9,'internal_count':len(internal_masks),'base_row_count':sum(len(v) for A,v in B),'pre_external_cap_colorings':pre,'remaining_colorings':sum(len(r['colorings']) for r in survivors),'remaining_internals':len(survivors),'survivors':survivors,'decisions_sha256':hashlib.sha256(json.dumps(decisions,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=10);ap.add_argument('--k',type=int,default=6);ap.add_argument('--r10',type=int,default=0);ap.add_argument('--r9',type=int,default=0);ap.add_argument('--expect');ap.add_argument('--output');a=ap.parse_args()
    start=time.monotonic();small=verify_small_inputs();out=json.loads(json.dumps(run(a.m,a.k,a.r10,a.r9)))
    if a.expect:
        old=json.loads(Path(a.expect).read_text())
        for k,v in out.items():
            if k=='decisions_sha256':continue
            require(v==old[k],('component checker disagreement',k))
    result={'status':'PASS','result':out,'small_inputs':small,'seconds':time.monotonic()-start}
    print(json.dumps(result,indent=2),flush=True)
    if a.output:Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
