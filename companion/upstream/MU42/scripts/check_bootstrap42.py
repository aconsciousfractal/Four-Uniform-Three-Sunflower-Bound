"""Two complete reconstructions of R42.6 and N42.6, with joint H-lower bounds."""
from pathlib import Path
import json,time,argparse
import component42 as producer
import audit_components42 as auditor
import correlated42 as joint_p
import audit_correlated42 as joint_a
ROOT=Path(__file__).resolve().parents[1]
KEYS=('mu','central_size','outside_cap','r10','r9','internal_count','base_row_count','pre_external_cap_colorings','remaining_colorings','remaining_internals','survivors')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def normal(x):return json.loads(json.dumps(x))
def run():
 results=[];start=time.monotonic();small=auditor.verify_small_inputs()
 for m,pre,old in ((10,341,16),(9,666,24)):
  name=f'm{m}_k5_r0_0';p=normal(producer.run(m,5,42,0,0));a=normal(auditor.run(m,5,0,0,42))
  saved=json.loads((ROOT/'certificates/bootstrap'/f'{name}.json').read_text())
  for key in KEYS:need(p[key]==a[key]==saved[key],('scalar state mismatch',m,key))
  need(p['pre_external_cap_colorings']==pre and p['remaining_colorings']==old,'pre-correlation universe')
  jp=joint_p.refine(p);ja=joint_a.refine(a);js=json.loads((ROOT/'certificates/bootstrap'/f'correlated_{name}.json').read_text())
  need(jp==ja==js,'joint exterior requirements differ')
  need(jp['budget_vectors']==256 and jp['input_states']==old and jp['open_states']==0,'incomplete joint exclusion')
  # Compare the complete retained local alternatives on every remaining internal mask.
  for mask in sorted({v['internal_mask'] for v in jp['states']}):
   r1=joint_p.relations(m,5,0,0,mask);r2=joint_a.alternatives(m,5,0,0,mask)
   x=[(A,{d:set(v) for d,v in R.items()}) for A,R in r1]
   need(x==r2,'complete local alternative mismatch')
  results.append({'component':m,'internal_count':p['internal_count'],'base_row_count':p['base_row_count'],'pre_scalar_capacity':pre,'before_joint':old,'joint_tests':256*old,'after_joint':0,'literal_reconstructions':True})
  print('P'+str(m),'all states excluded at k<=5',flush=True)
 return {'status':'PASS','mu':42,'claim':'s=9 or 10 implies k>=6, under the declared inputs','stages':results,'small_geometry':small,'seconds':time.monotonic()-start}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();need(not a.output.exists(),'fresh output');out=run();a.output.write_text(json.dumps(out,indent=2)+'\n')
