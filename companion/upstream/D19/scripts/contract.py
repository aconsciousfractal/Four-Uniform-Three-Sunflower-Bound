"""Proof stages and exact coverage binding, independently of numerical output."""
import json
from common import ROOT,need
EXTERNAL_MARKS=((0,1,2,6),(0,1,2,9),(0,1,2,12),(0,1,3,6),(0,1,3,9),(0,1,3,12),(0,1,6,7),(0,1,6,9),(0,1,6,10),(0,1,6,12),(0,1,9,10),(0,1,9,12),(0,6,7,8),(0,6,7,9),(0,6,7,11),(0,6,7,12),(0,6,9,10),(0,6,9,11),(0,6,9,12),(0,6,10,12),(0,9,10,11),(0,9,10,12),(6,7,8,12),(6,7,9,12),(6,7,11,12),(6,9,10,12),(6,9,11,12),(9,10,11,12))
FULL_MARKED={9,11,15,18,19,21}
CONTRACT={'family_size':69,'mu_min':42,'max_degree':19,'pair_cap':6,'triple_cap':2,'simple':True,'empty_core_forbidden':True,'support_min':16,'support_max':23,'minimum_used_degree':4,'minimum_used_pair_degree_sum':20,'minimum_anchor_degree_sum':52,'center_label':22,'fixed_members':19,'residual_members':50,'r10':7,'r9':7,'global_bound':[54,69],'F69_excluded':False,'max19_excluded':True,'max20_imported_excluded':True,'max18_excluded':False,'max17_excluded':False,'low16_excluded':False}
def expected_records():
    def case(ident,mark=None,empty=False,marked=False,assigned=None):
        d={'id':ident,'mark':None if mark is None else list(mark),'empty':empty,'marked':marked,'min_w':0,'objective':'cardinality'}
        if assigned is not None:d['assigned']=assigned
        return d
    rows=[]
    def add(stage,c):rows.append({'stage':stage,'file':'certificates/'+c['id']+'.json','case':c})
    for i,m in enumerate(((6,7,8,9),(6,7,9,10),(6,7,9,11)),1):add('P9-individual',case('I%02d'%i,m))
    for k in (1,2):add('P9-complete',case('J'+str(k),assigned={'1':[[v,9,10,11] for v in range(6,6+k)]}))
    cat=json.loads((ROOT/'data/P10_FULL_INTERIOR_CATALOGUE.json').read_text())
    need(len(cat['classes'])==13 and cat['classes'][0]['representative']==[],'thirteen P10 classes')
    for i,item in enumerate(cat['classes'][1:],1):add('P10-after-P9-empty',case('P%02d'%i,assigned={'0':item['representative'],'1':[]}))
    for i,m in enumerate(EXTERNAL_MARKS):
        if i in (24,26):continue
        add('external-after-interiors-empty',case('E%02d'%i+('M' if i in FULL_MARKED else ''),m,True,i in FULL_MARKED))
    need(len(rows)==43,'43 main certificates');return rows

def expected_index():
    return {'schema':'E20_F69_D19_PROOF_INDEX_V1','contract':CONTRACT,'records':expected_records(),'admitted_large_orbits':['E24','E26'],'terminal':{'mixed_residual_cap':44,'residual_target':50,'kappa_reference':11,'deficit_upper':3,'deficit_required':37,'lower_disjoint_pairs':547,'H27_capacity':513}}
def validate_index(data=None):
    expected=expected_index();data=json.loads((ROOT/'certificates/INDEX.json').read_text()) if data is None else data
    need(data==expected,'proof index or contract mismatch')
    for row in data['records']:
        cert=json.loads((ROOT/row['file']).read_text());need(cert['case']==row['case'],'case coverage binding '+row['case']['id'])
        need(cert['target']==50,'residual target 50')
    return data
