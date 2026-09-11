# NS-FUB-A1C — Residual-Centered Validated Tube

**Date:** 2026-09-11  
**Status:** fixed-`N=1` candidate until dedicated CI is green.  
**Parent issue:** `#31`.

## Why the previous absolute tube is not enough

The absolute tube rule is sound but can destroy state localization. For the trivial ODE

\[
x'=1,\qquad x(0)=0,
\]

propagating only

\[
I_{m+1}=I_m+[-h,h]
\]

for `n` equal steps with `T=nh` yields the interval `[-T,T]`. Its halfwidth is `T` no matter how fine the mesh is.

Therefore failure or excessive width of this certificate class is not a dynamical obstruction and must never be promoted to a Navier--Stokes singularity witness.

The reference path `p(t)=t`, by contrast, has residual exactly zero.

## Residual-centered certificate

For a rational reference path

\[
p(t)=a+t v,
\]

an incoming exact point `a` in the present calibration, and a tube

\[
\|x(t)-p(t)\|_\infty\le r,
\]

compute exact bounds on the full path/error tube:

\[
R\ge\sup\|F(p(t)+e)-v\|_\infty,
\qquad
L\ge\sup\|DF\|_\infty.
\]

The fail-closed gates are

\[
hR\le r,
\qquad
hL<1.
\]

For the Picard error operator

\[
(\mathcal Te)(t)=\int_0^t \bigl(F(p(s)+e(s))-p'(s)\bigr)\,ds,
\]

the first inequality gives a self-map of the error tube and the second gives a contraction. Hence the exact finite Galerkin trajectory lies in the residual tube and its endpoint lies in

\[
p(h)+[-r,r]^d.
\]

The key difference is that the endpoint center moves with the reference path.

## N=1 affine predictor calibration

The executable

`reproduction/checks/check_ns_fub_a1c_n1_residual_tube.py`

uses the exact existing `N=1` Galerkin tensor and the Euler predictor

\[
v=F(a),\qquad p(t)=a+tF(a).
\]

It searches a finite declared list of rational step sizes and uses `r=h/10`, accepting only a candidate whose exact residual and Lipschitz intervals satisfy stronger half-margin gates

\[
hR/r\le1/2,
\qquad
hL\le1/2.
\]

The endpoint box is converted to full Fourier coefficient rectangles and fed to A1V.

The same checker contains the exact `x'=1` negative control and compares the residual endpoint radius against the absolute endpoint radius at the same `h`.

## Status boundary

### `NS-FUB-A1C-RV`

Residual-centered finite tube verification under supplied exact bounds: the trajectory-enclosure implication is `DERIVED` from the contraction argument. Fixed-N executable status is assigned only after CI.

### `NS-FUB-A1C-RG1`

Pinned `N=1` finite search for an affine residual certificate: executable status assigned only after CI.

### `NS-FUB-A1C-G`

Adaptive generator that reaches arbitrary declared finite target times with sufficiently sharp endpoint localization, for arbitrary admissible finite cutoffs, with a termination/resource theorem: **OPEN**.

### `NS-FUB-A1C-X`

Finite-time singularity implies a constructible validated A1V exceedance certificate: **OPEN**.

## Next theorem target

The important theorem is now a **finite certificate completeness/localization** statement, not merely existence of local tubes:

> if a fixed finite Galerkin trajectory exists on a finite interval and a finite-time observable has a strict positive margin, then a sufficiently refined residual-centered rational certificate chain can validate that margin.

This must be proved with explicit hypotheses and must keep initial-data representation, arbitrary-`N` construction and any complexity/termination claim separate.
