"""Literal finite corroboration of the covering lemma with pure triple exceptions.
The proof treats an arbitrary outside support; fresh symbols below encode traces.
"""
from itertools import combinations
from common import need,main,ROOT,dump
P=tuple(frozenset(map(int,s)) for s in '012 015 023 034 045 124 134 135 235 245'.split())

def sunflower(a,b,c):return a&b==a&c==b&c

def family_check(ff):
    need(all(len(q)==4 for q in ff) and len(ff)==len(set(ff)),'simple quadruples')
    count=0
    for a,b,c in combinations(ff,3):
        need(not sunflower(a,b,c),'positive control has sunflower');count+=1
    return count

def run():
    roots=[];tot=outcov=exceptions=0
    for k1,k2 in ((10,10),(10,9),(9,9)):
        H1=P if k1==10 else P[1:];H2=P if k2==10 else P[1:]
        H2=tuple(frozenset(v+6 for v in t) for t in H2)
        L=H1+H2;known=tuple(t|{22} for t in L)
        # Compute every exceptional pure triple directly from its missing cone witness.
        bad={}
        for side,H in enumerate((H1,H2)):
            S=set(range(6*side,6*side+6))
            for y in sorted(S):
                bs=[frozenset(U) for U in combinations(sorted(S),3) if y in U and not any(t&set(U)=={y} for t in H)]
                need(len(bs)==(1 if len(H)==9 and y%6 in (0,1,2) else 0),'P5 unique exception')
                need(all(U not in H for U in bs),'exception triple has no fixed extension')
                bad[y]=bs
        pure=[frozenset(U) for S in (range(6),range(6,12)) for U in combinations(S,3)]
        cores=[frozenset(U) for r in range(3) for U in combinations(range(12),r)]+pure
        root_count=root_exception=root_forbidden=0
        for y in range(6):
            for z in range(6,12):
                M=frozenset((y,z,12,13));exception_triples=set(bad[y]+bad[z])
                for C in cores:
                    for r in range(min(2,4-len(C))+1):
                        for A in combinations((12,13),r):
                            Q=C|frozenset(A)|frozenset(range(100,100+4-len(C)-r))
                            root_count+=1
                            if {y,z}<=Q or Q&{12,13}:continue
                            witnesses=[R for R in known if sunflower(R,M,Q)]
                            if not witnesses:
                                need(C in exception_triples and len(C)==3,'uncovered non-exception')
                                root_exception+=1
                            else:
                                need(C not in exception_triples,'exception unexpectedly forbidden by marked cone')
                                root_forbidden+=1
        roots.append({'components':[k1,k2],'trace_cases':root_count,'outside_cover_with_sunflower':root_forbidden,'exception_traces':root_exception,'exception_triples':{str(v):[sorted(U) for U in ss] for v,ss in bad.items()},'universal_residual_cap':f'2*Delta+4+2*e, e<= {int(k1==9)+int(k2==9)}'})
        tot+=root_count;exceptions+=root_exception;outcov+=root_forbidden
    # Concrete exception: the missing P9 cone is genuinely absent.
    fixed=tuple(t|{22} for t in P)+tuple(frozenset(v+6 for v in t)|{22} for t in P[1:])
    M=frozenset((0,6,12,13));Q1=frozenset((6,9,11,14));Q2=frozenset((6,9,11,15))
    F=fixed+(M,Q1,Q2);ternas=family_check(F)
    need(not {0,6}<=Q1 and not Q1&{12,13},'example outside old cover')
    need(Q1&set(range(12))==Q2&set(range(12))=={6,9,11},'two exceptional extensions')
    data={'components':[10,9],'center':22,'family':[sorted(q) for q in F],'mu':min(sum(bool(q&r) for r in F) for q in F)}
    stored=ROOT/'data/POSITIVE_TWO_EXCEPTIONS.json'
    need(stored.exists() and __import__('json').loads(stored.read_text())==data,'positive fixture differs')
    need(50>2*19+4+2,'cover cap at F69 max19')
    return {'status':'PASS','roots':roots,'trace_cases':tot,'outside_cover_forbidden':outcov,'exception_traces':exceptions,'max_F69_D19_mixed_residuals':44,'required_residuals':50,'positive_control_members':len(F),'positive_control_ternas':ternas,'positive_mu':data['mu'],'no_support_bound_in_cover_lemma':True}
if __name__=='__main__':main(run)
