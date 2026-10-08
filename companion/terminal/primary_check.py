"""Small, exact self-checks for the manuscript's explicit finite identities."""
from itertools import combinations, permutations
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sunflower(a, b, c):
    return a & b == a & c == b & c


def sf_free(family):
    return not any(sunflower(*triple) for triple in combinations(family, 3))


def q8(hubs, triad, leaves):
    return tuple(frozenset((h, *pair)) for h in hubs for pair in combinations(triad, 2)) + tuple(
        frozenset((*hubs, leaf)) for leaf in leaves
    )


def transversals(family, size=2, omitted=None):
    support = sorted(set().union(*family))
    return tuple(frozenset(pair) for pair in combinations(support, size)
                 if (omitted is None or not frozenset(pair) & omitted)
                 and all(frozenset(pair) & member for member in family if member != omitted))


def main():
    p10 = tuple(frozenset(map(int, block)) for block in
                ('012', '015', '023', '034', '045', '124', '134', '135', '235', '245'))
    need(sf_free(p10) and all(a & b for a, b in combinations(p10, 2)), 'P10 properties')
    pstar = tuple(member for member in p10 if member not in (frozenset((0, 1, 2)), frozenset((0, 1, 5))))
    q = q8((0, 1), (2, 3, 4), (5, 6))
    need(sf_free(q) and all(a & b for a, b in combinations(q, 2)), 'Q8 properties')
    expected_p = {'023': ['45'], '034': [], '045': ['23'], '124': ['35'],
                  '134': [], '135': ['24'], '235': [], '245': []}
    expected_q = {'023': ['14'], '024': ['13'], '034': ['12'], '123': ['04'],
                  '124': ['03'], '134': ['02'], '015': [], '016': []}
    def label(member):
        return ''.join(map(str, sorted(member)))
    def table(family):
        return {label(member): sorted(label(pair) for pair in transversals(family, omitted=member))
                for member in family}
    need(table(pstar) == expected_p and table(q) == expected_q, 'Exact quasi-transversal tables')
    need(transversals(pstar) == (frozenset((3, 4)),), 'Pstar unique cover')
    need(transversals(q) == (frozenset((0, 1)),), 'Q8 unique cover')
    covered = []
    for omitted in combinations(p10, 2):
        remainder = tuple(member for member in p10 if member not in omitted)
        if transversals(remainder):
            covered.append(frozenset(remainder))
            need(len(omitted[0] & omitted[1]) == 2, 'Omitted blocks intersect in two')
    need(len(covered) == 15, '15 eligible P8 among 45')
    automorphisms = [perm for perm in permutations(range(6))
                     if {frozenset(perm[x] for x in member) for member in p10} == set(p10)]
    need(len(automorphisms) == 60, 'P10 automorphism count')
    orbit = {frozenset(frozenset(perm[x] for x in member) for member in pstar)
             for perm in automorphisms}
    need(orbit == set(covered), 'Complete 15-model orbit')

    def shift(family, offset):
        return tuple(frozenset(x + offset for x in member) for member in family)
    models = [pstar + shift(pstar, 6), pstar + shift(q, 6)]
    for shared in range(3):
        leaves = ((12, 13), (5, 12), (5, 6))[shared]
        models.append(q + q8((7, 8), (9, 10, 11), leaves))
    cases = nonempty = 0
    for family in models:
        need(len(set(family)) == 16 and sf_free(family), 'Separated 16-link properties')
        need(len(transversals(family, size=4)) == 1, 'Unique four-cover')
        for omitted in family:
            result = transversals(family, size=4, omitted=omitted)
            need(len(result) <= 1, 'At most one quasi-four-cover')
            cases += 1
            nonempty += bool(result)
    need((cases, nonempty) == (80, 54), 'Five-model table counts')

    groups = (range(3), range(3, 6), range(6, 9))
    d27 = tuple(frozenset((*left, *right)) for i, j in combinations(range(3), 2)
                for left in combinations(groups[i], 2) for right in combinations(groups[j], 2))
    f54 = d27 + shift(d27, 9)
    need(len(set(f54)) == 54 and sf_free(f54), 'Explicit lower construction')
    positive = q8((0, 1), (2, 3, 4), (5, 6)) + q8((5, 6), (7, 8, 9), (0, 1))
    need(sf_free(positive) and len(transversals(positive, size=4)) == 7, 'Positive R16 guard')
    need(all(sum(not member & other for other in positive) <= 7 for member in positive),
         'Positive R16 disjoint-count definition')
    print(json.dumps(dict(status='PASS',scope='explicit construction and transversal identities only',
                         lower54_triples=24804,P8_omission_pairs=45,P8_coverable_models=15,
                         P10_automorphisms=60,separated_link_cases=cases,
                         nonempty_quasi_transversal_cases=nonempty,positive_R16_transversals=7,
                         F69_families_enumerated=0,F68_families_enumerated=0),sort_keys=True))


if __name__ == '__main__':
    main()
