"""Exact small corroborations, genuine positive controls, and stage-scope checks.
The degree-two exclusion is an ordinary argument in PROOF.md, not inferred
from examples. This program checks the finite model facts used in that argument.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from math import comb
import argparse, json, time
ROOT=Path(__file__).resolve().parents[1]
P=tuple(frozenset(map(int,t)) for t in ('012','015','023','034','045','124','134','135','235','245'))

def need(ok,msg):
 if not ok: raise ValueError(msg)
def sf(a,b,c):return a&b==a&c==b&c
def q8(hubs=(0,1),triangle=(2,3,4),leaves=(5,6)):
 return tuple(frozenset((h,*e)) for h in hubs for e in combinations(triangle,2))+tuple(frozenset((*hubs,z)) for z in leaves)
def family(F,size=None,intersecting=False):
 need(F and len(set(F))==len(F),'simple nonempty family')
 need(len({len(a) for a in F})==1,'uniformity')
 if size is not None:need(len(F)==size,'size')
 need(not any(sf(a,b,c) for a,b,c in combinations(F,3)),'sunflower')
 if intersecting:need(all(a&b for a,b in combinations(F,2)),'not intersecting')
 vertices=set().union(*F);ds={v:sum(v in A for A in F) for v in vertices}
 return {'members':len(F),'support':len(vertices),'degrees':dict(Counter(ds.values())), 'checked_ternae':comb(len(F),3), 'mu':min(sum(bool(a&b) for b in F) for a in F)}
def fourcycles(F,y):
 edges={frozenset(A-{y}) for A in F if y in A};vs=set().union(*edges) if edges else set();out=set()
 for four in combinations(vs,4):
  for subset in combinations([e for e in edges if e<=set(four)],4):
   d=Counter(v for e in subset for v in e)
   if len(d)==4 and set(d.values())=={2}:out.add(frozenset(subset))
 return len(out)
def shift(F,by):return tuple(frozenset(v+by for v in A) for A in F)
def sdist(F):return Counter(sum(not(A&B) for B in F) for A in F)
def bvalues(d,dist):
 return {'17_7_10':7*dist[7]-10*dist[10] if d==17 else 0,
         '17_8_9':8*dist[8]-9*dist[9] if d==17 else 0,
         '18_8_10':8*dist[8]-10*dist[10] if d==18 else 0,
         '19_9_10':9*dist[9]-10*dist[10] if d==19 else 0,
         'split16':9*dist[9]-7*dist[7] if d==16 else 0}
def run():
 start=time.monotonic();Q=q8();family(P,10,True);family(Q,8,True)
 need([sum(v in A for A in Q) for v in range(7)]==[5,5,4,4,4,1,1], 'Q8 hubs/triangle/leaves')
 need([fourcycles(Q,v) for v in range(7)]==[0,0,1,1,1,0,0], 'C4 is carried exactly by Q8 triangle points')
 need(all(fourcycles(P,v)==0 for v in range(6)), 'P10 point link contains no C4')
 # Every labelled Q8 on the seven prescribed points; the core fixes hubs/triangle.
 A=frozenset((0,1,2));H=frozenset((3,4));core={frozenset((h,*pair)) for h in H for pair in combinations(A,2)}
 containing=[];models=[]
 for hubs in combinations(range(7),2):
  rest=set(range(7))-set(hubs)
  for triangle in combinations(sorted(rest),3):
   leaves=sorted(rest-set(triangle));f=q8(hubs,triangle,leaves);models.append(frozenset(f))
   if core<=set(f):containing.append((hubs,triangle,tuple(leaves)))
 need(len(models)==len(set(models))==210,'full labelled Q8 census')
 need(containing==[((3,4),(0,1,2),(5,6))],'six-core uniqueness in Q8')
 E18=(P+shift(tuple(A for i,A in enumerate(P) if i not in (0,4)),7),
      P+shift(tuple(A for i,A in enumerate(P) if i not in (0,1)),7),
      P+shift(Q,7),P[1:]+shift(P[1:],7))
 e18=[]
 for F in E18:
  z=family(F,18);deg=Counter(v for T in F for v in T)
  need(max(sum(deg[v]==1 for v in T) for T in F)<=1,'triple with three degree-one points in E18')
  e18.append(z)
 # Additional labels model a transversal with one or more points outside P10.
 two=[t for t in combinations(range(9),2) if all(set(t)&B for B in P)]
 three=[frozenset(t) for t in combinations(range(9),3) if all(set(t)&B for B in P)]
 need(not two and set(three)==set(P),'all 3-transversals, including external points')
 # Genuine thin-point controls: no general prohibition of degree two is claimed.
 A=(1,2,3);C=(4,5,6);x=0;y=7
 base=tuple(frozenset((*a,*c)) for a in combinations(A,2) for c in combinations(C,2))
 core11=base+(frozenset((x,*A)),frozenset((y,*A)))
 core13=core11+(frozenset((x,*C)),frozenset((y,*C)))
 control11=family(core11,11);control13=family(core13,13)
 ds=Counter(v for T in core13 for v in T)
 need(ds[x]==ds[y]==2 and all(ds[v]==8 for v in A+C),'thin point positive boundary')
 # Exact structural balance checks on genuinely separated link families.
 I7=P[:7];P8a=tuple(T for i,T in enumerate(P) if i not in(0,4));P8b=tuple(T for i,T in enumerate(P) if i not in(0,1))
 balance_cases=[P+shift(I7,7),P[1:]+shift(P8a,7),P[1:]+shift(P8b,7),P[1:]+shift(Q,7),
                P+shift(P8a,7),P+shift(P8b,7),P+shift(Q,7),P[1:]+shift(P[1:],7),
                P+shift(P[1:],7),P+shift(P,7),P[1:]+shift(I7,7)]
 balances=[]
 for F in balance_cases:
  family(F);d=len(F);dist=sdist(F);vals=bvalues(d,dist)
  need(all(vals[k]==0 for k in vals if k!='split16') and vals['split16']<=0,'separated-star identity')
  need(sum(s*n for s,n in dist.items())<=2*(d*d//4),'Mantel star bound')
  balances.append({'size':d,'singleton_histogram':dict(dist),'balance':vals})
 # A valid R16 which is NOT a B4 separation into 8+8.
 R16=q8((0,1),(4,5,6),(2,3))+q8((2,3),(7,8,9),(0,1))
 R16meta=family(R16,16);dist=sdist(R16)
 need(max(dist)<=7 and bvalues(16,dist)['split16']<=0,'R16 positive control')
 # Corroborate Mantel on every graph of order four; ordinary proof in the note.
 edges=tuple(combinations(range(4),2));triangle_free=0
 for mask in range(64):
  E={edges[j] for j in range(6) if mask>>j&1}
  if any(all(tuple(sorted(e)) in E for e in combinations(T,2)) for T in combinations(range(4),3)):continue
  triangle_free+=1;need(len(E)<=4,'Mantel order-four check')
 # Lower bound construction, independently inspected as actual quadruples.
 def D27(offset):
  groups=[tuple(range(offset+3*j,offset+3*j+3)) for j in range(3)]
  return tuple(frozenset((*a,*b)) for i,j in combinations(range(3),2) for a in combinations(groups[i],2) for b in combinations(groups[j],2))
 F54=D27(0)+D27(9);low=family(F54,54)
 need(low['checked_ternae']==24804 and low['mu']==27,'54 control is not a mu42 example')
 return {'status':'PASS','Q8_labelled_models':210,'Q8_six_core_completions':containing,'Q8_C4_counts':[fourcycles(Q,v) for v in range(7)],
 'E18_models_checked':e18,'P10_two_transversals':len(two),'P10_three_transversals':len(three),'thin_point_controls':[control11,control13],
 'star_balance_controls':balances,'R16_control':R16meta,'triangle_free_graphs_order4':triangle_free,'lower_bound54':low,
 'degree2_ordinary_proof':'PROOF.md section 4; no degree2-free universal claim without the six degree18 neighbours',
 'seconds':time.monotonic()-start}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();need(not args.output.exists(),'fresh output')
 out=run();args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('E18_models_checked','star_balance_controls')},indent=2))
