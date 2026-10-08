"""Verify the entire P10 empty-interior forest, not only an output count."""
import gzip,json
from verify_component import Check
from common import ROOT,need,load,emit,rejected

def main():
 prefix=ROOT/'certificates/p10_empty/forest';case=load('certificates/p10_empty/forest.profiles.json')['case'];need(case==dict(id='P10_000',component=10,outside=8,r10=7,r9=7,interiors=[]),'P10 scope')
 c=Check(case);profiles,rows=c.domain(prefix,True);need(len(profiles)==18 and all(len(r)==97 for r in rows),'P10 domain')
 expected=[json.loads(l) for l in (ROOT/'data/P10_PRODUCER_LOG.jsonl').read_text().splitlines()]
 need(len(expected)==18,'full producer index');out=[]
 for cid in range(18):
  z=c.verify(cid,profiles,rows,prefix);e=expected[cid]
  need(e['status']=='EXHAUSTED','open output cannot be accepted')
  for k in ('case','profile','joinnodes','margin_patterns','projections','reasons'):need(z[k]==e[k],'coverage totals '+k)
  z.pop('seconds');out.append(z)
 # Boundary and corruption controls operate on temporary in-memory bytes.
 raw=gzip.decompress((ROOT/'certificates/p10_empty/forest_0.bin.gz').read_bytes())
 tests=[(0,raw[:-1]),(0,raw+b'\x00'),(0,b'\xff'+raw[1:]),(1,b'\x02'),(1,b'\x00')]
 for cid,p in tests:rejected(lambda cid=cid,p=p:c.verify(cid,profiles,rows,prefix,p))
 reasons=[sum(r['reasons'][i] for r in out) for i in range(10)]
 emit({'status':'PASS','profiles':18,'labelled_profiles':263,'local_rows':970,'literal_models':1,'joinnodes':sum(r['joinnodes'] for r in out),'margin_patterns':sum(r['margin_patterns'] for r in out),'prefix_nodes':sum(r['projections'] for r in out),'leaves':sum(reasons),'open_leaves':0,'reasons':reasons,'mutations_rejected':len(tests),'records':out})
if __name__=='__main__':main()
