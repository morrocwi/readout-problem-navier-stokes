# A Readout Problem for Fefferman's Existence and Smoothness of the Navier-Stokes Equation

Author: Yaoharee Lahtee. License: CC BY 4.0 (see `LICENSE`). Original paper DOI: [10.5281/zenodo.22673246](https://doi.org/10.5281/zenodo.22673246).

This repository contains three clearly separated research layers:

1. the deposited v0.1.0 readout paper (`paper/main.tex`, `paper/main.pdf`), which poses the Navier-Stokes readout dichotomy and proves finite-state/retained-layer results;
2. the finite **energy-observability** lane, which studies what total/shell energy histories determine inside a fixed Fourier-Galerkin state modulo translation; and
3. the later **Discrete Epsilon-Completion (EPSC)** lane, which develops finite-to-continuum omitted-information certificates and composes them with finite observability.

**None of these layers proves global regularity, finite-time blow-up, uniqueness of arbitrary weak solutions, or the Clay Millennium Navier-Stokes problem.** See `CLAIMS.md`.

## Papers and analytic notes

- `paper/main.tex`, `paper/main.pdf` — original deposited paper; not overwritten by later work.
- `paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex`, `.pdf` — finite-resolution energy observability and structural ceilings.
- `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex`, `.pdf` — standalone EPSC manuscript.
- `paper/NS_OBSERVABLE_TO_CONTINUUM_CERTIFICATES.tex` — synthesis connecting certified finite observability to certified continuum error budgets.
- `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` — Leray-Hopf spacetime Fourier-tail certificate.
- `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` — terminal a-posteriori energy-budget certificate.
- `paper/NS_RELATIVE_ENERGY_ADAPTER_CERTIFICATE.md` — relative-energy adapter and exact continuous-time RK4-tape enclosure.
- `paper/NS_EPSC18_N1_ROWWISE_RADIUS.md` — full-`N=1` local inverse and row-aware quantitative-radius tightening.

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

For the final finite energy-observability paper, use the dedicated lane:

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

Exact modular certificates attain the translation ceiling at the earliest structurally admissible order for four recorded cases: `N=1` total energy, `N=1` shell energies, `N=2` total energy, and `N=3` shell energies. Generic earliest-order saturation for every finite `N` remains `PROP-NSOBS-07` OPEN.

A constructive all-cutoff triad-connectivity lemma removes one kinematic obstruction to that conjecture, but does not prove nonvanishing/algebraic independence of enough observation minors.

## Full N=1 retained inverse

At `N=1`, the finite real state dimension is 52. Spatial translation contributes three invisible directions, and an explicit translation-transverse 49-dimensional coordinate slice has been constructed. An exact modular certificate supplies a nonzero selected 49-by-49 shell-energy Taylor-jet minor, hence a local real inverse exists on that finite slice.

A deterministic small-integer full-rank center with `max |x_j|=3` was found. The first quantitative proof used one worst-row Cramer/Hadamard bound and certified

\[
10^{-7934}<r_{\rm uniform}\le10^{-7933},
\qquad q\le\frac12.
\]

The row-aware refinement `PROP-EPSC-26` keeps one Jacobian-row and one Hessian-row majorant per selected observation. If

\[
R_j\ge\|J_{0,j*}\|_1,
\qquad
H_j\ge\sup_{x\in B}\|D J_{j*}(x)\|_{\infty\to1},
\]

then

\[
\|J_0^{-1}(J(x)-J_0)\|_\infty
\le
r\sum_j\left(\prod_{k\ne j}R_k\right)H_j.
\]

Choosing

\[
\boxed{
r_{\rm row}=\frac{1}{2\sum_j(\prod_{k\ne j}R_k)H_j}
}
\]

again gives `q<=1/2`. The reproduced denominator drops from 7934 to 3878 decimal digits, so

\[
\boxed{10^{-3878}<r_{\rm row}\le10^{-3877}.}
\]

This is a 4056-decimal-order improvement in the rigorous power-of-ten bracket. It closes existence of a **strictly positive quantitative full-`N=1` local inverse radius**, but it is still astronomically too small to call measurement-ready. The practical `rho_1` problem remains `PROP-EPSC-24` OPEN and requires an actual entrywise interval Jacobian, an effective rational preconditioner, branch containment and noise propagation.

## Discrete Epsilon-Completion: outer completeness

The base fail-closed structure is

\[
\delta_K=\|R_Kx_{K+1}-x_K\|,
\qquad
\|Q_Kx\|_Y\le\beta_{K,Y},
\]

with certification allowed only when refinement evidence is paired with a proved/certified omitted-information bound. A small nested defect or boundary-shell energy alone is not a continuum certificate.

For an unforced Leray-Hopf trajectory on the `2*pi` periodic three-torus,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

provides an explicit spacetime `beta_K -> 0` without assuming global smoothness.

A terminal relative-energy route uses a divergence-free comparison path `v` with residual

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

For the energy-reader application `G=T^3` is spatial translation. `PROP-EPSC-17` records this conditional composition.

The present full-`N=1` result supplies a mathematical positive local radius, not yet a useful measurement-derived `rho_1`. Arbitrary-`N`, branch-stable and noise-stable inversion therefore remains open.

## Toledo lineage and current frontiers

The energy-observability proposal family runs through `PROP-NSOBS-11`. The EPSC proposal family currently runs through `PROP-EPSC-26`. These are proposal/provenance identifiers, not automatically canonical Toledo theorem codes.

The major open problems are deliberately separated:

- `PROP-NSOBS-07` — prove/refute earliest-order generic energy-observability saturation for every finite resolution;
- `PROP-EPSC-16` — make outer path certification tighter and scalable for larger cutoff/horizon;
- `PROP-EPSC-24` — replace the conservative full-`N=1` determinant/derivative radius by an effective measurement-scale interval/preconditioned `rho_1`;
- `PROP-EPSC-19` — propagate measurement/window uncertainty through that retained inverse and the outer EPSC certificate.

## Finite numerical evidence and non-claim

The short Taylor-Green refinement diagnostic (`nu=0.01`, `dt=0.005`, `T=0.05`) passed its declared nested operational gate at K=4 and K=5. This remains a finite diagnostic, not a proof that K=5 contains all continuum information.

The prior negative coarse turbulent validation also remains in force: K<=3 did not reproduce the published Re=1600 Taylor-Green dissipation curve in the external-reference test. Finite algebra correctness is therefore distinct from physical/continuum adequacy.

The repository's governing distinction is:

```text
finite observability / finite algebra
    != measurement-ready retained-state inversion
    != continuum mathematical certification
    != physical turbulence validation
```
