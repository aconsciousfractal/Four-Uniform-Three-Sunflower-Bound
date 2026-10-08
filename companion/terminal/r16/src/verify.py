"""Replay all current finite proof certificates, with bounded mutation tests."""
from __future__ import annotations
from pathlib import Path
import json,gzip,copy,argparse
import check_seven,check_r16,check_structural
ROOT=Path(__file__).resolve().parents[1]
CONTRACT={'R16_size':16,'R16_disjoint_cap':7,'I7_support_cap':7,'global_gate':'all used points degree16 AND every singleton of every anchor at most7','global67_proved':False,'formalized':False}

def rejected_mutations(seven,trees):
    rejected=[]
    def test(name,source,change,checker):
        c=copy.deepcopy(source);change(c)
        try:checker(c)
        except (check_seven.Invalid,check_r16.Invalid,KeyError,IndexError,TypeError,ValueError):rejected.append(name);return
        raise ValueError('accepted mutation: '+name)
    test('missing_seven_type',seven,lambda d:d['rows'].pop(),check_seven.verify)
    test('wrong_orbit_size',seven,lambda d:d['rows'][0].__setitem__('labelled_count',121),check_seven.verify)
    test('missing_mixed_trace',seven,lambda d:d['rows'][0]['mixed_allowed'].pop(),check_seven.verify)
    test('false_mixed_witness',seven,lambda d:d['rows'][0]['mixed_forbidden'][0].__setitem__('witness',[0,0]),check_seven.verify)
    test('duplicate_catalogue_root',seven,lambda d:d['rows'].__setitem__(1,copy.deepcopy(d['rows'][0])),check_seven.verify)
    t=trees[0]
    test('lower_target_to_15',t,lambda d:d.__setitem__('target',15),check_r16.check_tree)
    test('raise_disjoint_cap_to_7',t,lambda d:d.__setitem__('disjoint_cap',7),check_r16.check_tree)
    test('raise_minimum_degree_to_4',t,lambda d:d.__setitem__('minimum_used_degree',4),check_r16.check_tree)
    test('reduce_support_cap_to_10',t,lambda d:d.__setitem__('n',10),check_r16.check_tree)
    test('delete_seed_block',t,lambda d:d['seed'].pop(),check_r16.check_tree)
    test('delete_root_branch',t,lambda d:d['nodes'][0]['children'].pop(),check_r16.check_tree)
    test('delete_candidate_from_cover',t,lambda d:d['nodes'][0]['classes'][0].pop(),check_r16.check_tree)
    test('false_count_at_root',t,lambda d:d['nodes'].__setitem__(0,{'end':'count'}),check_r16.check_tree)
    test('cyclic_child',t,lambda d:d['nodes'][0]['children'].__setitem__(0,0),check_r16.check_tree)
    test('orphan_record',t,lambda d:d['nodes'].append({'end':'count'}),check_r16.check_tree)
    return {'rejected':len(rejected),'names':rejected}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-mutations',action='store_true');a=ap.parse_args()
    seven=json.loads((ROOT/'results/seven_certificate.json').read_text());trees=json.loads(gzip.decompress((ROOT/'results/r16_mu10_certificate.json.gz').read_bytes()))
    if trees.get('format')!='E20_R16_mu10_proof_v1' or [t['kind'] for t in trees['trees']]!=['two_triangles','cycle5','triangle_path']:raise ValueError('incomplete root cover')
    out={'status':'PASS','contract':CONTRACT,'seven':check_seven.verify(seven),'R16_low_disjoint':[check_r16.check_tree(t) for t in trees['trees']],'structural_checks':check_structural.verify(),'projection_limit':check_structural.check_projection()}
    if not a.skip_mutations:out['mutations']=rejected_mutations(seven,trees['trees'])
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
