# EPSC-19 fixed-N=1 sample interpolation conditioning

Status: finite-first conditioning note. This document sharpens the measurement-interface boundary after the derivative-free finite-time sample-chart existence result.

The fixed-`N=1` structural result uses 49 shell-energy values:

- shell 0 at times `0,h,...,23h`,
- shell 1 at times `0,h,...,23h`,
- shell 2 once at time 0.

The corresponding direct 49-sample map is locally invertible for all sufficiently small nonzero `h` because its Jacobian determinant has a nonzero `h^552` leading coefficient. That statement is structural. It does not by itself give a useful noise factor.

## 1. Conditioning of the Taylor-intermediate route

For either 24-sample primary shell channel, write

\[
y_j=\sum_{n=0}^{23} a_n (jh)^n
\]

for the degree-23 interpolation/truncated-Taylor model. Let

\[
V_{jn}=j^n,\qquad
D_h=\operatorname{diag}(1,h,\ldots,h^{23}).
\]

The existing exact `N=1` retained inverse uses the row-scaled Taylor chart

\[
z_n=s_n a_n,\qquad s_n=600^n n!.
\]

Therefore sample interpolation followed by conversion to the existing scaled chart is exactly

\[
\boxed{z=S D_h^{-1}V^{-1}y.}
\]

Its induced infinity norm is

\[
\boxed{
\kappa_\infty(h)
=
\max_{0\le n\le23}
600^n n!\,|h|^{-n}
\sum_{j=0}^{23}|(V^{-1})_{nj}|.
}
\]

This is an exact finite linear-algebra statement. If `||delta y||_inf<=sigma`, then

\[
\|\delta z\|_\infty\le\kappa_\infty(h)\sigma.
\]

If an independently validated analytic-flow/truncation remainder contributes sample-space radius `r_sample`, replace `sigma` by `sigma+r_sample`.

## 2. Exact N=1 diagnostic

`reproduction/checks/check_volume7_eps19_n1_sample_interpolation_conditioning.py` constructs `V^{-1}` exactly over the rationals by Lagrange interpolation and checks the induced norm without floating matrix inversion.

For nodes `0,...,23`, the highest-order inverse row satisfies

\[
\sum_j |(V^{-1})_{23,j}|=\frac{16}{49308808782358125}.
\]

With the current scales `600^n n!`, order 23 dominates at the tested spacings. Exact power-of-ten brackets are

\[
10^{70}\le\kappa_\infty(1)<10^{71},
\]

\[
10^{93}\le\kappa_\infty(10^{-1})<10^{94},
\]

\[
10^{116}\le\kappa_\infty(10^{-2})<10^{117},
\]

and

\[
10^{134}\le\kappa_\infty(1/600)<10^{135}.
\]

Thus making `h` small enough to support the structural asymptotic invertibility theorem does **not** make the route

\[
\text{samples}\to\text{high-order Taylor coefficients}\to H_1
\]

measurement-ready. The `|h|^{-23}` factor is severe, and the existing `600^n n!` row scaling further enlarges the intermediate coordinates.

## 3. What this changes

This is not a no-go theorem for finite-time energy measurements. The direct sample map

\[
\mathcal S_h(x)
=
(I_0(\phi_{jh}(x)))_{j=0}^{23}
\oplus
(I_1(\phi_{jh}(x)))_{j=0}^{23}
\oplus I_2(x)
\]

need not inherit the conditioning of the explicit interpolation back to the scaled Taylor chart. The next quantitative target should therefore work directly with `D\mathcal S_h`:

\[
A_h\approx D\mathcal S_h(x_*)^{-1},
\qquad
q_h=\sup_{x\in B}\|I-A_hD\mathcal S_h(x)\|_\infty<1.
\]

A validated flow/tangent enclosure over a declared branch would then give a direct sample-noise-to-state radius without numerically recovering derivatives of order 23.

## 4. Claim boundary

This note certifies only the finite interpolation operator and its exact error amplification for the declared `N=1` sample nodes and scaled Taylor rows. It does not yet provide an explicit useful spacing for the direct sample map, a branch-wide `q_h<1`, a sensor model, model-discrepancy bound, branch capture, arbitrary-finite-`N` theorem, continuum tail certificate, Navier--Stokes regularity result, or Clay Millennium solution.
