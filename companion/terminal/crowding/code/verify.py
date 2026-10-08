#!/usr/bin/env python3
"""Independent full finite replay. Standard library only.
Does not import build_certificate.py. Orbits use BFS, not union-find.
The predicate uses points of multiplicity exactly two, not equal intersections.
Q8 placements use a hub/triad construction, not a permutation list.
"""
from __future__ import annotations
from collections import Counter, deque
from itertools import combinations, combinations_with_replacement, permutations, product
from fractions import Fraction
from pathlib import Path
from copy import deepcopy
from math import comb
import gzip, hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
P=tuple(sorted(tuple(int(x) for x in s) for s in ('012','015','023','034','045','124','134','135','235','245')))
class Invalid(ValueError):pass
def need(p,msg):
    if not p:raise Invalid(msg)
def encode(H):return tuple(sorted(tuple(sorted(e)) for e in H))
def action(H,p):return encode([p[v] for v in e] for e in H)
def mask(e):return sum(2**v for v in e)
def unpack(v):return frozenset(i for i in range(v.bit_length()) if v>>i&1)
def sf_bits(a,b,c):return (((a&b)&~c)|((a&c)&~b)|((b&c)&~a))==0
def sf_sets(A,B,C):return 2 not in Counter(list(A)+list(B)+list(C)).values()
def cross(A,B):return all(set(a)&set(b) for a in A for b in B)
def check_sf(F):return not any(sf_sets(*t) for t in combinations(F,3))

PERMS=tuple(permutations(range(6)))
DESIGNS=tuple(sorted({action(P,p) for p in PERMS}))

def reconstruct_pairs(a,b):
    seed=P if a==10 else P[1:]
    group=[p for p in PERMS if action(seed,p)==seed]
    universe=set()
    for bits in range(64):
        shared=tuple(v for v in range(6) if bits>>v&1)
        labels=shared+tuple(range(6,12-len(shared)))
        for design in DESIGNS:
            F=action(design,labels)
            for H in ([F] if b==10 else combinations(F,9)):universe.add(tuple(H))
    remaining=set(universe);rows=[]
    while remaining:
        rep=min(remaining);n=max(6,1+max(v for e in rep for v in e))
        ops=[p+tuple(range(6,n)) for p in group]
        for v in range(6,n-1):
            p=list(range(n));p[v],p[v+1]=p[v+1],p[v];ops.append(p)
        orbit={rep};Q=deque([rep])
        while Q:
            H=Q.popleft()
            for op in ops:
                F=action(H,op);need(F in universe,'action leaves normalized carrier')
                if F not in orbit:orbit.add(F);Q.append(F)
        need(orbit<=remaining,'overlapping orbit partition');remaining-=orbit
        rows.append((rep,len(orbit),n))
    return seed,len(universe),len(group),rows

def safe_old_traces(A,B,n):
    aa=[mask(e) for e in A];bb=[mask(e) for e in B]
    allowed=[];tests=0
    # The old trace alone determines every equality. Fresh points occur once.
    for size in range(4):
        for t in combinations(range(n),size):
            tests+=1;z=mask(t)
            if not any(sf_bits(a,b,z) for a in aa for b in bb):allowed.append(z)
    return tuple(sorted(allowed)),tests

def third_templates(target):
    forms6=set()
    for D in DESIGNS:
        for omitted in combinations(range(10),10-target):
            forms6.add(encode(e for j,e in enumerate(D) if j not in omitted))
    models={6:tuple(sorted(forms6))}
    if target==8:
        forms7=set()
        for hub in combinations(range(7),2):
            other=[i for i in range(7) if i not in hub]
            for triad in combinations(other,3):
                leaves=[i for i in other if i not in triad]
                H=[{h,*e} for h in hub for e in combinations(triad,2)]+[set(hub)|{l} for l in leaves]
                forms7.add(encode(H))
        models[7]=tuple(sorted(forms7))
    out={}
    for n,Hs in models.items():
        triples=list(combinations(range(n),3));idx={t:i for i,t in enumerate(triples)}
        out[n]=(triples,tuple(sorted(sum(1<<idx[t] for t in H) for H in Hs)))
    return out

def reconstruct_third(A,B,n,target,templates,allowed):
    safe=set(allowed);oldmask=(1<<n)-1;result=set();supports=0;candidate_count=0
    for size,(triples,patterns) in templates.items():
        # Subsets represented by masks, rather than combinations of a chosen size.
        for bits in range(1<<n):
            k=bits.bit_count()
            if k>size:continue
            old=tuple(i for i in range(n) if bits>>i&1)
            labels=old+tuple(range(n,n+size-k));supports+=1;candidate_count+=len(patterns)
            signature=0;images=[]
            for j,t in enumerate(triples):
                z=mask(labels[i] for i in t);images.append(z)
                if z&oldmask in safe:signature|=1<<j
            if signature.bit_count()<target:continue
            for p in patterns:
                if p&signature!=p:continue
                family=encode(unpack(images[j]) for j in range(len(triples)) if p>>j&1)
                need(family not in result,'duplicate template or carrier');result.add(family)
    records=[];positive_triples=0
    for C in sorted(result):
        fs=(A,B,C);cp=[list(ij) for ij in combinations(range(3),2) if cross(fs[ij[0]],fs[ij[1]])]
        need(cp,'rainbow-free extension without a cross pair')
        last=max(v for H in fs for e in H for v in e)+1
        lifted=[set(e)|{last+i} for i,H in enumerate(fs) for e in H]
        need(len(lifted)==27 and len({frozenset(e) for e in lifted})==27,'positive family not simple')
        need(check_sf(lifted),'positive lifted family contains a sunflower')
        positive_triples+=comb(27,3)
        records.append({'third':[list(e) for e in C],'cross_pairs':cp})
    return {'normalized_supports':supports,'candidate_families':candidate_count,'extensions':records},positive_triples

def verify_cover(A,B,n,cover):
    X,Y=n,n+1
    seed=[set(e)|{X} for e in A]+[set(e)|{Y} for e in B]
    need(check_sf(seed),'cover base is not SF4')
    anchor=set(unpack(cover['anchor']));need(anchor in seed,'cover anchor not an actual base member')
    known=sum(bool(e&anchor) for e in seed)
    caps={1:18,2:6,3:2,4:1};resources=[];seen=set();cost=Fraction(0)
    for rr in cover['resources']:
        r=set(unpack(rr['subset']));num,den=rr['weight'];need(type(num)is int and type(den)is int and den>0,'nonrational weight')
        w=Fraction(num,den);need(w>0,'nonpositive resource weight')
        need(1<=len(r)<=4 and r<=set(range(n+2)),'resource outside carrier')
        need(rr['subset'] not in seen,'duplicate resource');seen.add(rr['subset'])
        cap=caps[len(r)]-sum(r<=e for e in seed);need(cap>=0,'negative residual capacity')
        resources.append((r,w));cost+=cap*w
    tested=excluded=charged=0
    for k in range(5):
        for t0 in combinations(range(n+2),k):
            t=set(t0)
            if not t&anchor or t in seed:continue
            tested+=1
            if any(sf_sets(e,f,t) for e,f in combinations(seed,2)):excluded+=1;continue
            coverage=sum((w for r,w in resources if r<=t),Fraction(0))
            need(coverage>=1,'uncovered future member trace');charged+=1
    bound=known+cost
    need(bound<=40,'cover does not contradict mu41')
    need(bound==cover['expected_bound'],'wrong recorded neighbourhood bound')
    return {'bound':str(bound),'traces':tested,'forbidden':excluded,'charged':charged}

def mathematical_replay(data):
    need(data.get('format')=='E20_GLOBAL_SUPPORT23_V1','certificate format')
    need(data.get('hypotheses')=={'minimum_closed_neighbourhood':41,'maximum_point_degree':18},'hypotheses changed')
    need(data.get('conclusions')=={'top_three_singletons':26,'minimum_used_degree':7,'support_at_cardinality_68':23,'global_67_proved':False},'conclusions changed')
    need(isinstance(data.get('normalization'),str) and data['normalization'],'normalization absent')
    names=['10_10_7','10_9_8','9_9_9'];need(set(data['sections'])==set(names),'missing a size regime')
    stat=Counter();details=[];expected_rows={};cover_results=[]
    for a,b,k,name in [(10,10,7,names[0]),(10,9,8,names[1]),(9,9,9,names[2])]:
        A,positions,order,orbits=reconstruct_pairs(a,b);s=data['sections'][name]
        need(s['first']==[list(e) for e in A],'wrong first colored family')
        need(s['pair_placements']==positions and s['automorphism_order']==order,'orbit metadata')
        need(len(s['rows'])==len(orbits),'orbit list incomplete')
        tpls=third_templates(k) if k>7 else None
        if tpls:need(s['third_template_counts']=={str(n):len(t[1]) for n,t in tpls.items()},'third template universe')
        methods=Counter();section_candidates=section_supports=section_positives=0
        for i,((B,orb,n),row) in enumerate(zip(orbits,s['rows'])):
            need(row['second']==[list(e) for e in B] and row['orbit_size']==orb and row['union_size']==n,'wrong pair representative')
            method=row['method'];methods[method]+=1
            base={'second':[list(e) for e in B],'orbit_size':orb,'union_size':n,'method':method}
            if method=='neighbourhood_cover':
                need(row['cover']['row']==i,'mislabelled cover')
                res=verify_cover(A,B,n,row['cover']);cover_results.append({'section':name,'row':i,**res});stat['cover_traces']+=res['traces']
                base['cover']=deepcopy(row['cover'])
            elif method=='cross_first_pair':
                need(cross(A,B) and len(A)+len(B)>=16,'invalid cross-intersection guard')
            else:
                allowed,nt=safe_old_traces(A,B,n);stat['tail_trace_tests']+=nt
                need(row['safe_traces']==list(allowed),'tail trace list not complete');base['safe_traces']=list(allowed)
                if method in ('no_intersecting_seven','separated_tail_pool'):
                    need(k==7 and all(z.bit_count()==3 for z in allowed),'mixed tail survives asserted confinement')
                    pool=list(map(unpack,allowed))
                    if method=='no_intersecting_seven':
                        nchecks=0
                        for chosen in combinations(pool,7):
                            nchecks+=1;need(any(not e&f for e,f in combinations(chosen,2)),'seven intersecting tails survive')
                        need(row['subset_checks']==nchecks,'seven-tail count');base['subset_checks']=nchecks;stat['seven_tail_subsets']+=nchecks
                    else:
                        W=set().union(*map(set,A));V=set().union(*map(set,B))
                        need(not W&V,'separation guard absent')
                        need(set(allowed)==set(map(mask,A))|set(map(mask,B)),'separated tail pool wrong')
                        # An intersecting family cannot use both disjoint carriers.
                elif method=='enumerate_third':
                    need(k in (8,9),'unrecognized target size')
                    rebuilt,positive=reconstruct_third(A,B,n,k,tpls,allowed)
                    for key,v in rebuilt.items():need(row[key]==v,'third family census mismatch: '+key)
                    base.update(rebuilt);stat['positive_ternas']+=positive
                    section_candidates+=rebuilt['candidate_families'];section_supports+=rebuilt['normalized_supports'];section_positives+=len(rebuilt['extensions'])
                else:raise Invalid('unknown proof method')
            need(set(row)==set(base),'extra or missing row fields');expected_rows[(name,i)]=base
        details.append({'section':name,'normalized_pair_positions':positions,'pair_orbits':len(orbits),'first_automorphisms':order,'methods':dict(methods),'third_supports_enumerated':section_supports,'third_candidate_families_covered':section_candidates,'third_positive_records':section_positives})
        stat['pair_orbits']+=len(orbits);stat['pair_positions']+=positions
    return {'sections':details,'covers':cover_results,**stat},expected_rows

def local_and_global_checks():
    models=[]
    for om in (0,1,2):
        for idx in combinations(range(10),om):models.append([set(e) for j,e in enumerate(P) if j not in idx])
    Q=[{h,*e} for h in (0,1) for e in combinations((2,3,4),2)]+[{0,1,5},{0,1,6}];models.append(Q)
    root_records=set()
    for H in models:
        need(check_sf(H) and all(a&b for a,b in combinations(H,2)),'bad imported model')
        for A in H:
            for v,j,k in permutations(A):
                t=sum(v in e for e in H)
                p=sum(e&A=={j} for e in H);q=sum(e&A=={k} for e in H);T=sum(e&A=={j,k} for e in H)
                root_records.add((len(H),t,p,q,T))
    counts={}
    for m in (5,6):
        n=0
        for s in product(range(11),repeat=3):
            S=sum(s)
            if S>26 or m+S+10<41:continue
            for p in product(range(4),repeat=3):
                for T in (0,1):
                    if m+S+sum(p)+T<41:continue
                    r=(p[0]+p[1],p[0]+p[2],p[1]+p[2])
                    for t in product(range(1,m+1),repeat=3):
                        kk=tuple(t[i]+r[i]+T for i in range(3))
                        if any(s[i]+kk[i]>18 for i in range(3)):continue
                        high=[i for i in range(3) if s[i]>=8]
                        need(len(high)>=2,'not two large singleton classes')
                        ok=True
                        for i in high:
                            pp=([p[0],p[1]],[p[0],p[2]],[p[1],p[2]])[i]
                            if kk[i]>10:ok=False;break
                            if kk[i]>=8 and (kk[i],t[i],pp[0],pp[1],T) not in root_records:ok=False;break
                        if not ok:continue
                        n+=1;need(all(t[i]==1 for i in high),'nonprivate point survives')
        counts[str(m)]=n
    # Cardinality at most four for an SF3 family with >=2 private points per triple.
    # The general proof is a matching argument in the written report.
    tuple_count=0;table={};qmax=Fraction(0);witness=None
    for d in combinations_with_replacement(range(7,19),4):
        m=d[0]
        if d[0]+d[1]<19 or sum(d[1:])<59-2*m:continue
        tuple_count+=1;c=sum((Fraction(1,x) for x in d),Fraction(0))
        if c>qmax:qmax=c;witness=d
        if m not in table or c>table[m][0]:table[m]=(c,d)
    need(qmax==Fraction(439,1260),'reciprocal bound mismatch')
    need((68*qmax).__floor__()==23,'support bound')
    need(all(m+26+9+1<41 for m in range(1,5)),'small degree bound')
    # A true sunflower-free configuration violating the conclusion without mu41.
    W2=[set(v+6 for v in e) for e in P]
    F=[set(e)|{12} for e in P]+[set(e)|{13} for e in P]+[e|{14} for e in W2]+[{12,13,14,15}]
    need(check_sf(F) and len(F)==31,'mu-guard positive control')
    deg=Counter(v for e in F for v in e);mu=min(sum(bool(e&f) for f in F) for e in F)
    singletons=[sum(e&{12,13,14,15}=={v} for e in F) for v in (12,13,14,15)]
    need(singletons==[10,10,10,0] and mu<41,'guard not discriminating')
    # Eight Boolean membership patterns: exactly-two is exactly the witness against a sunflower.
    truth=[]
    for abc in product((0,1),repeat=3):truth.append({'bits':list(abc),'witness':sum(abc)==2})
    return {'rooted_model_projection_records':len(root_records),'five_six_root_states':counts,'sorted_degree_tuples_checked':tuple_count,'max_reciprocal_charge':str(qmax),'maximizing_relaxed_tuple':witness,'support_bound_for_68':23,'charge_by_minimum':{str(m):{'charge':str(c),'tuple':d} for m,(c,d) in table.items()},'positive_mu_guard':{'members':31,'delta':max(deg.values()),'mu':mu,'singleton_profile':singletons,'ternas_checked':comb(31,3)},'incidence_truth_table':truth}

def mutations(original,expected):
    tests=[]
    def quick(d):
        need(d.get('hypotheses')==original['hypotheses'],'changed hypotheses')
        need(d.get('conclusions')==original['conclusions'],'changed conclusion scope')
        need(set(d['sections'])==set(original['sections']),'missing regime')
        for name,sec in d['sections'].items():
            original_sec=original['sections'][name]
            for key in ('first','pair_placements','automorphism_order','third_template_counts'):
                need(sec.get(key)==original_sec.get(key),'wrong rebuilt orbit/template metadata')
            need(len(sec['rows'])==len(original_sec['rows']),'missing pair orbit')
            for i,row in enumerate(sec['rows']):
                e=expected[(name,i)]
                for k,v in e.items():
                    if k!='cover':need(row.get(k)==v,'wrong rebuilt '+k)
                need(set(row)==set(e),'row fields changed')
                if 'cover' in row and row['cover']!=e['cover']:
                    verify_cover(sec['first'],row['second'],row['union_size'],row['cover'])
    def trial(name,fn):
        d=deepcopy(original);fn(d)
        try:quick(d)
        except (Invalid,KeyError,IndexError,TypeError,ZeroDivisionError) as ex:tests.append({'name':name,'rejected':str(ex)})
        else:raise Invalid('accepted mutation: '+name)
    trial('drop_size_regime',lambda d:d['sections'].pop('9_9_9'))
    trial('drop_pair_orbit',lambda d:d['sections']['10_9_8']['rows'].pop())
    trial('wrong_group_order',lambda d:d['sections']['9_9_9'].__setitem__('automorphism_order',60))
    trial('wrong_pair_count',lambda d:d['sections']['9_9_9'].__setitem__('pair_placements',7679))
    trial('omit_Q8_templates',lambda d:d['sections']['10_9_8']['third_template_counts'].pop('7'))
    name='9_9_9';i=next(i for i,r in enumerate(original['sections'][name]['rows']) if r.get('extensions'))
    trial('drop_third_positive',lambda d:d['sections'][name]['rows'][i]['extensions'].pop())
    trial('erase_cross_guard',lambda d:d['sections'][name]['rows'][i]['extensions'][0].__setitem__('cross_pairs',[]))
    trial('wrong_candidate_count',lambda d:d['sections'][name]['rows'][i].__setitem__('candidate_families',1))
    trial('fake_fresh_support',lambda d:d['sections']['10_9_8']['rows'][0].__setitem__('union_size',23))
    j=next(i for i,r in enumerate(original['sections']['10_10_7']['rows']) if r['method']=='no_intersecting_seven')
    trial('omit_allowed_tail',lambda d:d['sections']['10_10_7']['rows'][j]['safe_traces'].pop())
    trial('wrong_seven_subset_count',lambda d:d['sections']['10_10_7']['rows'][j].__setitem__('subset_checks',0))
    trial('delete_cover_resources',lambda d:d['sections']['10_10_7']['rows'][0]['cover'].__setitem__('resources',[]))
    trial('fake_cover_anchor',lambda d:d['sections']['10_10_7']['rows'][0]['cover'].__setitem__('anchor',1))
    trial('negative_weight',lambda d:d['sections']['10_10_7']['rows'][0]['cover']['resources'][0].__setitem__('weight',[-1,1]))
    trial('inflated_cover_conclusion',lambda d:d['sections']['10_10_7']['rows'][0]['cover'].__setitem__('expected_bound',1))
    trial('drop_max_degree_guard',lambda d:d['hypotheses'].__setitem__('maximum_point_degree',19))
    trial('claim_67',lambda d:d['conclusions'].__setitem__('global_67_proved',True))
    trial('claim_support22',lambda d:d['conclusions'].__setitem__('support_at_cardinality_68',22))
    return tests

def main():
    raw=gzip.decompress((ROOT/'certificates/crowding26.json.gz').read_bytes());data=json.loads(raw)
    main_stats,expected=mathematical_replay(data);aux=local_and_global_checks();neg=mutations(data,expected)
    print(json.dumps({'status':'PASS_GLOBAL_SUPPORT23_REPLAY','main':main_stats,'auxiliary':aux,'rejected_mutations':neg,'certificate_sha256':hashlib.sha256((ROOT/'certificates/crowding26.json.gz').read_bytes()).hexdigest(),'global_67_proved':False,'dependency_boundary':'A1/B1/B4 and the cross-star cap15 theorem are explicit imports. Cross15 has a separate replay. Written reductions, not raw counts, transfer to arbitrary support.'},ensure_ascii=False,sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except (Invalid,KeyError,ValueError,TypeError,IndexError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}));raise
