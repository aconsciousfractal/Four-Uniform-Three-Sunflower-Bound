from common import *
import models,audit_model

def run():
    cores=load('data/CORES.json');cases=load('data/CERTIFICATE_CASES.json');out=[]
    for c in cases:
        rec=cores[c['root']];core=rec['cores'][c['core']];a=models.build(core,rec['row'],c);b=audit_model.build(core,rec['row'],c)
        require(a==b,'models differ literally: '+c['id'])
        cert=load('certificates/'+c['id']+'.json');require(cert['label']==c['id'],'certificate identity')
        out.append(models.verify_certificate(b,cert))
    require(len(out)==5,'five needed certificates')
    emit(dict(status='PASS',certificates=out,literal_comparisons=5,models_use_support_bound=False,h27_pools=7))
if __name__=='__main__':run()
