# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). Original paper DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository contains three separated research layers:

1. the deposited v0.1.0 readout paper (`paper/main.tex`, `paper/main.pdf`), which poses the Navier-Stokes readout dichotomy and proves finite-state/retained-layer results;
2. the finite **energy-observability** lane, which studies what total/shell-energy histories determine inside a fixed Fourier-Galerkin state modulo translation; and
3. the later **Discrete Epsilon-Completion (EPSC)** lane, which develops finite-to-continuum omitted-information certificates and composes them with certified finite observability.

**None of these layers proves global regularity, finite-time blow-up, uniqueness of arbitrary weak solutions, physical DNS adequacy at an arbitrary cutoff, or the Clay Millennium Navier-Stokes problem.** See `CLAIMS.md`.

## Papers and analytic notes

- `paper/main.tex`, `paper/main.pdf` — original deposited paper; not overwritten by later work.
- `paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex`, `.pdf` — finite-resolution energy observability and structural ceilings.
- `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex`, `.pdf` — standalone EPSC manuscript.
- `paper/NS_OBSERVABLE_TO_CONTINUUM_CERTIFICATES.tex` — synthesis connecting certified finite observability to certified continuum error budgets.
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — Leray-Hopf spacetime Fourier-tail certificate.
- `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` — terminal a-posteriori energy-budget certificate.
- `paper/NS_RELATIVE_ENERGY_ADAPTER_CERTIFICATE.md` — relative-energy adapter and exact continuous-time RK4-tape enclosure.
- `paper/NS_EPSC18_N1_ROWWISE_RADIUS.md` — row-aware full-`N=1` quantitative local-inverse radius.
- `paper/NS_EPSC18_N1_EXACT_PRECONDITIONER.md` — actual characteristic-zero selected Jacobian and exact rational preconditioner.
- `paper/NS_EPSC18_N1_COMPONENTWISE_RADIUS.md` — exact coefficient-tensor/componentwise tightening of the `N=1` radius.

## Four-repository architecture

- `morrocwi/information-discrete-math` — general executable finite-first mathematics and fail-closed certificate machinery;
- `morrocwi/toledo` — proposal/equation provenance and tier/status;
- `morrocwi/readout_genesis` — interpretation/application map only;
- this repository — Navier-Stokes specialization, manuscripts, finite experiments, observability certificates, reproduction and claim boundaries.

## Reproduction

Run the development-series/EPSC ledger:

```bash
bash reproduction/reproduce_all.sh
```

For the finite energy-observability paper, use the dedicated lane:

```bash
bash reproduction/reproduce_energy_observability.sh --quick
bash reproduction/reproduce_energy_observability.sh
```

See `reproduction/ENERGY_OBSERVABILITY_REPRODUCE.md` and `reproduction/results/energy_observability_manifest_v1.json` for the pinned environment, expected ranks, provenance hashes and claim boundary.

Volumes 1-6 are the deposited development series. Volume 7 in the reproduction ledger is a later EPSC research lane and should not be confused with the deposited series.

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

Exact modular certificates attain the translation ceiling at the earliest structurally admissible order for four recorded cases: `N=1` total energy, `N=1` shell energies, `N=2` total energy, and `N=3` shell energies. Generic earliest-order saturation for every finite `N` remains `PROP-NSOBS-07` OPEN. A constructive all-cutoff triad-connectivity lemma closes one kinematic obstruction but does not prove the required all-`N` minor nonvanishing/algebraic independence.

## Full N=1 retained inverse: current quantitative chain

At `N=1`, the finite real state dimension is 52. Spatial translation contributes three invisible directions. An explicit translation-transverse 49-dimensional coordinate slice and an exact modular nonzero selected `49x49` shell-energy Taylor-jet minor give a local real inverse on that finite slice.

A deterministic small-integer full-rank center with `max |x_j|=3` anchors successive fail-closed quantitative certificates:

\[
\boxed{
10^{-7934}
\longrightarrow
10^{-3878}
\longrightarrow
10^{-59}
\longrightarrow
10^{-28}.
}
\]

The four stages remove different sources of proof slack:

1. **Uniform Cramer/Hadamard:** `10^-7934 < r <= 10^-7933`, `q<=1/2`.
2. **Row-aware Cramer/Hadamard (`PROP-EPSC-26`):** `10^-3878 < r <= 10^-3877`, improving the lower-bracket scale by 4056 decimal orders.
3. **Exact characteristic-zero preconditioner (`PROP-EPSC-27`):** reconstruct the actual `C^n n!`-scaled integer selected Jacobian `J_0`, cross-check all selected rows modulo `p=1,000,003`, invert `J_0` exactly over `Q`, and certify

   \[
   1.28<\|J_0^{-1}\|_\infty<1.29,
   \qquad
   10^{-59}<r\le10^{-58}.
   \]

   The nonzero exact determinant has 2561 decimal digits.
4. **Componentwise coefficient-tensor enclosure (`PROP-EPSC-28`):** construct the exact scaled `52x52x52` quadratic coefficient tensor, with 2096 nonzero coefficients and exact induced infinity row-sum bound 36000, then propagate componentwise rational state/first-/second-derivative majorants on a radius-`10^-3` local box. With the same exact `A=J_0^{-1}`, the reproduced certificate gives

   \[
   \boxed{10^{-28}<r_{cw}\le10^{-27}},
   \qquad q\le\frac12.
   \]

   This is a further 31-decimal-order improvement over the scalar exact-preconditioner envelope, and the derived radius is certified to lie inside the box used for the majorants.

The result now closes existence of a **strictly positive quantitatively certified full-`N=1` local inverse radius** in a substantially less pessimistic finite enclosure. It still does **not** supply a practical sensor/noise tolerance. A measurement-informative branch-stable `rho_1`, robust noise propagation and arbitrary-`N` inversion remain open.

## Discrete Epsilon-Completion: outer completeness

The fail-closed structure is

\[
\delta_K=\|R_Kx_{K+1}-x_K\|,
\qquad
\|Q_Kx\|_Y\le\beta_{K,Y},
\]

with certification allowed only when finite refinement evidence is paired with a proved/certified omitted-information bound. Small nested defect or boundary-shell energy alone is not a continuum certificate.

For an unforced Leray-Hopf trajectory on the `2*pi` periodic three-torus,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

provides an explicit spacetime `beta_K -> 0` without assuming global smoothness.

A terminal relative-energy route uses a divergence-free comparison path `v`, residual

\[
r=\partial_tv+P[(v\cdot\nabla)v]-\nu\Delta v-Pf,
\]

and

\[
A_T=2\int_0^T\|\nabla v\|_\infty dt,
\qquad
B_T=\int_0^T\|r\|_{H^{-1}}^2dt,
\]

with

\[
\sup_{t\le T}\|u(t)-v(t)\|_2^2
\le
e^{A_T}\left(e_0^2+B_T/\nu\right).
\]

`PROP-EPSC-15` supplies an exact finite piecewise-linear reconstruction of stored binary64 RK4 nodes and rigorous continuous-time residual summaries for the declared tape. Tightness/cost at larger cutoff and horizon is the distinct `PROP-EPSC-16` OPEN frontier.

## Observable-to-continuum synthesis

The two layers answer different questions:

```text
inner completeness:  do observations determine the retained finite state?
outer completeness:  how much continuum state can remain outside the cutoff?
```

If a certified observation layer supplies

\[
\inf_{g\in G}\|P_Nu(T)-g\widehat x_N\|_2\le\rho_N
\]

and EPSC supplies

\[
\|(I-P_N)u(T)\|_2\le\beta_N,
\]

then orthogonality gives

\[
\boxed{
\inf_{g\in G}\|u(T)-g\widehat x_N\|_2
\le\sqrt{\rho_N^2+\beta_N^2}.
}
\]

For the energy-reader application `G=T^3` is spatial translation. `PROP-EPSC-17` records this conditional composition. A mathematical local radius is now available at the one certified full `N=1` chart, but a measurement-derived, branch/noise-stable `rho_1` and arbitrary-`N` analogue are still open.

## Current proposal frontiers

The energy-observability proposal family runs through `PROP-NSOBS-11`. The EPSC proposal family runs through `PROP-EPSC-28`. These are proposal/provenance identifiers, not automatically canonical Toledo theorem codes.

The principal open fronts are:

- `PROP-NSOBS-07` — all-resolution earliest-order generic energy-observability saturation;
- `PROP-EPSC-16` — tighter/scalable outer path certification at larger cutoff/horizon;
- `PROP-EPSC-24` — practical branch-stable, noise-aware full-`N=1` retained-state radius, now narrowed past determinant and scalar-majorant slack;
- `PROP-EPSC-19` — full noisy measurement-to-continuum propagation;
- arbitrary-finite-`N` extension of the explicit retained inverse remains open.

## Finite numerical evidence and non-claim

The short Taylor-Green refinement diagnostic (`nu=0.01`, `dt=0.005`, `T=0.05`) passed its declared nested operational gate at K=4 and K=5. This is a finite diagnostic, not a proof that K=5 contains all continuum information.

The prior negative coarse turbulent validation remains in force: K<=3 did not reproduce the published Re=1600 Taylor-Green dissipation curve in the external-reference test. Finite algebra correctness is therefore distinct from physical or continuum adequacy.

The repository's governing distinction is:

```text
finite observability / finite algebra
    != measurement-ready retained-state inversion
    != continuum mathematical certification
    != physical turbulence validation
```
