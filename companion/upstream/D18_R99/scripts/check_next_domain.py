"""New cap17 contract; not a premise of the R99 closure."""
from common import *
import sys,hashlib
from itertools import combinations
sys.path.insert(0,str(ROOT/'inherited/inputs'))
import local43 as p,audit43 as a

def run():
 def degree(r,i):return 1+r[10+i]+sum(r[j] for j in p.INC[i])+sum(r[6:10])-r[6+i]
 first=sorted(bytes(r) for r in p.enumerate_rows(mu=42,r10=7,r9=7,cap_degree=17) if min(degree(r,i) for i in range(4))>=4)
 second=sorted(r for r in a.enumerate_rows(mu=42,r10=7,r9=7,cap=17) if min(degree(r,i) for i in range(4))>=4)
 need(first==second,'literal next domain')
 profiles={tuple(degree(r,i) for i in range(4)) for r in first}
 data={'status':'PASS','mu':42,'degree_cap':17,'r10':7,'r9':7,'rows':len(first),'profiles':len(profiles),'sha256':hashlib.sha256(b''.join(first)).hexdigest(),'min_degree':min(d[0] for d in profiles),'min_pair_sum':min(d[0]+d[1] for d in profiles),'min_member_sum':min(map(sum,profiles)),'max_neighbourhood':max(1+sum(r) for r in first),'next_cardinality':69,'prescribed_at_degree17':17,'residuals_at_degree17':52,'support':[17,23]}
 expected=load('data/NEXT_DOMAIN.json');need(data==expected,'saved next domain')
 emit(data)
if __name__=='__main__':run()
