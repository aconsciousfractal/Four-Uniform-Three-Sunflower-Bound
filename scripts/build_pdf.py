"""Export using an existing pdflatex installation; no package installation."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
PDF_STEM='Four-Uniform-Three-Sunflower-Bound'
def need(c,m):
 if not c:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--engine',default='pdflatex');a=ap.parse_args()
 out=Path(a.output).resolve();need(not out.exists(),'Use a new build directory');print(str(out));out.mkdir(parents=True)
 source=ROOT/'paper/main.tex';version=subprocess.run([a.engine,'--version'],capture_output=True,check=True).stdout.decode(errors='replace')
 flags=['--disable-installer'] if 'MiKTeX' in version else []
 command=[a.engine,*flags,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-jobname='+PDF_STEM,'-output-directory='+str(out),source.name]
 runs=[]
 for number in (1,2,3):
  r=subprocess.run(command,cwd=source.parent,capture_output=True,timeout=90)
  (out/f'pass{number}.stdout.txt').write_bytes(r.stdout);(out/f'pass{number}.stderr.txt').write_bytes(r.stderr)
  runs.append(dict(pass_number=number,returncode=r.returncode));need(r.returncode==0,'Build failed: see captured diagnostics')
 log=(out/(PDF_STEM+'.log')).read_text(encoding='utf8',errors='replace')
 need('undefined references' not in log and 'undefined on input line' not in log,'Unresolved reference/citation')
 need('Overfull' not in log,'Overfull layout box')
 pdf=ROOT/'paper'/(PDF_STEM+'.pdf');pdf.write_bytes((out/(PDF_STEM+'.pdf')).read_bytes())
 result=dict(status='PASS_BUILD',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),runs=runs,engine_version=version.splitlines()[0],package_installation=False)
 (out/'BUILD_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result))
if __name__=='__main__':main()
