# Claim boundaries

This repository contains an original deposited v0.1.0 paper plus later finite-observability and EPSC research lanes. They must not be conflated. Read this file before citing any layer.

## Original deposited paper

| Claim | Status |
|---|---|
| There is a finite 8-state system with an admissible domain reading for which no finite observation horizon decides a nonconstant domain question | **Proved** in the deposited paper; independently re-verified by exact enumeration |
| Exact domain-dynamics welding and reader factorization generally imply finite-horizon decidability of an arbitrary domain question | **Refuted** by the same finite witness |
| The Navier-Stokes readout dichotomy (R)/(N) is answered by the deposited paper | **No. Posed, not answered.** |
| A finite retained-turbulence linear layer with finite dimension, positive time constant, fixed finite generator and locally integrable drive has a unique bounded finite-interval solution | **Proved** by standard finite-dimensional ODE analysis |
| The deposited paper solves or partially solves the Clay Millennium Navier-Stokes problem | **Explicitly not claimed.** |

## Energy-observability research lane

Primary source: `paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex` / `.pdf`.

| Energy-observability claim | Status |
|---|---|
| The declared real finite Fourier-Galerkin phase-space dimension is `d_N=2((2N+1)^3-1)` | **Definition/bookkeeping.** |
| Total-energy Lie-jet rank obeys `rank D E_R <= min(R+1,d_N-3)` and cannot reach the translation ceiling before `R=d_N-4` | **Derived analytic (`Dr`) structural ceiling.** |
| Full shell-energy Lie-jet rank obeys `rank D J_R <= min(m_N+(m_N-1)R,d_N-3)` with the stated structural minimum depth | **Derived analytic (`Dr`) structural ceiling.** |
| Energy-observability jet ranks are independent of every positive viscosity value | **Derived analytic (`Dr`) result** from finite NS scaling. The endpoint `nu=0` is separate. |
| Exact modular certificates reach the translation ceiling in the four recorded cases `N=1` total, `N=1` shell, `N=2` total, `N=3` shell | **Finite exact certificate evidence.** |
| Those saturation records imply local finite-state completeness modulo spatial translations at generic free-action states | **Derived local quotient statement (`Dr`).** Not global injectivity. |
| Shell energy admits `dI_s/dt=T_s-2 nu s I_s+F_s`, with `sum_s T_s=0` in the unforced closed finite system | **Standard finite NS identity**, registered as `PROP-NSOBS-09`. |
| `(I,T)` has extra local rank beyond `(I,dI/dt)` for prescribed forcing | **No.** `T=dI/dt+2 nu S I-F`; they are invertibly related and have the same local rank (`PROP-NSOBS-10`). |
| Every new boundary mode is kinematically disconnected from the preceding cutoff | **No.** For every `N>=2`, a constructive non-collinear triad connects each new boundary mode to an old mode (`PROP-NSOBS-11`); finite sweep verified through `N=8`. |
| Earliest-order saturation holds generically for every finite `N` | **Still OPEN (`PROP-NSOBS-07`).** Connectivity is closed; the needed all-`N` nonvanishing/algebraic-independence statement remains open. |

The observability proposal family is registered in Toledo as `PROP-NSOBS-01..11`.

## Full N=1 symmetry-slice inverse

Primary sources:

- `reproduction/checks/check_volume7_eps18_n1_local_inverse.py`
- `reproduction/checks/check_volume7_eps18_n1_small_witness.py`
- `reproduction/checks/check_volume7_eps18_n1_explicit_radius.py`
- `reproduction/checks/check_volume7_eps18_n1_rowwise_radius.py`
- `paper/NS_EPSC18_N1_ROWWISE_RADIUS.md`

| Full-N=1 inverse claim | Status |
|---|---|
| The `N=1` real finite Fourier-Galerkin state has dimension 52 and energy readers have a three-dimensional translation kernel | **Finite/analytic structure.** |
| An explicit three-coordinate gauge is transverse to translation and leaves a 49-dimensional slice | **Finite exact certificate PASS.** |
| A selected 49-by-49 shell-energy Taylor-jet minor is nonzero | **Finite exact certificate PASS.** Nonzero good-prime reduction implies the corresponding rational minor is nonzero. |
| A local real inverse exists on that full 49-dimensional finite symmetry slice | **Derived (`Dr`).** Ordinary finite-dimensional inverse-function theorem after the exact nonzero minor certificate. |
| A small-integer full-rank center exists | **Finite exact certificate PASS.** Deterministic seed `20260910`, `max |x_j|=3`. |
| There exists an explicit strictly positive quantitative local-inverse radius | **Derived (`Dr`). CLOSED at fixed `N=1`.** The first conservative Cramer/Hadamard construction gives `10^-7934 < r <= 10^-7933` with `q<=1/2`. |
| Retaining one row majorant per selected observation improves that rigorous radius | **Derived/PASS.** The row-aware construction gives `10^-3878 < r <= 10^-3877`; the denominator loses 4056 decimal digits relative to the uniform-row proof. |
| The present radius is a realistic sensor/noise tolerance | **No.** It remains astronomically small and is only a conservative mathematical existence/conditioning certificate. |
| A practically informative measurement-derived `rho_1` is already available | **No. OPEN (`PROP-EPSC-24`).** An actual entrywise interval Jacobian, effective rational preconditioner, branch containment and noise propagation are still required. |
| The fixed-`N=1` local inverse proves arbitrary-`N` inversion | **No.** No automatic extension to arbitrary finite cutoff is claimed. |

The Toledo proposal chain for this stage is `PROP-EPSC-22..26`. These are proposal/provenance identifiers, not canonical verified theorem codes.

## Energy-transfer observability bridge

Primary source: `reproduction/NS_ENERGY_TRANSFER_OBSERVABILITY_BRIDGE.md` and `reproduction/checks/check_volume7_energy_transfer_observability.py`.

Internal energy transfer is useful because it keeps shell-to-shell redistribution visible and permits finite-window balance measurements. It does **not** evade the Lie-jet rank ceiling, since `(I,T)` and `(I,dI/dt)` are equivalent coordinates at first order for prescribed forcing.

The analytic three-mode reduced subcase has the explicit quantitative inverse

`r=(J1_a+2 nu x)/(2 c_a)`, `c_a=3/10`,

with

`|r-rhat| <= (sigma_J+2 nu sigma_x)/(2|c_a|)`.

At `nu=1/200`, this is `(5/3) sigma_J + (1/60) sigma_x`. This is `PROP-EPSC-20` and should not be confused with the separate full-`N=1` 49-dimensional result above.

The integrated shell balance

`int T_s dt = I_s(t1)-I_s(t0)+2 nu s int I_s dt-int F_s dt`

admits direct interval-radius propagation. This is `PROP-EPSC-21` and removes numerical differentiation from one EPSC-19 substep; it does not itself give a full noisy state inverse.

## Standalone EPSC research lane

Primary source: `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex` / `.pdf` and later analytic notes.

| EPSC claim | Status |
|---|---|
| The finite Fourier-Galerkin NS recurrence can be executed directly on integer Fourier records and ordered triads without constructing a spatial grid in its production path | **Finite implementation statement.** Not an ontological claim about continuum space. |
| Direct-triad and padded-FFT implementations agree on the recorded K=2 finite state | **Finite diagnostic PASS.** Max RHS difference `1.041e-16`; one-RK4-step difference `8.674e-19`. |
| The short Taylor-Green run (`nu=0.01`, `dt=0.005`, `T=0.05`) passes the declared nested operational gate at K=4 and K=5 | **Finite diagnostic PASS.** K=4 `delta=3.551e-08`; K=5 `delta=7.741e-10`. |
| K=5 therefore contains all continuum NS information | **No.** Nested agreement and boundary energy alone do not bound the complete omitted tail. |
| Low terminal Fourier coefficients alone identify a universal finite omitted-tail bound over unrestricted divergence-free L2 terminal states | **No. Analytic obstruction.** Arbitrary divergence-free high modes can leave the retained record unchanged. |
| Spectral `H^s -> L2` tail inequality | **Standard analytic (`Dr`) result.** Registered for role/provenance, not originality. |
| Unforced Leray-Hopf spacetime certificate `||(I-P_K)u||_{L2_tL2_x} <= ||u0||/(sqrt(2 nu)(K+1))` | **Derived analytic (`Dr`).** Gives a computable `beta_K -> 0` in the declared spacetime norm without global smoothness. |
| Forced spacetime analogue for `f in L2_t H^-1` | **Derived analytic (`Dr`)** under the declared normalization. |
| Lipschitz readouts inherit a certified state-space tail bound | **Derived analytic (`Dr`).** |
| A terminal certificate follows from a separately certified pointwise H^s bound | **Conditional analytic statement.** |
| A terminal L2 bound follows from a certified retained energy/dissipation tape | **Derived analytic (`Dr`).** For actual continuum projection/directional certificates, `tail^2 <= U0^2 - L_K(T)^2 - 2D_K(T)`. |
| The energy-budget certificate necessarily tends to zero for every Leray-Hopf solution | **No.** Its exact-projection asymptotic floor includes the energy-inequality slack; closure to zero requires independently justified energy equality. |
| Raw finite-Galerkin values may be silently identified with the actual continuum projection | **No.** A proved/certified adapter is required. |
| Residual-based relative-energy estimate `sup ||u-v||_2^2 <= exp(A_T)(e0^2+B_T/nu)` for a divergence-free comparison path | **Standard analytic (`Dr`) estimate specialized to EPSC.** |
| The finite Fourier residual of a K-supported comparison path is finite-computable, including its homogeneous H^-1 norm | **Finite algebra/definition with checker support.** |
| A stored binary64 RK4 node tape can be turned into a rigorous continuous-time finite comparison path without assuming the RK4 recurrence is the exact PDE | **Yes for the declared periodic Fourier setting (`PROP-EPSC-15`).** Exact dyadic capture, exact Leray projection, continuous piecewise-linear path. |
| `A_T` and `B_T` can be bounded over the whole continuous interval rather than sampled only at nodes | **Finite diagnostic PASS.** |
| EPSC-15 remains open | **No.** The declared finite-tape continuous-time construction is executable; high-cutoff tightness/scaling is separated as `PROP-EPSC-16` OPEN. |
| The short K=1 Taylor-Green path certificate proves K=1 is physically adequate turbulence resolution | **No.** It certifies the declared path construction only. |

## Observable-to-continuum synthesis lane

Primary source: `paper/NS_OBSERVABLE_TO_CONTINUUM_CERTIFICATES.tex`.

The synthesis separates **inner completeness** (what observations determine inside `P_N`) from **outer completeness** (how much state may remain in `Q_N`).

| Synthesis claim | Status |
|---|---|
| If `inf_g ||P_N u(T)-g xhat_N||_2 <= rho_N` and `||Q_N u(T)||_2 <= beta_N`, then `inf_g ||u(T)-g xhat_N||_2 <= sqrt(rho_N^2+beta_N^2)` | **Derived analytic composition (`PROP-EPSC-17`).** Orthogonality gives the Pythagorean radius. |
| The generic triangle bound `rho_N+beta_N` is the sharp composition required here | **No.** Orthogonality gives the sharper square-root composition. |
| Translation ambiguity prevents a quotient-state continuum certificate | **No.** The composition is naturally stated modulo the isometric translation group. |
| Rank saturation alone already supplies `rho_N` | **No.** Rank alone does not. For full `N=1`, later work supplies a strictly positive local radius, but a practical measurement-derived `rho_1` is still missing. |
| No quantitative inner inverse exists anywhere in the programme | **No.** There is a reduced three-mode quantitative inverse (`PROP-EPSC-20`) and now a full-`N=1` strictly positive local radius (`PROP-EPSC-22..26`). |
| A noise-stable end-to-end certificate from measured energy time series is already proved | **No. Full problem remains OPEN (`PROP-EPSC-19`).** Measurement-scale conditioning/branch stability remains missing. |
| All-resolution energy saturation is required for the conditional composition theorem itself | **No.** `PROP-EPSC-17` is conditional and resolution-local; `PROP-NSOBS-07` is the separate all-resolution observability question. |

The EPSC proposal family is registered in Toledo through `PROP-EPSC-26`; energy observability is registered through `PROP-NSOBS-11`. Proposal identifiers are not automatically canonical Toledo theorem codes.

## Current measurement-to-continuum chain

```text
shell-energy measurements / finite windows
    -> certified transfer summaries                         [NSOBS-09/10; EPSC-21]
    -> full N=1 local retained inverse exists               [EPSC-22]
    -> explicit strictly positive N=1 radius                [EPSC-25/26]
    -> practical measurement-derived rho_1                  [EPSC-24 OPEN]
    -> certified omitted-tail beta_N                        [EPSC outer lane]
    -> sqrt(rho_N^2 + beta_N^2)                             [EPSC-17]
    -> fail-closed continuum L2 tolerance verdict modulo translation
```

The major open frontiers are now narrower and deliberately distinct:

```text
PROP-NSOBS-07  all-resolution earliest-order saturation: connectivity closed; minor independence open
PROP-EPSC-16   scalable/tight outer comparison-path certification
PROP-EPSC-24   practical entrywise/preconditioned full-N=1 measurement radius
PROP-EPSC-19   full noisy measurement-to-continuum propagation
```

The methodological rule remains: **finite observability or finite algebra does not automatically imply a useful retained reconstruction radius; a certified retained reconstruction does not automatically bound the omitted continuum tail; continuum mathematical certification does not automatically imply physical turbulence validation.**
