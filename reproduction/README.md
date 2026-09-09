# Reproduction system -- Readout-Navier-Stokes Development Series

This directory is an independent, one-command reproduction system for every mechanically
checkable claim across:

- **GLS-2026-006** -- this repository's own published note (`paper/`, `verification/`,
  `CLAIMS.md`), and
- **GLS-2026-007** -- the larger 6-volume "Readout-Navier-Stokes Development Series"
  (Volumes 1-6, v0.1-v0.6), of which Volume 1 and Volume 2 correspond to the two source
  documents this repository was originally built from.

It does **not** replace `verification/verify_state_breakdown_math.py` or `CLAIMS.md` --
those remain the canonical claim-boundary documents for GLS-2026-006's own paper. This is
an addition, covering the full 6-volume series with a machine-generated ledger.

## How to reproduce everything

```
cd reproduction
bash reproduce_all.sh
```

This runs every `checks/check_volumeN.py` script (N=1..6), prints each script's evidence
to stdout, and regenerates `LEDGER.json` and `LEDGER.md`. Exit code is `0` if every claim
a script actually attempted to check came back PASS, and nonzero if any attempted check
FAILed. **A nonzero tier count for `Dr` or `Open` is not a failure** -- those claims were
never attempted because they are not mechanically checkable (see below).

You can also run a single volume's check directly, e.g.:

```
python3 checks/check_volume3.py
```

Or regenerate just the ledger from the existing check scripts:

```
python3 generate_ledger.py
```

## What the tiers mean

This reproduction system follows the workspace's own IDM (Information Discrete
Mathematics) tier discipline. Every claim in `LEDGER.json`/`LEDGER.md` carries exactly one
of:

| Tier | Meaning |
|---|---|
| `Th_coqc` | Machine-checked in Coq. **None of the claims in this reproduction pass carry this tier** -- no `.v` file was compiled by this system. (Volume 1's own arXiv bundle references a `NSR01_finite_witness.v` Coq script that the paper itself flags as not independently compiled; this reproduction system's Python re-derivation of the same finite claim is recorded as `finite_diagnostic`, not `Th_coqc`.) |
| `finite_diagnostic` | An independent script in `checks/` actually ran a finite enumeration, a numeric simulation, or a symbolic (sympy) algebraic check, and printed concrete evidence (numbers, witnesses, residuals) -- not just `True`/`False`. |
| `Dr` | Standard, textbook-level derived mathematics (classical real/functional analysis: Gronwall bounds, Cauchy sequences in Banach spaces, Galerkin compactness, weak-* limits) that is **not mechanically checkable by a finite script** because it quantifies over an arbitrary hypothetical solution, not a concrete numeric instance. Recorded with a one-line reason; never faked as checked. |
| `Open` | An explicitly unresolved, hypothetical, or posed-not-answered item -- either a standing assumption the papers themselves never claim to establish (e.g. that a real Navier-Stokes solution with an H^3 blow-up and a genuine finite-energy weak continuation past it actually exists), or a bridge obligation Volume 1 poses without answering (NSR-02/03/04). |

A claim that is a bare **definition** (not itself a provable/checkable statement) is also
recorded under `Dr` with a note that it is definitional, so no claim silently disappears
from the ledger.

## Honest statement of scope

**This reproduces the finite/mechanical claims only.** Across all 6 volumes, the series
makes exactly one substantive *mathematical* move that is finite and combinatorial by
construction -- the 8-state exact-weld witness (Volume 1's NSR-01, restated as Volume 2
Theorem 3.1 and Volume 3 Theorem 9.1) -- plus a family of linear-ODE / Fourier-Galerkin
bookkeeping identities (stability eigenvalue thresholds, Duhamel recurrences, Parseval
orthogonality splits, finite-horizon sufficiency inductions) that are exact algebra for any
*fixed, finite* truncation. All of that is reproduced here.

Everything else in the series -- existence of Fourier-mode limits via bounded-variation
arguments, Galerkin/weak-* compactness existence of a weak-solution restart, Sobolev-norm
localization arguments, and above all the standing **Assumption 1.1** in Volumes 3, 4, 5,
and 6 (that a smooth Navier-Stokes solution with a genuine H^s/H^3 continuum breakdown,
together with a real finite-energy weak continuation past it, actually exists) -- is
classical continuum mathematics that **no script in this repository verifies, and none
should claim to**. Those items are recorded as `Dr` or `Open` with a stated reason. This
reproduction system is a **floor, not a ceiling**, on rigor: passing every check here means
the finite/mechanical backbone of the series is exactly as claimed, not that any part of
the Clay Millennium Navier-Stokes problem has been resolved. Neither this repository nor
the series itself claims that.

## Known reproducibility gap (flagged, not hidden)

Volume 2 Section 13's worked numerical example (stability threshold + a 4-row error table
with ratios ~2.0 confirming `O(h)` convergence) is **partially** reproduced: the
lambda_max/stability-threshold arithmetic matches exactly, but the paper's prose does not
specify the forcing vector `G_R` or initial condition `I_R(0)` used to generate its
published error table, and a naive constant/kernel-aligned choice trivializes the test. See
`checks/check_volume2.py`'s `check_convergence_order` and `BUILD_STATUS.md` for the
explicit, documented substitute values used here, and what they do and do not confirm.

## Two internal document defects found and flagged (not fixed here)

Independent extraction of the source PDF found two apparent cross-reference slips in the
papers' own proof text:

- Volume 2 Theorem 11.1's proof cites "Theorem 9.1", which does not exist as a numbered
  theorem in Volume 2 (Section 9 is an unnumbered open-problem discussion) -- most likely a
  typo for Theorem 8.1.
- Volume 6 Theorem 6.1's proof cites "Theorem 2.1", which does not exist in the extracted
  pages (Section 2 only contains Lemma 2.1), and appears to conflate Theorem 4.1
  (zero-defect identities) with Theorem 5.1 (horizon sufficiency).

Both are recorded in `LEDGER.json`/`LEDGER.md` on the affected claim and in
`BUILD_STATUS.md`; this reproduction system does not edit the source papers.

## Files

- `checks/check_volume1.py` .. `checks/check_volume6.py` -- one independent verification
  script per volume.
- `generate_ledger.py` -- runs every check script, parses its structured `RESULT_JSON`
  output, and writes `LEDGER.json` + `LEDGER.md`.
- `reproduce_all.sh` -- the one-command entry point.
- `LEDGER.json`, `LEDGER.md` -- auto-generated; do not hand-edit.
- `BUILD_STATUS.md` -- build notes for the next (review) pass: what was built, counts,
  and the extraction-phase findings this system is built on.
