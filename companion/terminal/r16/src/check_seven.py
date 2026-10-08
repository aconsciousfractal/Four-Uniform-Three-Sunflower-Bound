"""No-import checker using complementary-pair enumeration and set incidences."""
from itertools import combinations,permutations,product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
class Invalid(Exception):pass
def req(ok,s):
    if not ok:raise Invalid(s)
def sf(a,b,c):return not any((v in a)+(v in b)+(v in c)==2 for v in a|b|c)
def family(F):return len(F)==len(set(F)) and all(a&b for a,b in combinations(F,2)) and not any(sf(a,b,c) for a,b,c in combinations(F,3))
def verify(d):
    req(d['format']=='E20_I7_catalogue_v1','format');rows=d['rows'];req([r['id'] for r in rows]==list(range(8)),'eight roots')
    all_labelled=set();mixed=0;obs=[]
    for i,row in enumerate(rows):
        n=6 if i<7 else 7;req(row['support']==n,'support')
        F=tuple(frozenset(a) for a in row['blocks']);req(len(F)==7 and all(len(a)==3 for a in F) and set.union(*(set(a) for a in F))==set(range(n)),'root domain');req(family(F),'root SF')
        allowed={frozenset(x) for x in row['mixed_allowed']};forbid={frozenset(x['trace']):x['witness'] for x in row['mixed_forbidden']}
        universe={frozenset(x) for k in (1,2) for x in combinations(range(n),k)}
        req(not allowed&forbid.keys() and allowed|forbid.keys()==universe,'trace coverage')
        req(len(forbid)==len(row['mixed_forbidden']) and len(allowed)==len(row['mixed_allowed']),'duplicate trace')
        for X in universe:
            mixed+=1
            if X in allowed:req(not any(sf(a,b,X) for a,b in combinations(F,2)),'false allowed trace')
            else:
                a,b=forbid[X];req(0<=a<b<7 and sf(F[a],F[b],X),'false trace witness')
        if i<7:
            orbit={frozenset(frozenset(p[v] for v in a) for a in F) for p in permutations(range(6))}
            req(not orbit&all_labelled,'isomorphic roots');req(len(orbit)==row['labelled_count'],'orbit size');all_labelled|=orbit;obs.append(len(orbit))
    U=frozenset(range(6));triples=[frozenset(x) for x in combinations(range(6),3)]
    pairs=[(a,U-a) for a in triples if tuple(sorted(a))<tuple(sorted(U-a))]
    req(len(pairs)==10,'complement pairs');visited=0;actual=set()
    for ids in combinations(range(10),7):
        for choices in product((0,1),repeat=7):
            F=tuple(pairs[i][c] for i,c in zip(ids,choices));visited+=1
            if family(F):actual.add(frozenset(F))
    req(actual==all_labelled,'complete six-point census');req(d['labelled_n6']==len(actual) and d['subsets_n6_tested']==77520,'reported counts')
    # Match the seven-point root to the fully described degree-five non-C5 case.
    Q=[frozenset((h,)+p) for h in (0,1) for p in combinations((2,3,4),2)]+[frozenset((0,1,5)),frozenset((0,1,6))]
    req(frozenset(map(frozenset,rows[7]['blocks']))==frozenset(a for a in Q if a!=frozenset((1,2,3))),'seven-point type')
    # Named finite facts used in the R16 case split, not just the mixed table.
    for i in (0,1,5):
        F=[set(a) for a in rows[i]['blocks']]
        req(all(len(t)==2 and sum(set(t)<=a for a in F)==1 and any(not set(t)&a for a in F) for t in rows[i]['mixed_allowed']),'pair-only capacity')
    for i,anchor,exception in [(6,{1,2,5},{1,2}),(7,{0,2,3},{2,3})]:
        F=[set(a) for a in rows[i]['blocks']];req(anchor in F,'seven gate anchor')
        req(all(set(t)==exception or not(set(t)&anchor) for t in rows[i]['mixed_allowed']),'disjoint gate')
        req(sum(exception<=a for a in F)==1,'exception capacity')
    return {'status':'PASS','seven_isomorphism_types_on_six_points':7,'one_type_on_seven_points':1,'labelled_on_six':len(actual),'orbit_sizes':obs,'independent_complement_selections':visited,'mixed_traces_checked':mixed}
def main():print(json.dumps(verify(json.loads((ROOT/'results/seven_certificate.json').read_text())),sort_keys=True,indent=2))
if __name__=='__main__':main()
