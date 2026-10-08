"""Verify the named finite companion; written reductions and theorem imports remain explicit."""
from pathlib import Path
import argparse,copy,datetime,hashlib,json,os,platform,re,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8',newline='\n')
def load(p):return json.loads(p.read_bytes())
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf8')
def validate_manifest(root,manifest):
 need(manifest['schema']=='BOUND68_COMPUTATIONAL_MANIFEST_V1','Manifest schema')
 need(len(manifest['files'])==len({r['path'] for r in manifest['files']}),'Duplicate manifest path')
 for row in manifest['files']:
  p=(root/row['path']).resolve()
  need(p.is_relative_to(root.resolve()) and p.is_file() and not p.is_symlink(),'Missing/escaping input '+row['path'])
  need(p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256'],'Changed input '+row['path'])
def semantic(data,suite):
 d=copy.deepcopy(data)
 for key in suite.get('volatile_keys',[]):
  need(key.startswith('$.'),'Explicit volatile key syntax')
  tokens=re.findall(r'([^.\[\]]+)|\[(\d+)\]',key[2:]);at=d
  for name,index in tokens[:-1]:at=at[int(index)] if index else at[name]
  name,index=tokens[-1]
  if index:raise ValueError('Do not remove array items as volatile')
  need(name in at,'Missing declared volatile key '+key);del at[name]
 return d
def validate_semantic(data,suite):
 d=semantic(data,suite)
 need(d==suite['expected_semantic'],'Unexpected semantic result '+suite['id'])
 return d
def launch(command,*,cwd,env,timeout):
 return subprocess.run(command,cwd=cwd,env=env,capture_output=True,timeout=timeout)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--mode',choices=['quick','complete'],required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve()
 if out.exists():
  print(json.dumps({'status':'FAIL_EXISTING_OUTPUT','message':'Use a new receipt directory'}));return 2
 need(not out.is_relative_to(ROOT),'Receipts must be outside the package')
 print(str(out),flush=True);out.mkdir(parents=True)
 receipt=dict(status='RUNNING',mode=a.mode,utc_started=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),executions=[],pairs=[],complete_finite_companion=False,external_theorems_replayed=False,formalized=False,filesystem_boundary='Python audit hook; no OS sandbox or other-machine claim')
 save(out/'RECEIPT.json',receipt)
 try:
  manifest=load(ROOT/'COMPUTATIONAL_MANIFEST.json');validate_manifest(ROOT,manifest)
  plan=load(ROOT/'SUITE_PLAN.json')
  need(plan['suite_count']==len(plan['commands']) and len({s['id'] for s in plan['commands']})==len(plan['commands']),'Suite identity/coverage')
  need(plan['suite_count']==42 and len(plan['upstream_blocks'])==9,'Full declared closure')
  commands=plan['commands'] if a.mode=='complete' else [s for s in plan['commands'] if s['id'] in plan['quick_ids']]
  need(len(commands)==(42 if a.mode=='complete' else len(plan['quick_ids'])),'Selected suite cover')
  receipt['computational_manifest_sha256']=sha((ROOT/'COMPUTATIONAL_MANIFEST.json').read_bytes())
  receipt['plan_sha256']=sha((ROOT/'SUITE_PLAN.json').read_bytes())
  env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1';env['PYTHONHASHSEED']='0'
  for suite in commands:
   pair=[]
   for mode in ('normal','optimized'):
    stem=suite['id'].replace('.','_')+'_'+mode;job=out/stem;job.mkdir();scratch=job/'tmp';scratch.mkdir()
    env.update(TEMP=str(scratch),TMP=str(scratch),TMPDIR=str(scratch))
    args=[str(job/'semantic.json') if arg=='{output_json}' else arg for arg in suite['argv'][1:]]
    checker=suite['argv'][0]
    command=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+['-X','utf8',str(ROOT/'scripts/guarded_checker.py'),str(out),checker,*args]
    started=time.monotonic()
    try:r=launch(command,cwd=ROOT/suite.get('cwd','.'),env=env,timeout=suite['timeout_seconds'])
    except subprocess.TimeoutExpired as exc:
     (job/'stdout.txt').write_bytes(exc.stdout or b'');(job/'stderr.txt').write_bytes(exc.stderr or b'')
     receipt['executions'].append(dict(id=suite['id'],mode=mode,status='TIMEOUT',timeout_seconds=suite['timeout_seconds']))
     raise ValueError('Timeout '+suite['id']+' '+mode) from exc
    (job/'stdout.txt').write_bytes(r.stdout);(job/'stderr.txt').write_bytes(r.stderr)
    rec=dict(id=suite['id'],mode=mode,argv=command,cwd=str(ROOT/suite.get('cwd','.')),returncode=r.returncode,elapsed_seconds=round(time.monotonic()-started,6),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    receipt['executions'].append(rec);save(out/'RECEIPT.json',receipt)
    need(r.returncode==0,'Checker failed '+suite['id']+' '+mode+'; see '+stem+'/stderr.txt')
    data=load(job/'semantic.json') if suite.get('json_source')=='file' else json.loads(r.stdout)
    normalized=validate_semantic(data,suite);save(job/'normalized.json',normalized);pair.append(canonical(normalized))
    rec['semantic_sha256']=sha(pair[-1]);rec['status']='PASS_EXPECTED_SEMANTICS'
    save(out/'RECEIPT.json',receipt);print(suite['id']+' '+mode+' PASS',flush=True)
   need(pair[0]==pair[1],'Normal/-O semantic disagreement '+suite['id'])
   receipt['pairs'].append(dict(id=suite['id'],semantic_identical=True,semantic_sha256=sha(pair[0])))
  receipt['status']='COMPLETE_COMPANION_PASS' if a.mode=='complete' else 'QUICK_PARTIAL_PASS'
  receipt['complete_finite_companion']=a.mode=='complete'
  receipt['utc_finished']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(out/'RECEIPT.json',receipt)
  print(json.dumps(dict(status=receipt['status'],executions=len(receipt['executions']),pairs=len(receipt['pairs']))));return 0
 except Exception as exc:
  receipt['status']='FAIL_INCOMPLETE';receipt['error']=str(exc);receipt['exception_type']=type(exc).__name__
  receipt['utc_finished']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(out/'RECEIPT.json',receipt)
  print(json.dumps(dict(status=receipt['status'],error=str(exc))));return 1
if __name__=='__main__':raise SystemExit(main())

