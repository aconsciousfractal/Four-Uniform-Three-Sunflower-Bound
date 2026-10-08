"""Synthetic repository and receipt tampering controls; no mathematical suites."""
from pathlib import Path
import argparse
import copy
import contextlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_repository as repository
import check_receipt as checker
import run_checks as wrapper

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--temp-root')
options, remaining = parser.parse_known_args()
sys.argv = [sys.argv[0], *remaining]


def row(name, raw):
    return dict(path=name, bytes=len(raw), sha256=repository.sha(raw))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + '\n', encoding='utf8')


@contextlib.contextmanager
def scratch():
    with tempfile.TemporaryDirectory(prefix='e20-repository-tools-', dir=options.temp_root) as directory:
        yield Path(directory)


def fixture_receipt(directory, mode='quick'):
    suites = [dict(id=name, argv=['probe.py'], cwd='.', expected_semantic={'status': 'PASS', 'count': 3}, volatile_keys=['$.seconds'])
              for name in ('terminal.f69_bridge', 'terminal.primary')]
    suites += [dict(suites[0], id='synthetic.' + str(i)) for i in range(40)]
    plan = dict(schema='BOUND68_COMPLETE_PLAN_V1', suite_count=42,
                upstream_blocks=['block' + str(i) for i in range(9)], commands=suites,
                quick_ids=['terminal.f69_bridge', 'terminal.primary'])
    complete = mode == 'complete'
    receipt = dict(mode=mode, status='COMPLETE_COMPANION_PASS' if complete else 'QUICK_PARTIAL_PASS',
                   complete_finite_companion=complete, external_theorems_replayed=False, formalized=False,
                   utc_finished='2026-10-08T00:00:00+00:00', computational_manifest_sha256='a' * 64,
                   plan_sha256='b' * 64, executions=[], pairs=[])
    package = directory.parent / 'recorded-package'
    output = directory.parent / 'recorded-receipts'
    for suite in suites if complete else suites[:2]:
        for mode_name in ('normal', 'optimized'):
            stem = suite['id'].replace('.', '_') + '_' + mode_name
            job = directory / stem
            data = dict(suite['expected_semantic'], seconds=0.001)
            stdout = json.dumps(data).encode('utf8')
            job.mkdir(parents=True)
            (job / 'stdout.txt').write_bytes(stdout)
            (job / 'stderr.txt').write_bytes(b'')
            save(job / 'normalized.json', suite['expected_semantic'])
            digest = repository.sha(checker.canonical(suite['expected_semantic']))
            argv = [sys.executable, '-B'] + (['-O'] if mode_name == 'optimized' else [])
            argv += ['-X', 'utf8', str(package / 'scripts/guarded_checker.py'), str(output), 'probe.py']
            receipt['executions'].append(dict(id=suite['id'], mode=mode_name, status='PASS_EXPECTED_SEMANTICS',
                                              returncode=0, stdout_sha256=repository.sha(stdout), stderr_sha256=repository.sha(b''),
                                              semantic_sha256=digest, argv=argv, cwd=str(package)))
        receipt['pairs'].append(dict(id=suite['id'], semantic_identical=True, semantic_sha256=digest))
    save(directory / 'RECEIPT.json', receipt)
    return plan, receipt


class RepositoryControls(unittest.TestCase):
    def test_manifest_duplicate_escape_changed_and_lfs(self):
        with scratch() as directory:
            raw = b'ordinary bytes\n'
            (directory / 'input.bin').write_bytes(raw)
            packet = dict(schema='fixture', files=[row('input.bin', raw)])
            repository.verify_rows(directory, repository.manifest_rows(packet, 'fixture'))
            duplicate = dict(packet, files=packet['files'] * 2)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                repository.manifest_rows(duplicate, 'fixture')
            for path in ('../escape', '/absolute', 'a/../escape', 'C:/escape', 'a\\escape', './input.bin', 'a//b'):
                with self.assertRaisesRegex(ValueError, 'Escaping'):
                    repository.safe_path(directory, path)
            (directory / 'input.bin').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Changed'):
                repository.verify_rows(directory, packet['files'])
            pointer = repository.LFS_PREFIX + b'\noid sha256:' + b'0' * 64 + b'\nsize 123\n'
            (directory / 'input.bin').write_bytes(pointer)
            with self.assertRaisesRegex(ValueError, 'LFS pointer'):
                repository.verify_rows(directory, [row('input.bin', pointer)])

    def test_closed_inventory_ignores_only_declared_generated_files(self):
        with scratch() as directory:
            (directory / 'keep.txt').write_bytes(b'keep')
            (directory / 'MANIFEST_SHA256.json').write_bytes(b'{}')
            for name in ('.git/metadata', 'build/receipt.json', 'inputs/derived.bin', 'scripts/__pycache__/tool.pyc'):
                p = directory / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b'generated')
            self.assertEqual(repository.distribution_files(directory), {'keep.txt'})
            p = directory / 'scripts/__pycache__/unexpected.txt'; p.write_bytes(b'extra')
            self.assertIn('scripts/__pycache__/unexpected.txt', repository.distribution_files(directory))

    def test_repository_rejects_extra_distribution_file_before_baseline(self):
        with scratch() as directory:
            (directory / 'listed.bin').write_bytes(b'listed')
            save(directory / 'MANIFEST_SHA256.json', dict(schema='BOUND68_STANDALONE_PAYLOAD_V1', files=[row('listed.bin', b'listed')]))
            (directory / 'unexpected.bin').write_bytes(b'unlisted')
            with self.assertRaisesRegex(ValueError, 'closed allowlist'):
                repository.check_repository(directory)

    def test_generated_root_exclusions_reject_regular_files_and_reparse_paths(self):
        with scratch() as directory:
            for name in ('build', 'inputs'):
                path = directory / name; path.write_bytes(b'unexpected regular file')
                with self.assertRaisesRegex(ValueError, 'Reserved generated-root path'):
                    repository.distribution_files(directory)
                path.unlink(); path.mkdir()
                original = Path.lstat
                def fake_lstat(item):
                    if item == path:
                        return type('Reparse', (), dict(st_mode=0, st_file_attributes=0x400))()
                    return original(item)
                with mock.patch.object(Path, 'lstat', fake_lstat):
                    with self.assertRaisesRegex(ValueError, 'Symlink/reparse'):
                        repository.distribution_files(directory)
                path.rmdir()

    def test_lexical_file_link_and_parent_link_rejected(self):
        with scratch() as directory:
            real = directory / 'real'; real.mkdir(); (real / 'input.bin').write_bytes(b'real')
            link = directory / 'linked'
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                if os.name != 'nt':
                    self.skipTest('This account cannot create symlinks: ' + str(exc))
                result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(real)], capture_output=True)
                if result.returncode:
                    self.skipTest('Neither symlink nor junction creation is available')
            try:
                with self.assertRaisesRegex(ValueError, 'Symlink/reparse'):
                    repository.safe_path(directory, 'linked/input.bin')
                with self.assertRaisesRegex(ValueError, 'Symlink/reparse'):
                    repository.distribution_files(directory)
            finally:
                if link.is_symlink():
                    link.unlink()
                else:
                    link.rmdir()  # Remove this fixture junction, preserving its real target.

    def test_reparse_attribute_rejected_without_following_target(self):
        with scratch() as directory:
            path = directory / 'probe'; path.write_bytes(b'x')
            original = Path.lstat
            def fake_lstat(item):
                if item == path:
                    return type('Reparse', (), dict(st_mode=0, st_file_attributes=0x400))()
                return original(item)
            with mock.patch.object(Path, 'lstat', fake_lstat):
                with self.assertRaisesRegex(ValueError, 'Symlink/reparse'):
                    repository.safe_path(directory, 'probe')

    def test_scope_coverage_is_not_partial(self):
        with scratch() as directory:
            plan, _ = fixture_receipt(directory / 'receipts')
            repository.validate_plan(plan)
            for field, value in (('suite_count', 41), ('upstream_blocks', ['one']), ('quick_ids', ['terminal.primary'])):
                bad = copy.deepcopy(plan); bad[field] = value
                with self.assertRaises(ValueError):
                    repository.validate_plan(bad)


class ReceiptControls(unittest.TestCase):
    def test_named_receipt_file_is_accepted(self):
        with scratch() as directory:
            plan, _ = fixture_receipt(directory)
            from_directory = checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)
            from_file = checker.validate_receipt(directory / 'RECEIPT.json', plan, 'a' * 64, 'b' * 64)
            self.assertEqual(from_file, from_directory)
            other = directory / 'other.json'; other.write_bytes(b'{}')
            with self.assertRaisesRegex(ValueError, 'Expected a receipt directory'):
                checker.receipt_directory(other)

    def test_rehashed_semantic_type_corruption_is_rejected(self):
        with scratch() as directory:
            plan, receipt = fixture_receipt(directory)
            for corrupted_count in (3.0, True):
                if corrupted_count is True:
                    plan['commands'][0]['expected_semantic']['count'] = 1
                raw = json.dumps(dict(status='PASS', count=corrupted_count, seconds=0.01)).encode('utf8')
                log = directory / 'terminal_f69_bridge_normal/stdout.txt'; log.write_bytes(raw)
                receipt['executions'][0]['stdout_sha256'] = repository.sha(raw)
                save(directory / 'RECEIPT.json', receipt)
                with self.assertRaisesRegex(ValueError, 'Unexpected raw-log semantics'):
                    checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)
        with scratch() as directory:
            plan, _ = fixture_receipt(directory)
            save(directory / 'terminal_f69_bridge_normal/normalized.json', dict(status='PASS', count=3.0))
            with self.assertRaisesRegex(ValueError, 'Normalized log mismatch'):
                checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)

    def test_good_synthetic_quick_and_complete_consistency(self):
        with scratch() as directory:
            for mode in ('quick', 'complete'):
                folder = directory / mode; plan, _ = fixture_receipt(folder, mode)
                result = checker.validate_receipt(folder, plan, 'a' * 64, 'b' * 64)
                self.assertEqual(result['executions'], 4 if mode == 'quick' else 84)
                self.assertEqual(result['pairs'], 2 if mode == 'quick' else 42)

    def test_missing_and_hash_wrong_raw_logs(self):
        with scratch() as directory:
            plan, _ = fixture_receipt(directory)
            log = directory / 'terminal_f69_bridge_normal/stdout.txt'
            raw = log.read_bytes(); log.unlink()
            with self.assertRaises(FileNotFoundError):
                checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)
            log.write_bytes(raw + b' ')
            with self.assertRaisesRegex(ValueError, 'Raw log hash'):
                checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)

    def test_rehashed_false_raw_semantics_and_normalized_tamper(self):
        with scratch() as directory:
            plan, receipt = fixture_receipt(directory)
            log = directory / 'terminal_f69_bridge_normal/stdout.txt'
            log.write_bytes(b'{"status":"FAIL","count":3,"seconds":0.1}')
            receipt['executions'][0]['stdout_sha256'] = repository.sha(log.read_bytes())
            save(directory / 'RECEIPT.json', receipt)
            with self.assertRaisesRegex(ValueError, 'Unexpected raw-log semantics'):
                checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)
        with scratch() as directory:
            plan, _ = fixture_receipt(directory)
            save(directory / 'terminal_f69_bridge_normal/normalized.json', {'status': 'PASS', 'count': 2})
            with self.assertRaisesRegex(ValueError, 'Normalized log mismatch'):
                checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)

    def test_false_complete_relabelled_optimized_missing_pair_and_input_pin(self):
        with scratch() as directory:
            plan, receipt = fixture_receipt(directory)
            changes = []
            bad = copy.deepcopy(receipt); bad.update(mode='complete', status='COMPLETE_COMPANION_PASS', complete_finite_companion=True); changes.append(bad)
            bad = copy.deepcopy(receipt); bad['executions'][1]['argv'].remove('-O'); changes.append(bad)
            bad = copy.deepcopy(receipt); bad['pairs'].pop(); changes.append(bad)
            bad = copy.deepcopy(receipt); bad['computational_manifest_sha256'] = 'c' * 64; changes.append(bad)
            bad = copy.deepcopy(receipt); bad['executions'][0]['returncode'] = 1; changes.append(bad)
            bad = copy.deepcopy(receipt); bad['status'] = 'FAIL_INCOMPLETE'; changes.append(bad)
            for bad in changes:
                save(directory / 'RECEIPT.json', bad)
                with self.assertRaises(ValueError):
                    checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)

    def test_semantic_file_logs_are_required(self):
        with scratch() as directory:
            plan, receipt = fixture_receipt(directory)
            suite = plan['commands'][0]; suite['json_source'] = 'file'; suite['argv'] = ['probe.py', '--output', '{output_json}']
            for i, mode in enumerate(('normal', 'optimized')):
                execution = receipt['executions'][i]
                output = checker.recorded_path(execution['argv'][-2])
                stem = 'terminal_f69_bridge_' + mode
                execution['argv'] += ['--output', str(output / stem / 'semantic.json')]
                save(directory / stem / 'semantic.json', dict(suite['expected_semantic'], seconds=1.0))
            save(directory / 'RECEIPT.json', receipt)
            checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)
            (directory / 'terminal_f69_bridge_normal/semantic.json').unlink()
            with self.assertRaises(FileNotFoundError):
                checker.validate_receipt(directory, plan, 'a' * 64, 'b' * 64)


class WrapperControls(unittest.TestCase):
    def test_runner_failure_and_timeout_preserve_captured_diagnostics(self):
        for timed_out in (False, True):
            with scratch() as directory:
                root = directory / 'repository'; root.mkdir()
                raw = b'fixture verifier bytes'
                verifier = root / 'scripts/verify.py'; verifier.parent.mkdir(); verifier.write_bytes(raw)
                rows = [row('scripts/verify.py', raw)]
                save(root / 'COMPUTATIONAL_MANIFEST.json', dict(schema='BOUND68_COMPUTATIONAL_MANIFEST_V1', files=rows))
                integrity = {'status': 'synthetic byte control'}
                if timed_out:
                    outcome = subprocess.TimeoutExpired(['synthetic'], 0.1, output=b'partial stdout', stderr=b'partial stderr')
                    patch = mock.patch.object(wrapper, 'execute', side_effect=outcome)
                else:
                    outcome = subprocess.CompletedProcess(['synthetic'], 1, b'failed stdout', b'failed stderr')
                    patch = mock.patch.object(wrapper, 'execute', return_value=outcome)
                with mock.patch.object(wrapper, 'check_repository', return_value=integrity), \
                     mock.patch.object(wrapper, 'manifest_rows', return_value=rows), patch:
                    output = directory / 'output'
                    result = wrapper.run_checks('quick', output, root=root, timeout_seconds=0.1)
                self.assertEqual(result['status'], 'FAIL_WRAPPER_CHECKS')
                self.assertEqual((output / 'runner.stdout.txt').read_bytes(), outcome.stdout)
                self.assertEqual((output / 'runner.stderr.txt').read_bytes(), outcome.stderr)
                self.assertEqual(verifier.read_bytes(), raw)
                if timed_out:
                    self.assertEqual(result['runner_status'], 'TIMEOUT')

    def test_failed_integrity_preserves_wrapper_receipt_and_logs(self):
        with scratch() as directory:
            root = directory / 'repository'; root.mkdir(); sentinel = root / 'sentinel'; sentinel.write_bytes(b'original')
            output = directory / 'output'
            result = wrapper.run_checks('quick', output, root=root)
            self.assertEqual(result['status'], 'FAIL_WRAPPER_CHECKS')
            self.assertTrue((output / 'WRAPPER_RECEIPT.json').is_file())
            self.assertTrue((output / 'runner.stdout.txt').is_file())
            self.assertTrue((output / 'runner.stderr.txt').is_file())
            self.assertEqual(sentinel.read_bytes(), b'original')
            with self.assertRaisesRegex(ValueError, 'fresh'):
                wrapper.run_checks('quick', output, root=root)

    def test_wrapper_rejects_in_payload_output(self):
        with scratch() as directory:
            with self.assertRaisesRegex(ValueError, 'Output must'):
                wrapper.run_checks('quick', directory / 'payload-output', root=directory)
            self.assertFalse((directory / 'payload-output').exists())


if __name__ == '__main__':
    unittest.main()
