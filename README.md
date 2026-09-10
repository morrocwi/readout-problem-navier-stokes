# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository holds a short, arXiv-style, single-column mathematical note that:

1. proves one elementary finite-state theorem — exact commuting domain translation together with exact reader factorization does not imply that any finite-horizon reader decides an arbitrary domain question (an explicit 8-state witness);
2. poses, without answering, the corresponding **Navier-Stokes readout problem**: a dichotomy (R)/(N) asking whether Fefferman's breakdown predicate is finite-readout-determined once a Navier-Stokes domain translation and a declared finite reader are fixed;
3. proves a separate finite retained-turbulence continuation theorem.

**The deposited v0.1.0 paper does not prove, disprove, or otherwise resolve the Clay Millennium Navier-Stokes existence-and-smoothness problem.** See `CLAIMS.md` for the exact claim boundary.

## Contents

- `paper/main.tex`, `paper/main.pdf` — deposited paper.
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — later analytic note refining the epsilon-completion problem by target norm.
- `verification/verify_state_breakdown_math.py` — finite-witness and Euler-convergence verification.
- `reproduction/` — wider development-series reproduction system.
- `CLAIMS.md` — exact claim boundary.
- `LICENSE` — CC BY 4.0.

## Reproducing the original verification

```bash
python3 verification/verify_state_breakdown_math.py
```

## Wider reproduction system

Run:

```bash
bash reproduction/reproduce_all.sh
```

The reproduction ledger separates machine/script checks, standard analytic derivations (`Dr`), and explicitly open items. The post-paper Volume-7 checker `reproduction/checks/check_volume7_spacetime_tail.py` tests the finite spectral algebra and non-identifiability witness while leaving the Leray-Hopf estimate at its honest analytic tier.

## Provenance and process

The project uses a four-repository separation:

- `morrocwi/information-discrete-math` — general executable mathematics and certificate machinery;
- `morrocwi/toledo` — equation/proposal provenance and status;
- `morrocwi/readout_genesis` — interpretation/application map only;
- this repository — Navier-Stokes specialization, proofs, experiments, reproduction and claim boundary.

---

## Post-paper research lane: Discrete Epsilon-Completion

The first numerical stage tested whether the finite Fourier-Galerkin NS recurrence can be evolved directly on integer Fourier records and whether nested refinements can provide an operational stopping diagnostic without promoting that diagnostic into a continuum claim.

Read:

- `reproduction/NS_DISCRETE_EPSILON_COMPLETION.md` — finite algorithm and recorded run;
- `reproduction/checks/check_discrete_epsilon_completion.py` — independent NumPy checker;
- `reproduction/results/discrete_epsilon_completion_v01.json` — frozen 2026-09-10 result;
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — analytic refinement of the missing tail-certificate problem;
- `CLAIMS.md` — current claim boundary.

The general implementation lives in Information Discrete Mathematics:

- `idm/ns_retained.py` — finite Fourier-Galerkin recurrence;
- `idm/ns_epsilon.py` — nested defect and fail-closed epsilon gate;
- `idm/ns_tail_certificate.py` — spectral-tail certificate helpers.

Equation/proposal provenance is registered Toledo-first in `registry/proposals/discrete_epsilon_completion.json` as `PROP-EPSC-01` through `PROP-EPSC-09`.

### What was learned

The original open target was

\[
\|(I-P_K)u\|\le\beta_K,\qquad \beta_K\to0.
\]

The key refinement is that `beta_K` must be indexed by the **declared target norm/readout and admissible assumptions**.

For an arbitrary terminal divergence-free `L2` state, finite retained Fourier coefficients alone cannot identify the omitted tail: an arbitrary high-frequency divergence-free conjugate pair can be added without changing `P_Ku`.

For an unforced Leray-Hopf trajectory on the `2*pi` periodic three-torus, however,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

by the spectral tail inequality plus the Leray-Hopf energy inequality. This bound is computable from declared problem data and tends to zero.

Thus the status is no longer simply "PROP-EPSC-04 open." It is:

```text
spacetime L2/readout completion: analytic certificate available
arbitrary prescribed terminal full-state completion: conditional/open
```

If a pointwise `H^s` bound is separately certified at time `T`, then

\[
\|(I-P_K)u(T)\|_2\le\frac{M_s(T)}{(K+1)^s}.
\]

The hard part is therefore not the Fourier tail inequality itself but obtaining globally valid pointwise regularity control in 3-D.

### Non-claim

This partial closure does **not** prove global regularity, finite-time blow-up, uniqueness of weak solutions, physical adequacy of a coarse cutoff, or the Clay Millennium problem. It identifies exactly which finite readouts can already receive a rigorous omitted-information certificate and where the classical 3-D obstacle remains.
