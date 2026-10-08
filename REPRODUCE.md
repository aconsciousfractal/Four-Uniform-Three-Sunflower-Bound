# Reproduce the paper and computations

Use Python 3.10 or newer. The proof-facing scripts use only its standard
library, with no solver or optimizer. The recorded verification used CPython
3.12.14. Run the commands below from the repository root. Each output
directory must be new; quote paths containing spaces.

## Check file integrity

    python -B scripts/check_repository.py

The root [MANIFEST_SHA256.json](MANIFEST_SHA256.json) identifies this
distribution. The preserved
[verification/BASELINE_MANIFEST_SHA256.json](verification/BASELINE_MANIFEST_SHA256.json)
identifies the earlier package.
[verification/ORIGIN.json](verification/ORIGIN.json) records the exact source
and current identities of adapted reader documents and metadata. The
executable checker code, exact data and certificates, and all 42 command
definitions and exact expected semantic results are unchanged. Current
written reductions and reader metadata have documented adaptations and are
bound by the current computational and repository manifests.

[COMPUTATIONAL_MANIFEST.json](COMPUTATIONAL_MANIFEST.json) binds the input
code, exact data, written reductions and plan. The manifests are integrity
checks, not signatures or independent authentication of their contents.

## Quick checks

    python -B scripts/run_checks.py --mode quick --output build/quick
    python -B scripts/check_receipt.py build/quick/receipts/RECEIPT.json

This checks the explicit 54-member construction, small transversal tables and
the final fibre census. Success reports `QUICK_PARTIAL_PASS`; it cannot
certify the complete finite companion.

## Complete finite route

    python -B scripts/run_checks.py --mode complete --output build/complete
    python -B scripts/check_receipt.py build/complete/receipts/RECEIPT.json

The required 42 suites are declared in [SUITE_PLAN.json](SUITE_PLAN.json).
Each executes twice, normally and with Python -O. Exact expected semantic
results include statuses, counts, complete profile lists and certificate
outcomes. Only explicitly enumerated timing fields are excluded from
comparison. Complete success reports `COMPLETE_COMPANION_PASS`, with 84
successful executions and 42 equal normal/-O pairs.

The wrapper uses a separate computational copy inside the new output
directory and places its receipts in `receipts/`. It delegates mathematical
execution to the preserved `scripts/verify.py`, which checks computational
input identities before running suites. A Python audit hook limits checker
file access to packaged files, receipts and the interpreter installation.
This is a Python-level boundary, not an operating-system sandbox or a
different-machine reproduction.

Keep `receipts/RECEIPT.json` and its per-execution directories together. They
contain commands, interpreter information, elapsed times, stdout and stderr,
output hashes and normalized semantic results. The receipt checker checks
their consistency with the fixed plan and inputs; it does not rerun the
mathematics or authenticate a claim of past execution.

A missing or altered input, failed semantic comparison, nonzero exit,
incomplete suite or timeout prevents complete success. The preserved runner
reports `FAIL_INCOMPLETE` and retains its receipt and available output;
existing output is rejected without overwriting it. Investigate failures:
increasing the budget or treating two failures as agreement is insufficient.

Written reductions establish arbitrary-support coverage, symmetry
representatives, necessary inequalities and pruning soundness; the scripts
verify their finite objects. H27 and Jin remain named mathematical imports.
The external H27 calculation is not replayed. Some inherited output fields describe local
stages of the proof; the paper and complete dependency chain define the
global claim.

## Build the paper

An existing pdflatex installation with the packages named in `paper/main.tex`
is required. No installer is invoked:

    python -B scripts/build_paper.py --output build/paper

Use `--engine` to select an existing executable if it is not on PATH. The
wrapper isolates the build script and source, leaving the
distributed `paper/Four-Uniform-Three-Sunflower-Bound.pdf` unchanged. The `scripts/build_pdf.py`
writes its rebuilt PDF into its own package root; use the wrapper for a
build that preserves the distributed artifact.

The underlying build performs three passes, rejects unresolved references
and citations and overfull boxes, disables MiKTeX automatic package
installation, and records the engine and source/PDF identities. Retain the
new output directory and its diagnostics. Success reports `PASS_ISOLATED_BUILD`
and creates `build/paper/Four-Uniform-Three-Sunflower-Bound.pdf` and
`BUILD_RECEIPT.json` when using the command above. Rebuilt PDF bytes may differ
with the TeX environment.

## Test failure handling

    python -B tests/test_verifier.py
    python -B tests/test_repository_tools.py
    python -B tests/test_document_adaptations.py

The verifier tests exercise missing or altered input, wrong semantic results
or coverage counts, existing output and timeout handling. The repository-tool
tests check the reader wrappers and integrity controls. These tests do not
repeat the mathematical suites. On systems with a restricted or long
temporary path, use:

    python -B tests/test_verifier.py --temp-root <short-writable-temp>

Keep generated files under ignored `build/` or in an explicitly chosen
external workspace or temporary directory. The replay wrapper makes
`build/quick` and `build/complete` usable without changing the original
runner’s requirement that receipts lie outside its computational package.

## Historical verification record

[verification/complete_summary.json](verification/complete_summary.json)
records 42 suites, 84 successful executions and 42 equal normal/-O
scientific pairs. The first run completed 14 suite pairs before a packaging
failure identified missing stage-contract metadata. After repair, an
isolated continuation completed the remaining 28 pairs without repeating
successful computations. Code/data identities and exact expected outputs
were checked before carrying forward the completed pairs.

This is a qualified complete verification record, not one uninterrupted
run. The retained summary identifies the predecessor document, plan and input
bytes. It is not a fresh replay against the currently adapted document bytes
by this repository’s reader wrappers. The provenance record relates those
identities to the current distribution; documentary adaptation supplies no
new scientific execution. Total measured successful checker time was 3189.8 seconds (about
53.2 minutes); peak memory was not measured. The earlier adverse-input panel
passed five tests and an added end-to-end failure-receipt test. These are
historical observations, not resource guarantees for another machine.

The complete command above executes the whole finite suite from scratch.
Neither historical verification nor fresh finite replay proves the written
reductions by software, re-executes the named external theorems, establishes
novelty, supplies proof-assistant formalization or constitutes external human
review.
