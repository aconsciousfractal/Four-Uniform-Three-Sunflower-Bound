"""Input identity, branch ledger, and the next cap19 domain at mu42."""
from pathlib import Path
import hashlib,json,sys,zipfile
from fractions import Fraction
from common import ROOT,need,main,check_index
sys.path.insert(0,str(ROOT/'sources'))
import audit43 as A
import local43 as B

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 index=json.loads((ROOT/'certificates/INDEX.json').read_text());check_index(index)
 lock=json.loads((ROOT/'data/INPUT_LOCK.json').read_text());need(lock['schema']=='E20_F69_D20_INPUT_LOCK_V1','input lock')
 for name,h in lock['sources'].items():need(sha(ROOT/name)==h,'input source altered '+name)
 members=0 # Nested historical ZIP custody is outside the mathematical suite.
 rows=A.enumerate_rows(mu=42,r10=7,r9=7,cap=19)
 kept=[];profiles=set();mind=99;pairmin=99;anchor=99
 for r in rows:
  ds=tuple(1+r[10+i]+sum(r[j] for j,(a,b) in enumerate(A.PAIR_LIST) if i in (a,b))+sum(r[6:10])-r[6+i] for i in range(4))
  if ds[0]<4:continue
  kept.append(r);profiles.add(ds);mind=min(mind,ds[0]);pairmin=min(pairmin,ds[0]+ds[1]);anchor=min(anchor,sum(ds))
 other=[]
 for r in B.enumerate_rows(mu=42,r10=7,r9=7,cap_degree=19):
  dd=tuple(1+r[10+i]+sum(r[j] for j,(a,b) in enumerate(B.PAIRS) if i in (a,b))+sum(r[6:10])-r[6+i] for i in range(4))
  if min(dd)>=4:other.append(bytes(r))
 need(sorted(other)==kept,'literal next-domain mismatch')
 need(mind>=4 and pairmin>=20 and anchor>=52,'next-domain prerequisites')
 frontier=json.loads((ROOT/'FRONTIER.json').read_text())
 expected={'schema':'E20_F69_D20_FRONTIER_V1','global_bound':[54,69],'F69_excluded':False,'F69_max20':'CLOSED_CONDITIONALLY','F69_max19':'OPEN','F69_max18':'OPEN','F69_max17':'OPEN','F69_max_le16':'OPEN','next_mu':42,'next_prescribed':19,'next_residuals':50,'next_universe_points':23,'next_support':[16,23],'next_terminal_kappa':11,'next_deficit':37}
 need(frontier==expected,'frontier scope')
 return {'status':'PASS','input_sources':len(lock['sources']),'baseline_members':members,'baseline_sha256':lock['baseline']['sha256'],'global_bound':[54,69],'F69_excluded':False,'F69_max20_excluded':True,'next_cap19_domain':{'mu':42,'rows':len(kept),'profiles':len(profiles),'min_degree':mind,'min_pair_sum':pairmin,'min_anchor_degree_sum':anchor,'prescribed':19,'residuals':50,'terminal_required':550,'H27_capacity':513,'deficit_required':37}}
if __name__=='__main__':main(run)
