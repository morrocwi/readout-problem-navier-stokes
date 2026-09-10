# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). Original paper DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository contains three clearly separated research layers:

1. the deposited v0.1.0 readout paper (`paper/main.tex`, `paper/main.pdf`), which poses the Navier-Stokes readout dichotomy and proves finite-state/retained-layer results;
2. the finite **energy-observability** lane, which studies what total/shell energy histories can determine inside a fixed Fourier-Galerkin state modulo translation; and
3. the later **Discrete Epsilon-Completion (EPSC)** lane, which develops finite-to-continuum omitted-information certificates and now composes them with finite observability.

**None of these layers proves global regularity, finite-time blow-up, uniqueness of arbitrary weak solutions, or the Clay Millennium Navier-Stokes problem.** See `CLAIMS.md`.

## Papers and analytic notes

- `paper/main.tex`, `paper/main.pdf` — original deposited paper.
- `paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex`, `.pdf` — finite-resolution energy observability: universal all-`N` structural ceilings, positive-viscosity rank universality, exact saturation certificates at four declared reader/resolution pairs, and an all-`N` saturation conjecture.
- `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex`, `.pdf` — standalone EPSC manuscript.
- `paper/NS_OBSERVABLE_TO_CONTINUUM_CERTIFICATES.tex` — synthesis manuscript connecting certified finite observability to certified continuum error budgets.
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — Leray-Hopf spacetime Fourier-tail certificate.
- `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` — terminal a-posteriori energy-budget certificate.
- `paper/NS_RELATIVE_ENERGY_ADAPTER_CERTIFICATE.md` — relative-energy adapter plus the exact continuous-time RK4-tape enclosure construction.

## Four-repository architecture

- `morrocwi/information-discrete-math` — general executable mathematics, certificate and composition machinery;
- `morrocwi/toledo` — equation/proposal provenance and tier/status;
- `morrocwi/readout_genesis` — interpretation/application map only;
- this repository — Navier-Stokes specialization, manuscripts, experiments, observability certificates, reproduction and claim boundaries.

## Reproduction

Run the development-series/EPSC ledger:

```bash
bash reproduction/reproduce_all.sh
```

For the final finite energy-observability paper, use the dedicated lane:

```bash
bash reproduction/reproduce_energy_observability.sh --quick
bash reproduction/reproduce_energy_observability.sh
```

See `reproduction/ENERGY_OBSERVABILITY_REPRODUCE.md` and `reproduction/results/energy_observability_manifest_v1.json` for the pinned environment, expected ranks, provenance hashes and claim boundary.

The generated development-series ledger separates finite/script checks, standard analytic derivations (`Dr`), and explicitly open obligations. The EPSC and observable-to-continuum work remain post-paper research lanes rather than being retroactively inserted into the deposited Volumes 1-6 series.

## Energy observability: inner completeness

For cutoff `N`, the declared real finite-state dimension is

\[
d_N=2((2N+1)^3-1).
\]

For the total-energy Lie jet,

\[
\operatorname{rank}D\mathcal E_R\le\min(R+1,d_N-3),
\qquad R_E^{\min}=d_N-4.
\]

For the full shell-energy reader with `m_N` shell channels,

\[
\operatorname{rank}D\mathcal J_R\le\min(m_N+(m_N-1)R,d_N-3),
\]

\[
R_I^{\min}=\left\lceil\frac{d_N-3-m_N}{m_N-1}\right\rceil.
\]

Exact modular certificates attain the translation ceiling at the earliest structurally admissible order for four recorded cases: `N=1` total energy, `N=1` shell energies, `N=2` total energy, and `N=3` shell energies. This is **local finite-state completeness modulo spatial translations** at those certified cases, not global or noise-stable inversion. Generic earliest-order saturation for every finite `N` remains `PROP-NSOBS-07` OPEN.

## Discrete Epsilon-Completion: outer completeness

The base fail-closed structure is

\[
\delta_K=\|R_Kx_{K+1}-x_K\|,
\qquad
\|Q_Kx\|_Y\le\beta_{K,Y},
\]

with certification allowed only when the declared refinement evidence is paired with a **proved/certified** omitted-information bound. A small nested defect or boundary-shell energy alone is not a continuum certificate.

For an unforced Leray-Hopf trajectory on the `2*pi` periodic three-torus,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

provides an explicit spacetime `beta_K -> 0` without assuming global smoothness.

A terminal relative-energy route uses a divergence-free comparison path `v` with

\[
r=\partial_tv+P[(v\cdot\nabla)v]-\nu\Delta v-Pf,
\]

\[
A_T=2\int_0^T\|\nabla v\|_\infty dt,
\qquad
B_T=\int_0^T\|r\|_{H^{-1}}^2dt,
\]

and

\[
\sup_{t\le T}\|u(t)-v(t)\|_2^2
\le
e^{A_T}\left(e_0^2+B_T/\nu\right).
\]

`PROP-EPSC-15` supplies an exact-dyadic piecewise-linear continuous-time reconstruction of stored RK4 nodes and rigorous finite residual summaries for the declared tape. Tightness/cost at larger cutoff and horizon is the distinct `PROP-EPSC-16` OPEN frontier.

## Observable-to-continuum synthesis

The two layers answer different questions:

```text
inner completeness:  do observations determine the retained finite state?
outer completeness:  how much continuum state can remain outside the cutoff?
```

They compose only after the observation side supplies a **quantitative certified retained-state radius**. If

\[
\inf_{g\in G}\|P_Nu(T)-g\widehat x_N\|_2\le\rho_N
\]

and EPSC supplies

\[
\|(I-P_N)u(T)\|_2\le\beta_N,
\]

then orthogonality gives the new synthesis rule

\[
\boxed{
\inf_{g\in G}\|u(T)-g\widehat x_N\|_2
\le\sqrt{\rho_N^2+\beta_N^2}.
}
\]

For the energy-reader application `G=T^3` is spatial translation. This conditional composition is registered as `PROP-EPSC-17` and implemented fail-closed in `information-discrete-math:idm/ns_observable_to_continuum.py`.

Crucially, **rank saturation is not `rho_N`**. It provides local qualitative identifiability modulo symmetry, but not a certified inverse radius, branch control, conditioning, or noise bound. The quantitative inverse is `PROP-EPSC-18` OPEN; its noisy/stable extension is `PROP-EPSC-19` OPEN.

## Toledo lineage and current frontiers

The energy-observability family is registered as `PROP-NSOBS-01..08`. The EPSC family now runs through `PROP-EPSC-19`.

The major open problems are deliberately separated:

- `PROP-NSOBS-07` — prove/refute earliest-order generic energy-observability saturation for every finite resolution;
- `PROP-EPSC-16` — make outer path certification tight and scalable for larger cutoff/horizon;
- `PROP-EPSC-18` — construct a certified inverse from energy Lie jets to retained-state radius `rho_N`;
- `PROP-EPSC-19` — propagate measurement/noise/differentiation uncertainty through the inverse and final continuum certificate.

These are parts of one measurement-to-continuum programme, but they are not the same mathematical problem.

## Finite numerical evidence and non-claim

The short Taylor-Green refinement diagnostic (`nu=0.01`, `dt=0.005`, `T=0.05`) passed its declared operational nested gate at K=4 and K=5. This remains a finite diagnostic, not a proof that K=5 contains all continuum information. It also does not overturn the prior negative coarse turbulent validation: K<=3 did not reproduce the published Re=1600 Taylor-Green dissipation curve in the external-reference test.

The repository's governing distinction is:

```text
finite observability / finite algebra
    != certified retained-state inversion
    != continuum mathematical certification
    != physical turbulence validation
```
