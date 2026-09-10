# Claim boundaries

This repository contains an original deposited v0.1.0 paper and a later EPSC research lane. They must not be conflated. Read this file before citing either layer.

## Original deposited paper

| Claim | Status |
|---|---|
| There is a finite 8-state system with an admissible domain reading for which no finite observation horizon decides a nonconstant domain question | **Proved** in the deposited paper; independently re-verified by exact enumeration |
| Exact domain-dynamics welding and reader factorization generally imply finite-horizon decidability of an arbitrary domain question | **Refuted** by the same finite witness |
| The Navier-Stokes readout dichotomy (R)/(N) is answered by the deposited paper | **No. Posed, not answered.** |
| A finite retained-turbulence linear layer with finite dimension, positive time constant, fixed finite generator and locally integrable drive has a unique bounded finite-interval solution | **Proved** by standard finite-dimensional ODE analysis |
| The deposited paper solves or partially solves the Clay Millennium Navier-Stokes problem | **Explicitly not claimed.** |

## Later standalone EPSC manuscript / research lane

Current manuscript source: `paper/EPSC_NAVIER_STOKES_CERTIFICATES.tex`, titled *Finite Readout Certificates for Navier-Stokes: Discrete Epsilon-Completion, Spectral Tails, and A Posteriori Adapters*.

This lane assembles later EPSC results and executable checks but does not retroactively modify the deposited v0.1.0 paper.

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
| A stored binary64 RK4 node tape can be turned into a rigorous continuous-time finite comparison path without assuming the RK4 recurrence is the exact PDE | **Yes for the declared periodic Fourier setting.** `PROP-EPSC-15`: interpret stored floats as exact dyadic rationals, Leray-project exactly, and join nodes piecewise linearly |
| `A_T` and `B_T` for that piecewise-linear path can be bounded rigorously over the whole continuous interval rather than sampled only at nodes | **Finite diagnostic PASS.** The residual is degree <=2 per time cell, its H^-1 norm squared integrates exactly as a rational degree <=4 polynomial, and the gradient integral is bounded by a rational Fourier-l1 majorant |
| The resulting exponential can be used without hidden downward floating rounding | **Yes in the finite checker.** `exp(A_bar)` is upper-bounded by a rational Taylor sum plus geometric remainder and the displayed beta is rounded upward with integer arithmetic |
| The short K=1 Taylor-Green EPSC-15 witness proves K=1 is a physically adequate Navier-Stokes turbulence resolution | **No.** It proves the declared path-certificate construction on that finite run; adequacy and tightness are separate claims |
| The EPSC family is registered in Toledo | **Yes, as proposals rather than canonical verified theorem codes, through `PROP-EPSC-16`.** `PROP-EPSC-16` is the open high-cutoff tightness/scaling frontier |
| The EPSC results solve the Clay Millennium problem | **No.** They neither prove global smoothness nor finite-time blow-up and do not establish uniqueness of arbitrary 3-D weak solutions |
| The short refinement result overturns the prior negative coarse Taylor-Green turbulent validation | **No.** Nested short-horizon stability, a posteriori mathematical certification, and external physical/DNS adequacy are different claims |

## Current end-to-end chain

```text
stored binary64 RK4 node tape
    -> exact dyadic capture + exact Leray projection
    -> continuous piecewise-linear K-supported comparison path
    -> exact/rigorous A_bar_T and B_bar_T
    -> PROP-EPSC-13 relative-energy theorem (Dr)
    -> terminal continuum L2 / omitted-tail beta_K
    -> fail-closed epsilon certificate for the declared target
```

This closes the **continuous-time enclosure obligation** formerly labelled OPEN as `PROP-EPSC-15`. The next engineering question is `PROP-EPSC-16`: whether these conservative bounds can remain tight and computationally affordable for substantially larger `K` and longer `T`.

The key methodological rule is unchanged: **finite algebra / nested stability does not by itself imply continuum completion, and continuum mathematical certification does not by itself imply physical turbulence validation.**
