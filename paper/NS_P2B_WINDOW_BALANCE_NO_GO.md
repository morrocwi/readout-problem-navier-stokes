# NS P2B — window-balance accounting no-go

**Date:** 2026-09-11  
**Parent:** issue #44.  
**Status:** abstract accounting countermodel / negative bridge audit.  
**Claim boundary:** the construction is not an NSE solution and does not respect the full Fourier triad algebra. It refutes only deductions based on shell window balances, transfer conservation, and finite energy/dissipation budgets alone.

## 1. Question

IDM supplies the exact unforced shell identity

\[
\Delta I_s
=
\int_I T_s\,dt
-
2\nu s\int_I I_s\,dt
\]

and finite-system transfer conservation

\[
\sum_s T_s(t)=0.
\]

Could these identities, added to finite energy/dissipation budgets, force the strict P2B anti-intermittency/scale-contraction margin?

No. They are accounting identities; without an additional restriction on the admissible transfer amplitudes/geometry, they allow a critical Zeno cascade.

## 2. Exact integrated countermodel

Choose `2 nu = 1` and dyadic spatial scales

\[
N_j=2^j,
\qquad
s_j=N_j^2.
\]

During episode `j`, prescribe a high-shell plateau with

\[
I_j=N_j^{-1}
\]

for duration

\[
\delta_j=N_j^{-2}.
\]

Its `H1`-squared amplitude is

\[
s_j I_j=N_j,
\]

which is exactly the critical P2B spike amplitude.

The integrated high-shell viscous loss is

\[
D_j
=
s_j I_j\delta_j
=N_j^2\,N_j^{-1}\,N_j^{-2}
=N_j^{-1}.
\]

Let the high shell begin and end the accounting cell with the same shell energy (`Delta I_j=0`). Set its net integrated nonlinear transfer to

\[
Q_j:=\int T_jdt=D_j=N_j^{-1}.
\]

Then the exact integrated shell balance holds:

\[
0=Q_j-D_j.
\]

Introduce a donor/reservoir shell and set

\[
Q_j^{res}=-Q_j,
\]

so integrated nonlinear transfer is exactly conservative on the two-shell accounting block:

\[
Q_j+Q_j^{res}=0.
\]

Any nonnegative finite reservoir viscous cost `d_j^{res}` can be included by defining its energy decrement to be

\[
\Delta I_j^{res}=Q_j^{res}-d_j^{res}.
\]

For the exact calibration choose

\[
d_j^{res}=N_j^{-2}.
\]

All cumulative costs remain finite:

\[
\sum_j D_j=\sum_j2^{-j}<\infty,
\qquad
\sum_j d_j^{res}=\sum_j4^{-j}<\infty,
\qquad
\sum_j\delta_j=\sum_j4^{-j}<\infty.
\]

Thus a sufficiently large finite initial reservoir can support the entire abstract sequence while satisfying the integrated accounting identities.

## 3. Observation scaling remains critical

For `p>2`, the high-shell episode contributes

\[
K_{N_j}^2
\sim
\left[
(N_j)^p N_j^{-2}
\right]^{1/p}
=N_j^{1-2/p}.
\]

At `p=4`,

\[
(K_{N_j}^2)^4=N_j^2=\Lambda_j,
\]

so the dimensionless critical ratio from `NS_P2B_SCALE_CONTRACTION.md` is

\[
R_j=1.
\]

There is no strict scale contraction.

## 4. What this falsifies

The following inference is invalid:

```text
exact shell time-window balance
+ conservation of nonlinear transfer across shells
+ finite total energy/dissipation accounting
    -> strict anti-intermittency / scale contraction.
```

The countermodel satisfies the premises at the integrated accounting level while maintaining critical observation spikes.

This is stronger than the earlier energy-only no-go because it explicitly incorporates the two IDM identities that initially motivated the P2B route.

## 5. What it does not falsify

The countermodel does **not** satisfy the full Navier--Stokes Fourier interaction law. In particular it does not enforce:

- exact triad incidence and coefficients;
- divergence-free polarization constraints inside every transfer event;
- phase/coherence constraints;
- locality/nonlocality restrictions actually implied by the quadratic convolution;
- a pointwise-in-time realization of the prescribed integrated transfer record by one NSE trajectory.

Therefore it does not refute a proof based on genuine triadic structure.

## 6. Refined residual theorem

After this no-go, `NS-P2B-SCALE-CONTRACTION-UNIFORM` cannot be obtained from conservation/accounting alone. A successful proof must establish an additional **triadic transfer tax / contraction law** for actual NSE interactions.

A useful target has the form

\[
R_{j+1}\le\kappa R_j+\beta_j,
\qquad
\kappa<1,
\qquad
\beta_j\to0,
\]

where the strict `kappa<1` is derived from the true quadratic convolution, viscosity, incompressibility, and certified time-window structure rather than postulated.

**Status:** accounting-only route REFUTED.  
**Triad-level uniform contraction:** OPEN/HOLD.  
**Clay Navier--Stokes:** OPEN.
