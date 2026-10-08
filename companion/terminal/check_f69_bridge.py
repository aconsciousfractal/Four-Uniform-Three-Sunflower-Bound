"""Exact finite verification of the written F69 fibre/quasi bridge.

This bounded reconstruction uses no imported producer, solver or stored fibre
output. The support reduction for quasi-transversals is a written theorem,
not inferred from this finite check. It follows the set-based reconstruction
method retained in the September30 cross-review; no human independence claim.
"""
from itertools import combinations,product,permutations
import json

P={frozenset(map(int,t)) for t in '012 015 023 034 045 124 134 135 235 245'.split()}
Q={frozenset(map(int,t)) for t in '023 024 034 123 124 134 015 016'.split()}

def require(x,m):
    if not x:raise ValueError(m)

def canonical(v):
    n=len(v);return min(tuple(v[(s*i+o)%n] for i in range(n)) for s in (1,-1) for o in range(n))

def fibres(k):
    n=3*k-1;neighbours=[{j for j in range(n) if k<=(j-i)%n<=2*k-1} for i in range(n)]
    # b_i=27-delta_i; delta in 0..2, sum(delta)=27(3k-1)-69k.
    reps=sorted({canonical(v) for v in product(range(3),repeat=n) if sum(v)==27*n-69*k})
    records=[];exceptions=[]
    for pid,delta in enumerate(reps):
        a=tuple(12-delta[i]-delta[(i+k)%n]-delta[(i+2*k-1)%n] for i in range(n));r=tuple(2-d for d in delta)
        require(sum(a)==69 and all(sum(a[j] for j in neighbours[i])==27-delta[i] for i in range(n)),'fibre algebra')
        for mask in range(1,1<<n):
            I={i for i in range(n) if mask>>i&1};nonisolated={i for i in I if neighbours[i]&I}
            if not nonisolated or any(len(neighbours[i]&I)>r[i] for i in I):continue
            coordinates=sorted(I);t=[0]*n
            def visit(pos,left):
                if pos==len(coordinates):
                    if left or any(sum(t[j] for j in neighbours[i])>r[i] for i in I):return
                    J={j for j in range(n) if not neighbours[j]&I};B=sum(a[j]-t[j] for j in J)
                    require(B>=1,'missing full transversal')
                    records.append((pid,tuple(t),B))
                    if B==1:
                        witnesses=[i for i in range(n) if sum(t[j] for j in neighbours[i])==1 and a[i]-t[i]>=9]
                        require(witnesses,'exception lacks nine quasi-transversals')
                        exceptions.append({'profile':pid,'t':list(t),'J':sorted(J),'witness':witnesses[0],'external_members':a[witnesses[0]]-t[witnesses[0]]})
                    return
                i=coordinates[pos];maximum=min(2 if i in nonisolated else a[i],left-(len(coordinates)-pos-1))
                for v in range(1,maximum+1):t[i]=v;visit(pos+1,left-v)
                t[i]=0
            visit(0,16)
    return {'profiles':len(reps),'nonindependent_vectors':len(records),'exceptional_vectors':len(exceptions),'exceptional_profile_count':len({e['profile'] for e in exceptions}),'missing_witnesses':0,'witnesses':exceptions}

def relabel(H,mapping):return {frozenset(mapping[v] for v in t) for t in H}

def local_tables():
    star=P-{frozenset((0,1,2)),frozenset((0,1,5))};models=[]
    models.append((star,relabel(star,{v:v+6 for v in range(6)})))
    models.append((star,relabel(Q,{v:v+6 for v in range(7)})))
    for overlap in (0,1,2):
        mapping={v:v+7 for v in range(5)};mapping[5]=5 if overlap>=1 else 12;mapping[6]=6 if overlap==2 else 13
        models.append((Q,relabel(Q,mapping)))
    cases=nonempty=0;maximum=0
    for H,K in models:
        L=H|K;W=sorted(set().union(*L));require(len(L)==16,'local model size')
        full=[frozenset(c) for c in combinations(W,4) if all(set(c)&t for t in L)]
        require(len(full)==1,'B4 full transversal uniqueness')
        for t in L:
            found=[frozenset(c) for c in combinations(W,4) if not set(c)&t and all(set(c)&u for u in L-{t})]
            cases+=1;nonempty+=bool(found);maximum=max(maximum,len(found));require(len(found)<=1,'quasi-transversal counterexample')
    covering=[]
    for omitted in combinations(P,2):
        H=P-set(omitted);covers=[c for c in combinations(range(6),2) if all(set(c)&t for t in H)]
        require(bool(covers)==(len(omitted[0]&omitted[1])==2),'P8 covering reduction')
        if covers:covering.append(H)
    aut=[p for p in permutations(range(6)) if relabel(P,p)==P]
    require(len(aut)==60 and len(covering)==15,'P10 automorphism/covers')
    orbit={frozenset(relabel(star,p)) for p in aut};require(orbit==set(map(frozenset,covering)),'Pstar orbit coverage')
    return {'models':5,'omission_cases':cases,'nonempty_quasi_sets':nonempty,'maximum_quasi_sets':maximum,'P8_covering_models':15,'P10_automorphisms':60}

def main():
    a3,a4=fibres(3),fibres(4);table=local_tables()
    require((a3['profiles'],a4['profiles'])==(70,1),'profile census')
    require(a3['nonindependent_vectors']+a4['nonindependent_vectors']==1293,'point-vector census')
    require(a3['exceptional_vectors']==52 and a4['exceptional_vectors']==0 and a3['exceptional_profile_count']==23,'exception census')
    require(table['omission_cases']==80 and table['nonempty_quasi_sets']==54,'local table census')
    print(json.dumps({'status':'PASS_F69_FIBRE_QUASI_BRIDGE','A3':a3,'A4':a4,'quasi_table':table},sort_keys=True,indent=2))

if __name__=='__main__':main()
