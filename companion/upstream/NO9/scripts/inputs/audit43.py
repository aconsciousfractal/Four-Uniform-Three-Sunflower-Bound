"""Second exact anchor-domain enumerator, independent of local43.py.
It constructs rooted signatures with bit masks, tests external identifications
against all set partitions, and enumerates t before p. Universal classification
inputs are declared in docs/DEPENDENCIES.md; they are not re-proved by this code.
"""
from itertools import combinations,permutations,product
from fractions import Fraction
from functools import lru_cache
from collections import Counter
from pathlib import Path
import json,hashlib,argparse,time
PAIR_LIST=tuple(combinations(range(4),2))
TRIPLES=('012','015','023','034','045','124','134','135','235','245')
P_BITS=tuple(sum(1<<int(i) for i in t) for t in TRIPLES)
Q_BITS=tuple((1<<u)|sum(1<<a for a in A) for u in (0,1) for A in combinations((2,3,4),2))+(35,67)

def require(ok,msg):
    if not ok:raise ValueError(msg)

def bit_signatures():
    result={}
    for n in (8,9,10):
        fs=[tuple(P_BITS[i] for i in I) for I in combinations(range(10),n)]
        if n==8:fs.append(Q_BITS)
        sig=set()
        for family in fs:
            for R in family:
                pts=[i for i in range(7) if R>>i&1]
                for order in permutations(pts):
                    sig.add(tuple(sum(B&R==1<<v for B in family) for v in order)+tuple(sum(B&R==R^(1<<v) for B in family) for v in order))
        result[n]=frozenset(sig)
    require([len(result[n]) for n in (8,9,10)]==[21,6,1],'signature census')
    return result
SIGNATURES=bit_signatures()

def partition_masks():
    out=set()
    for tags in product(range(4),repeat=4):
        out.add(sum(1<<j for j,(u,v) in enumerate(PAIR_LIST) if tags[u]==tags[v]))
    require(len(out)==15,'Bell four')
    return tuple(out)
PARTITIONS=partition_masks()
@lru_cache(None)
def consistent(equal,different):
    return any(equal&mask==equal and different&mask==0 for mask in PARTITIONS)

@lru_cache(None)
def choices(alpha,tau,other_t,r10,r9,cap):
    k=1+sum(alpha)+sum(tau)
    allowed={17:((7,10),(8,9),(9,8),(10,7)),18:((8,10),(9,9),(10,8)),19:((9,10),(10,9)),20:((10,10),)}
    out=[]
    for s in range(11):
        d=k+s
        if d<1 or d>cap:continue
        if d>=17 and (s,k) not in allowed[d]:continue
        if s==10 and k<r10 or s==9 and k<r9:continue
        if s>=8:
            if sum(alpha)>6 or k>10:continue
            if any(weight>2 and flag for weight,flag in zip(alpha,tau)):continue
            if k>=9 and any(weight>2 for weight in alpha):continue
            if k in SIGNATURES and alpha+tau not in SIGNATURES[k]:continue
        out.append((s,d))
    return tuple(out)

def condition_global(p,t,s,k,d,mu):
    if sum(s)+sum(p)+sum(t)<mu-1:return False
    if sum(x>=19 for x in d)>2:return False
    if sum(p)+sum(t)>(12,14,17,19,22)[sum(x<8 for x in s)]:return False
    eq=0;neq=0
    for z,(i,j) in enumerate(PAIR_LIST):
        if p[z]==2 and t[i] and t[j] and s[i]>=8 and s[j]>=8:eq|=1<<z
        if t[i] and t[j] and any(s[x]>=8 and k[x]>=9 for x in range(4) if x not in (i,j)):neq|=1<<z
    return consistent(eq,neq)

def enumerate_rows(mu=44,r10=0,r9=0,cap=20,no_p10_17=False):
    rows=[]
    # A different outer order from the production enumerator; final sort fixes the digest gauge.
    for t in product(range(2),repeat=4):
        for p in product(range(4),repeat=6):
            C=[];K=[]
            for x in range(4):
                others=[i for i in range(4) if i!=x]
                alpha=tuple(p[PAIR_LIST.index(tuple(sorted((x,i))))] for i in others)
                tau=tuple(t[i] for i in others);K.append(1+sum(alpha)+sum(tau))
                C.append(tuple((s,d) for s,d in choices(alpha,tau,t[x],r10,r9,cap) if not(no_p10_17 and d==17 and s not in (8,9))))
            if any(not c for c in C):continue
            need=mu-1-sum(p)-sum(t)
            maxima=[max(s for s,d in c) for c in C]
            if sum(maxima)<need:continue
            def visit(i,ss,dd,tot):
                if i==4:
                    if condition_global(p,t,ss,K,dd,mu):rows.append(bytes(p+t+tuple(ss)))
                    return
                for s,d in C[i]:
                    if dd and d<dd[-1]:continue
                    if tot+s+sum(maxima[i+1:])<need:continue
                    visit(i+1,ss+[s],dd+[d],tot+s)
            visit(0,[],[],0)
    rows.sort();require(len(rows)==len(set(rows)),'duplicate canonical anchor row')
    return rows

def enumeration(mu=44,r10=0,r9=0,cap=20,no_p10_17=False):
    rows=enumerate_rows(mu,r10,r9,cap,no_p10_17)
    counts=Counter();degrees=set();best=Fraction(0);worst=[];hmax=0
    for row in rows:
        p=row[:6];t=row[6:10];s=row[10:]
        d=tuple(s[i]+1+sum(p[j] for j,e in enumerate(PAIR_LIST) if i in e)+sum(t)-t[i] for i in range(4))
        counts[d]+=1;degrees.update(d);hmax=max(hmax,1+sum(s)+sum(p)+sum(t))
        w=sum((Fraction(1,x) for x in d),Fraction(0))
        if w>best:best=w;worst=[d]
        elif w==best and d not in worst:worst.append(d)
    require(bool(rows),'empty domain')
    minimal=[d for d in counts if not any(e!=d and all(x<=y for x,y in zip(e,d)) for e in counts)]
    return {'rows':len(rows),'row_sha256':hashlib.sha256(b''.join(rows)).hexdigest(),'degree_profiles':len(counts),'degree_values':sorted(degrees),'min_degree':min(d[0] for d in counts),'min_pair_sum':min(d[0]+d[1] for d in counts),'min_anchor_degree_sum':min(map(sum,counts)),'max_neighbourhood':hmax,'max_reciprocal':str(best),'worst_profiles':sorted(worst),'minimal_profiles':sorted(minimal),'profile_counts':{','.join(map(str,d)):counts[d] for d in sorted(counts)}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mu',type=int,default=44);ap.add_argument('--r10',type=int,default=0);ap.add_argument('--r9',type=int,default=0);ap.add_argument('--cap-degree',type=int,default=20);ap.add_argument('--no-p10-17',action='store_true');ap.add_argument('--expect');ap.add_argument('--output');a=ap.parse_args()
    start=time.monotonic();v=enumeration(a.mu,a.r10,a.r9,a.cap_degree,a.no_p10_17)
    v=json.loads(json.dumps(v))
    if a.expect:
        old=json.loads(Path(a.expect).read_text())
        for key,value in v.items():
            if key=='worst_profiles':require(sorted(value)==sorted(old[key]),key)
            else:require(value==old[key],('enumerator disagreement',key))
    out={'status':'PASS','mu':a.mu,'r10':a.r10,'r9':a.r9,'cap_degree':a.cap_degree,'no_p10_17':a.no_p10_17,'result':v,'seconds':time.monotonic()-start}
    print(json.dumps({k:( {q:r for q,r in val.items() if q!='profile_counts'} if k=='result' else val) for k,val in out.items()},indent=2),flush=True)
    if a.output:Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
