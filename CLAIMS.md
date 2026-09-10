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
| Total-energy Lie-jet rank obeys `rank D E_R <= min(R+1,d_N-3)` and therefore cannot reach the translation ceiling before `R=d_N-4` | **Derived analytic (`Dr`) structural ceiling.** |
| Full shell-energy Lie-jet rank obeys `rank D J_R <= min(m_N+(m_N-1)R,d_N-3)` with the stated structural minimum depth | **Derived analytic (`Dr`) structural ceiling.** |
| Energy-observability jet ranks are independent of the value of every positive viscosity | **Derived analytic (`Dr`) result** from the finite NS scaling. The endpoint `nu=0` is separate. |
| Exact modular certificates reach the translation ceiling in the four recorded cases `N=1` total, `N=1` shell, `N=2` total, `N=3` shell | **Finite exact certificate evidence.** |
| Those saturation records imply local finite-state completeness modulo spatial translations at generic free-action states | **Derived local quotient statement (`Dr`).** Not global injectivity. |
| The structural formulas expose a measurement-channel versus temporal-depth tradeoff | **Derived structural statement.** At `N=3`, one scalar channel has lower bound `R>=680`, while the 18-shell reader is exactly saturated at `R=39`. |
| The same earliest-order saturation holds generically for every finite resolution `N` | **OPEN conjecture (`PROP-NSOBS-07`).** The four recorded exact cases do not prove it. |
| Saturated rank alone gives a certified numerical inverse with known error radius under noisy measurements | **No.** Rank is local qualitative identifiability; conditioning, branch control, quantitative radius and noise propagation remain open. |

The observability proposal family is registered in Toledo as `PROP-NSOBS-01..08`.

## Standalone EPSC research lane

Primary source: `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex` / `.pdf`.

| EPSC claim | Status |
|---|---|
| The finite Fourier-Galerkin NS recurrence can be executed directly on integer Fourier records and ordered triads without constructing a spatial grid in its production path | **Finite implementation statement.** Not an ontological claim about continuum space |
| Direct-triad and padded-FFT implementations agree on the recorded K=2 finite state | **Finite diagnostic PASS.** Max RHS difference `1.041e-16`; one-RK4-step difference `8.674e-19` |
| The short Taylor-Green run (`nu=0.01`, `dt=0.005`, `T=0.05`) passes the declared nested operational gate at K=4 and K=5 | **Finite diagnostic PASS.** K=4 `delta=3.551e-08`; K=5 `delta=7.741e-10` |
| K=5 therefore contains all continuum NS information | **No.** Nested agreement and boundary energy alone do not bound the complete omitted tail |
| Low terminal Fourier coefficients alone identify a finite universal omitted-tail bound over unrestricted divergence-free L2 terminal states | **No. Analytic obstruction.** An arbitrary divergence-free conjugate pair can be placed entirely above the cutoff without changing the retained record |
| Spectral `H^s -> L2` tail inequality | **Standard analytic (`Dr`) result.** Registered for role/provenance, not originality |
| Unforced Leray-Hopf spacetime certificate `||(I-P_K)u||_{L2_tL2_x} <= ||u0||/(sqrt(2 nu)(K+1))` | **Derived at analytic (`Dr`) tier.** Gives a computable `beta_K -> 0` in the declared spacetime norm without global smoothness |
| Forced spacetime analogue for `f in L2_t H^-1` | **Derived at analytic (`Dr`) tier** under the declared normalization |
| Lipschitz readouts inherit a certified state-space tail bound | **Derived at analytic (`Dr`) tier** |
| A terminal certificate follows from a separately certified pointwise H^s bound | **Conditional analytic statement** |
| A terminal L2 bound follows from a certified retained energy/dissipation tape | **Derived at analytic (`Dr`) tier.** For actual continuum projection/directional certificates, `tail^2 <= U0^2 - L_K(T)^2 - 2D_K(T)` |
| The energy-budget certificate necessarily tends to zero for every Leray-Hopf solution | **No.** Its exact-projection asymptotic squared floor is the energy-inequality slack; it closes to zero under independently justified energy equality |
| Raw values from a finite Galerkin solver may be silently identified with the actual continuum projection | **No.** A proved/certified adapter is required |
| Residual-based relative-energy estimate `sup ||u-v||_2^2 <= exp(A_T)(e0^2+B_T/nu)` for a divergence-free comparison path | **Standard analytic (`Dr`) estimate specialized to EPSC.** Under the declared hypotheses it supplies a terminal continuum bound when `v(T)` is K-supported |
| The finite Fourier residual of a K-supported comparison path is finite-computable, including its homogeneous H^-1 norm | **Finite algebra/definition with checker support.** |
| A stored binary64 RK4 node tape can be turned into a rigorous continuous-time finite comparison path without assuming the RK4 recurrence is the exact PDE | **Yes for the declared periodic Fourier setting.** `PROP-EPSC-15`: exact dyadic capture, exact Leray projection, continuous piecewise-linear path |
| `A_T` and `B_T` for that path can be bounded rigorously over the whole continuous interval rather than sampled only at nodes | **Finite diagnostic PASS.** The residual is degree <=2 per time cell, its H^-1 norm squared integrates exactly as a rational degree <=4 polynomial, and the gradient integral is bounded by a rational Fourier-l1 majorant |
| The resulting exponential can be used without hidden downward floating rounding | **Yes in the finite checker.** `exp(A_bar)` is upper-bounded by a rational Taylor sum plus geometric remainder and the displayed beta is rounded upward with integer arithmetic |
| The short K=1 Taylor-Green EPSC-15 witness proves K=1 is a physically adequate turbulence resolution | **No.** It proves the declared path-certificate construction only |
| EPSC-15 remains open | **No.** The declared finite-tape continuous-time construction has executable evidence; high-cutoff tightness/scaling is separated as `PROP-EPSC-16` OPEN |

## Observable-to-continuum synthesis lane

Primary source: `paper/NS_OBSERVABLE_TO_CONTINUUM_CERTIFICATES.tex`.

The synthesis separates **inner completeness** (what observations determine inside `P_N`) from **outer completeness** (how much state may remain in `Q_N`).

| Synthesis claim | Status |
|---|---|
| If a certified finite observation/inversion layer supplies `inf_g ||P_N u(T)-g xhat_N||_2 <= rho_N` and EPSC supplies `||Q_N u(T)||_2 <= beta_N`, then `inf_g ||u(T)-g xhat_N||_2 <= sqrt(rho_N^2+beta_N^2)` | **Derived analytic composition (`PROP-EPSC-17`).** Follows from orthogonality of the retained and omitted Fourier subspaces |
| The generic triangle bound `rho_N+beta_N` is the sharp composition required here | **No.** Orthogonality permits the sharper Pythagorean radius `sqrt(rho_N^2+beta_N^2)` |
| The unavoidable spatial-translation ambiguity in invariant energy readers prevents a quotient-state continuum certificate | **No.** The composition theorem is naturally stated modulo the isometric translation group preserving the cutoff |
| Existing rank saturation already supplies the quantitative `rho_N` required by the composition theorem | **No.** This is precisely the open `PROP-EPSC-18` certified energy-jet inversion-radius problem |
| A noise-stable end-to-end certificate from measured energy time series is already proved | **No. OPEN (`PROP-EPSC-19`).** Measurement noise, numerical differentiation, conditioning and branch stability must be certified |
| `PROP-EPSC-16` and the observability inverse are the same frontier | **No.** `EPSC-16` is outer-certificate cost/tightness; `EPSC-18/19` are inner reconstruction and noise-stability problems |
| All-resolution energy saturation is required for the conditional composition theorem itself | **No.** `EPSC-17` is a general conditional composition rule. `NSOBS-07` is separately needed for an all-resolution observability statement |

The EPSC family is registered in Toledo through `PROP-EPSC-19`; the energy-observability family is registered as `PROP-NSOBS-01..08`. These remain proposal/provenance records, not automatically canonical verified Toledo theorem codes.

## Current measurement-to-continuum chain

```text
energy measurements / Lie jets
    -> certified retained-state quotient radius rho_N       [PROP-EPSC-18 OPEN]
    -> retained finite state / comparison path
    -> certified omitted-tail beta_N                        [EPSC family; EPSC-15 supplies one path adapter]
    -> sqrt(rho_N^2 + beta_N^2)                             [PROP-EPSC-17]
    -> fail-closed continuum L2 tolerance verdict modulo translation
```

The major open frontiers are deliberately distinct:

```text
PROP-NSOBS-07  all-resolution earliest-order saturation
PROP-EPSC-16   scalable/tight outer path certification
PROP-EPSC-18   certified quantitative energy-jet inverse
PROP-EPSC-19   noise-stable measurement-to-continuum propagation
```

The key methodological rule is unchanged: **finite observability or finite algebra does not by itself imply a certified finite reconstruction radius; a certified finite reconstruction does not by itself bound the omitted continuum tail; continuum mathematical certification does not by itself imply physical turbulence validation.**
