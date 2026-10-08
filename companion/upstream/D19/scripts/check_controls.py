"""Finite positive families and explicit rejection of wrong proof scopes."""
from itertools import combinations
from collections import Counter
import copy,json
from common import ROOT,need,main
from contract import validate_index
import audit

def family_check(F):
    need(len(F)==len(set(F)) and all(len(q)==4 for q in F),'simple four-set family')
    count=0
    for A,B,C in combinations(F,3):
        need(not A&B==A&C==B&C,'sunflower in positive control');count+=1
    maxima={}
    for k,cap in ((1,20),(2,6),(3,2)):
        cc=Counter(T for Q in F for T in combinations(sorted(Q),k));m=max(cc.values());need(m<=cap,'capacity in positive control');maxima[str(k)]=m
    mu=min(sum(bool(A&B) for B in F) for A in F)
    return {'members':len(F),'ternas':count,'mu':mu,'maximum_codegrees':maxima}

def run():
    index=validate_index();rejected=[]
    def bad(tag,d):
        try:validate_index(d)
        except ValueError as e:rejected.append({'tag':tag,'message':str(e)})
        else:raise ValueError('invalid scope accepted '+tag)
    d=copy.deepcopy(index);d['records'].pop();bad('missing-external-case',d)
    d=copy.deepcopy(index);d['records'][3]['case']['assigned']['0']=[];bad('P10-premature-empty-in-J1',d)
    d=copy.deepcopy(index);d['records'][5]['case']['assigned'].pop('1');bad('P9-stage-missing',d)
    d=copy.deepcopy(index);d['records'][17]['case']['min_w']=2;bad('two-W-premise-forbidden',d)
    d=copy.deepcopy(index);d['contract']['mu_min']=43;bad('old-mu43',d)
    d=copy.deepcopy(index);d['contract']['global_bound']=[54,68];bad('false-bound68',d)
    d=copy.deepcopy(index);d['contract']['F69_excluded']=True;bad('unproved-full-F69',d)
    d=copy.deepcopy(index);d['contract']['max18_excluded']=True;bad('unproved-max18',d)
    d=copy.deepcopy(index);d['admitted_large_orbits']=[];bad('exceptions-erased',d)
    d=copy.deepcopy(index);d['terminal']['deficit_upper']=0;bad('unpaid-deficit',d)
    d=copy.deepcopy(index);d['terminal']['mixed_residual_cap']=42;bad('P5-exception-not-counted',d)
    d=copy.deepcopy(index);d['records']=d['records'][5:]+d['records'][:5];bad('proof-order-changed',d)
    fixed=tuple(frozenset((22,*T)) for T in audit.CONES);positive=[]
    for row in index['records']:
        case=row['case'];selected=set()
        if case['mark'] is not None:selected.add(frozenset(case['mark']))
        for vv in case.get('assigned',{}).values():selected.update(frozenset(q) for q in vv)
        F=fixed+tuple(sorted(selected,key=lambda x:tuple(sorted(x))))
        positive.append({'case':case['id'],**family_check(F)})
    def d27(base):
        groups=[tuple(range(base+3*i,base+3*i+3)) for i in range(3)]
        return tuple(frozenset(a+b) for i,j in combinations(range(3),2) for a in combinations(groups[i],2) for b in combinations(groups[j],2))
    lower=family_check(d27(0)+d27(9));need(lower['members']==54 and lower['ternas']==24804,'lower construction')
    exception=json.loads((ROOT/'data/POSITIVE_TWO_EXCEPTIONS.json').read_text())
    F=tuple(frozenset(q) for q in exception['family']);exc=family_check(F);need(exc['members']==22 and exc['ternas']==1540 and exc['mu']==11,'exception control')
    need(all(x['mu']<42 for x in positive),'positive controls not claimed as F69')
    return {'status':'PASS','negative_tests':len(rejected),'rejected':rejected,'positive_prescribed_families':positive,'positive_prescribed_ternas':sum(x['ternas'] for x in positive),'lower54':lower,'two_exception_control':exc,'finite_tests_do_not_prove_general_solver_correctness':True}
if __name__=='__main__':main(run)
