"""Scope lock, exact certificate identities, and deliberately corrupted inputs."""
from pathlib import Path
from math import comb
from copy import deepcopy
import json,hashlib,zipfile,argparse,time
import audit_projection42 as audit
import charge42
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_frontier(f):
 need(f.get('schema')=='E20_F69_MU42_FRONTIER_V1','frontier schema')
 need(f.get('global_bound')==[54,69] and f.get('bound_status')=='IMPORTED_CONDITIONAL_UNCHANGED','no new global numerical bound')
 need(f.get('mu')==42 and f.get('target_cardinality')==69,'correct cardinality/threshold')
 need(f.get('support')==[16,23] and f.get('minimum_used_degree')==4,'new support and minimum-degree scope')
 need(f.get('r10_min_k')==f.get('r9_min_k')==7,'certified local level')
 need(f.get('no_P10_at17') is False and f.get('current_task_excludes_any_F69_maximum_degree_branch') is False,'no hidden F69 exclusion')
 branches=f.get('branches');need(type(branches)is list and len(branches)==5,'all F69 branches present')
 need([b['maximum_degree'] for b in branches]==['at_most_16',17,18,19,20] and all(b['status']=='OPEN' for b in branches),'complete open frontier')
 need([b['support'] for b in branches]==[[18,23],[17,23],[16,23],[16,23],[16,23]],'branch support bounds')
 r=f.get('next_root',{});need((r.get('fixed_members'),r.get('residual_members'),r.get('ambient_labels'),r.get('residual_universe'))==(20,49,23,comb(22,4)),'next-root arithmetic')
 need(r.get('target_kappa')==12 and r.get('necessary_deficit')==12*49-27*20==48,'next-root deficit')
def validate_names(names):
 expected={f'P10_{i:03d}.cert.json' for i in range(13)}|{f'P9_{i:03d}.cert.json' for i in range(79)}
 need(set(names)==expected and len(names)==92,'all 92 certificate branches covered')
def run():
 start=time.monotonic();f=json.loads((ROOT/'FRONTIER.json').read_text());validate_frontier(f)
 names=[p.name for p in (ROOT/'certificates/projections').glob('*.cert.json')];validate_names(names)
 identity={'status':'OMITTED_DOCUMENTARY_BASELINE_INTEGRITY','mathematical_premise':False}
 rejected=[]
 def bad(name,fn):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError) as e:rejected.append({'test':name,'rejected':True,'reason':str(e)})
  else:raise ValueError('MUTATION ACCEPTED: '+name)
 for id in ('P10_000','P9_000','P9_004'):
  c=json.loads((ROOT/'certificates/projections'/(id+'.cert.json')).read_text());d=audit.build(c['case']);audit.check(c,d)
  changes=[('schema',lambda x:x.update(schema='UNSUPPORTED')),
   ('nonpositive_scale',lambda x:x.update(scale=0)),('column_count',lambda x:x.update(columns=x['columns']+1)),
   ('row_count',lambda x:x.update(equal_rows=x['equal_rows']-1)),('false_gap',lambda x:x.update(value=x['value']-1)),
   ('false_rhs',lambda x:x.update(rhs=x['rhs']+1)),('false_box',lambda x:x.update(box_min=x['box_min']-1)),
   ('missing_multiplier',lambda x:x['equal'].pop()),('repeated_row',lambda x:x['equal'].append(list(x['equal'][0]))),
   ('row_out_of_range',lambda x:x['equal'][0].__setitem__(0,x['equal_rows'])),
   ('zero_multiplier',lambda x:x['equal'][0].__setitem__(1,0)),
   ('false_case_binding',lambda x:x['case'].update(outside=7))]
  for name,change in changes:
   cc=deepcopy(c);change(cc);bad(id+':'+name,lambda cc=cc,d=d:audit.check(cc,d))
 c=json.loads((ROOT/'certificates/STAR_CHARGE42.json').read_text());charge42.validate(c)
 for name,change in [('mu43',lambda x:x.update(mu=43)),('false_minimum',lambda x:x.update(minimum_degree=5)),
  ('unproved_noP10',lambda x:x.update(no_P10_at17=True)),('negative_mantel',lambda x:x['mantel'].update({'4':-26})),
  ('negative_split',lambda x:x.update(split16=-18)),('weak_constant',lambda x:x.update(constant=3500)),
  ('lost_balance',lambda x:x['balance'].pop('18_8_10')),('lost_rows',lambda x:x.update(expected_rows=292559))]:
  cc=deepcopy(c);change(cc);bad('charge:'+name,lambda cc=cc:charge42.validate(cc))
 for name,change in [('false_bound68',lambda x:x.update(global_bound=[54,68])),('F69_closed',lambda x:x['branches'][4].update(status='CLOSED')),
  ('missing_branch',lambda x:x['branches'].pop()),('wrong_mu',lambda x:x.update(mu=43)),('wrong_support',lambda x:x.update(support=[16,21])),
  ('wrong_residuals',lambda x:x['next_root'].update(residual_members=50))]:
  ff=deepcopy(f);change(ff);bad('frontier:'+name,lambda ff=ff:validate_frontier(ff))
 bad('coverage:missing_P9',lambda:validate_names(names[:-1]));bad('coverage:duplicate_branch',lambda:validate_names(names+[names[0]]))
 for label,case in [('circular_P9',{'id':'x','component':9,'outside':6,'r10':7,'r9':7,'interiors':[]}),
                    ('changed_outside',{'id':'x','component':10,'outside':7,'r10':6,'r9':6,'interiors':[]})]:
  bad('stage:'+label,lambda case=case:audit.build(case))
 need(len(rejected)==54,'mutation-suite completeness')
 return {'status':'PASS','baseline_integrity_only':identity,'baseline_recursive_replay':False,'new_certificates':92,'negative_tests':len(rejected),'rejections':rejected,'frontier':f,'seconds':time.monotonic()-start}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();need(not a.output.exists(),'fresh output');o=run();a.output.write_text(json.dumps(o,indent=2)+'\n');print('scope, integrity, and',o['negative_tests'],'negative tests PASS')
