"""Non-importing standard-library verifier. Uses sets and incidence multiplicities.

Does not import the producer, its transversal-pool code, or an optimizer.
The reductions to these finite roots are stated in docs/PROOF.md.
"""
from itertools import combinations, permutations
from collections import Counter
from pathlib import Path
import copy,json,math,sys
ROOT=Path(__file__).resolve().parent.parent
class InvalidCertificate(ValueError):pass

def need(condition,message):
    if not condition:raise InvalidCertificate(message)

def members(mask):
    need(type(mask) is int and mask>=0,'invalid mask')
    return frozenset(i for i in range(mask.bit_length()) if (mask//(2**i))%2)

def integer(s):return sum(2**v for v in s)

def sunflower(a,b,c):
    # A triple is a sunflower iff no point occurs in exactly two members.
    counts=Counter(tuple(a)+tuple(b)+tuple(c))
    return 2 not in counts.values()

P=[frozenset(int(v) for v in t) for t in ('012','015','023','034','045','124','134','135','235','245')]
Q=[frozenset(t) for t in ((0,2,3),(0,2,4),(0,3,4),(1,2,3),(1,2,4),(1,3,4),(0,1,5),(0,1,6))]
ROOTS={'P10_6':(P,6,0),'P9_7':(P[1:],7,0),
       'P8_I2_8':([p for i,p in enumerate(P) if i not in (0,1)],8,2),
       'P8_I1_8':([p for i,p in enumerate(P) if i not in (0,7)],8,2),
       'Q8_8':(Q,8,2)}

def rebuild_census():
    expected={};audit=[]
    for name,(H,target,extra) in ROOTS.items():
        n=max(set().union(*H))+1;universe=set(range(n))
        need(all(len(h)==3 for h in H),'source not triples')
        need(all(a&b for a,b in combinations(H,2)),'source not intersecting')
        need(not any(sunflower(*a) for a in combinations(H,3)),'source has sunflower')
        covers=[frozenset(c) for c in combinations(universe,2) if all(set(c)&h for h in H)]
        need(len(covers)==(1 if name in ('P8_I2_8','Q8_8') else 0),'two-cover reduction failed')
        need(all(sum(v in h for h in H)<len(H) for v in universe),'one-cover reduction failed')
        pool=[]
        for c in combinations(range(n+extra),3):
            t=frozenset(c)
            if all(t&h for h in H):pool.append(t)
        accepted=set();candidates=0
        # Full subset-mask traversal, different ordering from the producer.
        for b in range(1<<len(pool)):
            if b.bit_count()!=target:continue
            candidates+=1
            K=[pool[i] for i in range(len(pool)) if b>>i&1]
            if any(not a&c for a,c in combinations(K,2)):continue
            if any(sunflower(*t) for t in combinations(K,3)):continue
            support=set().union(*K)
            if extra and n+1 in support and n not in support:continue
            accepted.add(tuple(sorted(integer(k) for k in K)))
        expected[name]=accepted
        audit.append({'type':name,'candidates':candidates,'accepted':len(accepted),
                      'pool':sorted(integer(p) for p in pool),'two_covers':sorted(integer(c) for c in covers)})
    return expected,audit

def verify_transport(data):
    t=data['transport'];Pset=set(P);aut=[]
    for p in permutations(range(6)):
        if {frozenset(p[v] for v in r) for r in P}==Pset:aut.append(p)
    need(len(t['automorphisms'])==len(aut) and set(map(tuple,t['automorphisms']))==set(aut),'automorphism coverage')
    recs=t['omission_transports'];need(len(recs)==45,'omission transport count')
    seen=set()
    for r in recs:
        ij=tuple(r['omissions']);need(len(ij)==2 and ij[0]<ij[1] and ij[0]>=0 and ij[1]<10,'omission pair')
        need(ij not in seen,'duplicate omission transport');seen.add(ij)
        p=tuple(r['permutation']);need(p in aut,'transport not P10 automorphism')
        target={P[0],P[1]} if len(P[ij[0]]&P[ij[1]])==2 else {P[0],P[7]}
        need({members(m) for m in r['target']}==target,'wrong omission target')
        need({frozenset(p[v] for v in P[i]) for i in ij}==target,'wrong omission transport')
    return len(aut)

def verify_case(c):
    name=c['type'];need(name in ROOTS,'unknown source type')
    H=list(map(members,c['H']));K=list(map(members,c['K']))
    need(len(set(H))==len(H) and set(H)==set(ROOTS[name][0]),'source mismatch')
    need(len(K)==ROOTS[name][1] and len(set(K))==len(K),'target cardinality')
    support=set().union(*H,*K);v=max(support)+1
    need(support==set(range(v)) and c['residual_vertices']==v,'residual support')
    need(c['centers']==[v,v+1],'centers enter residual support')
    x,y=c['centers'];B=[h|{x} for h in H]+[k|{y} for k in K]
    need(len(B)==16 and len(set(B))==16,'not sixteen distinct base members')
    need(not any(sunflower(*t) for t in combinations(B,3)),'invalid base family')
    ai=c['anchor_index'];need(type(ai) is int and 0<=ai<len(H),'anchor index')
    anchor=H[ai]
    resources=[];budget=0
    for r in c['resources']:
        s=members(r['subset']);need(s<=support and len(s) in (3,4),'invalid resource support')
        capacity=(2 if len(s)==3 else 1)-sum(s<=b for b in B)
        need(r['capacity']==capacity and capacity>=0,'resource capacity does not subtract base')
        resources.append(s);budget+=capacity
    need(len(set(resources))==len(resources),'duplicate resource')
    need(c['budget']==budget and budget<=4,'resource budget')
    tests={}
    for row in c['trace_tests']:
        t=members(row['trace']);need(t not in tests,'duplicate trace receipt');tests[t]=row
    required={frozenset(t) for k in range(5) for t in combinations(range(v),k) if set(t)&anchor}
    need(set(tests)==required,'trace coverage mismatch')
    charges=0;negative=0
    for t,row in tests.items():
        if 'charge' in row:
            k=row['charge'];need(type(k) is int and 0<=k<len(resources),'resource index')
            need(resources[k]<=t,'charge not contained in trace');charges+=1
        else:
            ij=row.get('sunflower',[]);need(len(ij)==2,'missing sunflower witness')
            i,j=ij;need(0<=i<len(H) and 0<=j<len(K),'sunflower index')
            C=t|frozenset(range(v+2,v+6-len(t)))
            need(len(C)==4 and not C&{x,y},'fresh test member')
            need(sunflower(H[i]|{x},K[j]|{y},C),'false sunflower witness');negative+=1
    return {'budget':budget,'trace_tests':len(tests),'charged':charges,'sunflower_witnesses':negative}

def verify_certificate(data,expected,audit):
    need(data['schema']=='e20.cross-stars.v1','schema')
    need(list(map(members,data['P10']))==P and list(map(members,data['Q8']))==Q,'canonical models')
    aut=verify_transport(data)
    seen={name:set() for name in ROOTS};stats=Counter();budgets=Counter()
    for c in data['cases']:
        name=c['type'];need(name in ROOTS,'case type')
        key=tuple(sorted(c['K']));need(key not in seen[name],'duplicate root case');seen[name].add(key)
    need(seen==expected,'cross-family census coverage mismatch')
    metadata={r['type']:r for r in data['census']}
    need(len(metadata)==5 and len(data['census'])==5,'census metadata count')
    for r in audit:
        s=metadata[r['type']]
        need(s['accepted']==r['accepted'] and s['candidates']==r['candidates'],'census metadata wrong')
        need(sorted(s['pool'])==r['pool'],'transversal pool wrong')
    by_type={name:Counter() for name in ROOTS}
    for c in data['cases']:
        r=verify_case(c);budgets[r['budget']]+=1;by_type[c['type']][r['budget']]+=1
        stats.update({k:v for k,v in r.items() if k!='budget'})
    for name,bp in by_type.items():
        need({int(k):v for k,v in metadata[name]['budget_profile'].items()}==dict(bp),'budget metadata wrong')
    return {'status':'PASS','candidate_families':sum(r['candidates'] for r in audit),'cases':sum(len(v) for v in expected.values()),
            'census':[{k:r[k] for k in ('type','candidates','accepted')} for r in audit],
            'automorphisms':aut,'omission_transports':45,'budget_profile':dict(sorted(budgets.items())),**dict(stats)}

def mutation_tests(original,expected,audit):
    tests=[]
    def trial(name,change):
        d=copy.deepcopy(original);change(d)
        try:verify_certificate(d,expected,audit)
        except (InvalidCertificate,KeyError,IndexError,TypeError) as ex:tests.append({'name':name,'rejected_with':str(ex)})
        else:raise InvalidCertificate('mutation accepted: '+name)
    trial('drop_case',lambda d:d['cases'].pop())
    trial('duplicate_case',lambda d:d['cases'].append(copy.deepcopy(d['cases'][0])))
    trial('omit_Q8_branch',lambda d:d.update(cases=[c for c in d['cases'] if c['type']!='Q8_8']))
    trial('wrong_census',lambda d:d['census'][0].update(accepted=209))
    trial('wrong_resource_capacity',lambda d:d['cases'][0]['resources'][0].update(capacity=0))
    trial('missing_trace',lambda d:d['cases'][0]['trace_tests'].pop())
    def false_sf(d):
        c=d['cases'][0]
        row=next(r for r in c['trace_tests'] if 'sunflower' in r)
        for i in range(len(c['H'])):
            for j in range(len(c['K'])):
                t=members(row['trace']);h=members(c['H'][i]);k=members(c['K'][j])
                if not (t&h==t&k==h&k):row['sunflower']=[i,j];return
        raise InvalidCertificate('no false-witness fixture')
    trial('invented_sunflower',false_sf)
    trial('invalid_anchor',lambda d:d['cases'][0].update(anchor_index=999))
    trial('center_inside_support',lambda d:d['cases'][0].update(centers=[0,7]))
    trial('omit_transport',lambda d:d['transport']['omission_transports'].pop())
    def bad_charge(d):
        c=d['cases'][0]
        r=next(r for r in c['trace_tests'] if 'sunflower' in r and not any((r['trace']&a['subset'])==a['subset'] for a in c['resources']))
        r.pop('sunflower');r['charge']=0
    trial('unguarded_resource_charge',bad_charge)
    return tests

def positive_controls():
    two=[t|{6} for t in P]+[t|{7} for t in P]
    E=[frozenset(e) for U in ((8,9,10),(11,12,13)) for e in combinations(U,2)]
    F=two+[e|{6,7} for e in E]
    need(len(set(F))==26 and not any(sunflower(*t) for t in combinations(F,3)),'positive control SF')
    deg=Counter(v for f in F for v in f);mu=min(sum(bool(f&g) for g in F) for f in F)
    need(max(deg.values())==16 and mu==26,'positive control degrees')
    return {'double_P10_plus_two_triangles':{'members':26,'maximum_degree':16,'minimum_closed_neighbourhood':26,
             'reason':'the lower bound on mu is essential; dense cross stars are not universally impossible'}}

def verify_benchmarks():
    path=ROOT/'results/benchmarks.json'
    if not path.exists():return {'status':'NOT_RUN'}
    data=json.loads(path.read_text());out=[]
    for rec in data['benchmarks']:
        model=data['models'][str(rec['shared_high_mask'])];vec=rec['vector']
        need(len(vec)==len(model['variables']),'benchmark dimension')
        need(all(type(v) is int for v in vec),'benchmark is not integral')
        for row in model['inequalities']:
            need(sum(vec[i]*a for i,a in row['terms'])<=row['rhs'],'benchmark violates inherited inequality')
        for row in model['equalities']:
            need(sum(vec[i]*a for i,a in row['terms'])==row['rhs'],'benchmark violates inherited equality')
        for v,(lo,hi) in zip(vec,model['bounds']):
            need(lo is None or v>=lo,'benchmark lower bound');need(hi is None or v<=hi,'benchmark upper bound')
        idx={tuple(a):i for i,a in enumerate(model['variables'])}
        mass=sum(vec[i] for i,(kind,_) in enumerate(model['variables']) if kind=='n')
        need(mass==68 and vec[idx['n',0]]==8,'benchmark mass or q')
        sums=[vec[idx['n',1<<a]]+vec[idx['n',1<<b]] for a,b in [(2,3),(4,5)]]
        need(sums==rec['petal_pair_sums'],'benchmark projected sums')
        out.append({'name':rec['name'],'mass':mass,'inherited_inequalities':len(model['inequalities']),
                    'equalities':len(model['equalities']),'variables':len(vec),'petal_pair_sums':sums,
                    'survives_cap15':all(s<=15 for s in sums),'is_realized_family':False})
    return {'status':'PASS','matrix_scope':'inherited assembler, not independently semantically reconstructed','records':out}

def main():
    data=json.loads((ROOT/'results/cross16_certificate.json').read_text())
    expected,audit=rebuild_census();result=verify_certificate(data,expected,audit)
    result['mutations']=mutation_tests(data,expected,audit)
    result['positive_controls']=positive_controls();result['benchmarks']=verify_benchmarks()
    result['main_proof_uses_optimizer']=False
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except (InvalidCertificate,KeyError,IndexError,TypeError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},sort_keys=True));sys.exit(1)
