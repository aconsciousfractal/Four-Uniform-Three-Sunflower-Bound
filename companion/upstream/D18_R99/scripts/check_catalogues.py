"""Complete coverage and73 inherited P9 certificates. No solver."""
from common import *
from itertools import combinations,permutations,combinations_with_replacement,product
import audit_pair as a,pair_model as p,auditor,copy

M=tuple(a.a.blocks(9))
def autos():return tuple(g for g in permutations(range(6)) if {tuple(sorted(g[v] for v in T)) for T in M}==set(M))
def internal_orbit(I,G):return {tuple(sorted(tuple(sorted(g[v] for v in Q)) for Q in I)) for g in G}
def orbit(mark,G):
 out=set();A=tuple(v for v in mark if v<6);B=tuple(v-6 for v in mark if 6<=v<12);hasext=12 in mark
 for g,h in product(G,repeat=2):
  U=tuple(g[v] for v in A);V=tuple(h[v]+6 for v in B)
  for flip in (False,True):
   T=tuple((v+6 if v<6 else v-6) if flip else v for v in U+V)
   for w in range(12,22) if hasext else (None,):out.add(tuple(sorted(T+((w,) if hasext else ()))))
 return out

def coverage(records,front):
 G=autos();need(len(G)==6,'Aut(P9)')
 rem=front['remaining'];need(len(rem)==6,'six inherited types')
 one=set().union(*(internal_orbit(r['interiors'],G) for r in rem));need(len(one)==19,'19 labelled interiors')
 covered=set();inter=[x['problem'] for x in records if x['problem']['stage']=='interior_pair']
 need(len(inter)==20,'20 nonempty pairs')
 seen=set()
 for prob in inter:
  pair=prob['pair'];need(prob['id']==pair['id'] and prob['id'] not in seen,'pair identity');seen.add(prob['id'])
  I=tuple(tuple(Q) for Q in pair['interiors_first']);J=tuple(tuple(v-6 for v in Q) for Q in pair['interiors_second'])
  O={(x,y) for x,y in product(internal_orbit(I,G),internal_orbit(J,G))};O|={(y,x) for x,y in O}
  need(not covered&O,'duplicate pair orbit');need(len(O)==pair['labelled_orbit_size'],'pair orbit size');covered|=O
 need(covered==set(product(one,repeat=2))-{((),())},'360 nonempty pair coverage')
 families={}
 for stage,size in [('mixed_four',4),('mixed_three',3)]:
  branches=[x['problem'] for x in records if x['problem']['stage']==stage]
  need(len(branches)==(22 if size==4 else 8),'mixed orbit count')
  union=set();sizes=[]
  for pr in branches:
   mark=pr['mark'];need(len(mark)==4 and len(set(mark))==4 and sorted(mark)==mark,'marker')
   if size==4:need(max(mark)<12,'no exterior in stage4')
   else:need(mark[-1]==12,'one canonical exterior')
   O=orbit(mark,G);need(not union&O,'disjoint mark orbits');union|=O;sizes.append(len(O))
  expected=set()
  for Q in combinations(range(22),4):
   y=set(Q)&set(range(6));z=set(Q)&set(range(6,12))
   if len(y)+len(z)==size and y and z:expected.add(Q)
  need(union==expected,'full mixed coverage '+stage);families[stage]={'covered':len(union),'orbit_sizes':sizes}
 return {'labelled_interiors':len(one),'labelled_pairs':len(covered)+1,'new_nonempty_pairs':len(covered),'mark_stages':families}

def run():
 ca=a.a.catalog(9);cp=p.p.catalog(9);need(ca==cp,'literal inherited interior catalogue')
 need(ca['internal_count']==373 and len(ca['records'])==79,'373/79')
 idx=load('data/INHERITED_INDEX.json');need(len(idx)==73,'73 imported certificates')
 front=load('data/ENTRY_R99_INTERIOR_FRONTIER.json');ids={r['id'] for r in front['remaining']}
 need({r['id'] for r in ca['records']}-{r['id'] for r in idx}==ids,'exact imported remaining classes')
 out=[]
 for rec in idx:
  c=load(rec['path']);need(c['case']==rec['case'],'inherited case binding')
  d=a.a.build(c['case']);prod=p.p.build(c['case']);d['upper']=a.a.pair_rows(c['case']);prod['upper']=p.p.pair_constraints(prod,9)
  for key in ('bounds','equal','upper','quads','zero','caps','anchor_rows'):need(d[key]==prod[key],'inherited model '+key)
  out.append(a.a.check(c,d))
 cases=load('data/CASES.json');cov=coverage(cases,front)
 mutations=0
 for cid in ('R99_0_1','MIX_01','MIX_00_K2'):
  alt=[x for x in cases if x['problem']['id']!=cid];rejected(lambda alt=alt:coverage(alt,front));mutations+=1
 alt=copy.deepcopy(cases);next(x for x in alt if x['problem']['stage']=='mixed_three')['problem']['mark'][-1]=13
 rejected(lambda:coverage(alt,front));mutations+=1
 emit({'status':'PASS','inherited_certificates':len(out),'inherited_literal_models':len(out),'interior_catalogue':{'families':373,'orbits':79},'coverage':cov,'mutations_rejected':mutations,'inherited_records':out})
if __name__=='__main__':run()
