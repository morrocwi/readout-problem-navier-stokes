# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository holds a short, arXiv-style, single-column mathematical note that:

1. proves one elementary finite-state theorem — exact commuting domain translation together with exact reader factorization does not imply that any finite-horizon reader decides an arbitrary domain question (an explicit 8-state witness);
2. poses, without answering, the corresponding **Navier-Stokes readout problem**: a dichotomy (R)/(N) asking whether Fefferman's breakdown predicate is finite-readout-determined once a Navier-Stokes domain translation and a declared finite reader are fixed;
3. proves a separate finite retained-turbulence continuation theorem.

**The deposited v0.1.0 paper does not prove, disprove, or otherwise resolve the Clay Millennium Navier-Stokes existence-and-smoothness problem.** See `CLAIMS.md` for the exact claim boundary.

## Contents

- `paper/main.tex`, `paper/main.pdf` — deposited paper.
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — later analytic note: unconditional Leray-Hopf spacetime Fourier-tail certificate.
- `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` — later analytic note: a-posteriori terminal tail bound from a certified retained energy tape.
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

The reproduction ledger separates finite/script checks, standard analytic derivations (`Dr`), and explicitly open items. Volume 7 now contains finite witnesses for both the spacetime tail certificate and the terminal energy-budget certificate; the analytic Leray-Hopf steps remain honestly tagged `Dr` rather than being faked as finite proofs.

## Four-repository architecture

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
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — target-norm refinement and spacetime certificate;
- `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` — terminal retained-energy-tape certificate;
- `reproduction/checks/check_volume7_spacetime_tail.py` and `check_volume7_terminal_energy_budget.py` — finite witness checkers;
- `CLAIMS.md` — current claim boundary.

The general implementation lives in Information Discrete Mathematics:

- `idm/ns_retained.py` — finite Fourier-Galerkin recurrence;
- `idm/ns_epsilon.py` — nested defect and fail-closed epsilon gate;
- `idm/ns_tail_certificate.py` — spectral/spacetime tail certificate helpers;
- `idm/ns_terminal_certificate.py` — fail-closed terminal energy-budget certificate.

Equation/proposal provenance is registered Toledo-first. `PROP-EPSC-01..09` live in `registry/proposals/discrete_epsilon_completion.json`; `PROP-EPSC-10..12` live in `registry/proposals/discrete_epsilon_completion_terminal_energy.json`.

### Result 1 — target-space refinement

The original target

\[
\|(I-P_K)u\|\le\beta_K,\qquad \beta_K\to0
\]

is not meaningful enough until the target norm/readout and admissible assumptions are declared.

For terminal Fourier coefficients alone, an unrestricted omitted high-frequency divergence-free pair can change the tail without changing `P_Ku`; so retained terminal coefficients by themselves do not identify a universal useful terminal tail.

For an unforced Leray-Hopf trajectory on the `2*pi` periodic three-torus,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

by the spectral tail inequality plus the Leray-Hopf energy inequality. This is an explicit computable `beta_K -> 0` in the declared spacetime norm, without assuming global smoothness.

### Result 2 — prescribed terminal-time energy-budget bound

For the actual Leray-Hopf projection, define the retained energy tape

\[
\mathcal R_K^{EB}
=
\left(
\|P_Ku(T)\|_2,
\nu\int_0^T\|\nabla P_Ku(t)\|_2^2dt
\right).
\]

Then

\[
\boxed{
\|(I-P_K)u(T)\|_2^2
\le
\|u_0\|_2^2
-
\|P_Ku(T)\|_2^2
-
2\nu\int_0^T\|\nabla P_Ku(t)\|_2^2dt
}.
\]

This is a genuine finite-K terminal upper bound **if the retained quantities are exact or certified directional bounds for the actual continuum projection**. Raw values from an uncertified Galerkin surrogate are not enough.

Its asymptotic floor is the energy-inequality slack

\[
\mathcal D_E(T)=
\|u_0\|_2^2-
\|u(T)\|_2^2-
2\nu\int_0^T\|\nabla u\|_2^2dt.
\]

If energy equality is independently justified, `D_E(T)=0` and the terminal energy-budget certificate tends to zero as `K -> infinity`.

### The new frontier

The main bridge is now sharper than “find any beta.” The next target is Toledo `PROP-EPSC-12`:

```text
finite Galerkin record
        ↓ certified directional adapter error
actual continuum projected energy tape
        ↓ terminal energy-budget theorem
rigorous terminal beta_K
```

In other words, the immediate research problem is to certify that the finite solver's retained terminal energy and accumulated retained dissipation bound the corresponding actual continuum quantities in the directions required by the theorem.

### Non-claim

These results do **not** prove global regularity, finite-time blow-up, uniqueness of weak solutions, physical adequacy of a coarse cutoff, or the Clay Millennium problem. They partially close `PROP-EPSC-04` and isolate the remaining finite-to-continuum adapter obligation.
