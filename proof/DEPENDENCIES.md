# Mathematical dependency map

The proof concerns finite simple four-uniform families with no three-sunflower, including the empty kernel. M(4,3) is the maximum free cardinality. The nine preliminary blocks use their declared actual-anchor domains at μ ≥ 42; their source-to-model reductions, symmetry normalization and pruning arguments are part of the proof.

The logical order is acyclic: ordinary graph/triple foundations → universal R16 classification and maximality → high-link alternatives → trace foundations and C5 → neighbourhood bootstrap → maximum-degree exclusions → singleton/neighbourhood exclusions → fibre bridge → application of local R61 → contradiction at 69.

R61 has its own local proof from ordinary foundations, R16, cross-intersecting stars and crowding; it does not require the global degree-exclusion conclusion. Applying it at the end creates no reverse dependency.

## Ordinary premises and source replacements

| Required statement | Actual proof available to the reader |
|---|---|
| SF2 capacities and global point/pair/triple caps 20/6/2 | Paper §3, lem:sf2, prop:i810 and cor:triple20 |
| Intersecting triple models I8/I9/I10, with arbitrary I7 | Paper §3, prop:i810; no classification of an arbitrary I7 is assumed |
| P10/P9 isolation and B4 separation at eight disjoint triples | Paper lem:isolation and lem:b4 |
| High-link forms at degrees 17–20; degree-six hubs in R16 | Paper thm:r16class and lem:r16maximal, derived on arbitrary support |
| Exact extension-point equality/distinction, all five trace margins 12/14/17/19/22, at most two high points in an anchor | [Complete trace foundations](../companion/upstream/MU42/TRACE_FOUNDATIONS.md), §§D/E |
| Separate C5 obstruction and its local corollary | [C5 proof](../companion/upstream/MU42/C5_PROOF.md), MU42.check_c5 and its binary certificate |
| C5/P5 cone confinement and the 5h+9b ≤ 59 resource bound | [Degree-17 universal extension lemmas](../companion/upstream/D17/UNIVERSAL_EXTENSION_LEMMAS.md), with SF2/I8/isolation |
| Bootstrap k ≥ 7 for singleton sizes 9/10, minimum used degree four, support range at 69 | Paper prop:bootstrap42 and MU42 complete suite |
| Both degree-17 cores and applicability at 17/42 | [Degree-17 proof](../companion/upstream/D17/PROOF.md), §§2.2–2.3, check_p10_bridge, ALL15 and ONE14 |
| The 77 local degree-16 exclusions used by NO9 | NO9 proof and inherited checker; separately checked local domain, not transfer of the degree-17 theorem |
| Actual intersection guards for all seven H27 pools | [Neighbourhood exclusion proof](../companion/upstream/NO45/PROOF.md), §3.1 |
| Jin's strict theorem and deletion maps | Paper §2 and §§6–7; Nikiforov Theorem A; displayed cyclic maps |
| Cross-intersecting actual tails with external centres | Paper §8, all three crowding regimes and explicit cross-star guard |

The separate C5 lemma and both D17 cores are indispensable premises. Provenance identifiers identify source records; the proof and execution inputs are the linked reductions and files bound by the computational manifest.

## Preliminary finite blocks

Each linked proof gives the necessary model, full normalized domain, complete root cover and sound closing rules. Exact suite identifiers below resolve in SUITE_PLAN.json. Inputs are bound by COMPUTATIONAL_MANIFEST.json. The parent verifier requires every named suite in both modes.


### MU42: Neighbourhood bootstrap and separate C5

[Written proof](../companion/upstream/MU42/PROOF.md).

- `MU42.check_bootstrap42`: `companion/upstream/MU42/scripts/check_bootstrap42.py`.
- `MU42.check_c5`: `companion/upstream/MU42/scripts/check_c5.py`.
- `MU42.check_domain42`: `companion/upstream/MU42/scripts/check_domain42.py`.
- `MU42.check_projections42`: `companion/upstream/MU42/scripts/check_projections42.py`.
- `MU42.check_scope42`: `companion/upstream/MU42/scripts/check_scope42.py`.
- `MU42.check_small42`: `companion/upstream/MU42/scripts/check_small42.py`.

### D20: Maximum degree twenty

[Written proof](../companion/upstream/D20/PROOF.md).

- `D20.check_controls`: `companion/upstream/D20/scripts/check_controls.py`.
- `D20.check_cover_lemma`: `companion/upstream/D20/scripts/check_cover_lemma.py`.
- `D20.check_geometry`: `companion/upstream/D20/scripts/check_geometry.py`.
- `D20.check_linear`: `companion/upstream/D20/scripts/check_linear.py`.
- `D20.check_scope`: `companion/upstream/D20/scripts/check_scope.py`.

### D19: Maximum degree nineteen

[Written proof](../companion/upstream/D19/PROOF.md).

- `D19.check_controls`: `companion/upstream/D19/scripts/check_controls.py`.
- `D19.check_extended_cover`: `companion/upstream/D19/scripts/check_extended_cover.py`.
- `D19.check_geometry`: `companion/upstream/D19/scripts/check_geometry.py`.
- `D19.check_linear`: `companion/upstream/D19/scripts/check_linear.py`.
- `D19.check_scope`: `companion/upstream/D19/scripts/check_scope.py`.

### D18_P10: Degree eighteen with a P10 component

[Written proof](../companion/upstream/D18_P10/PROOF.md).

- `D18_P10.check_catalogues`: `companion/upstream/D18_P10/scripts/check_catalogues.py`.
- `D18_P10.check_forest`: `companion/upstream/D18_P10/scripts/check_forest.py`.
- `D18_P10.check_geometry`: `companion/upstream/D18_P10/scripts/check_geometry.py`.
- `D18_P10.check_linear`: `companion/upstream/D18_P10/scripts/check_linear.py`.
- `D18_P10.check_scope`: `companion/upstream/D18_P10/scripts/check_scope.py`.

### D18_R99: Degree eighteen with two P9 components

[Written proof](../companion/upstream/D18_R99/PROOF.md).

- `D18_R99.check_catalogues`: `companion/upstream/D18_R99/scripts/check_catalogues.py`.
- `D18_R99.check_geometry`: `companion/upstream/D18_R99/scripts/check_geometry.py`.
- `D18_R99.check_models`: `companion/upstream/D18_R99/scripts/check_models.py`.
- `D18_R99.check_next_domain`: `companion/upstream/D18_R99/scripts/check_next_domain.py`.
- `D18_R99.check_scope`: `companion/upstream/D18_R99/scripts/check_scope.py`.

### D17: Maximum degree seventeen and transported cores

[Written proof](../companion/upstream/D17/PROOF.md).

- `d17_forests`: `companion/upstream/D17/scripts/check_forests.py`.
- `d17_linear`: `companion/upstream/D17/scripts/check_linear.py`.
- `d17_p10_bridge`: `companion/upstream/D17/scripts/check_p10_bridge.py`.

### LOW15: Maximum degree at most fifteen; separately guarded degree-sixteen bonus

[Written proof](../companion/upstream/LOW15/PROOF.md).

- `low15_graph`: `companion/upstream/LOW15/scripts/check_graph.py`.
- `low15_math`: `companion/upstream/LOW15/scripts/check_math.py`.

### NO9: No singleton nine at maximum degree sixteen

[Written proof](../companion/upstream/NO9/PROOF.md).

- `no9_domain`: `companion/upstream/NO9/scripts/check_domain.py`.
- `no9_forests`: `companion/upstream/NO9/scripts/check_forests.py`.
- `no9_inherited`: `companion/upstream/NO9/scripts/check_inherited.py`.

### NO45: Closed neighbourhoods cannot reach forty-five

[Written proof](../companion/upstream/NO45/PROOF.md).

- `no45_certificates`: `companion/upstream/NO45/scripts/check_certificates.py`.
- `no45_cores`: `companion/upstream/NO45/scripts/check_cores.py`.

## Final structural checks

The paper contains the ordinary reductions for R16, maximality, near-covers, the fibre census and local R61. The lower construction is classical.

- `terminal.cap61`: `companion/terminal/cap61/src/verify.py`.
- `terminal.cross15`: `companion/terminal/cross15/src/verify.py`.
- `terminal.crowding`: `companion/terminal/crowding/code/verify.py`.
- `terminal.f69_bridge`: `companion/terminal/check_f69_bridge.py`.
- `terminal.primary`: `companion/terminal/primary_check.py`.
- `terminal.r16`: `companion/terminal/r16/src/verify.py`.

A complete PASS checks these named finite objects. It does not re-execute H27, prove written reductions by software, certify novelty or constitute external human review.
