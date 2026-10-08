from common import *
from core_generation import census,canon
import models,audit_model
import sys
sys.path.insert(0,str(ROOT/'scripts/inputs'))
import local43,audit43

def run():
    a=tuple(sorted(tuple(r)for r in local43.enumerate_rows(mu=42,r10=7,r9=7,cap_degree=16)if max(r[10:])<=8 and min(degree(r))>=4))
    b=tuple(sorted(tuple(r)for r in audit43.enumerate_rows(mu=42,r10=7,r9=7,cap=16)if max(r[10:])<=8 and min(degree(r))>=4))
    require(a==b==base_rows(),'independent base row lists')
    roots=high_roots();data=load('data/CORES.json');require(len(roots)==len(data)==36,'root coverage')
    require(sum(r['ordered_count']for r in roots)==157,'all N45 rows covered')
    for r,stored in zip(roots,data):
        require(r['id']==stored['id']and r['row']==stored['row'],'root identity')
        x,sx=census(r['row']);y,sy=census(r['row'],True)
        expected=[tuple(tuple(q)for q in c)for c in stored['cores']]
        require(x==y==expected,'entire core coverage: '+str(r['id']))
        require(sx==stored['primary_levels']and sy==stored['alternate_levels'],'level counts')
    screen=load('data/ANCHOR_SCREEN.json');require(screen['complete_through']==35,'screen incomplete')
    ref={(r['root'],r['core']):r for r in screen['refuted']};left={(r['root'],r['core'])for r in screen['survive']}
    allkeys={(r['id'],i)for r in data for i in range(len(r['cores']))}
    require(not set(ref)&left and set(ref)|left==allkeys,'full core partition')
    cases=load('data/CERTIFICATE_CASES.json');require({(c['root'],c['core'])for c in cases}==left,'linear leaves cover all survivors')
    for (ri,ci),rec in ref.items():
        core=data[ri]['cores'][ci];row=data[ri]['row'];Q=rec['anchor']
        require(Q in core,'not an actual anchor')
        F,ts,bs=audit_model.trace_sets(core)
        fs,lo,hi,rows=audit_model.bounds_for_anchor(core,row,Q,F,ts,bs)
        require(list(lo)==rec['low']and list(hi)==rec['upper'],'trace intervals mismatch')
        require(not rows,'claimed empty domain is nonempty')
    emit(dict(status='PASS',base_rows=len(a),oriented_rows=len(oriented_rows()),high_rows=157,root_orbits=36,empty_root_orbits=sum(not r['cores']for r in data),cores=len(allkeys),anchor_refutations=len(ref),linear_leaves=len(left),last_root_cores=len(data[35]['cores']),same_complete_lists=True))
if __name__=='__main__':run()
