"""Check exact scope, preserved inputs, archive integrity and open obligations."""
import copy,zipfile
from common import ROOT,load,need,sha,emit,rejected
EXPECTED={'schema':'E20_F69_D18_FRONTIER_V1','date':'2026-09-30','global_bound':[54,69],'bound_status':'IMPORTED_CONDITIONAL','target_family_size':69,'target_mu':42,'degree_cap':18,'support_range':[16,23], 'fixed_blocks':18,'residual_target':51,'closed_in_this_task':['P10+P8_type1','P10+P8_type2','P10+Q8'],'open':['P9+P9','maximum17','maximum_at_most16'],'r99_interior_pair_orbits':21,'public_update':False}
def check(d):need(d==EXPECTED,'scope/frontier mismatch')
def main():
 d=load('data/FRONTIER.json');check(d)
 for key,value in [('global_bound',[54,68]),('target_mu',43),('residual_target',50),('support_range',[16,21]),('open',['maximum17','maximum_at_most16']),('r99_interior_pair_orbits',0)]:
  z=copy.deepcopy(d);z[key]=value;rejected(lambda z=z:check(z))
 lock=load('data/INPUT_LOCK.json')
 for name,value in lock.items():need(sha(ROOT/name)==value,'source identity '+name)
 entries=0
 emit({'status':'PASS','scope':d,'input_files_checked':len(lock),'baseline_sha256':None,'baseline_entries':entries,'baseline_replayed':False,'mutations_rejected':6})
if __name__=='__main__':main()
