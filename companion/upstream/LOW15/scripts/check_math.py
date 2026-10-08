"""Replay all exact core exclusions; no numerical library or solver is loaded."""
from pathlib import Path
import json,hashlib
from collections import Counter
from itertools import combinations
import primary as P,independent as A
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
def check_certificate(cert,data):
    need(cert.get('schema')=='E20_F69_CAP15_CORE_CERT_V1','certificate schema')
    need((cert.get('row_id'),cert.get('core_id'))==(7,7),'certificate case')
    n=len(data['bounds'])
    for key,value in [('columns',n),('upper_rows',len(data['upper'])),('equal_rows',len(data['equal']))]:
        need(type(cert.get(key))is int and cert[key]==value,'dimension '+key)
    need(type(cert.get('scale'))is int and cert['scale']>0,'scale')
    q=[0]*n;H=0
    for kind in ('upper','equal'):
        need(type(cert[kind])is list,'multipliers');seen=set()
        for item in cert[kind]:
            need(type(item)is list and len(item)==2,'multiplier shape')
            i,w=item
            need(type(i)is int and i not in seen and 0<=i<len(data[kind]),'multiplier index')
            need(type(w)is int and w!=0 and(kind!='upper'or w>0),'multiplier sign/type')
            seen.add(i);_,terms,rhs=data[kind][i];H+=w*rhs
            for j,c in terms.items():q[j]+=w*c
    L=sum(min(c*lo,c*hi)for c,(lo,hi)in zip(q,data['bounds']))
    need(H<L,'not a strict contradiction')
    for key,value in [('H',H),('L',L),('gap',H-L)]:need(type(cert.get(key))is int and cert[key]==value,'exact '+key)
    return dict(columns=n,equalities=len(data['equal']),inequalities=len(data['upper']),upper_terms=len(cert['upper']),equal_terms=len(cert['equal']),H=H,L=L,gap=H-L)

def run():
    rr=P.rows();need(rr==A.rows(),'complete 7074-row literal comparison');need(len(rr)==7074,'source domain cardinality')
    ori=P.oriented();need(ori==A.oriented(),'full orientation comparison');need(len(ori)==29043,'oriented domain cardinality')
    roots=P.high_anchors();need(roots==A.high_anchors(),'anchor orbit comparison');need(roots==read('data/HIGH_ANCHORS.json'),'anchor catalogue')
    need(len(roots)==28 and sum(x['ordered_count']for x in roots)==161,'complete high-anchor coverage')
    records=read('data/CORES.json');need(len(records)==35,'core record total')
    keys=[(r['row_id'],r['core_id'])for r in records];need(len(set(keys))==35,'distinct core records')
    lookup={k:r for k,r in zip(keys,records)};stats=[]
    for root in roots:
        cs,n1,c1=P.census(root['row']);aa,n2,c2=A.census(root['row'])
        need(cs==aa,'full core census '+str(root['id']))
        expected=tuple(tuple(tuple(q)for q in lookup[root['id'],j]['core'])for j in range(len(cs)))
        need(cs==expected,'stored core coverage '+str(root['id']))
        need(sum(k[0]==root['id']for k in lookup)==len(cs),'extra/missing core record')
        stats.append(dict(id=root['id'],cores=len(cs),primary_nodes=n1,independent_nodes=n2,primary_raw=c1,independent_raw=c2))
    counts=Counter();last=None
    for rec in records:
        row=roots[rec['row_id']]['row'];core=rec['core'];status=rec['status'];counts[status]+=1
        need(all(len(set(q))==4 for q in core),'simple quadruples')
        ff=list(map(frozenset,core));need(len(set(ff))==len(ff),'no duplicates')
        need(not any(a&b==b&c==c&a for a,b,c in combinations(ff,3)),'core sunflower')
        if status=='NO_LOCAL_ROW':
            w=rec['witness'];Q=w['Q'];need(Q in core,'witness is a real core anchor')
            fp,lp,up,rp=P.anchor_domain(core,row,Q);fa,la,ua,ra=A.anchor_domain(core,row,Q)
            need(lp==la and up==ua and rp==ra,'independent trace bounds and rows')
            need(list(lp)==w['lows']and list(up)==w['ups'],'stored trace bounds')
            need(not rp,'nonempty witness anchor domain')
        elif status=='EXACT_LINEAR':
            need((rec['row_id'],rec['core_id'])==(7,7),'linear case key')
            d=P.build(core,row);a=A.build(core,row)
            need(d==a,'literal comparison of every coefficient, box, variable and row')
            cert=read('certificates/FINAL_CORE.json')
            last=check_certificate(cert,a)
            q=[0]*len(a['bounds'])
            for kind in ('upper','equal'):
                for i,w in cert[kind]:
                    for j,v in a[kind][i][1].items():q[j]+=w*v
            expanded=dict(schema='E20_FINAL_CORE_EXPANSION_V1',q=q,H=last['H'],L=last['L'],
                          negative_box_columns=[j for j,v in enumerate(q) if min(v*a['bounds'][j][0],v*a['bounds'][j][1])<0])
            need(expanded==read('data/FINAL_CERTIFICATE_EXPANSION.json'),'literal readable-certificate expansion')
        elif status=='TRANSPORT':
            p=rec['permutation'];need(sorted(p)==list(range(10)),'transport permutation')
            target=lookup[tuple(rec['target'])]
            transported=sorted(sorted(p[v]for v in q)for q in core)
            need(transported==target['core'],'complete core transport')
            # p on the first four labels is an involution here.
            need(P.relabel_row(row,p[:4])==tuple(roots[target['row_id']]['row']),'row transport')
            need(target['status']=='EXACT_LINEAR','transport to a checked refutation')
        else:raise ValueError('unrecognized/open leaf')
    need(counts=={'NO_LOCAL_ROW':33,'EXACT_LINEAR':1,'TRANSPORT':1},'terminal coverage')
    result=dict(status='PASS',mu=42,degree_cap=15,rows=7074,oriented_rows=29043,
                neighbourhoods={str(k):v for k,v in sorted(Counter(1+sum(r)for r in rr).items())},
                high_rows=161,anchor_orbits=28,cores=35,core_supports={str(k):v for k,v in sorted(Counter(len(set().union(*map(set,r['core'])))for r in records).items())},
                terminal_counts=dict(counts),linear_certificate=last,census_statistics=stats,
                all_list_and_model_comparisons_literal=True)
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':run()
