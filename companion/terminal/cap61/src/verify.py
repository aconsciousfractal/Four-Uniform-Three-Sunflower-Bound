#!/usr/bin/env python3
"""Exact standard-library verifier; no producer import and no optimizer.

Reconstructs the complete core-count domain using a prescribed total and
bounded compositions; the C++ producer uses direct coordinate loops.
General reductions and the terminal intersecting-family proof are in PROOF.md.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
import json,copy,sys,math
ROOT=Path(__file__).resolve().parents[1]
K=frozenset(range(4));PAIRS=tuple(combinations(range(4),2))
P=tuple(frozenset(int(v) for v in s) for s in ('012','015','023','034','045','124','134','135','235','245'))
R=tuple([frozenset((h,*e)) for h in (0,1) for e in combinations((4,5,6),2)]+list(map(frozenset,combinations(range(4),3)))+[frozenset((h,*e)) for h in (2,3) for e in combinations((7,8,9),2)])
CONTRACT={'format':'E20_R16_STAR_CAP61_V1','simple_sf4':True,'empty_core_forbidden':True,
 'mu_min':41,'max_degree':18,'intrinsic_hub_cap':16,'root_singleton_top3_cap_import':26,
 'complete_16_link_classification_import':True,'R16_star_is_complete':True,
 'upper_members_if_R16':61,'terminal_P9_P10_intersecting_cap':20,
 'general_intersecting_P9_cap':26,'global67_proved':False,
 'carrier18_nohigh_fully_excluded':False,'H27_used_in_local_theorem':False}
def require(b,msg):
 if not b:raise ValueError(msg)
def enc(s):return sum(2**v for v in s)
def dec(m):
 require(type(m) is int and m>=0,'nonnegative integer mask required')
 return frozenset(v for v in range(m.bit_length()) if m//2**v%2)
def sunflower(a,b,c):
 return not any(sum(v in t for t in (a,b,c))==2 for v in a|b|c)
def sf(F):return len(F)==len(set(F)) and not any(sunflower(*t) for t in combinations(F,3))

@lru_cache(maxsize=1)
def reconstruct_profiles():
 stage=[0,0,0];records=[];outer=0
 for pp in product(range(4),repeat=6):
  p=dict(zip(PAIRS,pp));ps=sum(pp)
  for tt in product(range(2),repeat=4):
   ts=sum(tt)
   for q in (0,1):
    outer+=1
    if any(t+q>1 for t in tt):continue
    if any(p[a,b]+tt[i]>3 for a,b in PAIRS for i in K-{a,b}):continue
    fixed=ps+ts+q
    room=[10-(sum(p[tuple(sorted((i,j)))] for j in K-{i})+ts-tt[i]+q) for i in range(4)]
    if min(room)<0:continue
    # If E counts all nonempty K-traces, E-s_i>=25 and sum(s)=E-fixed.
    # Thus E>=ceil((100-fixed)/3), and E<=fixed+sum(room).
    for E in range(max(25,(100-fixed+2)//3),fixed+sum(room)+1):
     total=E-fixed;u=[min(r,E-25) for r in room]
     for a in range(max(0,total-sum(u[1:])),min(u[0],total)+1):
      for b in range(max(0,total-a-sum(u[2:])),min(u[1],total-a)+1):
       for c in range(max(0,total-a-b-u[3]),min(u[2],total-a-b)+1):
        d=total-a-b-c
        if not 0<=d<=u[3]:continue
        ss=(a,b,c,d);stage[0]+=1
        counts=Counter({frozenset((10,i)):3 for i in range(4)})
        counts.update({frozenset({10}|(K-{i})):1 for i in range(4)})
        counts.update({frozenset((i,)):ss[i] for i in range(4)})
        counts.update({frozenset(e):v for e,v in p.items()})
        counts.update({K-{i}:tt[i] for i in range(4)})
        counts[K]=q
        ds=[sum(v for t,v in counts.items() if j in t) for j in range(4)]
        require(all(6<=m<=16 for m in ds),'composition generator violates degree cap')
        singles={};ok=True
        for omitted in range(4):
         root={10}|(K-{omitted})
         require(sum(v for t,v in counts.items() if t&root)>=41,'composition generator violates neighborhood')
         vals=[]
         for j in K-{omitted}:
          val=sum(v for t,v in counts.items() if t&root=={j});singles[omitted,j]=val;vals.append(val)
          if val>10 or (val>=8 and ds[j]-val!=6):ok=False
         if sum(vals)>26:ok=False
        if not ok:continue
        stage[1]+=1
        for j in range(4):
         if ds[j]!=16:continue
         vals={singles[i,j] for i in K-{j}}
         if len(vals)!=1 or next(iter(vals)) not in (3,7,10):ok=False;break
         if vals!={10} and any(tt[i]+q!=1 for i in K-{j}):ok=False;break
        if ok:stage[2]+=1;records.append([*ss,*pp,*tt,q,*ds,E])
 require(outer==131072,'outer domain')
 require(stage==[21652,111,11],'census reconstruction differs')
 require(len(records)==len(set(map(tuple,records))),'duplicate reconstruction')
 return outer,stage,sorted(records)

@lru_cache(maxsize=1)
def structural_facts():
 require(sf(R) and len(R)==16,'R16 literal model')
 ds=Counter(v for t in R for v in t)
 require(ds==Counter({**{v:6 for v in range(4)},**{v:4 for v in range(4,10)}}),'R16 degrees')
 pairdeg=Counter(frozenset(e) for t in R for e in combinations(t,2))
 require(set(pairdeg.values())=={2},'R16 used-pair degree')
 root_count=0;completion_count=0
 for v in range(4):
  triad=frozenset((4,5,6) if v<2 else (7,8,9));hubtri=K-{v}
  actual={t-{v} for t in R if v in t}
  require(actual==set(map(frozenset,combinations(triad,2)))|set(map(frozenset,combinations(hubtri,2))),'pair-link triangles')
  for triangle,disjoint in ((triad,7),(hubtri,3)):
   for e in combinations(triangle,2):
    a=frozenset((v,*e));require(a in R,'R16 root absent')
    require(sum(not(a&b) for b in R)==disjoint,'R16 root disjoint count');root_count+=1
  require(triad not in R and hubtri in R,'R16 peripheral triple status')
  partner=1-v if v<2 else 5-v
  require(partner in hubtri,'paired hub is in the other triangle')
  for e in map(frozenset,combinations(triad,2)):
   require({next(iter(t-e)) for t in R if e<=t}=={v,partner},'peripheral pair has wrong completions');completion_count+=1
 # The 8..10 representatives have no point degree six; size seven follows
 # from the ordinary degree-six lemma, not a new finite classification here.
 q8=[frozenset((h,*e)) for h in (0,1) for e in combinations((2,3,4),2)]+[frozenset((0,1,5)),frozenset((0,1,6))]
 fams=[list(P),list(P[1:]),q8]+[[t for t in P if t not in omit] for omit in combinations(P,2)]
 for H in fams:require(max(Counter(v for t in H for v in t).values())<=5,'intersecting representative point cap')
 return {'R16_root_checks':root_count,'peripheral_pair_checks':completion_count,'used_pairs':len(pairdeg)}

def check_routes(rows):
 tally=Counter()
 for r in rows:
  v=r['values'];s,p,t,q,ds,E=v[:4],v[4:10],v[10:14],v[14],v[15:19],v[19];route=r['route'];kind=route['kind'];tally[kind]+=1
  if kind=='exact_P9_complement':
   require(sorted(s)==[8,8,9,9] and not any(p+t+[q]),'P9 complement profile')
   i=route['hub'];require(i in range(4) and s[i]==9,'wrong nine-star center')
   require(ds[i]==15 and 16+E-s[i]==41,'wrong exact root neighborhood')
   require(route['neighborhood']==41 and route['center_degree_in_disjoint_family']==9,'disjoint family metadata')
   require(route['disjoint_family_cap']==20 and route['global_cap']==61,'terminal bound not the proved one')
  elif kind=='P9_degree_two':
   require(s==[7]*4 and not any(t+[q]) and sorted(p)==[0,0,0,0,2,2],'matching profile')
   i,j=route['omitted_hub'],route['singleton_hub']
   require(i!=j and p[PAIRS.index(tuple(sorted((i,j))))]==2,'matching witness edge')
   require(s[j]+2==9 and route['marked_degree']==2,'P9 point-degree-two witness')
   require(set(Counter(x for e in P[1:] for x in e).values())=={4,5},'P9 degree list')
  elif kind=='forbidden_peripheral_triple':
   require(s==[6]*4 and p==[1]*6 and t==[0]*4 and q==1 and ds==[16]*4,'K4 profile')
   j=route['link_hub'];require(j in range(4) and set(route['triple'])==K-{j},'peripheral witness')
  elif kind=='incompatible_actual_tail':
   require(s==[7]*4 and p==[0]*6 and t==[1]*4 and q==0 and ds==[16]*4,'four triples profile')
   require(route['trace']==[1,2,3] and route['read_at_hubs']==[1,2],'shared-member readers')
   require(route['forced_disjoint_triads']==[[4,5,6],[7,8,9]],'tail-support mismatch')
   require(not set(route['forced_disjoint_triads'][0])&set(route['forced_disjoint_triads'][1]),'tail supports not disjoint')
  else:raise ValueError('unknown closing route')
 require(tally==Counter({'exact_P9_complement':6,'P9_degree_two':3,'forbidden_peripheral_triple':1,'incompatible_actual_tail':1}),'route coverage')
 return dict(sorted(tally.items()))

@lru_cache(maxsize=1)
def terminal_expected():
 out=[];loadchecks=0;shortchecks=0
 for omitted in (None,*map(enc,P)):
  H=[h for h in P if enc(h)!=omitted]
  tr=[]
  for size in range(4):
   for c in map(frozenset,combinations(range(9),size)):
    covers=all(c&h for h in H)
    if size<3:require(not covers,'short transversal counterexample');shortchecks+=1
    elif covers:tr.append(enc(c))
  expected=set(P) if omitted is None else set(P)|{frozenset(range(6))-dec(omitted)}
  require(set(map(dec,tr))==expected,'three-point transversal catalogue')
  loads=[]
  for c in map(frozenset,combinations(range(6),4)):
   n=sum(h<=c for h in H);loads.append([enc(c),n]);loadchecks+=1
   require(n==2 if omitted is None else n>=1,'internal quadruple load lower bound')
  out.append({'omitted':omitted,'triple_transversals':tr,'fourset_loads':loads})
 # Complements are disjoint. For external tails in a four-symbol universe,
 # check all two-class allocations of size at most two. The ordinary proof
 # reduces arbitrary external support to this case, independently of labels.
 complementary_tests=0;attained=0
 T=P[0];U=frozenset(range(6))-T
 options=[frozenset(c) for size in range(3) for c in combinations(range(6,10),size)]
 for a,b in product(options,repeat=2):
  F=[T|{v} for v in a]+[U|{v} for v in b];complementary_tests+=1
  if all(x&y for x,y in combinations(F,2)):
   require(len(F)<=2,'complementary trace capacity');attained=max(attained,len(F))
 require(attained==2,'joint capacity not reached')
 return out,{'terminal_omissions':len(out),'short_transversal_checks':shortchecks,'internal_load_checks':loadchecks,'complementary_tail_allocations':complementary_tests}

def check_positives(data):
 names=['single_R16_star','sharp_terminal_twenty','sharp_intersecting_twenty_six','nonintersecting_P9_link_guard']
 require([r['name'] for r in data]==names,'positive family coverage');counts=[];triples=0
 for r in data:
  F=list(map(dec,r['members']));require(all(len(f)==4 for f in F) and sf(F),'positive family invalid')
  ds=Counter(v for f in F for v in f);mu=min(sum(bool(f&g) for g in F) for f in F)
  require(r['M']==len(F) and r['support']==len(ds) and r['degrees']==sorted(ds.values()) and r['mu']==mu,'positive metadata differs')
  if r['name']=='single_R16_star':
   require(len(F)==16 and {f-{10} for f in F}==set(R),'R16 star control')
  elif r['name']=='sharp_terminal_twenty':
   require(len(F)==20 and all(a&b for a,b in combinations(F,2)),'twenty control')
   require({f-{6} for f in F if 6 in f}==set(P),'terminal full point link')
  elif r['name']=='sharp_intersecting_twenty_six':
   require(len(F)==26 and ds[6]==ds[7]==16 and all(a&b for a,b in combinations(F,2)),'twenty-six control')
   require(sum({6,7}<=f for f in F)==6,'universal pair-six guard')
  else:
   require(len(F)==35 and {f-{6} for f in F if 6 in f}==set(P[1:]),'nonintersecting exact-P9 control')
   require(any(not(a&b) for a,b in combinations(F,2)),'intersecting guard not actually violated')
  triples+=math.comb(len(F),3);counts.append({'name':r['name'],'M':len(F),'support':len(ds),'mu':mu,'max_degree':max(ds.values())})
 return triples,counts

def validate(data):
 require(data['contract']==CONTRACT,'changed theorem/import contract')
 require(data['pair_order']==list(map(list,PAIRS)),'pair order')
 require(data['P10']==list(map(enc,P)) and data['R16']==sorted(map(enc,R)),'model mismatch')
 outer,stage,records=reconstruct_profiles()
 require(data['outer_pair_triple_states']==outer and data['stage_counts']==stage,'census count mismatch')
 require([r['values'] for r in data['core_records']]==records,'profile list incomplete or changed')
 routing=check_routes(data['core_records']);facts=structural_facts()
 expected,term=terminal_expected();require(data['terminal_panel']==expected,'terminal coverage data changed')
 triples,positives=check_positives(data['positive_families'])
 return {'status':'PASS_R16_STAR_CAP61','global67_proved':False,'carrier18_nohigh_fully_excluded':False,
 'local_theorem':{'mu_min':41,'max_degree':18,'R16_star_upper_members':61},
 'finite_core':{'outer_states':outer,'stages':stage,'routes':routing},'structural_checks':facts,
 'terminal_checks':term,'positive_ternas':triples,'positive_families':positives}

def mutations(data):
 changes=[
 ('contract:mu_guard',lambda d:d['contract'].__setitem__('mu_min',40)),
 ('contract:global67',lambda d:d['contract'].__setitem__('global67_proved',True)),
 ('contract:whole_carrier',lambda d:d['contract'].__setitem__('carrier18_nohigh_fully_excluded',True)),
 ('omit_profile',lambda d:d['core_records'].pop()),
 ('duplicate_profile',lambda d:d['core_records'].append(copy.deepcopy(d['core_records'][0]))),
 ('wrong_stage_count',lambda d:d['stage_counts'].__setitem__(0,d['stage_counts'][0]+1)),
 ('wrong_tail_identification',lambda d:next(r for r in d['core_records'] if r['route']['kind']=='incompatible_actual_tail')['route'].__setitem__('forced_disjoint_triads',[[4,5,6],[4,8,9]])),
 ('wrong_marked_degree',lambda d:next(r for r in d['core_records'] if r['route']['kind']=='P9_degree_two')['route'].__setitem__('marked_degree',3)),
 ('incorrect_P9_center',lambda d:next(r for r in d['core_records'] if r['route']['kind']=='exact_P9_complement')['route'].__setitem__('hub',next(i for i,x in enumerate(next(r for r in d['core_records'] if r['route']['kind']=='exact_P9_complement')['values'][:4]) if x==8))),
 ('missing_exceptional_transversal',lambda d:d['terminal_panel'][1]['triple_transversals'].pop()),
 ('false_internal_load',lambda d:d['terminal_panel'][1]['fourset_loads'][0].__setitem__(1,99)),
 ('duplicate_positive_edge',lambda d:d['positive_families'][0]['members'].__setitem__(0,d['positive_families'][0]['members'][1])),
 ('wrong_positive_intersection',lambda d:d['positive_families'][3].__setitem__('mu',35)),
 ('missing_literal_R16_block',lambda d:d['R16'].pop())]
 out=[]
 for name,change in changes:
  d=copy.deepcopy(data);change(d)
  try:validate(d)
  except (ValueError,KeyError,IndexError,TypeError,StopIteration) as e:out.append({'name':name,'rejected':str(e)})
  else:raise ValueError('undetected mutation: '+name)
 return out

def main():
 path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'certificates/core_certificate.json'
 data=json.loads(path.read_text(encoding='utf-8'));out=validate(data);out['mutation_tests']=mutations(data)
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
