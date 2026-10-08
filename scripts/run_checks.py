"""Check repository integrity, then run its unchanged finite verifier in a separate copy."""
from pathlib import Path
import argparse
import datetime
import json
import os
import signal
import subprocess
import sys

from check_repository import ROOT, check_repository, manifest_rows, need, reject_links, safe_path, sha, verify_rows
from check_receipt import check_receipt


def save(path, result):
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf8', newline='\n')


def execute(command, *, cwd, env, timeout):
    """Capture a runner; an explicit outer timeout also stops its checker descendants."""
    options = {'start_new_session': True} if os.name != 'nt' else {}
    process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        if os.name == 'nt':
            # PID comes only from the process just created by this wrapper.
            cleanup = subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, timeout=10)
            if cleanup.returncode and process.poll() is None:
                process.kill()
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        stdout, stderr = process.communicate()
        exc.stdout, exc.stderr = stdout, stderr
        raise
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def run_checks(mode, output, root=ROOT, timeout_seconds=None):
    root = Path(os.path.abspath(root))
    output = Path(os.path.abspath(output))
    reject_links(output)
    need(not output.exists(), 'Use a fresh wrapper output directory')
    need(not output.is_relative_to(root) or
         (output.is_relative_to(root / 'build') and output != root / 'build'),
         'Output must be a fresh child of root build/ or outside repository')
    print(str(output), flush=True)
    output.mkdir(parents=True)
    receipt = dict(status='RUNNING', mode=mode, utc_started=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   mathematical_scope='Unchanged named finite verifier; no external theorem replay or formalization',
                   execution_authentication=False)
    save(output / 'WRAPPER_RECEIPT.json', receipt)
    (output / 'runner.stdout.txt').write_bytes(b'')
    (output / 'runner.stderr.txt').write_bytes(b'')
    try:
        need(mode in ('quick', 'complete'), 'Wrapper mode')
        receipt['repository_integrity'] = check_repository(root)
        raw = safe_path(root, 'COMPUTATIONAL_MANIFEST.json').read_bytes()
        rows = manifest_rows(json.loads(raw), 'BOUND68_COMPUTATIONAL_MANIFEST_V1', 1692)
        package = output / 'package'
        print(str(package), flush=True)
        package.mkdir()
        for row in rows:
            destination = safe_path(package, row['path'])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(safe_path(root, row['path']).read_bytes())
        (package / 'COMPUTATIONAL_MANIFEST.json').write_bytes(raw)
        verify_rows(package, rows)
        environment = dict(os.environ)
        environment.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONHASHSEED='0')
        command = [sys.executable, '-B', '-X', 'utf8', str(package / 'scripts/verify.py'),
                   '--mode', mode, '--output', str(output / 'receipts')]
        receipt['argv'] = command
        save(output / 'WRAPPER_RECEIPT.json', receipt)
        try:
            result = execute(command, cwd=package, env=environment, timeout=timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            (output / 'runner.stdout.txt').write_bytes(exc.stdout or b'')
            (output / 'runner.stderr.txt').write_bytes(exc.stderr or b'')
            receipt['runner_status'] = 'TIMEOUT'
            receipt['timeout_seconds'] = timeout_seconds
            raise ValueError('Wrapper timeout; partial runner receipt/logs retained') from exc
        (output / 'runner.stdout.txt').write_bytes(result.stdout)
        (output / 'runner.stderr.txt').write_bytes(result.stderr)
        receipt['runner_returncode'] = result.returncode
        need(result.returncode == 0, 'Runner failed; inspect retained receipt/logs')
        receipt['runner_receipt_check'] = check_receipt(output / 'receipts', package)
        receipt['runner_status'] = receipt['runner_receipt_check']['runner_status']
        receipt['repository_integrity_after'] = check_repository(root)
        need(receipt['repository_integrity_after'] == receipt['repository_integrity'], 'Source repository changed during checks')
        receipt['status'] = 'PASS_WRAPPER_CHECKS'
    except Exception as exc:
        receipt['status'] = 'FAIL_WRAPPER_CHECKS'
        receipt['error'] = str(exc)
        receipt['exception_type'] = type(exc).__name__
    receipt['stdout_sha256'] = sha((output / 'runner.stdout.txt').read_bytes())
    receipt['stderr_sha256'] = sha((output / 'runner.stderr.txt').read_bytes())
    receipt['utc_finished'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(output / 'WRAPPER_RECEIPT.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('quick', 'complete'), required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--timeout-seconds', type=float, help='Optional wrapper budget; timeout is always failure')
    args = parser.parse_args()
    try:
        need(args.timeout_seconds is None or args.timeout_seconds > 0, 'Timeout must be positive')
        result = run_checks(args.mode, args.output, timeout_seconds=args.timeout_seconds)
    except Exception as exc:
        print(json.dumps(dict(status='FAIL_WRAPPER_PREFLIGHT', error=str(exc))))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'PASS_WRAPPER_CHECKS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
