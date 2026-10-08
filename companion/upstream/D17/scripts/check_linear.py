"""Replay all87 NEW arithmetic certificates on two exact reconstructed models."""
from common import *
from copy import deepcopy
import projection as P,audit_projection as A

def run():
    entries=load("data/LINEAR_INDEX.json");need(len(entries)==87,"complete87 certificate index")
    expected=[]
    for m in (10,9):
        p=P.catalog(m);a=A.catalog(m);need(p==a,"all labelled interiors/orbits agree")
        need(p==load(f"data/CATALOGUE_P{m}.json"),"saved catalogue")
        remaining={"P10_000"} if m==10 else {"P9_000","P9_002","P9_003","P9_004"}
        expected.extend(row["id"]for row in p["records"]if row["id"]not in remaining)
    need([r["case"]["id"]for r in entries]==expected,"exact stage and orbit coverage")
    result=[];mutations=0
    for record in entries:
        cert=load(record["path"]);case=record["case"];need(cert["case"]==case,"indexed case identity")
        p=P.build(case);p["upper"]=P.pair_constraints(p,case["component"])
        a=A.build(case);a["upper"]=A.pair_rows(case)
        for key in ("case","bounds","upper","equal","quads","zero","objective","target","live_sizes","internal_degrees","caps","anchor_rows"):
            need(p[key]==a[key],"literal model mismatch "+key)
        out=A.check(cert,a);result.append(out)
        for field,value in (("value",cert["value"]+1),("scale",0),("columns",cert["columns"]+1)):
            bad=deepcopy(cert);bad[field]=value;rejected(lambda bad=bad:A.check(bad,a));mutations+=1
        bad=deepcopy(cert);bad["upper"]=[];bad["equal"]=[];rejected(lambda:A.check(bad,a));mutations+=1
        bad=deepcopy(cert);bad["case"]["outside"]+=1;rejected(lambda:A.check(bad,a));mutations+=1
    emit(dict(status="PASS",new_linear_certificates=len(result),literal_model_comparisons=len(result),p10=12,p9=75,mutations_rejected=mutations,records=result))
if __name__=="__main__":run()
