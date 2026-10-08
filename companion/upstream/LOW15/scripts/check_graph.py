"""Small exact checks for the imported-Jin corollary, and actual positive families."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
    if not c:raise ValueError(m)
def compositions(total,n):
    if n==1:
        yield (total,);return
    for v in range(total+1):
        for t in compositions(total-v,n-1):yield (v,)+t

def sf(A,B,C):return A&B==A&C==B&C

def positive54():
    groups=[range(3*j,3*j+3) for j in range(6)];F=[]
    for side in (0,3):
        for i,j in combinations(range(side,side+3),2):
            F.extend(frozenset(a+b)for a in combinations(groups[i],2)for b in combinations(groups[j],2))
    need(len(F)==len(set(F))==54,'54 distinct members')
    count=0
    for a,b,c in combinations(F,3):
        need(not sf(a,b,c),'positive54 sunflower');count+=1
    deg=Counter(v for q in F for v in q)
    return dict(members=54,support=len(deg),max_degree=max(deg.values()),min_neighbourhood=min(sum(bool(a&b)for b in F)for a in F),triples_checked=count)

def run():
    W=[[int((j-i)%8 in(1,4,7))for j in range(8)]for i in range(8)]
    B=[[int((j-i)%8 in(0,1,7))for j in range(8)]for i in range(8)]
    for i in range(8):
        for j in range(8):
            need(sum(W[i][k]*B[k][j]for k in range(8))==1+int(i==j),'Wagner matrix identity')
            need(W[(3*i)%8][(3*j)%8]==int(3<=(j-i)%8<=5),'Andrasfai-Wagner isomorphism')
    need(26*11>4*69,'strict Jin threshold')
    total=0
    for delta in compositions(9,8):
        a=[12-delta[(i-1)%8]-delta[i]-delta[(i+1)%8]for i in range(8)]
        need(sum(a)==69 and min(a)>=3,'positive fibres even before lower-neighbour condition')
        b=[sum(W[i][j]*a[j]for j in range(8))for i in range(8)]
        need(b==[27-v for v in delta],'fibre sums')
        need(min(b)<26,'sum208 versus207');total+=1
    weight=[8,8,8,9,9,9,9,9]
    b=[sum(W[i][j]*weight[j]for j in range(8))for i in range(8)]
    ind=[S for k in range(9)for S in combinations(range(8),k)if not any(W[i][j]for i,j in combinations(S,2))]
    alpha=max(sum(weight[i]for i in S)for S in ind)
    need(sum(weight)==69 and min(b)==25 and alpha==26,'positive graph boundary')
    print(json.dumps(dict(status='PASS',Jin_import_not_reproved=True,matrix_coefficients=64,deficit_compositions=total,
        forbidden_min_degree=26,sum_required=208,sum_available=207,
        positive_graph=dict(order=69,min_degree=25,independence=alpha),positive_family=positive54()),sort_keys=True))
if __name__=='__main__':run()
