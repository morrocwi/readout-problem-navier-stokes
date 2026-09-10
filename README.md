# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). Original paper DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository now contains two clearly separated research layers:

1. the deposited v0.1.0 readout paper (`paper/main.tex`, `paper/main.pdf`), which poses the Navier-Stokes readout dichotomy and proves finite-state/retained-layer results; and
2. the later **Discrete Epsilon-Completion (EPSC)** research lane, which develops finite-to-continuum omitted-information certificates without changing the original deposited claim.

**Neither layer proves global regularity, finite-time blow-up, uniqueness of weak solutions, or the Clay Millennium Navier-Stokes problem.** See `CLAIMS.md`.

## Papers and analytic notes

- `paper/main.tex`, `paper/main.pdf` — original deposited paper.
- `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex` — new standalone manuscript: *Finite Readout Certificates for Navier-Stokes: Discrete Epsilon-Completion, Spectral Tails, and A Posteriori Adapters*.
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — Leray-Hopf spacetime Fourier-tail certificate.
- `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` — terminal a-posteriori energy-budget certificate.
- `paper/NS_RELATIVE_ENERGY_ADAPTER_CERTIFICATE.md` — residual-based Galerkin/comparison-path to Leray-Hopf terminal adapter.

## Four-repository architecture

- `morrocwi/information-discrete-math` — general executable mathematics and certificate machinery;
- `morrocwi/toledo` — equation/proposal provenance and tier/status;
- `morrocwi/readout_genesis` — interpretation/application map only;
- this repository — Navier-Stokes specialization, manuscripts, experiments, reproduction and claim boundaries.

## Reproduction

Run:

```bash
bash reproduction/reproduce_all.sh
```

The ledger separates finite/script checks, standard analytic derivations (`Dr`), and explicitly open obligations. The EPSC work is tracked as the later Volume-7 research lane rather than being retroactively inserted into the deposited Volumes 1-6 series.

## Discrete Epsilon-Completion

The base fail-closed structure is

\[
\delta_K=\|R_Kx_{K+1}-x_K\|,
\qquad
\|Q_Kx\|_Y\le\beta_{K,Y},
\]

with certification allowed only when the declared numerical/refinement defect and a **proved** omitted-information bound satisfy the requested tolerance. A small nested defect or small boundary-shell energy alone is not a continuum certificate.

For an unforced Leray-Hopf trajectory on the `2*pi` periodic three-torus,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

provides an explicit computable spacetime `beta_K -> 0` without assuming global smoothness.

For prescribed terminal time, a separately certified pointwise `H^s` bound gives

\[
\|(I-P_K)u(T)\|_2\le M_s(T)/(K+1)^s.
\]

A richer retained energy/dissipation tape also gives

\[
\boxed{
\|(I-P_K)u(T)\|_2^2
\le
\|u_0\|_2^2
-\|P_Ku(T)\|_2^2
-2\nu\int_0^T\|\nabla P_Ku\|_2^2dt
}
\]

for the actual Leray-Hopf projection or certified directional bounds on those quantities.

## Relative-energy adapter

The latest step avoids silently identifying the finite Galerkin trajectory with the continuum projection. For a smooth divergence-free comparison path `v`, define

\[
r=\partial_tv+P[(v\cdot\nabla)v]-\nu\Delta v-Pf,
\]

\[
A_T=2\int_0^T\|\nabla v\|_\infty dt,
\qquad
B_T=\int_0^T\|r\|_{H^{-1}}^2dt.
\]

Then the standard relative-energy estimate gives

\[
\sup_{t\le T}\|u(t)-v(t)\|_2^2
\le
e^{A_T}\left(e_0^2+B_T/\nu\right).
\]

If `v(T)` is supported in the retained cutoff, this directly yields a terminal omitted-tail bound for the actual solution. For a finite Fourier comparison path the unresolved residual is itself a finite triad tape, implemented in `information-discrete-math`.

## Toledo lineage and current frontier

The EPSC family is registered Toledo-first through `PROP-EPSC-15`:

- `PROP-EPSC-01..09` — base/refinement, spectral and spacetime certificate family;
- `PROP-EPSC-10..12` — terminal energy-budget family and adapter obligation;
- `PROP-EPSC-13` — residual-based Leray relative-energy adapter;
- `PROP-EPSC-14` — finite Fourier unresolved residual tape;
- `PROP-EPSC-15` — **OPEN** validated RK4 continuous-time residual enclosure.

The remaining end-to-end numerical bridge is therefore precise:

```text
floating-point RK4 tape
    -> validated continuous-time Fourier interpolation
    -> certified upper bounds on A_T and B_T
    -> relative-energy beta_K
    -> terminal continuum L2 certificate
```

Nodewise residual samples or agreement between finite backends are not enough for this final step.

## Finite numerical evidence and non-claim

The short Taylor-Green refinement diagnostic (`nu=0.01`, `dt=0.005`, `T=0.05`) passed its declared operational nested gate at K=4 and K=5. This remains a finite diagnostic, not a proof that K=5 contains all continuum information. It also does not overturn the prior negative coarse turbulent validation: K<=3 did not reproduce the published Re=1600 Taylor-Green dissipation curve in the external-reference test.

The repository's governing distinction is:

```text
finite algebra / nested stability
    != continuum completion
    != physical turbulence validation
```
