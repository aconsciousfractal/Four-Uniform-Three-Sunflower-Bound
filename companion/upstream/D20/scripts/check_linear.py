"""Reconstruct every necessary model twice, then verify all eight certificates."""
import json
from fractions import Fraction
from common import ROOT,need,check_index,main
import model,audit

def run():
 index=json.loads((ROOT/'certificates/INDEX.json').read_text());check_index(index)
 need({p.name for p in (ROOT/'certificates').glob('*.json')}=={'INDEX.json'}|{c['id']+'.json' for c in index['cases']},'certificate file set')
 out=[]
 for case in index['cases']:
  c=json.loads((ROOT/'certificates'/(case['id']+'.json')).read_text());need(c['case']==case,'case binding')
  a=model.build(case);b=audit.build(case)
  need(set(a)==set(b),'model fields')
  for key in a:need(a[key]==b[key],'literal coefficients or domain mismatch: '+key)
  row=audit.verify(c,b);row['literal_models_equal']=True;out.append(row)
  print(case['id'],'PASS',row['ratio'],flush=True)
  del a,b
 return {'status':'PASS','certificates':len(out),'proof_certificates':7,'supplementary_certificates':1,'literal_model_comparisons':len(out),'upper':sum(v['mode']=='upper' for v in out),'infeasible':sum(v['mode']=='infeasible' for v in out),'results':out}
if __name__=='__main__':main(run)
