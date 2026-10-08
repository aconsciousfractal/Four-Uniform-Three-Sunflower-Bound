"""Both complete interior censuses; coverage of 21 remaining R99 assignments."""
from itertools import permutations,product,combinations
import copy
import projection as P,audit_projection as A
from common import ROOT,need,load,emit,rejected

def compute():
 cats=[P.catalog(10),P.catalog(9)];other=[A.catalog(10),A.catalog(9)];need(cats==other==load('data/CATALOGUES.json'),'literal complete catalogues')
 need([(c['internal_count'],len(c['records']),c['automorphism_count']) for c in cats]==[(292,13,60),(373,79,6)],'counts')
 index=load('data/LINEAR_INDEX.json');by={m:{r['id'] for r in index if r['component']==m} for m in(10,9)}
 need(by[10]=={r['id'] for r in cats[0]['records'][1:]},'all nonempty P10 types')
 frontier=load('data/R99_INTERIOR_FRONTIER.json');surv=[r for r in cats[1]['records'] if r['id'] not in by[9]]
 need(surv==frontier['remaining'] and len(by[9])==73 and len(surv)==6,'P9 complement')
 M=P.models(9);autos=[p for p in permutations(range(6)) if {tuple(sorted(p[y] for y in T)) for T in M}==set(M)]
 orbit=lambda I:{tuple(sorted(tuple(sorted(p[y] for y in T)) for T in I)) for p in autos}
 orbs=[orbit(r['interiors']) for r in surv];need([len(o) for o in orbs]==[1,3,3,6,3,3],'remaining orbit sizes')
 universe=set().union(*orbs);need(len(universe)==19,'19 labelled interiors')
 pairs=set(product(universe,repeat=2));covered=set();expected=[]
 for i,a in enumerate(surv):
  for j in range(i,6):
   b=surv[j];orb=set(product(orbs[i],orbs[j]))|set(product(orbs[j],orbs[i]));need(not(covered&orb),'disjoint orbit pairs');covered|=orb
   expected.append(dict(id=f'R99_{i}_{j}',types=[a['id'],b['id']],interiors_first=a['interiors'],interiors_second=[[v+6 for v in q] for q in b['interiors']],labelled_orbit_size=len(orb),status='OPEN'))
 need(covered==pairs and len(pairs)==361 and expected==frontier['pair_roots'],'complete R99 pair coverage')
 return cats,frontier

def main():
 cats,f=compute()
 emit({'status':'PASS','P10_interiors':292,'P10_orbits':13,'P10_nonempty_excluded':12,'P9_interiors':373,'P9_orbits':79,'P9_orbits_excluded':73,'P9_labelled_remaining':19,'R99_pair_orbits':21,'R99_labelled_pairs':361,'all_pair_states':'OPEN','catalogue_sizes':[len(c['records']) for c in cats]})
if __name__=='__main__':main()
