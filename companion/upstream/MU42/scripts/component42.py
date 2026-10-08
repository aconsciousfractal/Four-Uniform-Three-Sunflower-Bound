"""Exact finite necessary-state analysis of a P10/P9 component at mu=42.
Finite necessary-state generator. The imported geometry and proof order are in PROOF.md. No bound on the outside support is imposed.
"""
from itertools import combinations,product
from functools import lru_cache
from pathlib import Path
import json,time,argparse
from local43 import P,SIG,PAIRS,INC,equality_consistent,local_s_candidates
QUADS=tuple(frozenset(t) for t in combinations(range(6),4))

def sunflower(a,b,c):return a&b==a&c==b&c

def internals(M):
    fixed=tuple(A|{6} for A in M);out=[]
    def rec(j,C,F,mask):
        out.append((mask,tuple(C)))
        for i in range(j,15):
            q=QUADS[i]
            if any(sunflower(q,a,b) for a,b in combinations(F,2)):continue
            rec(i+1,C+[q],F+[q],mask|1<<i)
    rec(0,[],list(fixed),0)
    return sorted(out)

@lru_cache(None)
def escape_capacity(I):
    """All extra triples external to 7-point U meeting all fixed I.
    For C5 no escape; for P5 the unique 2-cover plus one external point.
    Two external points suffice since the common 2-cover has codegree <=2.
    """
    I=tuple(frozenset(a) for a in I)
    vs=set().union(*I);paircovers=[ab for ab in combinations(vs-{6},2) if all(set(ab)&t for t in I)]
    cand=[frozenset((*ab,z)) for ab in paircovers for z in (7,8)]
    # The C5/P5 spine leaves zero/one possible pair cover; checked in run.
    if len(paircovers)>1:raise ValueError(('spine pair covers',paircovers))
    ans=0
    for n in range(len(cand)+1):
        for extra in combinations(cand,n):
            F=I+extra
            if all(a&b for a,b in combinations(F,2)) and not any(sunflower(a,b,c) for a,b,c in combinations(F,3)):ans=max(ans,n)
    return ans


def base_rows(M,kcap,mu=42,r10=0,r9=0):
    result=[]
    for A0 in M:
        A=tuple(sorted(A0))
        alpha=tuple(sum(B&A0=={y} for B in M) for y in A)
        tau=tuple(sum(B&A0==A0-{y} for B in M) for y in A)
        recs=[]
        for w in product(range(4),repeat=3):
            p=alpha+w
            for e in (0,1):
                t=(e,*tau);T=sum(t);ks=tuple(1+sum(p[j] for j in INC[i])+T-t[i] for i in range(4))
                cs=[local_s_candidates(i,p,t,17,r10,r9) for i in (1,2,3)]
                for ss in product(*cs):
                    s=(kcap,*ss)
                    if sum(s)+sum(p)+T<mu-1:continue
                    ds=tuple(a+b for a,b in zip(s,ks))
                    # Universal baseline at mu42: minimum degree2, used-pair sum20, independently verified later.
                    if min(ds)<2 or any(ds[i]+ds[j]<20 for i,j in PAIRS):continue
                    if sum(d>=19 for d in ds)>2:continue
                    if sum(p)+T>(12,14,17,19,22)[sum(v<8 for v in s)]:continue
                    if not equality_consistent(p,t,s,ks):continue
                    recs.append((tuple(ds[1:]),tuple(ss),tuple(ks[1:]),w,e))
        result.append((A,recs))
    return result


def run(m=10,kcap=6,mu=42,r10=0,r9=0):
    if mu!=42 or m not in (9,10) or not 0<=kcap<=7:
        raise ValueError("This certified component interface is limited to mu42, m9/10, k0..7")
    start=time.monotonic();M=P if m==10 else P[1:]
    bases=base_rows(M,kcap,mu,r10,r9);ints=internals(M)
    survivors=[];colorings_total=0;precap_total=0;row_total=sum(len(r) for a,r in bases);counts=[]
    for mask,C in ints:
        Ufamily=tuple(A|{6} for A in M)+C
        links={y:tuple(sorted(tuple(sorted(q-{y})) for q in Ufamily if y in q)) for y in range(6)}
        clean={y:all(set(a)&set(b) for a,b in combinations(links[y],2)) for y in range(6)}
        esc={y:escape_capacity(links[y]) if clean[y] else 0 for y in range(6)}
        relations=[]
        for A,rs in bases:
            aset=frozenset(A)
            sint=tuple(sum(q&aset=={y} for q in C) for y in A)
            wint=tuple(sum(q&aset==set(ab) for q in C) for ab in combinations(A,2))
            eint=sum(q&aset==aset for q in C)
            rel={}
            for d,s,k,w,e in rs:
                if e<eint or any(a<b for a,b in zip(s,sint)) or any(a<b for a,b in zip(w,wint)):continue
                ok=True;lower=[]
                for i,y in enumerate(A):
                    if d[i]<len(links[y]):ok=False;break
                    # Universal empty-C5 obstruction after deleting internal triples.
                    if sum(y in A0 for A0 in M)==5 and d[i]-sum(y in q0 for q0 in C)>15:ok=False;break
                    controlled=s[i]>=8 or d[i]>=17
                    if controlled:
                        if not clean[y]:ok=False;break
                        cap=len(links[y])+esc[y]
                        # The size>=8 P8/Q8/P9/P10 classification confines K for P5.
                        if k[i]>=8:cap=len(links[y])
                        if not len(links[y])<=k[i]<=cap:ok=False;break
                    else:
                        # Every internal triple intersects the anchor unless it contributes to s.
                        near=sum(bool(set(t)&(aset-{y})) for t in links[y])
                        if k[i]<near:ok=False;break
                    lower.append(10 if s[i]==10 else 9 if s[i]==9 else 6 if s[i]==8 else 0)
                if not ok:continue
                if d in rel:rel[d]=tuple(min(a,b) for a,b in zip(rel[d],lower))
                else:rel[d]=tuple(lower)
            if not rel:break
            relations.append((A,rel))
        if len(relations)!=len(M):continue
        # Join ternary relations with one degree for each of six points.
        colors={(-1,)*6:(0,)*6}
        for A,rel in sorted(relations,key=lambda v:len(v[1])):
            nex={}
            for col,lb in colors.items():
                for d,l in rel.items():
                    if any(col[y]!=-1 and col[y]!=d[i] for i,y in enumerate(A)):continue
                    c=list(col);b=list(lb)
                    for i,y in enumerate(A):c[y]=d[i];b[y]=max(b[y],l[i])
                    cc=tuple(c);bb=tuple(b)
                    if cc in nex:nex[cc]=tuple(min(a,b) for a,b in zip(nex[cc],bb))
                    else:nex[cc]=bb
            colors=nex
            if not colors:break
        precap_total+=len(colors)
        good=[]
        for col,lb in colors.items():
            cap=20 if max(lb)>=10 else 22 if max(lb)>=9 else 10**6
            if sum(lb)>cap:continue
            good.append({'degrees':col,'external_lower':lb,'external_cap':None if cap==10**6 else cap})
        if good:survivors.append({'internal_mask':mask,'colorings':sorted(good,key=lambda x:x['degrees'])});colorings_total+=len(good)
        counts.append((mask,len(colors),len(good)))
    out={'status':'EXCLUDED_NECESSARY_STATES' if not survivors else 'OPEN_NECESSARY_STATES','mu':mu,'central_size':m,'outside_cap':kcap,'r10':r10,'r9':r9,'internal_count':len(ints),'base_row_count':row_total,'pre_external_cap_colorings':precap_total,'remaining_colorings':colorings_total,'remaining_internals':len(survivors),'survivors':survivors,'seconds':time.monotonic()-start}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,default=10);p.add_argument('--k',type=int,default=6);p.add_argument('--mu',type=int,default=42);p.add_argument('--r10',type=int,default=0);p.add_argument('--r9',type=int,default=0);p.add_argument('--output');a=p.parse_args()
    out=run(a.m,a.k,a.mu,a.r10,a.r9);print(json.dumps({k:v for k,v in out.items() if k!='survivors'},indent=2),flush=True)
    if a.output:Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
