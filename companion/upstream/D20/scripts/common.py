"""Receipt, scope and fixed task contract; no numerical dependencies."""
from pathlib import Path
import argparse,json,time,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def dump(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def expected_cases():
 marks=[('I00',[0,1,2,3],False,False,0),('E00',[0,1,2,6],True,False,0),('E01',[0,1,2,12],True,False,0),('E02',[0,1,3,6],True,False,0),('E03',[0,1,3,12],True,False,0),('E04',[0,1,6,7],True,False,0),('E05M',[0,1,6,12],True,True,0),('E06',[0,6,12,13],True,False,2)]
 return [dict(id=n,mark=m,empty=e,marked=a,min_w=w,objective='cardinality') for n,m,e,a,w in marks]
def check_index(index):
 need(type(index) is dict and index.get('schema')=='E20_F69_D20_INDEX_V1','index schema')
 contract={'family_size':69,'mu':42,'max_degree':20,'support':[16,23],'used_min_degree':4,'point_pair_sum':20,'anchor_degree_sum':52,'pair_cap':6,'triple_cap':2,'r10':7,'r9':7,'center_label':22,'fixed_members':20,'required_residuals':49}
 need(index.get('contract')==contract,'contract altered')
 need(index.get('cases')==expected_cases(),'coverage/stage altered')
 need(index.get('linear_proof_cases')==['I00','E00','E01','E02','E03','E04','E05M'] and index.get('supplementary_cases')==['E06'],'proof roles')
 need(index.get('terminal_strategy')=='cover-lemma (ordinary proof), then H27','terminal strategy')
 need(index.get('terminal')=={'kappa_min':12,'required':588,'capacity':540},'terminal scope')
 need(index.get('global_bound')==[54,69] and index.get('F69_excluded') is False and index.get('F69_max20_excluded') is True,'claim promotion or stale result')
 return True
def main(run):
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=a.output.resolve()
 need(not p.exists(),'fresh receipt');need(ROOT not in p.parents,'output outside immutable package');need(p.parent.exists(),'existing output directory')
 t=time.monotonic();out=run();out['seconds']=time.monotonic()-t;dump(p,out);print(json.dumps(out,ensure_ascii=False),flush=True)
