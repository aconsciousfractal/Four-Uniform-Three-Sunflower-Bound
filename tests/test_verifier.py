"""Targeted adverse-input tests; these do not repeat mathematical suites."""
from pathlib import Path
import argparse,contextlib,importlib.util,hashlib,json,os,shutil,subprocess,sys,tempfile,unittest,uuid
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(add_help=False);parser.add_argument('--temp-root');options,remaining=parser.parse_known_args();sys.argv=[sys.argv[0],*remaining]
TEMP_ROOT=Path(options.temp_root or tempfile.gettempdir()).resolve()
@contextlib.contextmanager
def scoped_tmp():
 target=(TEMP_ROOT/('bound68-adverse-'+uuid.uuid4().hex)).resolve()
 if not target.is_relative_to(TEMP_ROOT):raise ValueError('Test scratch escapes root')
 print(str(target),flush=True);target.mkdir(parents=True)
 try:yield str(target)
 finally:
  if not target.resolve().is_relative_to(TEMP_ROOT):raise ValueError('Cleanup escapes test root')
  shutil.rmtree(target)
spec=importlib.util.spec_from_file_location('bound68_verify',ROOT/'scripts/verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class AdverseInputs(unittest.TestCase):
 def test_missing_and_altered_input(self):
  with scoped_tmp() as tmp:
   root=Path(tmp);p=root/'certificate.json';good=b'{"coverage":42}';p.write_bytes(good)
   manifest=dict(schema='BOUND68_COMPUTATIONAL_MANIFEST_V1',files=[dict(path=p.name,bytes=len(good),sha256=hashlib.sha256(good).hexdigest())])
   p.write_bytes(b'{"coverage":41}')
   with self.assertRaisesRegex(ValueError,'Changed input'):v.validate_manifest(root,manifest)
   p.unlink()
   with self.assertRaisesRegex(ValueError,'Missing/escaping input'):v.validate_manifest(root,manifest)
 def test_false_status_and_missing_coverage(self):
  suite=dict(id='coverage-control',expected_semantic=dict(status='PASS',roots=42),volatile_keys=[])
  with self.assertRaisesRegex(ValueError,'Unexpected semantic'):v.validate_semantic(dict(status='FAIL',roots=42),suite)
  with self.assertRaisesRegex(ValueError,'Unexpected semantic'):v.validate_semantic(dict(status='PASS',roots=41),suite)
 def test_existing_output_is_preserved(self):
  with scoped_tmp() as tmp:
   out=Path(tmp)/'receipts';out.mkdir();sentinel=out/'sentinel';sentinel.write_bytes(b'preserve')
   r=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/verify.py'),'--mode','complete','--output',str(out)],capture_output=True)
   self.assertEqual(r.returncode,2);self.assertEqual(json.loads(r.stdout)['status'],'FAIL_EXISTING_OUTPUT');self.assertEqual(sentinel.read_bytes(),b'preserve')
 def test_real_timeout_is_not_success(self):
  with self.assertRaises(subprocess.TimeoutExpired):
   v.launch([sys.executable,'-B','-c','import time;time.sleep(1)'],cwd=ROOT,env=dict(os.environ),timeout=0.03)
 def test_failed_preflight_preserves_receipt(self):
  with scoped_tmp() as tmp:
   base=Path(tmp);package=base/'package';scripts=package/'scripts';scripts.mkdir(parents=True)
   (scripts/'verify.py').write_bytes((ROOT/'scripts/verify.py').read_bytes())
   manifest=dict(schema='BOUND68_COMPUTATIONAL_MANIFEST_V1',files=[dict(path='missing-certificate.bin',bytes=1,sha256='0'*64)])
   (package/'COMPUTATIONAL_MANIFEST.json').write_text(json.dumps(manifest))
   out=base/'receipts'
   r=subprocess.run([sys.executable,'-B',str(scripts/'verify.py'),'--mode','complete','--output',str(out)],cwd=package,capture_output=True)
   self.assertEqual(r.returncode,1);receipt=json.loads((out/'RECEIPT.json').read_bytes())
   self.assertEqual(receipt['status'],'FAIL_INCOMPLETE');self.assertFalse(receipt['complete_finite_companion']);self.assertEqual(receipt['executions'],[])
  for fixture in ('wrong-semantic','timeout'):
   with scoped_tmp() as tmp:
    base=Path(tmp);package=base/'package';scripts=package/'scripts';scripts.mkdir(parents=True)
    for name in ('verify.py','guarded_checker.py'):(scripts/name).write_bytes((ROOT/'scripts'/name).read_bytes())
    probe=package/'probe.py';probe.write_text('import time;time.sleep(1)\n' if fixture=='timeout' else 'print(\'{"status":"FAIL","roots":42}\')\n')
    commands=[dict(id='control'+str(i),argv=['probe.py'],cwd='.',timeout_seconds=0.03 if fixture=='timeout' else 5,expected_semantic=dict(status='PASS',roots=42),volatile_keys=[]) for i in range(42)]
    (package/'SUITE_PLAN.json').write_text(json.dumps(dict(suite_count=42,upstream_blocks=list(range(9)),commands=commands,quick_ids=[])))
    rows=[dict(path=p.relative_to(package).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in package.rglob('*') if p.is_file()]
    (package/'COMPUTATIONAL_MANIFEST.json').write_text(json.dumps(dict(schema='BOUND68_COMPUTATIONAL_MANIFEST_V1',files=rows)))
    out=base/'receipts';r=subprocess.run([sys.executable,'-B',str(scripts/'verify.py'),'--mode','complete','--output',str(out)],cwd=package,capture_output=True)
    self.assertEqual(r.returncode,1);receipt=json.loads((out/'RECEIPT.json').read_bytes())
    self.assertEqual(receipt['status'],'FAIL_INCOMPLETE');self.assertFalse(receipt['complete_finite_companion']);self.assertEqual(len(receipt['executions']),1)
    if fixture=='timeout':self.assertEqual(receipt['executions'][0]['status'],'TIMEOUT')
    else:self.assertIn('Unexpected semantic result',receipt['error'])
 def test_filesystem_boundary_rejects_external_read(self):
  with scoped_tmp() as tmp:
   base=Path(tmp);package=base/'package';scripts=package/'scripts';scripts.mkdir(parents=True);out=base/'out';out.mkdir()
   (scripts/'guarded_checker.py').write_bytes((ROOT/'scripts/guarded_checker.py').read_bytes())
   secret=base/'outside.txt';secret.write_text('outside')
   (package/'probe.py').write_text('from pathlib import Path\nPath('+repr(str(secret))+').read_bytes()\n')
   r=subprocess.run([sys.executable,'-B',str(scripts/'guarded_checker.py'),str(out),'probe.py'],cwd=package,capture_output=True)
   self.assertNotEqual(r.returncode,0);self.assertIn(b'Filesystem access outside',r.stderr)
if __name__=='__main__':unittest.main()
