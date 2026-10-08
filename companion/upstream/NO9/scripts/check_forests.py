"""Full, standard-library replay of the two new centre16/cap16 trace forests."""
from common import *
from verify_component import Check
import gzip

def run():
    result=[]
    for name,I,labelled,canonical in [('empty',[],30,11),('single',[[0,3,4,5]],82,49)]:
        prefix=ROOT/'data'/name/'forest';saved=load('data/'+name+'/forest.profiles.json')
        need((saved['mu'],saved['global_cap'])==(42,16),'new forest scope')
        c=dict(id='P9_000' if not I else 'P9_004',component=9,outside=7,r10=7,r9=7,interiors=I)
        need(c==saved['case'],'new component case')
        C=Check(c);profiles,rows=C.domain(prefix,compare=True)
        need(len(profiles)==canonical and len(saved['labelled'])==labelled,'complete profile counts')
        expected=load('data/'+name+'/EXPECTED.json');need(len(expected)==canonical,'all expected records')
        need({p.name for p in prefix.parent.glob('forest_*.bin.gz')}=={f'forest_{i}.bin.gz'for i in range(canonical)},'no missing or extra forest files')
        totals=dict(joinnodes=0,margin_patterns=0,projections=0);reasons=[0]*10
        for i in range(canonical):
            d=C.verify(i,profiles,rows,prefix);e=expected[i]
            need(e['status']=='EXHAUSTED','producer left a profile open')
            for key in ('case','profile','joinnodes','margin_patterns','projections','reasons'):need(e[key]==d[key],'literal replay statistics '+key)
            for key in totals:totals[key]+=d[key]
            reasons=[a+b for a,b in zip(reasons,d['reasons'])]
        need(not reasons[0] and not reasons[7] and not reasons[9],'no open/disabled leaves')
        result.append(dict(name=name,case=c,anchor_rows=sum(map(len,rows)),labelled_profiles=labelled,canonical_profiles=canonical,**totals,reasons=reasons,refutation_leaves=sum(reasons),open_leaves=0))
        C.components.cache_clear()
    need(sum(x['projections']for x in result)==41026 and sum(x['refutation_leaves']for x in result)==22777,'new forest totals')
    emit(dict(status='PASS',canonical_profiles=60,all_profiles_covered=True,open_leaves=0,records=result))
if __name__=='__main__':run()
