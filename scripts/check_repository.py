"""Check distribution bytes and declared coverage; this is not a mathematical review."""
from pathlib import Path, PurePosixPath
import argparse
import copy
import hashlib
import json
import os
import stat

ROOT = Path(__file__).absolute().parents[1]
BASELINE_SHA256 = '16fb15948d631cd1abb25e276b3476516161feb8151594b829a23ecab923f6c1'
BASELINE_COMPUTATIONAL_SHA256 = 'f8cb8594e3138f38397804542a98f2d5611edcd4605fd3080da9478a78681b16'
COMPUTATIONAL_SHA256 = 'ecc54817e8e81242a59ef6b033e74e472d3ffbb3e80f9f0d9f0e8264acf40b18'
DOCUMENT_ADAPTATIONS_SHA256 = '309ccf38ffc66302047edab219565677b710277cc13b8b4894efb34f609db591'
EXPECTED_RELOCATIONS = {'paper/main.pdf': 'paper/Four-Uniform-Three-Sunflower-Bound.pdf'}
BUILD_ADAPTATION_PATHS = frozenset(('scripts/build_pdf.py',))
DOCUMENTARY_PATHS = frozenset(('SUITE_PLAN.json', 'companion/upstream/D17/CURRENT_PREMISES.md', 'companion/upstream/D17/PROOF.md', 'companion/upstream/D17/PROVENANCE.json', 'companion/upstream/D17/UNIVERSAL_EXTENSION_LEMMAS.md', 'companion/upstream/D18_P10/PROOF.md', 'companion/upstream/D18_P10/README.md', 'companion/upstream/D18_R99/PROOF.md', 'companion/upstream/D18_R99/README.md', 'companion/upstream/D19/PROOF.md', 'companion/upstream/D19/README.md', 'companion/upstream/D20/PROOF.md', 'companion/upstream/D20/README.md', 'companion/upstream/LOW15/CURRENT_PREMISES.md', 'companion/upstream/LOW15/PROOF.md', 'companion/upstream/LOW15/PROVENANCE.json', 'companion/upstream/MU42/C5_PROOF.md', 'companion/upstream/MU42/PROOF.md', 'companion/upstream/MU42/README.md', 'companion/upstream/MU42/TRACE_FOUNDATIONS.md', 'companion/upstream/NO45/CURRENT_PREMISES.md', 'companion/upstream/NO45/PROOF.md', 'companion/upstream/NO45/PROVENANCE.json', 'companion/upstream/NO9/CURRENT_PREMISES.md', 'companion/upstream/NO9/PROOF.md', 'companion/upstream/NO9/PROVENANCE.json', 'paper/main.pdf', 'paper/main.tex', 'proof/DEPENDENCIES.md'))
PLAN_SOURCE_IDS = ('terminal.cap61', 'terminal.cross15', 'terminal.crowding',
                   'terminal.f69_bridge', 'terminal.primary', 'terminal.r16')
PROVENANCE_REASON_INDICES = {
    'companion/upstream/D17/PROVENANCE.json': (0, 974),
    'companion/upstream/LOW15/PROVENANCE.json': (0,),
    'companion/upstream/NO45/PROVENANCE.json': (0,),
    'companion/upstream/NO9/PROVENANCE.json': (0,),
}
METADATA_PROJECTION_SHA256 = {'SUITE_PLAN.json': 'ecbf080db0e20ae017f4d87d4b476c9b346b7c60d2b088f865d2f24fa1151806', 'companion/upstream/D17/PROVENANCE.json': 'd38dae2a2662be4c027715ed29911bfc7e991818095ceba0b8efbf84c542acdd', 'companion/upstream/LOW15/PROVENANCE.json': '0a6233e8c800f2a917a22f01c40aa62b094c5d86618f7179fbfeb456caed90c2', 'companion/upstream/NO45/PROVENANCE.json': '0dc032b96266ef4993f3e042fd86a46f7bd80e254311af38c6690ab0ae3bcb5e', 'companion/upstream/NO9/PROVENANCE.json': '976847df4ac845456dae5cf783fc986f5d5c2e0398708b440c8df139fb6a3598'}
DOCUMENTARY_PATHS = DOCUMENTARY_PATHS | {'THIRD_PARTY_NOTICES.md'}
MUTABLE_METADATA = {'.gitattributes', 'CITATION.cff', 'README.md', 'REPRODUCE.md'}
LFS_PREFIX = b'version https://git-lfs.github.com/spec/v1'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def reject_links(path):
    """Check lexical ancestors before resolve follows any link or junction."""
    absolute = Path(os.path.abspath(path))
    for part in reversed((absolute, *absolute.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        need(not stat.S_ISLNK(info.st_mode) and not
             (getattr(info, 'st_file_attributes', 0) &
              getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)),
             'Symlink/reparse path: ' + str(part))


def safe_path(root, name):
    need(isinstance(name, str) and bool(name), 'Invalid manifest path')
    parts = name.split('/')
    need('\\' not in name and ':' not in name and
         all(p not in ('', '.', '..') for p in parts) and
         not PurePosixPath(name).is_absolute(), 'Escaping/noncanonical path: ' + name)
    root = Path(os.path.abspath(root))
    path = root.joinpath(*parts)
    reject_links(path)
    need(path.resolve().is_relative_to(root.resolve()), 'Escaping path: ' + name)
    return path


def manifest_rows(packet, schema, count=None):
    need(isinstance(packet, dict) and packet.get('schema') == schema, 'Manifest schema')
    rows = packet.get('files')
    need(isinstance(rows, list), 'Manifest rows')
    if count is not None:
        need(len(rows) == count, 'Manifest row count')
    seen = set()
    for row in rows:
        need(isinstance(row, dict), 'Invalid manifest row')
        name = row.get('path')
        # Validate syntax even before opening the path.
        need(isinstance(name, str) and name not in seen, 'Duplicate/invalid manifest path')
        seen.add(name)
        need(type(row.get('bytes')) is int and row['bytes'] >= 0, 'Invalid byte count: ' + name)
        digest = row.get('sha256')
        need(isinstance(digest, str) and len(digest) == 64 and
             all(c in '0123456789abcdef' for c in digest), 'Invalid SHA256: ' + name)
    return rows


def verify_rows(root, rows):
    for row in rows:
        path = safe_path(root, row['path'])
        need(path.is_file(), 'Missing input: ' + row['path'])
        raw = path.read_bytes()
        need(not raw.startswith(LFS_PREFIX), 'Raw Git LFS pointer: ' + row['path'])
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'],
             'Changed input: ' + row['path'])


def distribution_files(root):
    root = Path(os.path.abspath(root))
    reject_links(root)
    found = set()
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                name = path.relative_to(root).as_posix()
                if path.parent == root and path.name == '.git':
                    continue
                reject_links(path)
                if path.parent == root and path.name in ('build', 'inputs'):
                    need(entry.is_dir(follow_symlinks=False), 'Reserved generated-root path must be a directory: ' + name)
                    continue
                if entry.is_dir(follow_symlinks=False):
                    walk(path)
                elif entry.is_file(follow_symlinks=False):
                    if name == 'MANIFEST_SHA256.json':
                        continue
                    if path.suffix == '.pyc' and '__pycache__' in path.relative_to(root).parts:
                        continue
                    found.add(name)
                else:
                    raise ValueError('Non-regular distribution entry: ' + name)
    walk(root)
    return found


def validate_plan(plan):
    need(plan.get('schema') == 'BOUND68_COMPLETE_PLAN_V1', 'Plan schema')
    commands = plan.get('commands', [])
    need(plan.get('suite_count') == 42 and len(commands) == 42 and
         len({s['id'] for s in commands}) == 42, 'Plan suite coverage')
    blocks = plan.get('upstream_blocks', [])
    need(len(blocks) == 9 and len(set(blocks)) == 9, 'Plan upstream coverage')
    need(plan.get('quick_ids') == ['terminal.f69_bridge', 'terminal.primary'], 'Quick suite coverage')
    return plan


def canonical(data):
    """Typed JSON identity: booleans and integers have distinct encodings."""
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf8')


def metadata_projection(name, packet):
    """Remove only the eleven explicitly identified documentary string fields."""
    result = copy.deepcopy(packet)
    if name == 'SUITE_PLAN.json':
        commands = result.get('commands', [])
        for suite_id in PLAN_SOURCE_IDS:
            matches = [s for s in commands if s.get('id') == suite_id]
            need(len(matches) == 1, 'Metadata projection suite identity: ' + suite_id)
            source = matches[0]['historical_expectation_source']
            need(isinstance(source.get('source'), str), 'Metadata source string: ' + suite_id)
            del source['source']
    else:
        need(name in PROVENANCE_REASON_INDICES, 'Unapproved metadata projection: ' + name)
        for index in PROVENANCE_REASON_INDICES[name]:
            row = result['files'][index]
            need(isinstance(row.get('adaptation_reason'), str), 'Metadata reason string: ' + name)
            del row['adaptation_reason']
    return result


def identity(name, detail):
    need(isinstance(detail, dict) and set(detail) == {'bytes', 'sha256'},
         'Document identity fields: ' + name)
    row = dict(path=name, **detail)
    manifest_rows(dict(schema='identity', files=[row]), 'identity')
    return row


def validate_adaptations(packet, baseline, original_computational, current_computational):
    """Authorize exact before/after identities; never grant a path or suffix bypass."""
    need(isinstance(packet, dict) and set(packet) == {
        'schema', 'reviewed_distribution_manifest_sha256', 'baseline_manifest_sha256',
        'baseline_computational_manifest_sha256', 'current_computational_manifest_sha256', 'relocations', 'files'},
        'Document adaptation fields')
    need(packet['schema'] == 'BOUND68_DOCUMENT_ADAPTATIONS_V2', 'Document adaptation schema')
    relocations = packet['relocations']
    need(isinstance(relocations, dict) and relocations == EXPECTED_RELOCATIONS,
         'Exact document relocation coverage')
    need(len(set(relocations.values())) == len(relocations) and
         not set(relocations) & set(relocations.values()), 'Duplicate/cyclic document relocation')
    need(packet['reviewed_distribution_manifest_sha256'] ==
         'bedf670dd173ecccc6247c44d4f74cb359f771c9c8c44c8c5b2ed404a2c2d2d5' and
         packet['baseline_manifest_sha256'] == BASELINE_SHA256 and
         packet['baseline_computational_manifest_sha256'] == BASELINE_COMPUTATIONAL_SHA256 and
         packet['current_computational_manifest_sha256'] == COMPUTATIONAL_SHA256,
         'Document adaptation source/current pins')
    files = packet['files']
    need(isinstance(files, list), 'Document adaptation rows')
    before = {r['path']: r for r in baseline}
    old_inputs = {r['path']: r for r in original_computational}
    new_inputs = {r['path']: r for r in current_computational}
    need([relocations.get(r['path'], r['path']) for r in original_computational] ==
         [r['path'] for r in current_computational], 'Computational path/order coverage')
    changed = {}
    for entry in files:
        need(isinstance(entry, dict) and set(entry) == {'path', 'before', 'after', 'reason'},
             'Document adaptation row fields')
        name = entry['path']
        need(isinstance(name, str) and name in DOCUMENTARY_PATHS | BUILD_ADAPTATION_PATHS and name not in changed,
             'Unapproved/duplicate document adaptation path')
        need(isinstance(entry['reason'], str) and bool(entry['reason']), 'Document adaptation reason')
        old = identity(name, entry['before'])
        current_name = relocations.get(name, name)
        new = identity(current_name, entry['after'])
        need(old == before.get(name), 'Document adaptation original identity: ' + name)
        need(canonical(old) != canonical(new), 'Unchanged document adaptation: ' + name)
        if name in old_inputs:
            need(old == old_inputs[name] and new == new_inputs[current_name],
                 'Document adaptation computational identities: ' + name)
        changed[name] = new
    need(set(changed) == DOCUMENTARY_PATHS | BUILD_ADAPTATION_PATHS, 'Exact document/build adaptation coverage')
    need(set(relocations) <= set(changed), 'Unrecorded document relocation')
    for name, old in old_inputs.items():
        need(canonical(new_inputs[relocations.get(name, name)]) == canonical(changed.get(name, old)),
             'Undeclared computational change: ' + name)
    return changed


def load_document_adaptations(root):
    raw = safe_path(root, 'verification/DOCUMENT_ADAPTATIONS.json').read_bytes()
    need(sha(raw) == DOCUMENT_ADAPTATIONS_SHA256, 'Document adaptation manifest pin')
    return json.loads(raw), sha(raw)


def check_repository(root=ROOT):
    root = Path(os.path.abspath(root))
    raw = safe_path(root, 'MANIFEST_SHA256.json').read_bytes()
    distribution = manifest_rows(json.loads(raw), 'BOUND68_STANDALONE_PAYLOAD_V1')
    need({r['path'] for r in distribution} == distribution_files(root),
         'Distribution closed allowlist mismatch')
    need(not set(EXPECTED_RELOCATIONS) & {r['path'] for r in distribution},
         'Old relocated artifact remains in distribution')
    verify_rows(root, distribution)
    baseline_raw = safe_path(root, 'verification/BASELINE_MANIFEST_SHA256.json').read_bytes()
    need(sha(baseline_raw) == BASELINE_SHA256, 'Baseline manifest pin')
    baseline = manifest_rows(json.loads(baseline_raw), 'BOUND68_READER_PAYLOAD_V1', 1704)
    need(MUTABLE_METADATA <= {r['path'] for r in baseline}, 'Baseline metadata coverage')
    original_raw = safe_path(root, 'verification/BASELINE_COMPUTATIONAL_MANIFEST.json').read_bytes()
    need(sha(original_raw) == BASELINE_COMPUTATIONAL_SHA256, 'Original computational manifest pin')
    original_computational = manifest_rows(json.loads(original_raw), 'BOUND68_COMPUTATIONAL_MANIFEST_V1', 1692)
    computational_raw = safe_path(root, 'COMPUTATIONAL_MANIFEST.json').read_bytes()
    need(sha(computational_raw) == COMPUTATIONAL_SHA256, 'Computational manifest pin')
    computational = manifest_rows(json.loads(computational_raw), 'BOUND68_COMPUTATIONAL_MANIFEST_V1', 1692)
    adaptations, adaptation_sha256 = load_document_adaptations(root)
    changed = validate_adaptations(adaptations, baseline, original_computational, computational)
    original_manifest_row = next((r for r in baseline if r['path'] == 'COMPUTATIONAL_MANIFEST.json'), None)
    need(original_manifest_row == dict(path='COMPUTATIONAL_MANIFEST.json', bytes=len(original_raw),
                                      sha256=sha(original_raw)), 'Baseline computational manifest identity')
    preserved = [r for r in baseline if r['path'] not in MUTABLE_METADATA | set(changed) |
                 {'COMPUTATIONAL_MANIFEST.json'}]
    need(len(preserved) == len(baseline) - len(MUTABLE_METADATA) - len(changed) - 1,
         'Baseline preserved coverage')
    verify_rows(root, preserved)
    verify_rows(root, list(changed.values()))
    verify_rows(root, computational)
    need(set(METADATA_PROJECTION_SHA256) == {'SUITE_PLAN.json'} | set(PROVENANCE_REASON_INDICES),
         'Metadata projection policy coverage')
    for name, expected in METADATA_PROJECTION_SHA256.items():
        data = json.loads(safe_path(root, name).read_bytes())
        need(sha(canonical(metadata_projection(name, data))) == expected,
             'Changed retained metadata/plan fields: ' + name)
    plan = validate_plan(json.loads(safe_path(root, 'SUITE_PLAN.json').read_bytes()))
    return dict(status='PASS_REPOSITORY_INTEGRITY', distribution_files=len(distribution),
                immutable_baseline_files=len(preserved), baseline_files=len(baseline),
                adapted_baseline_documents=len(DOCUMENTARY_PATHS),
                adapted_baseline_build_tools=len(BUILD_ADAPTATION_PATHS),
                relocated_baseline_files=len(adaptations['relocations']), adapted_manifest_bookkeeping_files=1,
                computational_files=len(computational),
                unchanged_computational_files=len(computational) - len(set(changed) & {r['path'] for r in computational}),
                adapted_computational_documents=len(DOCUMENTARY_PATHS & {r['path'] for r in computational}),
                adapted_computational_build_tools=len(BUILD_ADAPTATION_PATHS & {r['path'] for r in computational}),
                suite_count=plan['suite_count'], upstream_blocks=len(plan['upstream_blocks']),
                distribution_manifest_sha256=sha(raw), computational_manifest_sha256=sha(computational_raw),
                baseline_computational_manifest_sha256=sha(original_raw),
                document_adaptations_sha256=adaptation_sha256,
                scope='Byte identity and declared coverage; not mathematics, novelty or authentication')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(ROOT))
    args = parser.parse_args()
    try:
        result = check_repository(args.root)
    except Exception as exc:
        print(json.dumps(dict(status='FAIL_REPOSITORY_INTEGRITY', error=str(exc))))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
