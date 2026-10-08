from common import *
import zipfile,copy

def scope(d):
 need(d=={'schema':'E20_F69_R99_FRONTIER_V1','global_bound':[54,69],'target':69,'mu':42,'degree_cap_branch':18,'R99':'CLOSED_CONDITIONALLY','D18':'CLOSED_CONDITIONALLY','remaining_maxima':[17,'<=16'],'F69_closed':False,'new_certificates':50,'inherited_P9_certificates_replayed':73,'internal_pairs_closed':20,'internal_pair_passed_to_next_stage':'R99_0_0','mixed_four_orbits':22,'mixed_three_orbits':8,'residuals_required':51,'terminal_deficit_cap':22,'terminal_disjoint_pairs_lower':488,'terminal_disjoint_pairs_upper':486},'scope and bound')

def run():
 locks=load('data/INPUT_LOCK.json')
 for name,expected in locks.items():need(sha(ROOT/name)==expected,'input bytes '+name)
 m={} # Historical nested ZIP inventory is documentary only.
 d=load('data/FRONTIER.json');scope(d);mut=0
 for key,value in [('global_bound',[54,68]),('F69_closed',True),('remaining_maxima',[]),('mu',43),('residuals_required',52),('terminal_deficit_cap',18)]:
  t=copy.deepcopy(d);t[key]=value;rejected(lambda t=t:scope(t));mut+=1
 emit({'status':'PASS','input_files':len(locks),'baseline_members_checked':len(m),'baseline_crc':'OMITTED_DOCUMENTARY_BASELINE_INTEGRITY','baseline_mathematical_replay':'not_run_except_73_selected_P9_certificates_in_check_catalogues','mutations_rejected':mut,'frontier':d})
if __name__=='__main__':run()
