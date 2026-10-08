"""Deterministic I/O, local-row expansion and bit-set lookup. Standard library."""
from pathlib import Path
from itertools import combinations,permutations
from functools import lru_cache
import json
ROOT=Path(__file__).resolve().parents[1]
PAIRS=tuple(combinations(range(4),2))
PERMS=tuple(permutations(range(4)))
def require(ok,message):
    if not ok:raise ValueError(message)
def load(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def emit(obj):print(json.dumps(obj,sort_keys=True))
def mask(vs):return sum(1<<v for v in vs)
def degree(r):return tuple(1+r[10+i]+sum(r[j] for j,p in enumerate(PAIRS)if i in p)+sum(r[6:10])-r[6+i]for i in range(4))
def relabel(r,p):return tuple(r[PAIRS.index(tuple(sorted((p[i],p[j]))))]for i,j in PAIRS)+tuple(r[6+p[i]]for i in range(4))+tuple(r[10+p[i]]for i in range(4))
@lru_cache(None)
def base_rows():
    b=(ROOT/'data/no9_rows.bin').read_bytes();require(len(b)%14==0,'truncated row input')
    out=tuple(tuple(b[i:i+14])for i in range(0,len(b),14))
    require(len(out)==24002 and out==tuple(sorted(set(out))),'base row set')
    return out
@lru_cache(None)
def oriented_rows():return tuple(sorted({relabel(r,p)for r in base_rows()for p in PERMS}))
class RowIndex:
    def __init__(self,rows):
        self.rows=rows;self.degrees=tuple(map(degree,rows));size=(len(rows)+7)//8
        tables=[{}for _ in range(18)]
        for j,(r,d)in enumerate(zip(rows,self.degrees)):
            pos=j>>3;bit=1<<(j&7)
            for f,v in enumerate(r+d):
                if v not in tables[f]:tables[f][v]=bytearray(size)
                tables[f][v][pos]|=bit
        self.tables=[{v:int.from_bytes(b,'little')for v,b in t.items()}for t in tables]
        self.all=(1<<len(rows))-1
    def interval(self,f,lo,hi):
        out=0
        for v,b in self.tables[f].items():
            if lo<=v<=hi:out|=b
        return out
    def choose(self,order,given,fixed_degree,lo,hi):
        live=self.all
        for i,v in enumerate(order):
            a,b=(given[v],given[v])if v<4 else (max(8,fixed_degree[v]),16)
            live&=self.interval(14+i,a,b)
            if not live:return 0
        for i,(a,b)in enumerate(zip(lo,hi)):
            live&=self.interval(i,a,b)
            if not live:return 0
        return live
    def indices(self,bits):
        while bits:
            bit=bits&-bits;yield bit.bit_length()-1;bits-=bit
@lru_cache(None)
def row_index():return RowIndex(oriented_rows())
def high_roots():
    groups={}
    for r in base_rows():
        if 1+sum(r)!=45:continue
        key=min(relabel(r,p)for p in PERMS);groups.setdefault(key,[]).append(r)
    return [dict(id=i,row=list(r),ordered_count=len(v))for i,(r,v)in enumerate(sorted(groups.items()))]
