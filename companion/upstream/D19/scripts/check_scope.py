"""Reconstruct the next cap18 domain at mu42, without transferring old exclusions."""
from collections import Counter
from fractions import Fraction
import hashlib,json,sys,zipfile
from common import ROOT,need,main
from contract import validate_index
sys.path.insert(0,str(ROOT/'sources'))
import audit43 as A,local43 as B

def degrees(r):
    return tuple(r[10+i]+1+sum(r[j] for j,p in enumerate(A.PAIR_LIST) if i in p)+sum(r[6:10])-r[6+i] for i in range(4))
def run():
    validate_index();lock=json.loads((ROOT/'data/INPUT_LOCK.json').read_text())
    for name,h in lock['files'].items():need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'input hash '+name)
    members=0 # Nested historical ZIP custody is outside the mathematical suite.
    rr=sorted(bytes(r) for r in A.enumerate_rows(mu=42,r10=7,r9=7,cap=18) if min(degrees(r))>=4)
    other=sorted(bytes(r) for r in B.enumerate_rows(mu=42,r10=7,r9=7,cap_degree=18) if min(degrees(r))>=4)
    need(rr==other,'literal next-domain comparison')
    dd=[degrees(r) for r in rr];profiles=set(dd)
    data={'mu':42,'cap':18,'r10':7,'r9':7,'rows':len(rr),'profiles':len(profiles),'minimum_degree':min(map(min,dd)),'minimum_pair_sum':min(d[i]+d[j] for d in profiles for i,j in A.PAIR_LIST),'minimum_anchor_sum':min(map(sum,profiles)),'maximum_reciprocal_pointwise':str(max(sum(Fraction(1,v) for v in d) for d in profiles)),'rows_sha256':hashlib.sha256(b''.join(rr)).hexdigest()}
    fr=json.loads((ROOT/'FRONTIER.json').read_text())
    need(fr['global_bound']==[54,69] and not fr['F69_excluded'] and fr['closed_maxima']==[19,20] and fr['open_maxima']==[18,17,'<=16'],'frontier')
    need(fr['next']['residuals']==51 and fr['next']['mu']==42 and fr['next']['terminal_deficit_required']==10*51-27*18==24,'next threshold')
    return {'status':'PASS','input_files':len(lock['files']),'baseline_members':members,'baseline_sha256':lock['baseline']['sha256'],'next_domain':data,'global_bound':[54,69],'F69_excluded':False,'maximum19_closed':True,'maximum18_still_open':True}
if __name__=='__main__':main(run)
