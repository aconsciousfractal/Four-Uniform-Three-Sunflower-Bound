"""Independent proof-tree checker: set incidences, explicit colour witnesses.
Does not import the producer, C++ search, scipy or any optimizer.
"""
from __future__ import annotations
from itertools import combinations
from collections import Counter
from pathlib import Path
import gzip,json,sys,copy
ROOT=Path(__file__).resolve().parents[1]
class Invalid(Exception):pass

def require(ok,msg):
    if not ok:raise Invalid(msg)

def sunflower(a,b,c):
    return len([v for v in a|b|c if (v in a)+(v in b)+(v in c)==2])==0

def check_tree(tree):
    kind=tree['kind'];require(kind in ('two_triangles','cycle5','triangle_path'),'kind')
    if kind=='two_triangles':
        n,cap=11,6;edges=[p for g in ((1,2,3),(4,5,6)) for p in combinations(g,2)]
    elif kind=='cycle5':n,cap=10,5;edges=[(1,2),(2,3),(3,4),(4,5),(1,5)]
    else:n,cap=10,5;edges=[(1,2),(1,3),(2,3),(4,5),(4,6)]
    require((tree['n'],tree['degree_cap'],tree['target'],tree['disjoint_cap'],tree['minimum_used_degree'])==(n,cap,16,6,3),'scope')
    S=tuple(frozenset((0,)+e) for e in edges)
    require(tree['seed']==[sum(2**v for v in a) for a in S],'seed')
    sets=tuple(frozenset(t) for t in combinations(range(1,n),3));m=len(sets)
    # Cache the set-based forbidden pairs and triples, independent of producer masks.
    pair=[set() for _ in sets]
    for i in range(m):
        for j in range(i):
            if any(sunflower(sets[i],sets[j],a) for a in S):pair[i].add(j);pair[j].add(i)
    tri={}
    for i,j in combinations(range(m),2):
        tri[i,j]=frozenset(k for k in range(m) if k!=i and k!=j and sunflower(sets[i],sets[j],sets[k]))
    records=tree['nodes'];visited=set();hist=Counter();colpairs=0
    def visit(idx,F,chosen,C):
        nonlocal colpairs
        require(isinstance(idx,int) and 0<=idx<len(records),'child index')
        require(idx not in visited,'reused or cyclic child');visited.add(idx)
        rec=records[idx];deg=Counter(v for a in F for v in a)
        ds=[sum(a.isdisjoint(b) for b in F) for a in F]
        # Candidates already excluded by the parent have explicit selected-pair witnesses.
        good=set()
        for i in C:
            a=sets[i]
            if any(deg[v]>=cap for v in a):continue
            dis=[j for j,b in enumerate(F) if a.isdisjoint(b)]
            if len(dis)>6 or any(ds[j]>=6 for j in dis):continue
            good.add(i)
        C=good;need=16-len(F)
        if 'end' in rec:
            end=rec['end'];hist[end]+=1
            if end=='count':require(len(C)<need,'false count bound');return
            if end=='min':
                v=rec['v'];require(v in range(n),'minimum vertex')
                require(0<deg[v]<3 and deg[v]+sum(v in sets[i] for i in C)<3,'false degree bound');return
            require(end=='colour','solution or unknown leaf')
        else:hist['branch']+=1
        classes=rec['classes'];flat=sum(classes,[])
        require(len(flat)==len(set(flat)) and set(flat)==C,'colour coverage')
        require(all(cl for cl in classes),'empty colour')
        for cl in classes:
            for i,j in combinations(cl,2):
                require(j in pair[i],'non-independent colour');colpairs+=1
        if rec.get('end')=='colour':require(len(classes)<need,'false colour bound');return
        require(need>0 and len(classes)>=need,'invalid branch node')
        branch_order=[i for cl in reversed(classes[need-1:]) for i in reversed(cl)]
        children=rec['children'];require(len(children)==len(branch_order),'missing branch')
        for i,child in zip(branch_order,children):
            C.remove(i)
            blocked=set(pair[i])
            for j in chosen:blocked.update(tri[min(i,j),max(i,j)])
            allowed=C-blocked
            visit(child,F+(sets[i],),chosen+(i,),allowed)
        # Remaining candidates are covered by need-1 colour classes; all extensions covered.
        require(C==set(sum(classes[:need-1],[])),'uncovered prefix')
    visit(0,S,(),set(range(m)))
    require(len(visited)==len(records),'orphan records')
    expected={'nodes':len(records),'count':hist['count'],'min':hist['min'],'colour':hist['colour'],'branch':hist['branch'],'solutions':0}
    require(tree['counts']==expected,'count declaration')
    return {'kind':kind,**expected,'proper_colour_pairs_checked':colpairs}

def load():return json.loads(gzip.decompress((ROOT/'results/r16_mu10_certificate.json.gz').read_bytes()))

def main():
    d=load();require(d['format']=='E20_R16_mu10_proof_v1','format')
    require([t['kind'] for t in d['trees']]==['two_triangles','cycle5','triangle_path'],'root coverage')
    out={'status':'PASS','trees':[check_tree(t) for t in d['trees']]}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
