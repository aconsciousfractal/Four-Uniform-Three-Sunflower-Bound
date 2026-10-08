"""Supplementary exact controls for the written structural/global proofs."""
from itertools import combinations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
class Invalid(Exception):pass
def req(x,s):
    if not x:raise Invalid(s)
def sf(a,b,c):return a&b==a&c==b&c
def sunflower_free(F):return len(set(F))==len(F) and not any(sf(a,b,c) for a,b,c in combinations(F,3))
def components(faces,shared):
    todo=set(range(len(faces)));out=[]
    while todo:
        todo1=[todo.pop()];C=[]
        while todo1:
            i=todo1.pop();C.append(i)
            hit=[j for j in todo if len(faces[i]&faces[j])==shared]
            for j in hit:todo.remove(j);todo1.append(j)
        out.append(C)
    return out

def verify():
    L=[frozenset((h,)+e) for hubs,D in [((0,1),(4,5,6)),((2,3),(7,8,9))] for h in hubs for e in combinations(D,2)]+[frozenset(t) for t in combinations(range(4),3)]
    req(len(L)==16 and sunflower_free(L),'R16 positive')
    W=set().union(*L);degrees=sorted(sum(v in a for a in L) for v in W)
    disj=Counter(sum(a.isdisjoint(b) for b in L) for a in L)
    req(degrees==[4]*6+[6]*4 and disj=={3:4,7:12},'R16 incidence')
    usedpairs={p for a in L for p in combinations(sorted(a),2)}
    req(len(usedpairs)==24 and all(sum(set(p)<=a for a in L)==2 for p in usedpairs),'R16 pair regularity')
    cs=components(L,2);req(sorted(map(len,cs))==[4,6,6],'R16 sectors')
    sector_stats=[]
    for C in cs:
        faces=[L[i] for i in C];V=set().union(*faces)
        deg=sorted(sum(v in a for a in faces) for v in V)
        req((len(faces),len(V),deg) in [(4,4,[3]*4),(6,5,[3,3,4,4,4])],'sector shape')
        # Connected link of each vertex within each sector makes normalization valid.
        for v in V:
            lk=[a-{v} for a in faces if v in a]
            req(len(components(lk,1))==1,'disconnected sector link')
        sector_stats.append({'faces':len(faces),'vertices':len(V),'triangle_degrees':deg})
    # Core-six trace reduction used in section 5.
    H=[frozenset((h,)+e) for h in (0,1) for e in combinations((2,3,4),2)]
    allow=[]
    for k in (1,2,3):
        for q in combinations(range(5),k):
            Q=frozenset(q)
            if Q in H:continue
            if not any(sf(a,b,Q) for a,b in combinations(H,2)):allow.append(q)
    req(set(allow)=={(0,),(1,),(0,1)},'core-six mixed traces')
    # Graph bound profiles: every simple graph on six vertices, exact SF2.
    E=[frozenset(e) for e in combinations(range(6),2)];hist=Counter();n_graphs=0
    for mask in range(1<<15):
        ed=[E[i] for i in range(15) if mask>>i&1]
        deg=Counter(v for e in ed for v in e)
        if deg and max(deg.values())>2:continue
        if any(a.isdisjoint(b) and a.isdisjoint(c) and b.isdisjoint(c) for a,b,c in combinations(ed,3)):continue
        n_graphs+=1;hist[len(ed)]+=1
        req(len(ed)<=6,'SF2 edges')
        if len(ed)>=3: req(sum(d==2 for d in deg.values())>={3:1,4:2,5:4,6:6}[len(ed)],'SF2 repeated pairs')
    # Templates for the normalized tetrahedral components.
    templates=[('simplex_boundary',[frozenset(t) for t in combinations(range(5),4)]),('tetrahedron_suspension',[frozenset((a,)+t) for a in (0,1) for t in combinations((2,3,4,5),3)]),('triangle_join',[frozenset(a+b) for a in combinations((0,1,2),2) for b in combinations((3,4,5),2)])]
    normal=[]
    for name,F in templates:
        req(sunflower_free(F),'normalized template SF4')
        V=set().union(*F);ds=[]
        for v in V:
            lk=[a-{v} for a in F if v in a];ds.append(len(lk))
            req(len(lk) in (4,6),'normalized link size')
            req(len(components(lk,2))==1,'normal link connected')
            req(all(sum(set(e)<=a for a in lk)==2 for e in {e for a in lk for e in combinations(sorted(a),2)}),'normal link edge degree')
        req(all(sum(set(t)<=a for a in F)==2 for t in {t for a in F for t in combinations(sorted(a),3)}),'normal face degree')
        normal.append({'name':name,'tetrahedra':len(F),'vertices':len(V),'four_roles':ds.count(4),'six_roles':ds.count(6)})
    req([(d['tetrahedra'],d['four_roles'],d['six_roles']) for d in normal]==[(5,5,0),(8,2,4),(9,0,6)],'normal component counts')
    fits=[(a,b,c) for a in range(14) for b in range(9) for c in range(8) if 5*a+8*b+9*c==68 and 5*a+2*b==17 and 4*b+6*c==34]
    req(fits==[(3,1,5)],'68 arithmetic')
    # Countercontrol: cap seven is essential for the local R16 classification.
    P=[frozenset(map(int,s)) for s in ('012','015','023','034','045','124','134','135','235','245')]
    Loutside=P[:8]+[frozenset(v+6 for v in a) for a in P[:8]]
    req(sunflower_free(Loutside) and len(Loutside)==16 and max(sum(a.isdisjoint(b) for b in Loutside) for a in Loutside)==8,'cap-eight countercontrol')
    return {'status':'PASS','R16_degrees':degrees,'R16_disjoint_histogram':dict(disj),'R16_sectors':sector_stats,'core_six_allowed_traces':[list(a) for a in allow],'SF2_graphs_checked':n_graphs,'SF2_histogram':dict(sorted(hist.items())),'normalized_components':normal,'arithmetic_68_candidates':[list(a) for a in fits],'cap_eight_countercontrol':True}

def check_projection():
    d=json.loads((ROOT/'results/DOUBLEQ4_PROJECTION.json').read_text());values={frozenset(t['trace']):Fraction(t['value']) for t in d['nonzero']}
    L=[frozenset((h,)+e) for hubs,D in [((0,1),(4,5,6)),((2,3),(7,8,9))] for h in hubs for e in combinations(D,2)]+[frozenset(t) for t in combinations(range(4),3)]
    T=[frozenset(t) for k in range(5) for t in combinations(range(10),k)];req(set(values)<=set(T),'projection domain');req(sum(values.values())==52,'projection total')
    for t in T:
        cap=27 if len(t)==0 else 10 if len(t)==1 else (3 if any(t<=a for a in L) else 6) if len(t)==2 else 2-int(t in L) if len(t)==3 else 1
        req(0<=values.get(t,0)<=cap,'projection interval')
    for k,cap in ((1,16),(2,6),(3,2)):
        for p in combinations(range(10),k):
            P=frozenset(p);req(sum(v for t,v in values.items() if P<=t)+sum(P<=a for a in L)<=cap,'projection incidence')
    for a in L:req(sum(v for t,v in values.items() if t&a)>=25,'projection anchor')
    return {'status':'EXACT_RELAXATION_FEASIBLE_NOT_A_FAMILY','variables':len(T),'inequalities':10+45+120+16,'equalities':1,'noncentral_mass':52,'root_star_mass':16,'denominators':sorted({v.denominator for v in values.values()})}
if __name__=='__main__':print(json.dumps({'structural':verify(),'projection':check_projection()},sort_keys=True,indent=2))
