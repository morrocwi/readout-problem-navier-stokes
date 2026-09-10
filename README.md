# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository holds a short, arXiv-style, single-column mathematical note that:

1. proves one elementary finite-state theorem — exact commuting domain translation together with
   exact reader factorization does not imply that any finite-horizon reader decides an arbitrary
   domain question (an explicit 8-state witness);
2. poses, without answering, the corresponding **Navier-Stokes readout problem**: a dichotomy
   (R)/(N) asking whether Fefferman's breakdown predicate is finite-readout-determined once a
   Navier-Stokes domain translation and a declared finite reader are fixed;
3. proves a separate, further theorem — a finite retained-turbulence layer
   `tau_R dI_R/dt + L_R I_R = S_R + eta_R` has a unique, bounded solution on every finite time
   interval given finite dimension, positive time constant, a fixed finite generator, and a
   locally integrable drive — and states precisely what this does and does not imply about a
   hypothetical continuum breakdown transferring onto that reader.

**This note does not prove, disprove, or otherwise make progress on the Clay Millennium
Navier-Stokes existence-and-smoothness problem.** See `CLAIMS.md` for the exact claim boundary.
It cites exactly one external reference: Fefferman's own official Clay Mathematics Institute
problem statement.

## Contents

- `paper/main.tex`, `paper/main.pdf` — the paper.
- `verification/verify_state_breakdown_math.py` — the finite-witness and Euler-convergence
  verification script (independently re-run 2026-09-09, see `CLAIMS.md`).
- `CLAIMS.md` — exact claim boundary, what is proved vs. posed vs. explicitly not claimed.
- `LICENSE` — CC BY 4.0.

## Reproducing the verification

```
python3 verification/verify_state_breakdown_math.py
```

Expected output confirms: 8/8 dynamical and observational weld checks, `F^2 = Id`, the witness
pair's reader-equivalence holding through `k=9999`, and Euler-stepper error ratios converging to
approximately 2.0 (consistent with first-order `O(h)` convergence) across four halvings of the
step size.

### Wider reproduction system (whole 6-volume series)

This note is one document in a larger "Readout-Navier-Stokes Development Series" (6 volumes,
v0.1-v0.6). See `reproduction/` for a one-command reproducibility system covering every
mechanically checkable claim across all 6 volumes, with an auto-generated ledger
(`reproduction/LEDGER.md` / `reproduction/LEDGER.json`) honestly tiering every claim as
machine-checked, script-verified, standard-but-not-mechanical, or explicitly open. Run
`bash reproduction/reproduce_all.sh` to reproduce everything.

## Provenance and process

Both new theorems in this note were checked against, and registered in, an internal equation
registry (github.com/morrocwi/toledo) as proposals (pending canonical-code assignment) before
being written into the paper, following the maintaining project's own equation-registry-first
practice; see `CLAIMS.md` for the exact tiers and status of every claim. Independent adversarial
review is complete, this repository is public, and it has been deposited on Zenodo
(10.5281/zenodo.22673246).

---

## Post-paper research lane: Discrete Epsilon-Completion

A later, **finite-diagnostic** lane now tests whether the finite Fourier-Galerkin NS recurrence can
be evolved directly on integer Fourier records and whether nested finite refinements can provide an
operational stopping diagnostic without promoting that diagnostic into a continuum claim.

Read these together:

- `reproduction/NS_DISCRETE_EPSILON_COMPLETION.md` — NS-specific algorithm, recorded run, and claim boundary.
- `reproduction/checks/check_discrete_epsilon_completion.py` — independent NumPy reproduction checker.
- `reproduction/results/discrete_epsilon_completion_v01.json` — frozen 2026-09-10 finite-diagnostic result.
- `CLAIMS.md` — explicit separation of finite algebra, nested stability, continuum completion, and physical validation.

The general algorithm/certification layer lives in **Information Discrete Mathematics**, not here:
`github.com/morrocwi/information-discrete-math`, specifically `idm/ns_epsilon.py` and
`docs/DISCRETE_EPSILON_COMPLETION.md`.

Equation/definition provenance is registered **Toledo-first** in
`github.com/morrocwi/toledo/registry/proposals/discrete_epsilon_completion.json`:

- `PROP-EPSC-01` — Nested Readout Consistency Defect;
- `PROP-EPSC-02` — NS Fourier boundary-energy diagnostic;
- `PROP-EPSC-03` — fail-closed epsilon-completion gate;
- `PROP-EPSC-04` — **OPEN** computable omitted-information tail certificate.

The key boundary is fail-closed:

```
finite nested diagnostic may PASS
continuum / infinite-object epsilon certificate remains HOLD
until a proved PROP-EPSC-04 beta_K bound is supplied
```

This post-paper lane is **not part of the deposited v0.1.0 paper claim** unless a future release
explicitly incorporates it. It does not change the repository's non-claim on the Clay Millennium
problem.
