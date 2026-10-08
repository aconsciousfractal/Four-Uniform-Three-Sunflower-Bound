"""Check fresh runner receipt/log consistency; this cannot authenticate execution."""
from pathlib import Path, PurePosixPath, PureWindowsPath
import argparse
import copy
import json
import re

from check_repository import ROOT, COMPUTATIONAL_SHA256, manifest_rows, need, reject_links, safe_path, sha, validate_plan, verify_rows


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf8')


def normalized(data, suite):
    result = copy.deepcopy(data)
    for key in suite.get('volatile_keys', []):
        need(isinstance(key, str) and key.startswith('$.'), 'Volatile path syntax')
        tokens = re.findall(r'([^.\[\]]+)|\[(\d+)\]', key[2:])
        need(bool(tokens), 'Empty volatile path')
        at = result
        for name, index in tokens[:-1]:
            at = at[int(index)] if index else at[name]
        name, index = tokens[-1]
        need(not index and name in at, 'Missing/array volatile field: ' + key)
        del at[name]
    need(canonical(result) == canonical(suite['expected_semantic']), 'Unexpected raw-log semantics: ' + suite['id'])
    return result


def recorded_path(name):
    need(isinstance(name, str) and bool(name), 'Recorded path missing')
    path = PureWindowsPath(name) if '\\' in name or re.match(r'^[A-Za-z]:', name) else PurePosixPath(name)
    need(path.is_absolute(), 'Recorded path must be absolute')
    return path


def receipt_directory(location):
    """Accept the receipt directory or its named RECEIPT.json without following links."""
    path = Path(location).absolute()
    reject_links(path)
    if path.name == 'RECEIPT.json':
        need(path.is_file(), 'Missing named RECEIPT.json')
        return path.parent
    need(not path.is_file(), 'Expected a receipt directory or RECEIPT.json')
    return path


def validate_receipt(directory, plan, computational_sha256, plan_sha256):
    """Accept an unchanged fresh verify.py receipt, including its actual raw logs."""
    directory = receipt_directory(directory)
    receipt = json.loads(safe_path(directory, 'RECEIPT.json').read_bytes())
    mode = receipt.get('mode')
    need(mode in ('quick', 'complete'), 'Receipt mode')
    complete = mode == 'complete'
    suites = plan['commands'] if complete else [s for s in plan['commands'] if s['id'] in plan['quick_ids']]
    need(len(suites) == (42 if complete else 2), 'Receipt required suite coverage')
    need(receipt.get('status') == ('COMPLETE_COMPANION_PASS' if complete else 'QUICK_PARTIAL_PASS'), 'Receipt final status')
    need(receipt.get('complete_finite_companion') is complete and
         receipt.get('external_theorems_replayed') is False and receipt.get('formalized') is False,
         'Receipt scope flags')
    need(receipt.get('computational_manifest_sha256') == computational_sha256 and
         receipt.get('plan_sha256') == plan_sha256, 'Receipt input/plan pins')
    need(isinstance(receipt.get('utc_finished'), str) and bool(receipt['utc_finished']), 'Receipt unfinished')
    executions = receipt.get('executions', [])
    pairs = receipt.get('pairs', [])
    need([(r.get('id'), r.get('mode')) for r in executions] ==
         [(s['id'], m) for s in suites for m in ('normal', 'optimized')], 'Receipt ordered executions/coverage')
    need([p.get('id') for p in pairs] == [s['id'] for s in suites], 'Receipt ordered pairs/coverage')
    recorded_roots = None
    for index, suite in enumerate(suites):
        pair_hashes = []
        for offset, run_mode in enumerate(('normal', 'optimized')):
            execution = executions[2 * index + offset]
            need(type(execution.get('returncode')) is int and execution['returncode'] == 0 and
                 execution.get('status') == 'PASS_EXPECTED_SEMANTICS', 'Failed execution: ' + suite['id'])
            stem = suite['id'].replace('.', '_') + '_' + run_mode
            stdout = safe_path(directory, stem + '/stdout.txt').read_bytes()
            stderr = safe_path(directory, stem + '/stderr.txt').read_bytes()
            need(sha(stdout) == execution.get('stdout_sha256') and sha(stderr) == execution.get('stderr_sha256'), 'Raw log hash mismatch: ' + stem)
            data = json.loads(safe_path(directory, stem + '/semantic.json').read_bytes()) if suite.get('json_source') == 'file' else json.loads(stdout)
            scientific = normalized(data, suite)
            stored = json.loads(safe_path(directory, stem + '/normalized.json').read_bytes())
            need(canonical(stored) == canonical(scientific), 'Normalized log mismatch: ' + stem)
            digest = sha(canonical(scientific))
            need(execution.get('semantic_sha256') == digest, 'Execution semantic hash: ' + stem)
            argv = execution.get('argv')
            flags = ['-B'] + (['-O'] if run_mode == 'optimized' else []) + ['-X', 'utf8']
            need(isinstance(argv, list) and len(argv) >= len(flags) + 4 and
                 isinstance(argv[0], str) and bool(argv[0]) and argv[1:1 + len(flags)] == flags,
                 'Recorded normal/optimized argv: ' + stem)
            position = 1 + len(flags)
            guard = recorded_path(argv[position])
            output = recorded_path(argv[position + 1])
            package = guard.parent.parent
            need(guard == package / 'scripts' / 'guarded_checker.py', 'Recorded guarded checker: ' + stem)
            roots = (package, output)
            if recorded_roots is None:
                recorded_roots = roots
            need(recorded_roots == roots and not output.is_relative_to(package), 'Recorded package/output boundary: ' + stem)
            args = [str(output / stem / 'semantic.json') if a == '{output_json}' else a for a in suite['argv'][1:]]
            need(argv[position + 2:] == [suite['argv'][0], *args], 'Recorded suite argv: ' + stem)
            need(recorded_path(execution.get('cwd')) == package / suite.get('cwd', '.'), 'Recorded suite cwd: ' + stem)
            pair_hashes.append(digest)
        pair = pairs[index]
        need(pair_hashes[0] == pair_hashes[1] and pair.get('semantic_identical') is True and
             pair.get('semantic_sha256') == pair_hashes[0], 'Normal/optimized pair mismatch: ' + suite['id'])
    return dict(status='PASS_RECEIPT_CONSISTENCY', runner_status=receipt['status'], mode=mode, executions=len(executions), pairs=len(pairs),
                scope='Consistency of supplied receipt and logs; cannot authenticate past execution')


def check_receipt(directory, package_root=ROOT):
    raw = safe_path(package_root, 'COMPUTATIONAL_MANIFEST.json').read_bytes()
    need(sha(raw) == COMPUTATIONAL_SHA256, 'Computational manifest pin')
    plan_raw = safe_path(package_root, 'SUITE_PLAN.json').read_bytes()
    rows = manifest_rows(json.loads(raw), 'BOUND68_COMPUTATIONAL_MANIFEST_V1', 1692)
    verify_rows(package_root, rows)
    plan_row = next((r for r in rows if r['path'] == 'SUITE_PLAN.json'), None)
    need(plan_row is not None and len(plan_raw) == plan_row['bytes'] and
         sha(plan_raw) == plan_row['sha256'], 'Pinned plan bytes')
    return validate_receipt(directory, validate_plan(json.loads(plan_raw)), sha(raw), sha(plan_raw))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory')
    parser.add_argument('--package-root', default=str(ROOT))
    args = parser.parse_args()
    try:
        result = check_receipt(args.directory, args.package_root)
    except Exception as exc:
        print(json.dumps(dict(status='FAIL_RECEIPT_CONSISTENCY', error=str(exc))))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
