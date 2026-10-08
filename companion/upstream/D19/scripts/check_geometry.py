"""Complete finite covers and terminal coefficient check, using sets and signatures."""
from itertools import combinations,permutations
from collections import Counter
from functools import lru_cache
import json
from common import ROOT,need,main
import geometry as producer

P=tuple(frozenset(map(int,s)) for s in '012 015 023 034 045 124 134 135 235 245'.split())
P9=P[1:]

def autos(H):
    hh=set(H)
    return tuple(p for p in permutations(range(6)) if {frozenset(p[v] for v in T) for T in H}==hh)

def p10_interiors():
    q=tuple(map(frozenset,combinations(range(6),4)));fixed=tuple(T|{22} for T in P)
    need(not any(a&b==a&c==b&c for a,b,c in combinations(fixed,3)),'prescribed sunflower')
    cand=fixed+q;bad=set()
    for ids in combinations(range(len(cand)),3):
        a,b,c=(cand[i] for i in ids)
        if a&b==a&c==b&c:
            mask=sum(1<<(i-len(fixed)) for i in ids if i>=len(fixed));need(mask>0,'fixed contradiction');bad.add(mask)
    # All binary choices; no prefix search or producer catalogue is used.
    fam={tuple(tuple(sorted(q[i])) for i in range(15) if m>>i&1) for m in range(1<<15) if all(m&b!=b for b in bad)}
    aut=autos(P);todo=set(fam);reps=[];sizes=[]
    while todo:
        rep=min(todo,key=lambda x:(len(x),x))
        orb={tuple(sorted(tuple(sorted(p[v] for v in Q)) for Q in rep)) for p in aut}
        need(orb<=todo,'interior orbit disjointness');todo-=orb
        reps.append({'representative':[list(Q) for Q in rep],'orbit_size':len(orb)});sizes.append(len(orb))
    return fam,reps,len(bad)

def run():
    from contract import validate_index
    validate_index()
    au,av=autos(P),autos(P9);need((len(au),len(av))==(60,6),'automorphisms')
    @lru_cache(None)
    def canonical(U,side):
        aa=au if side==0 else av
        return min(tuple(sorted(p[v] for v in U)) for p in aa)
    allq=list(combinations(range(22),4));part={}
    for Q in allq:
        key=(canonical(tuple(v for v in Q if v<6),0),canonical(tuple(v-6 for v in Q if 6<=v<12),1),sum(v>=12 for v in Q))
        part.setdefault(key,set()).add(Q)
    def orb(q):
        key=(canonical(tuple(v for v in q if v<6),0),canonical(tuple(v-6 for v in q if 6<=v<12),1),sum(v>=12 for v in q))
        return part[key]
    source=json.loads((ROOT/'data/ORBIT_CATALOGUE.json').read_text())
    need(source['internals']==producer.catalogue('internal') and source['external']==producer.catalogue('external'),'producer tables')
    for kind,rows in (('internal',source['internals']),('external',source['external'])):
        seen=set()
        for row in rows:
            Q=tuple(row['mark']);o=orb(Q);need(o==producer.orbit(Q),'literal orbit cover')
            need(not seen&o and len(o)==row['size'],'size and disjointness');seen|=o
        target={Q for Q in allq if (max(Q)<6 or min(Q)>=6 and max(Q)<12)} if kind=='internal' else {Q for Q in allq if not(max(Q)<6 or min(Q)>=6 and max(Q)<12) and sum(v>=12 for v in Q)<=1}
        need(seen==target,'complete orbit union')
    # Three individual P9 exclusions leave a seven-element interior domain.
    covered=set().union(*(orb(row['mark']) for row in source['internals'][1:4]))
    remain={Q for Q in allq if min(Q)>=6 and max(Q)<12}-covered
    need(remain=={(u,9,10,11) for u in (6,7,8)},'last P9 orbit')
    choices=[tuple(c) for k in range(3) for c in combinations(sorted(remain),k)]
    need(len(choices)==7,'P9 codegree cap permits precisely seven choices')
    for k in range(3):
        rep=choices[0] if k==0 else tuple(sorted(remain))[:k]
        images={tuple(sorted(tuple(sorted(6+p[v-6] for v in Q)) for Q in rep)) for p in av}
        need(images=={c for c in choices if len(c)==k},'all P9 assignments by size')
    fam,reps,bad_count=p10_interiors()
    cat=json.loads((ROOT/'data/P10_FULL_INTERIOR_CATALOGUE.json').read_text())
    need(cat=={'labelled':292,'classes':reps},'P10 assigned catalogue')
    need(len(fam)==292 and len(reps)==13 and reps[0]['representative']==[],'P10 complete counts')
    # Main proof intentionally keeps the two pure-triple orbits E24 and E26.
    excluded_int=set().union(*(orb(row['mark']) for row in source['internals']))
    external_rows=[r for r in source['external'] if r['id'] not in ('E24','E26')]
    excluded_ext=set().union(*(orb(r['mark']) for r in external_rows))
    allowed=set(allq)-excluded_int-excluded_ext
    need(len(excluded_int)==30 and len(excluded_ext)==2605,'primary cover counts')
    exceptions={tuple(r['mark']) for r in source['external'] if r['id'] in ('E24','E26')}
    kept_large=set().union(*(orb(q) for q in exceptions))
    need({q for q in allowed if sum(v<12 for v in q)>=3}==kept_large and len(kept_large)==60,'only allowed large traces')
    need(all(sum(v<6 for v in q)==0 and sum(6<=v<12 for v in q)==3 for q in kept_large),'pure P9 triples')
    mixed={q for q in allowed if sum(v<6 for v in q)==1 and sum(6<=v<12 for v in q)==1 and sum(v>=12 for v in q)==2}
    need(len(mixed)==1620,'mixed domain')
    terminal=allowed-mixed;need(len(terminal)==3060,'terminal full universe')
    L=tuple(P)+tuple(frozenset(v+6 for v in T) for T in P9)
    special=(frozenset((6,7,11)),frozenset((6,8,9)),frozenset((7,8,10)))
    need(all(U in L for U in special),'three special fixed triples')
    histogram=Counter()
    for q in terminal:
        Q=set(q);k=sum(not Q&T for T in L);histogram[k]+=1
        # Sum 19 H27 rows and these three pairwise-distinct triple-cap rows.
        coefficient=k+sum(U<=Q for U in special)
        need(coefficient>=11,'terminal coefficient')
        if k<11:need(k==10 and any(U<=Q for U in special),'exact deficit class')
    need(dict(histogram)=={10:30,11:840,12:540,14:1080,15:360,19:210},'terminal histogram')
    terminal_cert=json.loads((ROOT/'data/TERMINAL.json').read_text())
    expected={'schema':'E20_F69_D19_TERMINAL_V1','H27_anchor_weights':[1]*19,'extra_triple_caps':[[[6,7,11],1,1],[[6,8,9],1,1],[[7,8,10],1,1]],'terminal_column_count':3060,'minimum_column_coefficient':11,'combined_rhs':516,'required_residuals':50,'deficit_required':37,'deficit_upper':3,'global_bound_unchanged':[54,69]}
    need(terminal_cert==expected,'terminal certificate binding')
    need(11*50-3>19*27,'strict terminal contradiction')
    return {'status':'PASS','automorphism_orders':[60,6],'internal_marked_orbits':5,'initial_P9_excluded':12,'P9_remaining_assignments':7,'P10_labelled_interiors':len(fam),'P10_full_orbits':len(reps),'P10_forbidden_patterns':bad_count,'P10_sizes':dict(sorted(Counter(map(len,fam)).items())),'external_orbits_total':28,'external_orbits_used':26,'primary_external_quads':len(excluded_ext),'universe':len(allq),'large_traces_retained':60,'mixed_excluded_by_lemma':1620,'terminal_quads':3060,'kappa_histogram':dict(sorted(histogram.items())),'deficit_required':37,'deficit_upper':3,'required_disjoint_pairs':547,'capacity':513,'terminal_upper_residuals':'516/11'}
if __name__=='__main__':main(run)
