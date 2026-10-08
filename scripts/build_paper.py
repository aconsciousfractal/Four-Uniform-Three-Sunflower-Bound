"""Rebuild the paper in a fresh isolated directory, preserving the distributed PDF."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = 'Four-Uniform-Three-Sunflower-Bound.pdf'

def need(condition, message):
    if not condition:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

def reject_links(path):
    for item in (path, *path.parents):
        if item.exists():
            need(not item.is_symlink(), 'Symbolic-link output path is not accepted')
            attrs = getattr(item.lstat(), 'st_file_attributes', 0)
            need(not attrs & 0x400, 'Reparse output path is not accepted')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='Fresh build directory, normally build/paper')
    parser.add_argument('--engine', default='pdflatex', help='Existing pdflatex executable; no installer is run')
    args = parser.parse_args()
    lexical = Path(args.output).absolute()
    reject_links(lexical)
    out = lexical.resolve()
    need(not out.exists(), 'Use a new build directory')
    if out.is_relative_to(ROOT):
        need(out.is_relative_to(ROOT / 'build') and out != ROOT / 'build', 'In-repository output must be a child of build/')
    print(str(out), flush=True)
    out.mkdir(parents=True)
    receipt = dict(status='RUNNING', package_installation=False, distributed_pdf_updated=False)
    save(out / 'BUILD_RECEIPT.json', receipt)
    try:
        check = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ROOT / 'scripts/check_repository.py')],
                               cwd=ROOT, capture_output=True, timeout=60)
        (out / 'integrity.stdout.txt').write_bytes(check.stdout)
        (out / 'integrity.stderr.txt').write_bytes(check.stderr)
        need(check.returncode == 0, 'Repository integrity check failed; inspect integrity logs')
        receipt.update(distributed_pdf_sha256=digest(ROOT / 'paper' / PDF_NAME),
                       source_sha256=digest(ROOT / 'paper/main.tex'),
                       package_manifest_sha256=digest(ROOT / 'MANIFEST_SHA256.json'))
        save(out / 'BUILD_RECEIPT.json', receipt)
        isolated = out / 'source'
        print(str(isolated), flush=True)
        (isolated / 'paper').mkdir(parents=True)
        (isolated / 'scripts').mkdir()
        for name in ('main.tex', PDF_NAME, 'bibliography.bib'):
            shutil.copyfile(ROOT / 'paper' / name, isolated / 'paper' / name)
        shutil.copyfile(ROOT / 'scripts/build_pdf.py', isolated / 'scripts/build_pdf.py')
        command = [sys.executable, '-B', '-X', 'utf8', str(isolated / 'scripts/build_pdf.py'),
                   '--output', str(out / 'latex'), '--engine', args.engine]
        receipt['command'] = command
        save(out / 'BUILD_RECEIPT.json', receipt)
        try:
            result = subprocess.run(command, cwd=isolated, capture_output=True, timeout=330)
        except subprocess.TimeoutExpired as error:
            (out / 'builder.stdout.txt').write_bytes(error.stdout or b'')
            (out / 'builder.stderr.txt').write_bytes(error.stderr or b'')
            raise ValueError('Isolated build timed out; available diagnostics retained') from error
        (out / 'builder.stdout.txt').write_bytes(result.stdout)
        (out / 'builder.stderr.txt').write_bytes(result.stderr)
        receipt['returncode'] = result.returncode
        need(result.returncode == 0, 'Isolated build failed; inspect builder and latex pass logs')
        child = json.loads((out / 'latex/BUILD_RECEIPT.json').read_bytes())
        need(child['status'] == 'PASS_BUILD' and len(child['runs']) == 3
             and all(run['returncode'] == 0 for run in child['runs']), 'Three successful TeX passes required')
        need(child['source_sha256'] == receipt['source_sha256'], 'Unexpected source in isolated build')
        need(digest(ROOT / 'paper' / PDF_NAME) == receipt['distributed_pdf_sha256'], 'Distributed PDF was changed')
        derived = out / PDF_NAME
        shutil.copyfile(isolated / 'paper' / PDF_NAME, derived)
        need(digest(derived) == child['pdf_sha256'], 'Derived PDF differs from build receipt')
        receipt.update(status='PASS_ISOLATED_BUILD', pdf=PDF_NAME, pdf_sha256=digest(derived),
                       source_pdf_preserved=True, runs=child['runs'], engine_version=child['engine_version'])
        save(out / 'BUILD_RECEIPT.json', receipt)
        print(json.dumps(receipt, ensure_ascii=False))
        return 0
    except Exception as error:
        receipt.update(status='FAIL_BUILD', error=str(error), exception_type=type(error).__name__)
        save(out / 'BUILD_RECEIPT.json', receipt)
        print(json.dumps(dict(status=receipt['status'], error=str(error))))
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
