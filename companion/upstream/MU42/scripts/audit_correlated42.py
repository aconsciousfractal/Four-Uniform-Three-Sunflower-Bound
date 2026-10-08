"""Separate reconstruction of joint exterior lower requirements.
Uses independent rooted signatures, t-before-p rows, and explicit level tests.
"""
from itertools import combinations,product
from functools import lru_cache
import audit_components42 as ac

def alternatives(m,kcap,r10,r9,mask):
    M=ac.P if m==10 else ac.P[1:]
    C=tuple(ac.QUADS[i] for i in range(15) if mask>>i&1)
    prescribed=tuple(T|{6} for T in M)+C
    link=[tuple(Q-{y} for Q in prescribed if y in Q) for y in range(6)]
    can_separate=[all(A&B for A,B in combinations(L,2)) for L in link]
    escape=[ac.escape(L) if can_separate[y] else 0 for y,L in enumerate(link)]
    out=[]
    for points,raw in table(m,kcap,r10,r9):
        A=frozenset(points)
        lowerS=[sum(Q&A=={y} for Q in C) for y in points]
        lowerP=[sum(Q&A==set(ab) for Q in C) for ab in combinations(points,2)]
        lowerT=sum(A<=Q for Q in C)
        relation={}
        for ds,ss,ks,ws,ee in raw:
            if ee<lowerT or any(x<y for x,y in zip(ss,lowerS)) or any(x<y for x,y in zip(ws,lowerP)):continue
            possible=True
            for i,y in enumerate(points):
                if ds[i]<len(link[y]):possible=False;break
                internal=sum(y in Q for Q in C)
                if sum(y in T for T in M)==5 and ds[i]>15+internal:possible=False;break
                if ss[i]>=8 or ds[i]>=17:
                    if not can_separate[y]:possible=False;break
                    ub=len(link[y])+ (escape[y] if ks[i]<8 else 0)
                    if ks[i]<len(link[y]) or ks[i]>ub:possible=False;break
                elif ks[i]<sum(bool(T&(A-{y})) for T in link[y]):possible=False;break
            if possible:
                lower=tuple(6 if s==8 else s if s>=9 else 0 for s in ss)
                relation.setdefault(ds,set()).add(lower)
        out.append((points,relation))
    return out
@lru_cache(None)
def table(m,k,r10,r9):return ac.base(ac.P if m==10 else ac.P[1:],k,r10,r9,42)

def refine(prior):
    m,k,r10,r9=(prior[j] for j in ('central_size','outside_cap','r10','r9'))
    # Enumerate all 4^6 possible rounded lower requirements, no bitset propagation.
    hs=[]
    for h in product((0,6,9,10),repeat=6):
        if max(h)==10 and sum(h)>20:continue
        if max(h)==9 and sum(h)>22:continue
        hs.append(h)
    states=[];opened=[]
    for interior in prior['survivors']:
        mask=interior['internal_mask'];rel=alternatives(m,k,r10,r9,mask)
        for record in interior['colorings']:
            ds=tuple(record['degrees']);poss=[]
            for A,R in rel:poss.append((A,R.get(tuple(ds[y] for y in A),set())))
            bits=0
            for j,h in enumerate(hs):
                accept=True
                for A,options in poss:
                    if not any(all(q<=h[y] for y,q in zip(A,lo)) for lo in options):accept=False;break
                if accept:bits+=2**j
            item={'internal_mask':mask,'degrees':list(ds),'H_bits':hex(bits),'H_count':bits.bit_count()}
            states.append(item)
            if bits:opened.append(item)
    return {'mu':42,'central_size':m,'outside_cap':k,'r10':r10,'r9':r9,'lower_levels':[0,6,9,10],
            'budget_vectors':len(hs),'input_states':len(states),'open_states':len(opened),'states':states,'open':opened}
