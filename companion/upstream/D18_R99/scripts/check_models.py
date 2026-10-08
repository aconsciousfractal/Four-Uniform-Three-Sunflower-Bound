"""Rebuild and compare all50 models, then check the exact dual inequalities."""
from common import *
import auditor,producer,copy
from fractions import Fraction
from collections import Counter

def run():
 records=load('data/CASES.json');need(len(records)==50,'50 cases')
 outs=[];mutations=0;count=Counter();minmargin=None;anatomy=[]
 for item in records:
  prob=item['problem'];c=load(item['certificate']);d=auditor.build(prob);p=producer.build(prob)
  for key in ('case','bounds','equal','upper','objective','types'):
   need(d[key]==p[key],'literal comparison '+prob['id']+' '+key)
  ans=auditor.check(c,prob,d);outs.append(ans);count[prob['stage']]+=1
  margin=(Fraction(51)-Fraction(c['value'],c['scale'])) if c['mode']=='upper' else -Fraction(c['value'],c['scale'])
  minmargin=margin if minmargin is None else min(minmargin,margin)
  tests=[]
  for key,val in [('value',c['value']+1),('scale',0),('target',52),('mu',43),('degree_cap',19),('columns',c['columns']+1)]:
   t=copy.deepcopy(c);t[key]=val;tests.append(t)
  t=copy.deepcopy(c);t['upper']=[[0,-1]];tests.append(t)
  t=copy.deepcopy(c);t['equal']=[[len(d['equal']),1]];tests.append(t)
  t=copy.deepcopy(c);t['upper']=[];t['equal']=[];tests.append(t)
  t=copy.deepcopy(c);t['problem']['stage']='historic-F70';tests.append(t)
  for t in tests:rejected(lambda t=t:auditor.check(t,prob,d));mutations+=1
  used=[d['upper'][i][0] for i,w in c['upper']]
  anatomy.append({'case':prob['id'],'stage':prob['stage'],'upper_used':len(c['upper']),'equal_used':len(c['equal']),'pool_used':sum('pure-pool' in s for s in used),'W_aggregate_used':sum(s=='W-degree' or 'W-pairs' in s or 'W-triples' in s for s in used),'H27_anchor_used':sum(s.startswith('H27') for s in used)})
 emit({'status':'PASS','new_certificates':len(outs),'literal_models':len(outs),'by_stage':dict(count),'modes':dict(Counter(x['mode'] for x in outs)),'minimum_normalized_margin':str(minmargin),'max_columns':max(x['columns'] for x in outs),'mutations_rejected':mutations,'records':outs,'anatomy':anatomy})
if __name__=='__main__':run()
