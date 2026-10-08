"""Independent integer reconstruction of the marked stages. No numerical libraries."""
from itertools import combinations
from math import comb
import audit_pair as ap
a=ap.a

def empty_pair():
 return dict(id='R99_0_0',interiors_first=[],interiors_second=[])

def build4(case):
 data=ap.build(empty_pair());data=dict(data);data['case']=case['id'];data['bounds']=list(data['bounds']);data['upper']=list(data['upper'])
 mark=tuple(case['mark']);need=a.need
 need(len(mark)==4 and tuple(sorted(set(mark)))==mark and min(mark)>=0 and max(mark)<12,'four-point mark')
 masks=tuple(a.bm(T) for T in data['types']);mm=a.bm(mark);j=masks.index(mm)
 data['bounds'][j]=(1,data['bounds'][j][1])
 cones=tuple(a.bm((22,*T)) for T in a.blocks(9))+tuple(a.bm((22,*(v+6 for v in T))) for T in a.blocks(9))
 for j,q in enumerate(masks):
  if any(F&mm==F&q==mm&q for F in cones):data['bounds'][j]=(0,0)
 data['upper'].append((f'H27-mark:{mark}',{j:1 for j,q in enumerate(masks) if q&mm==0},27-sum(F&mm==0 for F in cones)))
 need(data['bounds'][masks.index(mm)]==(1,1),'true marked member')
 return data

def build3(case):
 mark=tuple(case['mark']);need=a.need
 need(len(mark)==4 and tuple(sorted(set(mark)))==mark and mark[-1]==12 and mark[0]>=0,'three-point mark plus exterior')
 types=tuple(T for k in range(5) for T in combinations(range(13),k));ms=tuple(a.bm(T) for T in types);nz=len(types)
 cones=tuple(a.bm((22,*T)) for T in a.blocks(9))+tuple(a.bm((22,*(v+6 for v in T))) for T in a.blocks(9));MM=a.bm(mark);fixed=cones+(MM,)
 comps=(63,4032);bounds=[]
 for T,tm in zip(types,ms):
  lo=0;hi=comb(9,4-len(T))
  if len(T) in (1,2,3):hi=min(hi,{1:18,2:6,3:2}[len(T)]-sum(C&tm==tm for C in cones))
  if len(T)==4 and any(tm&S==tm for S in comps):hi=0
  if any(C&D==C&tm==D&tm for C,D in combinations(fixed,2)):hi=0
  if tm==MM:need(hi>=1,'forbidden marked member');lo=hi=1
  # Previous certified stage: every four-point trace on the12-point support is absent.
  if len(T)==4 and tm<4096 and tm&comps[0] and tm&comps[1]:lo=hi=0
  bounds.append((lo,hi))
 rows={'equal':[],'upper':[]};local=ap.local(())
 for side in (0,1):
  off=len(bounds);bounds.extend(local['bounds'])
  for kind in rows:
   rows[kind].extend((f's{side}/{name}',{j+off:w for j,w in co.items()},b) for name,co,b in local[kind])
  for j,U in enumerate(a.TYPES):
   mask=a.bm(tuple(v+6*side for v in U));co={h:1 for h,tm in enumerate(ms) if tm&comps[side]==mask};co[j+off]=-1
   rows['equal'].append((f'shared-trace:{side}:{U}',co,0))
  rows['upper'].append((f'pure-pool:{side}',{h:1 for h,tm in enumerate(ms) if (tm&comps[side]).bit_count()==1},27))
 ix=len(bounds);cols=list(range(ix,ix+15));bounds.extend([(0,1)]*15)
 rows['equal'].append(('ext-degree-choice:12',dict.fromkeys(cols,1),1))
 terms={h:1 for h,tm in enumerate(ms) if tm>>12&1};terms.update({j:-(4+j-ix) for j in cols})
 rows['equal'].append(('ext-degree-tie:12',terms,0))
 for k in (1,2,3):
  for U in combinations(range(13),k):
   bits=a.bm(U)
   cap=(18 if U[0]==12 else 16 if U[0]%6<3 else 15) if k==1 else {2:6,3:2}[k]
   rows['upper'].append((f'cap:{U}',{h:1 for h,tm in enumerate(ms) if tm&bits==bits},cap-sum(C&bits==bits for C in cones)))
 for i,F in enumerate(fixed):rows['upper'].append((f'H27:{i}',{h:1 for h,tm in enumerate(ms) if F&tm==0},27-sum(F&C==0 for C in cones)))
 rows['upper'].append(('W-degree',{h:4-len(T) for h,T in enumerate(types) if len(T)<4},162))
 for v in range(13):rows['upper'].append((f'yW-pairs:{v}',{h:4-len(T) for h,T in enumerate(types) if v in T and len(T)<4},54))
 for U in combinations(range(13),2):
  bits=a.bm(U);rows['upper'].append((f'pairW-triples:{U}',{h:4-len(T) for h,(T,tm) in enumerate(zip(types,ms)) if bits&tm==bits and len(T)<4},18))
 return dict(case=case['id'],bounds=bounds,**rows,nz=nz,types=types,objective=[1]*nz+[0]*(len(bounds)-nz),live=[],mark=mark,with_anchor=False)

