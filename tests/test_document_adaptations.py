"""Bounded documentary transitions and retained JSON fields; no mathematical replay."""
from pathlib import Path
import argparse
import copy
import json
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_repository as repository

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--temp-root')
options, remaining = parser.parse_known_args()
sys.argv = [sys.argv[0], *remaining]


def row(name, raw):
    return dict(path=name, bytes=len(raw), sha256=repository.sha(raw))


class DocumentaryControls(unittest.TestCase):
    def setUp(self):
        self.name = 'companion/upstream/D20/PROOF.md'
        self.old = row(self.name, b'old documentary exposition')
        self.new = row(self.name, b'current documentary exposition')
        self.code = row('scripts/verify.py', b'unchanged runner')
        self.data = row('certificate.json', b'{"roots":42}')
        self.baseline = [self.old, self.code, self.data]
        self.original = copy.deepcopy(self.baseline)
        self.current = [self.new, self.code, self.data]
        self.packet = dict(
            schema='BOUND68_DOCUMENT_ADAPTATIONS_V2',
            reviewed_distribution_manifest_sha256='bedf670dd173ecccc6247c44d4f74cb359f771c9c8c44c8c5b2ed404a2c2d2d5',
            baseline_manifest_sha256=repository.BASELINE_SHA256,
            baseline_computational_manifest_sha256=repository.BASELINE_COMPUTATIONAL_SHA256,
            current_computational_manifest_sha256=repository.COMPUTATIONAL_SHA256,
            relocations={},
            files=[dict(path=self.name, before={k: v for k, v in self.old.items() if k != 'path'},
                        after={k: v for k, v in self.new.items() if k != 'path'},
                        reason='Correct the current reader exposition')])
        self.policy = mock.patch.object(repository, 'DOCUMENTARY_PATHS', frozenset([self.name]))
        self.policy.start()
        self.addCleanup(self.policy.stop)
        for attribute, value in (('BUILD_ADAPTATION_PATHS', frozenset()), ('EXPECTED_RELOCATIONS', {})):
            patch = mock.patch.object(repository, attribute, value)
            patch.start(); self.addCleanup(patch.stop)

    def validate(self, packet=None, current=None):
        return repository.validate_adaptations(self.packet if packet is None else packet,
                                              self.baseline, self.original,
                                              self.current if current is None else current)

    def test_exact_transition_and_all_retained_input_rows(self):
        self.assertEqual(self.validate(), {self.name: self.new})

    def test_rejects_omitted_added_duplicate_and_unapproved_paths(self):
        packets = []
        missing = copy.deepcopy(self.packet); missing['files'] = []; packets.append(missing)
        duplicate = copy.deepcopy(self.packet); duplicate['files'] *= 2; packets.append(duplicate)
        for name in ('scripts/verify.py', 'certificate.json', '../escape', 'another/PROOF.md'):
            packet = copy.deepcopy(self.packet); packet['files'][0]['path'] = name; packets.append(packet)
        extra = copy.deepcopy(self.packet); extra['files'][0]['unchecked'] = True; packets.append(extra)
        for packet in packets:
            with self.subTest(packet=packet):
                with self.assertRaises(ValueError):
                    self.validate(packet)

    def test_rejects_false_original_and_adapted_identities(self):
        for side in ('before', 'after'):
            for field, value in (('bytes', 1), ('bytes', True), ('sha256', '0' * 64),
                                 ('sha256', 'A' * 64)):
                packet = copy.deepcopy(self.packet); packet['files'][0][side][field] = value
                with self.subTest(side=side, field=field, value=value):
                    with self.assertRaises(ValueError):
                        self.validate(packet)
        packet = copy.deepcopy(self.packet); packet['files'][0]['after'] = packet['files'][0]['before']
        with self.assertRaises(ValueError):
            self.validate(packet, self.original)

    def test_rejects_undeclared_code_data_paths_and_row_reordering(self):
        for index in (1, 2):
            current = copy.deepcopy(self.current); current[index]['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'Undeclared computational change'):
                self.validate(current=current)
        for current in (self.current[:-1], list(reversed(self.current)), self.current + [self.data]):
            with self.assertRaisesRegex(ValueError, 'path/order coverage'):
                self.validate(current=current)

    def test_exact_pdf_relocation_preserves_historical_before_identity(self):
        original_name = 'paper/main.pdf'
        current_name = 'paper/Four-Uniform-Three-Sunflower-Bound.pdf'
        old = row(original_name, b'predecessor pdf')
        new = row(current_name, b'current pdf')
        packet = copy.deepcopy(self.packet)
        packet['relocations'] = {original_name: current_name}
        packet['files'] = [dict(path=original_name,
                               before={k: v for k, v in old.items() if k != 'path'},
                               after={k: v for k, v in new.items() if k != 'path'}, reason='Rename public PDF')]
        with mock.patch.object(repository, 'DOCUMENTARY_PATHS', frozenset([original_name])), \
             mock.patch.object(repository, 'EXPECTED_RELOCATIONS', {original_name: current_name}):
            self.assertEqual(repository.validate_adaptations(packet, [old], [], []), {original_name: new})
            for relocation in ({}, {original_name: 'paper/unreviewed.pdf'},
                               {original_name: current_name, 'another.pdf': current_name},
                               {original_name: current_name, current_name: original_name}):
                bad = copy.deepcopy(packet); bad['relocations'] = relocation
                with self.subTest(relocation=relocation), self.assertRaisesRegex(ValueError, 'relocation'):
                    repository.validate_adaptations(bad, [old], [], [])

    def test_build_exception_does_not_authorize_mathematical_python(self):
        builder = 'scripts/build_pdf.py'
        old = row(builder, b'original builder')
        new = row(builder, b'canonical PDF builder')
        packet = copy.deepcopy(self.packet)
        packet['files'].append(dict(path=builder,
                                    before={k: v for k, v in old.items() if k != 'path'},
                                    after={k: v for k, v in new.items() if k != 'path'},
                                    reason='Only canonical PDF name and TeX jobname'))
        with mock.patch.object(repository, 'BUILD_ADAPTATION_PATHS', frozenset([builder])):
            current = self.current + [new]
            repository.validate_adaptations(packet, self.baseline + [old], self.original + [old], current)
            current = copy.deepcopy(current); current[1]['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'Undeclared computational change'):
                repository.validate_adaptations(packet, self.baseline + [old], self.original + [old], current)
            bad = copy.deepcopy(packet); bad['files'][-1]['path'] = self.code['path']
            with self.assertRaisesRegex(ValueError, 'Unapproved'):
                repository.validate_adaptations(bad, self.baseline + [old], self.original + [old], current)

    def test_sealed_map_and_adapted_bytes_reject_later_changes(self):
        with tempfile.TemporaryDirectory(dir=options.temp_root) as directory:
            root = Path(directory); target = root / 'verification/DOCUMENT_ADAPTATIONS.json'
            target.parent.mkdir(); raw = json.dumps(self.packet).encode('utf8'); target.write_bytes(raw)
            with mock.patch.object(repository, 'DOCUMENT_ADAPTATIONS_SHA256', repository.sha(raw)):
                self.assertEqual(repository.load_document_adaptations(root)[0], self.packet)
                target.write_bytes(raw + b'\n')
                with self.assertRaisesRegex(ValueError, 'manifest pin'):
                    repository.load_document_adaptations(root)
            document = root / self.name; document.parent.mkdir(parents=True)
            document.write_bytes(b'current documentary exposition')
            repository.verify_rows(root, [self.new])
            document.write_bytes(b'other documentary exposition')
            with self.assertRaisesRegex(ValueError, 'Changed input'):
                repository.verify_rows(root, [self.new])
            pointer = repository.LFS_PREFIX + b'\n'
            document.write_bytes(pointer)
            with self.assertRaisesRegex(ValueError, 'LFS pointer'):
                repository.verify_rows(root, [row(self.name, pointer)])

    def test_plan_projection_removes_only_six_source_strings(self):
        original = dict(commands=[dict(id=name, argv=['checker.py'], inputs=['certificate.json'],
                                       cwd='.', timeout_seconds=1,
                                       expected_semantic={'count': 42},
                                       historical_expectation_source={'source': 'old locator', 'sha256': 'a' * 64})
                                  for name in repository.PLAN_SOURCE_IDS])
        current = copy.deepcopy(original)
        for command in current['commands']:
            command['historical_expectation_source']['source'] = 'neutral locator'
        old = repository.canonical(repository.metadata_projection('SUITE_PLAN.json', original))
        self.assertEqual(old, repository.canonical(repository.metadata_projection('SUITE_PLAN.json', current)))
        for field, value in (('argv', ['other.py']), ('inputs', []), ('cwd', 'elsewhere'),
                             ('timeout_seconds', 2), ('expected_semantic', {'count': 42.0})):
            changed = copy.deepcopy(current); changed['commands'][0][field] = value
            self.assertNotEqual(old, repository.canonical(repository.metadata_projection('SUITE_PLAN.json', changed)))
        changed = copy.deepcopy(current)
        changed['commands'][0]['historical_expectation_source']['sha256'] = 'b' * 64
        self.assertNotEqual(old, repository.canonical(repository.metadata_projection('SUITE_PLAN.json', changed)))
        changed['commands'][0]['historical_expectation_source']['source'] = True
        with self.assertRaisesRegex(ValueError, 'source string'):
            repository.metadata_projection('SUITE_PLAN.json', changed)

    def test_provenance_projection_preserves_every_other_field(self):
        name = 'companion/upstream/NO9/PROVENANCE.json'
        original = dict(files=[dict(adaptation_reason='old reason', destination='PROOF.md',
                                    destination_sha256='a' * 64, destination_bytes=42),
                               dict(adaptation_reason=None, destination='certificate.json', destination_bytes=3)])
        changed = copy.deepcopy(original); changed['files'][0]['adaptation_reason'] = 'current reason'
        old = repository.canonical(repository.metadata_projection(name, original))
        self.assertEqual(old, repository.canonical(repository.metadata_projection(name, changed)))
        for index, field, value in ((0, 'destination_sha256', 'b' * 64), (0, 'destination_bytes', True),
                                    (1, 'adaptation_reason', 'unapproved reason')):
            bad = copy.deepcopy(changed); bad['files'][index][field] = value
            self.assertNotEqual(old, repository.canonical(repository.metadata_projection(name, bad)))


class ReleaseRootControls(unittest.TestCase):
    def test_actual_sealed_root_map_and_baseline_pins(self):
        result = repository.check_repository(ROOT)
        self.assertEqual(result['status'], 'PASS_REPOSITORY_INTEGRITY')
        self.assertEqual(result['adapted_baseline_documents'], 30)
        self.assertEqual(result['adapted_baseline_build_tools'], 1)
        self.assertEqual(result['relocated_baseline_files'], 1)
        self.assertFalse((ROOT / 'paper/main.pdf').exists())
        packet, _ = repository.load_document_adaptations(ROOT)
        self.assertEqual(packet['relocations'], repository.EXPECTED_RELOCATIONS)
        old = next(r for r in packet['files'] if r['path'] == 'paper/main.pdf')
        self.assertEqual(old['before']['sha256'], '65f6b24c2c63253b57ed13b25b37271c9bcac2700457f3d44c9676cf5b0d41a7')

    def test_old_pdf_duplicate_rejected_even_when_listed_in_current_manifest(self):
        with tempfile.TemporaryDirectory(dir=options.temp_root) as directory:
            root = Path(directory); (root / 'paper').mkdir()
            files = []
            for name in ('paper/main.pdf', 'paper/Four-Uniform-Three-Sunflower-Bound.pdf'):
                raw = name.encode('utf8'); (root / name).write_bytes(raw); files.append(row(name, raw))
            packet = dict(schema='BOUND68_STANDALONE_PAYLOAD_V1', files=files)
            (root / 'MANIFEST_SHA256.json').write_text(json.dumps(packet), encoding='utf8')
            with self.assertRaisesRegex(ValueError, 'Old relocated artifact'):
                repository.check_repository(root)


if __name__ == '__main__':
    unittest.main()
