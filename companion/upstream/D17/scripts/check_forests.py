"""Every profile and every branch of the four P9 forests is recomputed."""
from common import *
from verify_component import Check
import gzip
from copy import deepcopy

def validate_index(items):
    need([r["component_case"]["id"]for r in items]==["P9_000","P9_002","P9_003","P9_004"],"all four residual interiors")
    need([r["profiles"]for r in items]==[122,118,258,372],"complete profile domains")

def run():
    index=load("data/FOREST_INDEX.json");validate_index(index)
    rows=[];mutations=0
    for item in index:
        prefix=ROOT/item["directory"]/"forest";C=Check(item["component_case"])
        profiles,options=C.domain(prefix,compare=True)
        need(len(profiles)==item["profiles"],"all canonical degree profiles")
        expected=load(item["directory"]+"/EXPECTED.json");need(len(expected)==len(profiles),"complete producer record")
        stats={"joinnodes":0,"margin_patterns":0,"prefix_nodes":0};reasons=[0]*10
        tested=False
        for cid in range(len(profiles)):
            out=C.verify(cid,profiles,options,prefix);source=expected[cid]
            need(source["status"]=="EXHAUSTED","open producer record")
            for key in ("case","profile","joinnodes","margin_patterns","projections","reasons"):
                need(source[key]==out[key],"coverage mismatch "+key)
            stats["joinnodes"]+=out["joinnodes"];stats["margin_patterns"]+=out["margin_patterns"];stats["prefix_nodes"]+=out["projections"]
            reasons=[a+b for a,b in zip(reasons,out["reasons"])]
            # Mutation tests on a small nonempty proof, including invalid reason7.
            path=prefix.parent/(prefix.name+f"_{cid}.bin.gz")
            raw=gzip.decompress(path.read_bytes())
            if not tested and 0<len(raw)<1000:
                for bad in (raw[:-1],raw+b"\0",b"\x09",b"\x07",b""):
                    rejected(lambda bad=bad,cid=cid:C.verify(cid,profiles,options,prefix,bad));mutations+=1
                tested=True
        need(tested,"boundary tests performed for each interior")
        for key,value in stats.items():need(item[key]==value,"total "+key)
        need(reasons==item["leaf_reasons"],"all leaf reasons")
        need(reasons[0]==reasons[7]==reasons[9]==0,"no open leaf / no unused H8")
        rows.append(dict(case=item["component_case"],profiles=len(profiles),labelled_profiles=item["labelled_profiles"],**stats,leaf_reasons=reasons,leaves=sum(reasons),open_leaves=0))
        C.components.cache_clear()
    bad=deepcopy(index);bad.pop();rejected(lambda:validate_index(bad));mutations+=1
    bad=deepcopy(index);bad[0]["profiles"]-=1;rejected(lambda:validate_index(bad));mutations+=1
    emit(dict(status="PASS",canonical_cases=sum(r["profiles"]for r in rows),records=rows,joinnodes=sum(r["joinnodes"]for r in rows),margin_patterns=sum(r["margin_patterns"]for r in rows),prefix_nodes=sum(r["prefix_nodes"]for r in rows),leaves=sum(r["leaves"]for r in rows),open_leaves=0,mutations_rejected=mutations))
if __name__=="__main__":run()
