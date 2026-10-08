# Isolated P9 exclusion at degree16 and the post-exclusion domain

Premises: SF4, mu>=42, global cap16, an actual isolated P9 in a degree16 link, bootstrap minimum4, universal trace rules and C5. R42.7 forces k=7 when singleton9 occurs; its actual P9 support is disjoint from the other seven triples. This is a centre16 domain, not an automatic reuse of a cap17 predicate. No exterior support bound, Jin, H27 or M=69 is imposed inside these local trace systems.

check_inherited.py reconstructs every one of373 labelled interior assignments/79 orbits with two constructors and checks77 exact LP certificates. The75 immediate exclusions and two nontrivial exclusions leave precisely P9_000 and P9_004, corresponding to four labelled assignments. Two rational points are positive checks of that intermediate relaxation, not actual quadruple families.

check_forests.py closes those residual roots using11 empty-interior and49 internal-interior canonical profiles; all60 forests are supplied. Their30/82 labelled profiles and261/483 anchor rows are rebuilt;41026 prefix projections and22777 closed refutation leaves are consumed, with no open/disabled leaves. shared exterior identities are retained.

check_domain.py then generates the entire post-singleton9 domain twice, comparing all24002 ordered rows byte for byte,71 degree profiles and all four42..45 strata. The minimum used degree8 in this domain belongs to the F69/cap16/mu42 branch and is not transferred to F68. The pointwise support estimate18..21 is only an auxiliary necessary bound; the current graph reduction later strengthens it through the current proof.

PROOF.md §§1-3 supplies necessity, normalizations and pruning. After NO45 the proof applies Jin k4 and reconstructs the A3/A4 fibre profiles in the terminal.

The ambient object is a finite simple family of four-element sets with no three distinct members whose three pairwise intersections coincide; the empty common intersection is forbidden too. N[R] includes R and all members meeting R, and mu=min_R |N[R]|. Point degrees count actual family members. The theorem being composed is 54 <= M(4,3) <= 68 conditional on H27 and the stated mathematical imports; this directory makes no claim of 67.

The proof first establishes universal R16 classification and maximality, which supply the high-link alternatives and the R16/max5 input where used. The separate C5-empty theorem is checked in the MU42/C5 suite. Elementary codegree caps20/6/2, B4, signature/trace bounds and bootstrap R42.7/N42.7 with minimum used degree4 are proved premises. Their locations are given in the [mathematical dependency map](../../../proof/DEPENDENCIES.md).

SUITE_PLAN.json specifies exact expected semantic objects. The unified runner executes the listed commands in both modes and rejects any status/counter/record mismatch. Exact integer arithmetic and explicit exceptions remain active under -O. Recorded verification and a fresh replay are distinguished in [REPRODUCE.md](../../../REPRODUCE.md); integrity is distinct from mathematical coverage.

## Premises and locations

| Label or application | Premise and location | Role |
|---|---|---|
| E17/E18/C1 and universal high-link shapes | Reader paper: R16 classification followed by maximality and the ordinary high-link reductions | Supplies complete alternatives at degrees17..20 |
| R16/max5 | Reader paper: complete16-link classification and the ordinary maximum-degree-five argument | Supplies the required ordinary classification premise |
| R42.7/N42.7, minimum4 | MU42/C5 PROOF and semantic suite, using the current ordinary foundations | Supplies the actual42-threshold row predicates |
| C5-empty obstruction | Separate MU42/C5 theorem/certificate closure | Separate checked premise |
| Caps20/6/2, A1/B1/B4, signature/trace rules | Reader paper ordinary foundational proofs | Applies to actual members on arbitrary support |
| Pair/singleton and forced extension identities | D17/UNIVERSAL_EXTENSION_LEMMAS.md and inherited_p10/PROOF.md §§4-6 | Universal local geometry; actual shared exterior points retained |
| Preserved mu43/centre18 P10 headers | D17/PROOF.md §2 and check_p10_bridge.py | Identity of finite domains proved for17/42; no header relabel or global family transfer |
| H27 and Jin | Reader paper source statement: H27 intersecting only; Jin via Nikiforov Theorem A | Explicit conditional imports, never computationally re-proved here |
