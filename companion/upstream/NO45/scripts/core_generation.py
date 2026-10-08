"""Exact coloured-graph canonicalisation of high-anchor cores.
Only external vertices are relabelled. R=0,1,2,3 stays pointwise fixed.
"""
from itertools import combinations,permutations,product
from collections import defaultdict,Counter
from functools import lru_cache
from pathlib import Path
import json,time,sys

PAIRS=tuple(combinations(range(4),2))
def mask(q):return sum(1<<v for v in q)
def sunflower(a,b,c):return a&b==a&c==b&c
@lru_cache(300000)
def canon(core):
    # Reduce canonisation to disjoint, edge-coloured graphs on the external points.
    ext=sorted(set(v for q in core for v in q if v>=4))
    labels={v:0 for v in ext}; ed={v:{} for v in ext}
    for q in core:
        a=tuple(v for v in q if v<4);b=tuple(v for v in q if v>=4)
        if len(b)==1:labels[b[0]]|=1<<mask(a)
        elif len(b)==2:
            u,v=b;old=ed[u].get(v,0);ed[u][v]=ed[v][u]=old|(1<<mask(a))
    comps=[];seen=set()
    for v in ext:
        if v in seen:continue
        todo=[v];seen.add(v);cc=[]
        while todo:
            u=todo.pop();cc.append(u)
            for w in ed[u]:
                if w not in seen:seen.add(w);todo.append(w)
        cc.sort()
        colors={u:(labels[u],tuple(sorted(Counter(ed[u].values()).items())))for u in cc}
        ids={a:i for i,a in enumerate(sorted(set(colors.values())))};colors={u:ids[a]for u,a in colors.items()}
        while True:
            feat={u:(colors[u],tuple(sorted((w,colors[v])for v,w in ed[u].items())))for u in cc}
            ids={a:i for i,a in enumerate(sorted(set(feat.values())))};new={u:ids[a]for u,a in feat.items()}
            if len(set(new.values()))==len(set(colors.values())):colors=new;break
            colors=new
        parts=[tuple(u for u in cc if colors[u]==c)for c in sorted(set(colors.values()))]
        best=None;bestorder=None
        for groups in product(*(permutations(g)for g in parts)):
            order=sum((tuple(g)for g in groups),())
            key=(tuple(labels[u]for u in order),tuple(ed[u].get(v,0)for i,u in enumerate(order)for v in order[i+1:]))
            if best is None or key<best:best=key;bestorder=order
        comps.append((len(cc),best,bestorder))
    comps.sort(key=lambda a:(a[0],a[1]));mp={};at=4
    for _,__,order in comps:
        for v in order:mp[v]=at;at+=1
    return tuple(sorted(tuple(sorted(v if v<4 else mp[v]for v in q))for q in core))

def assignments(n,m,edges,root,alternate=False):
    # n is number of external points already in the partial core.
    seen=set()
    for fresh in range(m+1):
        if not alternate:
            fs=permutations(range(n+fresh),m)
        else:
            fs=(p for vs in combinations(range(n+fresh),m) for p in permutations(vs))
        new=set(range(n,n+fresh))
        for f in fs:
            if not new<=set(f) or [x for x in f if x>=n]!=sorted(x for x in f if x>=n):continue
            bs=tuple(sorted(tuple(sorted(root|{4+f[v]for v in e}))for e in edges))
            if bs not in seen:seen.add(bs);yield bs

def census(row,alternate=False):
    big=sum(1<<i for i,s in enumerate(row[10:])if s>=8);R=frozenset(range(4));cats=[]
    for j,p in enumerate(row[:6]):
        if p:
            edges={1:((0,1),),2:((0,1),(0,2)),3:((0,1),(0,2),(1,2))}[p]
            cats.append((2 if p==1 else 3,edges,frozenset(PAIRS[j]),('p',j)))
    for j,t in enumerate(row[6:10]):
        if t:cats.append((1,((0,),),R-{j},('t',j)))
    cats.sort(key=lambda c:(-len(c[1]),-((mask(c[2])&big).bit_count()),-len(c[2]),c[3]),reverse=False)
    if alternate:cats.sort(key=lambda c:(-((mask(c[2])&big).bit_count()),-len(c[1]),c[3]),reverse=False)
    states={((0,1,2,3),)};stats=[]
    for stage,(m,edges,root,_) in enumerate(cats):
        nexts=set();trial=0
        for core in sorted(states):
            n=max(v for q in core for v in q)-3;old=[mask(q)for q in core]
            for extra in assignments(n,m,edges,root,alternate):
                trial+=1;ff=old[:]
                for q in extra:
                    a=mask(q)
                    if a in ff or any((a&b).bit_count()==1 and ((a&b)&big)for b in ff) or any(sunflower(a,b,c)for b,c in combinations(ff,2)):break
                    ff.append(a)
                else:nexts.add(canon(tuple(sorted(core+extra))))
        states=nexts;stats.append([len(states),trial])
    return sorted(states),stats
