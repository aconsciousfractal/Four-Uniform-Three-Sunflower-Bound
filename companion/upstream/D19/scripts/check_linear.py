"""Rebuild all 43 systems twice and check exact integer certificates and mutations."""
import json,copy,gc
from collections import Counter
from fractions import Fraction
from common import ROOT,need,main
from contract import validate_index
import audit,model,audit_assigned,model_assigned

def mutations(cert,data,checker):
    cases=[]
    v=copy.deepcopy(cert);v['value']+=1;cases.append(('arithmetic',v))
    v=copy.deepcopy(cert);v['scale']=0;cases.append(('scale-zero',v))
    v=copy.deepcopy(cert);v['target']=49;cases.append(('wrong-target',v))
    v=copy.deepcopy(cert);v['equal'].append([len(data['equal']),1]);cases.append(('index',v))
    v=copy.deepcopy(cert)
    if v['upper']:v['upper'][0][1]=-abs(v['upper'][0][1])
    else:v['equal'][0][1]=0
    cases.append(('weight-sign-or-zero',v))
    v=copy.deepcopy(cert);v['upper']=[];v['equal']=[];cases.append(('empty-combination',v))
    records=[]
    for name,bad in cases:
        try:checker(bad,data)
        except ValueError as e:records.append({'test':name,'rejected':True,'message':str(e)})
        else:raise ValueError('corrupted certificate accepted: '+name)
    return records

def run():
    index=validate_index();out=[];hist=Counter();columns=0
    for row in index['records']:
        cert=json.loads((ROOT/row['file']).read_text());assigned='assigned' in row['case']
        prod=model_assigned if assigned else model;check=audit_assigned if assigned else audit
        a=prod.build(row['case']);b=check.build(row['case'])
        need(set(a)==set(b),'model keys '+row['case']['id'])
        for key in a:need(a[key]==b[key],'literal model mismatch '+row['case']['id']+' '+key)
        result=check.verify(cert,b);result['literal_fields_compared']=sorted(a);result['stage']=row['stage']
        result['mutations']=mutations(cert,b,check.verify)
        hist[result['mode']]+=1;columns+=result['columns'];out.append(result)
        print('CERT',row['case']['id'],'PASS',result['ratio'],flush=True)
        del a,b;gc.collect()
    need(len(out)==43 and hist=={'upper':11,'infeasible':32},'complete certificate counts')
    margins=[Fraction(50*r['scale']-r['value'],r['scale']) if r['mode']=='upper' else Fraction(-r['value'],r['scale']) for r in out]
    return {'status':'PASS','certificates':43,'modes':dict(hist),'literal_models':43,'columns_compared_with_repetitions':columns,'maximum_model_columns':max(r['columns'] for r in out),'negative_tests':sum(len(r['mutations']) for r in out),'minimum_normalized_margin':str(min(margins)),'results':out}
if __name__=='__main__':main(run)
