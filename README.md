# An upper bound for three-sunflower-free families of four-element sets

Oleksiy Babanskyy

[Read the paper](paper/Four-Uniform-Three-Sunflower-Bound.pdf) ·
[Reproduce the computations](REPRODUCE.md) ·
[Mathematical dependencies](proof/DEPENDENCIES.md)

The manuscript gives a computer-assisted upper bound of **68** for the
maximum size M(4,3) of a finite simple four-uniform family containing no three
distinct sets with equal pairwise intersections. The empty kernel is included
among the forbidden configurations. Together with the classical 54-member
construction, this gives

    54 ≤ M(4,3) ≤ 68.

Equivalently, every finite simple four-uniform family of at least 69 sets contains a three-sunflower.
The first forcing threshold is M(4,3)+1. Exclusion of size 68, optimality of
54, record priority and a solution of the general sunflower conjecture are
not claimed.

The proof imports the intersecting-family upper bound 27 from Proposition
6.7 of Axante et al., arXiv:2609.06175v1, and uses Jin’s strict graph
homomorphism theorem as stated in Nikiforov’s Theorem A. The companion does
not re-execute the external H27 calculation. Its finite route includes nine
preliminary blocks, the separate C5 obstruction, both degree-17 transport
cores and the terminal contradiction at 69. Finite comparisons use exact
integer or rational arithmetic; the paper and linked proofs establish the
reductions connecting them to the theorem.

## Verify

Python 3.10 or newer and its standard library suffice. From the repository
root:

    python -B scripts/check_repository.py
    python -B scripts/run_checks.py --mode quick --output build/quick
    python -B scripts/run_checks.py --mode complete --output build/complete

Each run requires a new output directory. The wrapper creates an isolated
computational copy and saves receipts under its output directory. Quick
checks report `QUICK_PARTIAL_PASS`; they are partial. Only the complete route
checks all 42 named finite suites, normally and with Python -O, and reports
`COMPLETE_COMPANION_PASS`. See [REPRODUCE.md](REPRODUCE.md) for receipt
checking, paper builds, failure controls and the qualified historical
verification record. A computational PASS does not formalize the written
proof or constitute external human reproduction.

## Repository

| Path | Contents |
| --- | --- |
| [paper/](paper/) | Manuscript PDF, LaTeX source and bibliography |
| [proof/DEPENDENCIES.md](proof/DEPENDENCIES.md) | Logical dependencies and links to written reductions |
| [companion/](companion/) | Preliminary and terminal proof code, exact data and certificates |
| [SUITE_PLAN.json](SUITE_PLAN.json) | The 42 finite suites and their exact expected results |
| [COMPUTATIONAL_MANIFEST.json](COMPUTATIONAL_MANIFEST.json) | Identities of the computational inputs |
| [scripts/](scripts/) | Integrity, replay, receipt-checking and paper-build entry points |
| [tests/](tests/) | Adverse-input and repository-tool checks |
| [verification/](verification/) | Preserved input identities and historical verification summary |
| [MANIFEST_SHA256.json](MANIFEST_SHA256.json) | Identities of the distributed repository files |
| [verification/ORIGIN.json](verification/ORIGIN.json) | Preserved-source identities and reader metadata changes |

The named author is responsible for the claims. AI tools assisted research,
software and manuscript review; they are not listed as authors.
[CITATION.cff](CITATION.cff) supplies citation metadata.
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) records attribution and
rights boundaries. No reuse license is granted for the manuscript or original
project payload.
