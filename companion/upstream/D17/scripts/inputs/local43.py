"""Necessary anchor domains at arbitrary minimum closed-neighbourhood size.
Only universal inputs: FOUNDATIONS A--E; E17/E18 (explicitly imported).
No R45/N45/no18/support19 premises are used. Python integer arithmetic.
"""
from itertools import combinations,permutations,product
from fractions import Fraction
from functools import lru_cache
import hashlib,json,time,argparse
from pathlib import Path
P=tuple(frozenset(map(int,t)) for t in '012 015 023 034 045 124 134 135 235 245'.split())
Q=tuple(frozenset((u,*ab)) for u in (0,1) for ab in combinations((2,3,4),2))+(frozenset((0,1,5)),frozenset((0,1,6)))
PAIRS=tuple(combinations(range(4),2))
INC=tuple(tuple(j for j,p in enumerate(PAIRS) if i in p) for i in range(4))

def signatures():
    out={8:set(),9:set(),10:set()}
    for k in out:
        fams=[tuple(P[i] for i in I) for I in combinations(range(10),k)]
        if k==8:fams.append(Q)
        for F in fams:
            for A in F:
                for a in permutations(A):
                    out[k].add(tuple(sum(B&A=={v} for B in F) for v in a)+tuple(sum(B&A==A-{v} for B in F) for v in a))
    return {k:frozenset(v) for k,v in out.items()}
SIG=signatures()

def equality_consistent(p,t,s,k):
    parent=list(range(4))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    for w,(i,j) in zip(p,PAIRS):
        if w==2 and s[i]>=8 and s[j]>=8 and t[i] and t[j]:parent[root(i)]=root(j)
    for x in range(4):
        if s[x]>=8 and k[x]>=9:
            occ=[root(j) for j in range(4) if j!=x and t[j]]
            if len(occ)!=len(set(occ)):return False
    return True

@lru_cache(None)
def local_s_candidates(x,p,t,emin,r10,r9):
    T=sum(t);r=sum(p[j] for j in INC[x]);k=1+r+T-t[x]
    others=[j for j in range(4) if j!=x]
    alpha=tuple(p[PAIRS.index(tuple(sorted((x,j))))] for j in others)
    tau=tuple(t[j] for j in others)
    out=[]
    for s in range(11):
        d=s+k
        if not 1<=d<=20:continue
        if s==10 and k<r10:continue
        if s==9 and k<r9:continue
        # Universal separated links for d=17/18 and C1 for 19/20.
        if d>=emin and d>=17 and not ((d==17 and (s,k) in ((7,10),(8,9),(9,8),(10,7))) or (d==18 and (s,k) in ((8,10),(9,9),(10,8))) or (d==19 and (s,k) in ((9,10),(10,9))) or (d==20 and (s,k)==(10,10))):continue
        if s>=8:
            if r>6 or k>10:continue
            if any(tj and a>2 for a,tj in zip(alpha,tau)):continue
            if k>=9 and max(alpha)>2:continue
            if k in SIG and alpha+tau not in SIG[k]:continue
        out.append(s)
    return tuple(out)

def enumerate_rows(mu=44,emin=17,r10=0,r9=0,cap_degree=20,no_p10_17=False):
    for p in product(range(4),repeat=6):
        Psum=sum(p)
        for t in product(range(2),repeat=4):
            T=sum(t);k=tuple(1+sum(p[j] for j in INC[x])+T-t[x] for x in range(4))
            cs=[tuple(s for s in local_s_candidates(x,p,t,emin,r10,r9) if s+k[x]<=cap_degree and not(no_p10_17 and s+k[x]==17 and s not in (8,9))) for x in range(4)]
            if any(not c for c in cs):continue
            need=mu-1-Psum-T
            if sum(c[-1] for c in cs)<need:continue
            for s0 in cs[0]:
                for s1 in cs[1]:
                    if s1+k[1]<s0+k[0]:continue
                    for s2 in cs[2]:
                        if s2+k[2]<s1+k[1]:continue
                        min_s3=max(s2+k[2]-k[3],need-s0-s1-s2)
                        for s3 in cs[3]:
                            if s3<min_s3:continue
                            s=(s0,s1,s2,s3);d=tuple(a+b for a,b in zip(s,k))
                            if sum(v>=19 for v in d)>2:continue
                            q=sum(v<8 for v in s)
                            if Psum+T>(12,14,17,19,22)[q]:continue
                            if not equality_consistent(p,t,s,k):continue
                            yield p+t+s

def summarize(rows):
    count=0;profiles={};degrees=set();mind=20;minpair=40;minsum=80;hmax=0
    hash=hashlib.sha256();maxrec=Fraction(0);worst=[]
    for row in rows:
        p=row[:6];t=row[6:10];s=row[10:];T=sum(t)
        k=tuple(1+sum(p[j] for j in INC[x])+T-t[x] for x in range(4))
        d=tuple(a+b for a,b in zip(s,k));count+=1;hash.update(bytes(row))
        profiles[d]=profiles.get(d,0)+1;degrees.update(d)
        mind=min(mind,d[0]);minpair=min(minpair,d[0]+d[1]);minsum=min(minsum,sum(d));hmax=max(hmax,1+sum(s)+sum(p)+T)
        rec=sum((Fraction(1,a) for a in d),Fraction(0))
        if rec>maxrec:maxrec=rec;worst=[d]
        elif rec==maxrec and d not in worst:worst.append(d)
    minima=[d for d in profiles if not any(e!=d and all(a<=b for a,b in zip(e,d)) for e in profiles)]
    return {'rows':count,'row_sha256':hash.hexdigest(),'degree_profiles':len(profiles),'degree_values':sorted(degrees),'min_degree':mind,'min_pair_sum':minpair,'min_anchor_degree_sum':minsum,'max_neighbourhood':hmax,'max_reciprocal':str(maxrec),'worst_profiles':worst,'minimal_profiles':sorted(minima),'profile_counts':{','.join(map(str,d)):profiles[d] for d in sorted(profiles)}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mu',type=int,default=44);ap.add_argument('--r10',type=int,default=0);ap.add_argument('--r9',type=int,default=0);ap.add_argument('--cap-degree',type=int,default=20);ap.add_argument('--no-p10-17',action='store_true');ap.add_argument('--output');a=ap.parse_args()
    start=time.monotonic();out=summarize(enumerate_rows(a.mu,r10=a.r10,r9=a.r9,cap_degree=a.cap_degree,no_p10_17=a.no_p10_17))
    out.update({'mu':a.mu,'r10_min_k':a.r10,'r9_min_k':a.r9,'degree_cap':a.cap_degree,'no_p10_17':a.no_p10_17,'seconds':time.monotonic()-start,'signature_counts':{k:len(v) for k,v in SIG.items()},'status':'NECESSARY_DOMAIN_ENUMERATED'})
    print(json.dumps({k:v for k,v in out.items() if k!='profile_counts'},indent=2))
    if a.output:Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
