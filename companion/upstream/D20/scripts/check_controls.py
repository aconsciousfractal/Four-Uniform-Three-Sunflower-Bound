"""Deliberately damaged certificates and explicit small family checks."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,copy
from common import ROOT,need,main,check_index
import audit

def family_check(F):
 need(len(F)==len(set(F)) and all(len(q)==4 for q in F),'simple uniform family')
 count=0
 for A,B,C in combinations(F,3):
  need(not A&B==A&C==B&C,'sunflower in positive control');count+=1
 for k,cap in ((1,20),(2,6),(3,2)):
  cnt=Counter(T for Q in F for T in combinations(sorted(Q),k));need(max(cnt.values())<=cap,'positive capacity')
 return count

def run():
 index=json.loads((ROOT/'certificates/INDEX.json').read_text());check_index(index);rejected=[]
 def rejection(tag,f):
  try:f()
  except (ValueError,KeyError,IndexError,TypeError):rejected.append(tag)
  else:raise ValueError('mutation accepted: '+tag)
 for case in index['cases']:
  original=json.loads((ROOT/'certificates'/(case['id']+'.json')).read_text());data=audit.build(case);audit.verify(original,data)
  bad=copy.deepcopy(original);bad['value']+=1;rejection(case['id']+':value',lambda:audit.verify(bad,data))
  bad=copy.deepcopy(original);bad['scale']=0;rejection(case['id']+':scale',lambda:audit.verify(bad,data))
  bad=copy.deepcopy(original);bad['target']=48;rejection(case['id']+':target',lambda:audit.verify(bad,data))
  bad=copy.deepcopy(original);bad['equal'].append([len(data['equal']),1]);rejection(case['id']+':row-index',lambda:audit.verify(bad,data))
  bad=copy.deepcopy(original);bad['upper'][0][1]*=-1;rejection(case['id']+':upper-sign',lambda:audit.verify(bad,data))
  bad=copy.deepcopy(original);bad['upper']=[];bad['equal']=[];rejection(case['id']+':zero-weights',lambda:audit.verify(bad,data))
  del data
 bad=copy.deepcopy(index);bad['cases'].pop();rejection('coverage:missing-last-case',lambda:check_index(bad))
 bad=copy.deepcopy(index);bad['cases'][1]['empty']=False;rejection('scope:empty-premise',lambda:check_index(bad))
 bad=copy.deepcopy(index);bad['cases'][-1]['min_w']=0;rejection('scope:wrong-stage',lambda:check_index(bad))
 bad=copy.deepcopy(index);bad['contract']['mu']=43;rejection('scope:old-threshold',lambda:check_index(bad))
 bad=copy.deepcopy(index);bad['global_bound']=[54,68];rejection('scope:false-global-bound',lambda:check_index(bad))
 bad=copy.deepcopy(index);bad['F69_excluded']=True;rejection('scope:unproved-all-branches',lambda:check_index(bad))
 fixed=tuple(frozenset((22,*T)) for T in audit.CONES)
 root_counts=[]
 for case in index['cases']:
  F=fixed+(frozenset(case['mark']),);root_counts.append({'case':case['id'],'members':len(F),'triples_checked':family_check(F)})
 # Abbott--Hanson-type inherited 54 witness, reconstructed; not a mu42 example.
 def d27(base):
  g=[range(base+3*i,base+3*i+3) for i in range(3)];return tuple(frozenset((*a,*b)) for i,j in combinations(range(3),2) for a in combinations(g[i],2) for b in combinations(g[j],2))
 F=d27(0)+d27(9);lower=family_check(F)
 need(len(rejected)==54 and lower==24804,'counts')
 return {'status':'PASS','negative_tests':len(rejected),'rejected':rejected,'positive_marked_stars':root_counts,'positive_marked_star_ternas':sum(r['triples_checked'] for r in root_counts),'lower_witness_members':len(F),'lower_witness_ternas':lower,'positive_controls_are_not_mu42_examples':True}
if __name__=='__main__':main(run)
