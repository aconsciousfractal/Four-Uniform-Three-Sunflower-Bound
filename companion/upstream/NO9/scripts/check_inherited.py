"""Replay the specific inherited 77 exclusions, not the entire bound69 history."""
from common import *
from fractions import Fraction
import projection as P,audit_projection as A

def primal(c,d):
    need(c['case']==d['case'],'primal binding')
    need(len(c['values'])==len(d['bounds']),'primal length')
    for z in c['values']:need(type(z)is list and len(z)==2 and all(type(a)is int for a in z) and z[1]>0,'rational entry')
    v=[Fraction(*z)for z in c['values']]
    need(all(a<=z<=b for z,(a,b)in zip(v,d['bounds'])),'primal box')
    for name,co,rhs in d['equal']:need(sum(w*v[j]for j,w in co.items())==rhs,'primal equality '+name)
    for name,co,rhs in d['upper']:need(sum(w*v[j]for j,w in co.items())<=rhs,'primal upper '+name)
    return dict(columns=len(v),noninteger=sum(a.denominator>1 for a in v),singleton_sum=str(sum(v[:6])))
def run():
    saved=load('data/inherited/D16_INTERIORS.json')
    need((saved['mu'],saved['global_cap'],saved['centre_degree'],saved['component'],saved['outside'])==(42,16,16,9,7),'inherited scope')
    cat=P.catalog(9);need(cat==A.catalog(9)==saved['catalogue'],'full inherited 373/79 catalogue')
    need(cat['internal_count']==373 and len(cat['records'])==79 and len(saved['records'])==79,'catalogue dimensions')
    out=[];openids=[];closed=immediate=0
    for spec,rec in zip(cat['records'],saved['records']):
        c=rec['case'];need(c==dict(id=spec['id'],component=9,outside=7,r10=7,r9=7,interiors=spec['interiors']),'case cover')
        p=P.build(c);d=A.build(c);p['upper']=P.pair_constraints(p,9);d['upper']=A.pair_rows(c)
        need(p==d,'literal inherited model '+spec['id'])
        if rec['status']=='CLOSED':
            cert=load('inherited/certificates/'+Path(rec['certificate']).name)
            need(cert['case']==c,'inherited certificate binding');res=A.check(cert,d);closed+=1;immediate+=0 in d['live_sizes']
        elif rec['status']=='OPEN':
            res=primal(load('data/inherited/'+Path(rec['primal']).name),d);openids.append(spec['id'])
        else:raise ValueError('bad inherited stage')
        out.append(dict(id=c['id'],historical_status=rec['status'],result=res))
    need(closed==77 and immediate==75 and openids==['P9_000','P9_004'],'inherited boundary')
    emit(dict(status='PASS',models_compared=79,certificates_replayed=77,immediate=75,primal_points_verified=2,remaining_before_new_forests=openids,records=out))
if __name__=='__main__':run()
