"""Reconstruct, rather than import, the domain with singleton9 excluded at mu42."""
from common import *
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0,str(ROOT/'scripts/inputs'))
import local43 as P,audit43 as A

def degree(r):return tuple(1+r[10+i]+sum(r[j]for j,p in enumerate(P.PAIRS)if i in p)+sum(r[6:10])-r[6+i]for i in range(4))
def domain():
    x=tuple(sorted(tuple(r)for r in P.enumerate_rows(mu=42,r10=7,r9=7,cap_degree=16)if max(r[10:])<=8 and min(degree(r))>=4))
    y=tuple(sorted(tuple(r)for r in A.enumerate_rows(mu=42,r10=7,r9=7,cap=16)if max(r[10:])<=8 and min(degree(r))>=4))
    need(x==y,'entire new domain differs')
    need(b''.join(bytes(r)for r in x)==(ROOT/'data/no9_rows.bin').read_bytes(),'saved domain bytes not the exact full list')
    return x

def run():
    rows=domain();stats=[]
    for h,count,md,mp,ms,rc in [(42,16823,8,24,54,Fraction(5,16)),(43,5732,9,25,56,Fraction(43,144)),(44,1290,13,27,58,Fraction(18,65)),(45,157,14,29,60,Fraction(4,15))]:
        dd=[degree(r)for r in rows if 1+sum(r)==h]
        need((len(dd),min(map(min,dd)),min(d[0]+d[1]for d in dd),min(map(sum,dd)))==(count,md,mp,ms),'neighbourhood minima/count')
        charge=max(sum((Fraction(1,d)for d in ds),Fraction(0))for ds in dd);need(charge==rc,'reciprocal maximum')
        stats.append(dict(neighbourhood=h,rows=count,min_degree=md,min_pair_sum=mp,min_member_sum=ms,max_charge=str(charge)))
    need(len(rows)==24002 and len({degree(r)for r in rows})==71,'new count/profile')
    emit(dict(status='PASS',mu=42,cap=16,singleton_cap=8,rows=24002,degree_profiles=71,global_support_from_pointwise_charge=[18,21],strata=stats,method='literal comparison of the full two independently generated lists'))
if __name__=='__main__':run()
