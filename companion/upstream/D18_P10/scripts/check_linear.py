"""Reconstruct and check 85 finite contradictions, with literal model comparison."""
import copy
import audit_projection as A,projection as P
from common import ROOT,need,load,emit,rejected

def main():
 index=load('data/LINEAR_INDEX.json');need(len(index)==85,'85 binding records')
 need(len({c['id'] for c in index})==85,'unique cases')
 results=[];mutations=0
 for row in index:
  cert=load(row['path']);need(cert['case']==row['case'] and row['id']==cert['case']['id'],'index binding')
  d=P.build(cert['case']);a=A.build(cert['case'])
  d['upper']=P.pair_constraints(d,cert['case']['component']);a['upper']=A.pair_rows(cert['case'])
  for key in ('case','bounds','upper','equal','quads','zero','objective','target','live_sizes','internal_degrees','caps','anchor_rows'):
   need(d[key]==a[key],'literal model mismatch '+row['id']+' '+key)
  ans=A.check(cert,a);results.append(ans)
  tests=[]
  for key,val in [('schema','wrong'),('scale',0),('columns',cert['columns']+1),('value',cert['value']+1)]:
   c=copy.deepcopy(cert);c[key]=val;tests.append(c)
  c=copy.deepcopy(cert);c['equal']=[[len(a['equal']),1]];tests.append(c)
  c=copy.deepcopy(cert);c['upper']=[[0,-1]];tests.append(c)
  c=copy.deepcopy(cert);c['upper']=[];c['equal']=[];tests.append(c)
  for c in tests:rejected(lambda c=c:A.check(c,a));mutations+=1
 emit({'status':'PASS','certificates':len(results),'literal_models':len(results),'mutations_rejected':mutations,'records':results})
if __name__=='__main__':main()
