"""Certificate binding and exact replay; standard-library only."""
import audit_pair as p
import audit_marked as m
from common import need

def build_finite_pilot(problem):
 if problem['stage']=='interior_pair':return p.build(problem['pair'])
 if problem['stage']=='mixed_four':return m.build4(problem)
 if problem['stage']=='mixed_three':return m.build3(problem)
 raise ValueError('unknown mathematical stage')

def check(cert,problem,data=None):
 expected={'schema','problem','target','mu','degree_cap','case','mode','scale','value','rhs','box','columns','upper_rows','equal_rows','upper','equal'}
 need(type(cert) is dict and set(cert)==expected,'certificate fields')
 need(cert['schema']=='E20_F69_R99_SHARED_TRACE_CERT_V1','schema')
 need(cert['problem']==problem,'problem binding')
 need(cert['case']==problem['id'],'case binding')
 for key,val in [('target',51),('mu',42),('degree_cap',18)]:need(type(cert[key]) is int and cert[key]==val,'wrong '+key)
 for k in ('columns','upper_rows','equal_rows'):need(type(cert[k]) is int and cert[k]>0,'dimension '+k)
 d=build(problem) if data is None else data
 return p.check(cert,d)

from support_free import normalize
def build(problem):
 return normalize(build_finite_pilot(problem),problem)
