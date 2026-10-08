"""Replay all 92 exact k=6 component certificates and their complete coverage."""
from pathlib import Path
import sys,json,time,argparse
import component_projection42 as producer
import audit_projection42 as auditor
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def run():
 start=time.monotonic();allresults=[];cats=[];names=[]
 for m,r10 in ((10,6),(9,7)):
  cp=producer.catalog(m);ca=auditor.catalog(m);saved=json.loads((ROOT/'data'/f'CATALOGUE_{m}.json').read_text())
  need(cp==ca==saved,'catalogue mismatch')
  need((ca['internal_count'],len(ca['records']))==((292,13) if m==10 else (373,79)),'complete interior census')
  cats.append({'component':m,'internal_count':ca['internal_count'],'orbits':len(ca['records']),'automorphisms':ca['automorphism_count']})
  for rec in ca['records']:
   name=rec['id']+'.cert.json';names.append(name);cert=json.loads((ROOT/'certificates/projections'/name).read_text())
   case={'id':rec['id'],'component':m,'outside':6,'r10':r10,'r9':6,'interiors':rec['interiors']}
   need(cert['case']==case,'certificate bound to wrong stage or interior')
   x=producer.build(case);y=auditor.build(case);need(x==y,'literal matrix/domain mismatch')
   allresults.append(auditor.check(cert,y))
  print('P'+str(m),'all',len(ca['records']),'certificates verified',flush=True)
 need(set(names)=={p.name for p in (ROOT/'certificates/projections').glob('*.cert.json')},'missing or extra certificate')
 return {'status':'PASS','mu':42,'claim':'s=9 or 10 implies k>=7, after the bootstrap k>=6','catalogues':cats,'certificates':len(allresults),'literal_model_comparisons':len(allresults),'direct_empty_anchor':sum(0 in r['live_sizes'] for r in allresults),'nontrivial':[r for r in allresults if 0 not in r['live_sizes']],'results':allresults,'seconds':time.monotonic()-start}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();need(not a.output.exists(),'fresh output');o=run();a.output.write_text(json.dumps(o,indent=2)+'\n')
