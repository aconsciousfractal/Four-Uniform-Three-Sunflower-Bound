"""Small exact global star-charge certificate for mu42 and used degree >=4."""
from fractions import Fraction
from math import lcm
PAIRS=tuple((a,b) for a in range(4) for b in range(a+1,4))
INC=tuple(tuple(j for j,p in enumerate(PAIRS) if i in p) for i in range(4))
BAL=('17_7_10','17_8_9','18_8_10','19_9_10')
L=lcm(*range(1,21))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def degree(row):return tuple(1+row[10+i]+sum(row[j] for j in INC[i])+sum(row[6:10])-row[6+i] for i in range(4))
def validate(c):
 need(type(c) is dict and c.get('schema')=='E20_MU42_STAR_CHARGE_V1','charge schema')
 need((c.get('mu'),c.get('r10'),c.get('r9'),c.get('cap_degree'),c.get('minimum_degree'))==(42,7,7,20,4),'charge hypotheses')
 need(c.get('no_P10_at17') is False,'do not silently exclude a degree17 root')
 need(type(c.get('denominator')) is int and c['denominator']>0,'denominator')
 need(type(c.get('constant')) is int and c['constant']>=0,'constant')
 need(69*c['constant']<24*c['denominator'],'support23 is not implied')
 need(set(c.get('balance',{}))==set(BAL) and all(type(w) is int for w in c['balance'].values()),'balance weights')
 need(type(c.get('mantel')) is dict and all(k.isdigit() and 1<=int(k)<=20 and type(w) is int and w>=0 for k,w in c['mantel'].items()),'nonnegative Mantel multipliers')
 need(type(c.get('split16')) is int and c['split16']>=0,'nonnegative split multiplier')
 need(c.get('expected_rows')==292560,'full charge-domain size')
def verify(c,rows):
 validate(c);count=0;minimum=None;worst=None;md=Fraction(99);profiles=set()
 ms={int(d):v for d,v in c['mantel'].items()};den=c['denominator'];constant=c['constant']
 for r in rows:
  ds=degree(r);need(all(4<=d<=20 for d in ds),'row degree range');profiles.add(ds);count+=1
  weight=0;balance=dict.fromkeys(BAL,0);split=0
  for d,s in zip(ds,r[10:]):
   weight+=ms.get(d,0)*(d*s-2*(d*d//4))
   if d==17:
    balance['17_7_10']+=7*(s==7)-10*(s==10);balance['17_8_9']+=8*(s==8)-9*(s==9)
   elif d==18:balance['18_8_10']+=8*(s==8)-10*(s==10)
   elif d==19:balance['19_9_10']+=9*(s==9)-10*(s==10)
   elif d==16:split+=9*(s==9)-7*(s==7)
  weight+=sum(c['balance'][key]*balance[key] for key in BAL)+c['split16']*split
  gap=L*(constant+weight)-den*sum(L//d for d in ds)
  need(gap>=0,('negative exact charge slack',list(r),gap))
  if minimum is None or gap<minimum:minimum=gap;worst=list(r)
 need(count==c['expected_rows'],'incomplete charge row universe')
 md=min(sum((Fraction(1,v) for v in d),Fraction()) for d in profiles)
 maxplain=max(sum((Fraction(1,v) for v in d),Fraction()) for d in profiles)
 slack=Fraction(minimum,den*L);upper=Fraction(constant,den)
 need(md==Fraction(37,170),'minimum reciprocal domain')
 return {'status':'PASS','rows':count,'degree_profiles':len(profiles),'pointwise_constant':str(upper),'minimum_pointwise_slack':str(slack),'maximum_corrected_charge':str(upper-slack),'worst_row':worst,'minimum_reciprocal':str(md),'maximum_uncorrected_reciprocal':str(maxplain),'F69_support_lower_rational':str(69*md),'F69_support_upper_rational':str(69*upper),'F69_support_integer':[16,23]}
