# NS-FUB-A1C — Validated Finite Galerkin Tube Adapter

**Date:** 2026-09-11  
**Status:** fixed-`N=1` finite exact calibration **PASS**; tube implication `DERIVED` from standard finite-dimensional contraction theory.  
**Parent target:** `NS-FUB-A1C` remains OPEN as an arbitrary-instance constructive bridge.

## 1. Goal

`NS-FUB-A1V` can verify an `H^3` exceedance from certified rational Fourier-coefficient intervals, but it deliberately does not prove where those intervals came from.

This note closes one checker-side gap: given a finite quadratic Galerkin ODE and a proposed rational state box, can finite arithmetic certify that the exact finite ODE trajectory stays in that box for a positive time and produce an endpoint enclosure?

For the existing `N=1` real Fourier-Galerkin coordinates, the audited dynamics have the exact form

\[
F(x)=\frac{1}{C}\left(Dx+T(x,x)\right),\qquad C=600,
\]

where:

- `D` is diagonal with scaled entries `-3 |k|^2` because `nu=1/200` and `C nu=3`;
- `T` is the exact integer tensor for `C` times the quadratic Galerkin map;
- the tensor audit reproduces `2096` nonzero integer coefficients and exact induced infinity row-sum bound `36000`.

No continuum trajectory is used inside the certificate calculation.

## 2. Rational tube certificate

Let the initial finite state be the already-reproduced deterministic small-integer center `x0`, and let

\[
X=x_0+[-r,r]^d,\qquad r=10^{-3},\qquad d=52.
\]

For every coordinate, finite exact arithmetic computes `M_i` satisfying

\[
|F_i(x)|\le M_i\qquad\forall x\in X.
\]

For the quadratic vector field this is bounded from the exact coefficients by

\[
M_i=\frac{1}{C}\left(
|D_i|R_i+
\sum_{j,k}|T_{ijk}|R_jR_k
\right),
\]

with

\[
R_j=|x_{0,j}|+r.
\]

The checker also computes an infinity-norm Lipschitz bound

\[
L_X=\frac1C\max_i\left(
|D_i|+
\sum_{j,k}|T_{ijk}|(R_j+R_k)
\right).
\]

It chooses a positive rational time step `h` no larger than

\[
\frac{r}{2\max_i M_i}
\quad\text{and}\quad
\frac{1}{2L_X}.
\]

Hence

\[
h\max_iM_i\le r/2,
\qquad
hL_X\le 1/2<1.
\]

## 3. Why this certifies a trajectory tube

For fixed initial point `x0`, consider the Picard operator on continuous paths valued in `X`:

\[
(\mathcal T y)(t)=x_0+\int_0^t F(y(s))\,ds.
\]

The self-map inequality follows from the `M_i` bounds, while

\[
\|\mathcal Ty-\mathcal Tz\|_\infty
\le hL_X\|y-z\|_\infty
\]

makes `T` a contraction. Standard Banach fixed-point theory therefore gives a unique finite-dimensional Galerkin trajectory on `[0,h]` contained in `X`.

The endpoint obeys the finite rational enclosure

\[
x_i(h)\in[x_{0,i}-hM_i,\ x_{0,i}+hM_i].
\]

The analytic theorem used here is ordinary finite-dimensional ODE/Banach fixed-point mathematics; all certificate inequalities and coefficients are finite exact rational/integer data.

## 4. Green fixed-N calibration

Dedicated GitHub Actions job `exact-validated-tube` passed on PR #29. The exact output was:

\[
\max_i M_i=\frac{52651213}{200000},
\qquad
L_X=\frac{2009}{8},
\]

with chosen step

\[
h=\frac{100}{52651213}>0.
\]

The certified margins are

\[
\frac{h\max_iM_i}{r}=\frac12,
\]

and

\[
hL_X=\frac{50225}{105302426}<\frac12.
\]

The same run independently reproduced the exact finite tensor statistics

```text
nonzero coefficients = 2096
infinity row-sum bound = 36000
```

and returned

```text
NS-FUB-A1C N1 VALIDATED TUBE PASS
```

These values are finite exact evidence for this fixed calibration only.

## 5. Composition with A1V

The checker `reproduction/checks/check_ns_fub_a1c_n1_validated_tube.py` converts the endpoint coordinate box through the exact divergence-free Fourier basis into rectangular intervals for all retained complex Fourier velocity coefficients.

Those intervals are passed to the existing exact verifier

`reproduction/checks/check_ns_fub_a1_h3_certificate.py`.

Thus the calibration pipeline is

```text
exact finite N=1 quadratic dynamics
    -> rational invariant tube + contraction certificate
    -> rational endpoint state enclosure
    -> exact Fourier coefficient rectangles
    -> A1V H^3 lower-bound verifier
    -> PASS/HOLD
```

The fixed threshold `B=1` is used only as an end-to-end sanity witness. The green run gave an exact positive `H^3` margin and `endpoint_H3_certificate = PASS`. This threshold is not a singularity threshold and has no Clay significance.

## 6. Status split

### `NS-FUB-A1C-V` — validated finite tube verifier

Given an explicitly represented finite quadratic vector field, initial state, box and positive margins satisfying the declared inequalities, the tube/endpoint implication is **DERIVED** from standard finite-dimensional contraction theory, while the inequalities themselves are exact finite checks.

For the repository's fixed `N=1` calibration, executable status is **PASS**.

### `NS-FUB-A1C-G` — general certificate generator

Required target: from an arbitrary admissible finite cutoff, declared initial-data representation and target time/subdivision, automatically construct a sequence of validated rational tubes or return HOLD, with a proved resource/termination statement appropriate to the claim.

**Status:** OPEN.

### `NS-FUB-A1C-X` — singularity-witness capture

Required target: combine the generator with `A1E` strongly enough that a finite-time singularity forces a constructible A1V exceedance certificate.

**Status:** OPEN.

## 7. What this does not prove

The fixed-N calibration does not prove:

- arbitrary-`N` validated integration;
- that a chosen finite step reaches a large `H^3` event;
- a uniform bound or a blow-up exclusion;
- convergence of validated finite trajectories to a continuum solution at the singular endpoint;
- Navier--Stokes global regularity.

The value of this layer is narrower: the gap between “finite state interval supplied” and “finite trajectory interval validated” can be handled by finite rational certificate arithmetic.

## 8. Next load-bearing target

After this verifier layer, the non-vacuous research question becomes:

> Can a finite, adaptive, validated Galerkin-tube generator be proved to either continue with controlled regularity-sensitive/tail margins or emit a finite obstruction, uniformly across requested cutoffs and finite times, without importing global regularity into its premises?

That generator/uniformity problem—not the fixed-N calibration—is the remaining A1C frontier.
