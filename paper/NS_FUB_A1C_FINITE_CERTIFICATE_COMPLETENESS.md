# NS-FUB-A1C — Finite Residual-Certificate Completeness

**Date:** 2026-09-11  
**Scope:** fixed finite-dimensional rational polynomial ODEs, including each fixed Fourier--Galerkin Navier--Stokes cutoff after an exact coordinate normalization.  
**Claim boundary:** this is not an arbitrary-`N` theorem, not an efficient validated-integrator theorem, not a continuum compactness theorem, and not a Navier--Stokes regularity result.

## 1. Why this theorem is needed

The existing `NS-FUB-A1C-RV` layer verifies a supplied residual-centered rational tube, and the pinned `N=1` calibration shows such a certificate can be found in at least one finite case.

That is not enough for the Clay bridge. A useful certificate class also needs a completeness statement:

> if a fixed finite trajectory really has a strict finite observable margin, then the certificate language is rich enough to validate that margin after sufficiently fine rational approximation.

Without this step, failure of a particular certificate search could still be a defect of the certificate language rather than a property of the dynamics.

## 2. Finite setting

Let

\[
F:\mathbb R^d\to\mathbb R^d
\]

be a polynomial vector field with rational coefficients. Let

\[
x:[0,T]\to\mathbb R^d
\]

be a classical solution of

\[
x'(t)=F(x(t)),\qquad x(0)=x_0,
\]

on a finite interval `[0,T]`.

For the exact-rational version below assume

\[
x_0\in\mathbb Q^d.
\]

Let `q in Q`, `0<q<=T`, and let

\[
\Phi:\mathbb R^d\to\mathbb R
\]

be a polynomial observable with rational coefficients. The finite Galerkin `H^3` squared norm used by A1V is of this form after the declared finite coordinate conversion.

Fix a rational threshold `b` and assume the strict margin

\[
\Phi(x(q))>b.
\]

## 3. Certificate language

A finite residual certificate chain consists of:

1. a rational partition

   \[
   0=t_0<t_1<\cdots<t_m=q,
   \]

2. rational affine reference paths on each link

   \[
   p_j(t)=a_j+(t-t_j)v_j,
   \qquad a_j,v_j\in\mathbb Q^d,
   \]

3. rational incoming endpoint-error radii `e_j>=0` and rational tube radii `r_j>0`,

4. rational exact upper bounds `R_j,L_j` satisfying on the declared tube

   \[
   \|F(p_j(t)+z)-v_j\|_\infty\le R_j
   \quad\text{for }\|z\|_\infty\le r_j,
   \]

   and

   \[
   \|DF(p_j(t)+z)\|_\infty\le L_j,
   \]

5. the fail-closed inequalities

   \[
   e_j+h_jR_j\le r_j,
   \qquad h_jL_j<1,
   \qquad h_j=t_{j+1}-t_j,
   \]

6. the endpoint-error transfer

   \[
   e_{j+1}\ge e_j+h_jR_j,
   \]

   after recentering at the next rational reference endpoint.

Because `F`, `p_j`, the time interval and the error box are polynomial/rational data, the residual and Jacobian bounds can be checked using finite rational arithmetic. For a polynomial expression on a rational box, expansion into rational coefficients followed by coefficientwise absolute-value bounds supplies a finite sound upper bound; sharper interval forms are optional.

## 4. Theorem — finite residual-certificate completeness

### `NS-FUB-A1C-COMP-Q`

Assume the finite setting above. If

\[
\Phi(x(q))>b,
\]

then there exists a finite rational residual certificate chain whose final rational endpoint box `I_q` satisfies

\[
x(q)\in I_q
\]

and whose exact finite lower-bound evaluation certifies

\[
\inf_{y\in I_q}\Phi(y)>b.
\]

Equivalently: every strict positive finite observable margin along a fixed rational polynomial ODE trajectory admits a finite machine-checkable rational residual certificate.

**Status:** DERIVED analytically under the stated finite hypotheses.

## 5. Proof

The proof is finite-dimensional and separates approximation, tube soundness, and strict-margin transfer.

### Step 1 — compact control neighborhood

The trajectory image

\[
K=x([0,q])
\]

is compact. Since `F` is polynomial, `F` and `DF` are continuous. Choose a bounded open neighborhood `U` of `K` with compact closure and let

\[
L_* > \sup_{y\in U}\|DF(y)\|_\infty
\]

be any finite rational upper bound.

Choose `rho_*>0` so that the closed `rho_*`-neighborhood of `K` lies in `U`.

### Step 2 — strict observable margin gives a target localization radius

Because `Phi` is continuous and

\[
\Phi(x(q))-b>0,
\]

there exists `epsilon_*>0` such that

\[
\|y-x(q)\|_\infty<\epsilon_*
\quad\Longrightarrow\quad
\Phi(y)>b.
\]

Shrink `epsilon_*` if necessary so `epsilon_*<rho_*`.

For the exact A1V-style rectangular lower bound, the same strict margin is enough: as a rational rectangle shrinks to `x(q)`, the coordinatewise lower bound used for a finite quadratic Fourier norm converges to the exact finite value. Hence there is a sufficiently small endpoint rectangle for which the finite lower bound is already strictly above `b`.

### Step 3 — rational piecewise-affine paths approximate the true trajectory and derivative

The derivative

\[
x'=F(x)
\]

is continuous on `[0,q]`, hence uniformly continuous.

Choose a rational partition with mesh small enough that `x'` varies by at most an arbitrarily prescribed `eta>0` on each subinterval. Because rational vectors are dense in `R^d`, choose rational nodes `a_j` arbitrarily close to `x(t_j)`, with `a_0=x_0` exactly.

The rational affine interpolant

\[
p_j(t)=a_j+\frac{t-t_j}{h_j}(a_{j+1}-a_j)
\]

then satisfies, after choosing the mesh and node approximations sufficiently fine,

\[
\sup_{[t_j,t_{j+1}]}\|p_j(t)-x(t)\|_\infty<\eta
\]

and

\[
\sup_{[t_j,t_{j+1}]}\|p_j'(t)-x'(t)\|_\infty<\eta.
\]

The second estimate follows from uniform continuity of `x'`: the exact secant slope of `x` is an average of `x'` on the interval, and the rational endpoint perturbations can be chosen `o(h_j)` so their contribution to the rational secant slope is also below `eta`.

### Step 4 — residuals can be made arbitrarily small

On `U`, `F` is Lipschitz with constant below `L_*`. Therefore

\[
\|F(p_j(t))-p_j'(t)\|_\infty
\le
L_*\|p_j(t)-x(t)\|_\infty
+
\|x'(t)-p_j'(t)\|_\infty.
\]

Thus the centerline residual can be made arbitrarily small by decreasing `eta`.

For an error tube `||z||_inf<=r_j`,

\[
\|F(p_j(t)+z)-p_j'(t)\|_\infty
\le
\delta_j+L_*r_j,
\]

where `delta_j` is an arbitrarily small centerline residual bound.

Because the residual expression is a rational polynomial in normalized time and the error variables, a rational coefficientwise majorant `R_j` exists with arbitrarily small excess over this analytic bound when the partition and tubes are fixed sufficiently small. Likewise a finite rational `L_j` can be chosen above the exact Jacobian supremum on the rational tube.

### Step 5 — choose a finite contraction mesh

Refine the finite rational partition so that

\[
h_jL_j\le\frac14
\]

for every link.

Start with `e_0=0`. For a chosen rational residual budget `delta>0`, select the path approximation tightly enough that all exact certificate residual bounds obey the required small budget after the tube contribution is included.

One explicit safe recursion is

\[
r_j=2(e_j+h_j\delta),
\]

and then choose the exact `R_j` so that

\[
R_j\le\delta+L_jr_j.
\]

With `h_jL_j<=1/4`,

\[
e_j+h_jR_j
\le
 e_j+h_j\delta+\frac14r_j
=
\frac34r_j
<r_j.
\]

Hence every link satisfies the strict self-map gate and also

\[
h_jL_j<1.
\]

The endpoint-error update may be taken as

\[
e_{j+1}=e_j+h_jR_j<r_j.
\]

Since the number of links `m` is finite, this recursion amplifies the residual budget by only a finite factor depending on the chosen partition and the bounded `L_j`. Therefore, by choosing the rational path approximation sufficiently accurate, `delta` can be made small enough that every `e_j` and `r_j` is below any prescribed positive tolerance, in particular below `rho_*`, and the final endpoint error is below `epsilon_*`.

No uniform-in-`N` or polynomial-resource bound is asserted here.

### Step 6 — per-link verification is sound

For each link define the Picard error operator

\[
(\mathcal T_j e)(t)=e(t_j)+\int_{t_j}^t
\bigl(F(p_j(s)+e(s))-p_j'(s)\bigr)\,ds.
\]

The self-map inequality follows from

\[
e_j+h_jR_j\le r_j,
\]

and the contraction estimate is

\[
\|\mathcal T_je-\mathcal T_jf\|_\infty
\le h_jL_j\|e-f\|_\infty.
\]

Since `h_jL_j<1`, Banach contraction gives the unique finite ODE trajectory in the certified tube. Finite induction transfers the endpoint enclosure through all links.

### Step 7 — strict observable margin is eventually machine-verifiable

The final endpoint enclosure can be made arbitrarily small around `x(q)`. By Step 2 choose it small enough that every point in the box has `Phi>b`.

For polynomial `Phi` with rational coefficients, a rational lower bound on `Phi` over the rational box is finite-computable. In the A1V `H^3` case the existing exact interval checker provides this lower bound directly.

Therefore the final certificate returns strict PASS.

This proves `NS-FUB-A1C-COMP-Q`.

## 6. Search corollary — semidecidable positive finite witnesses

The certificate language is countable: finite rational partitions, rational affine paths, rational radii and rational bound records can be effectively enumerated. Its verifier uses finite exact arithmetic and terminates on each candidate.

Consequently, under the hypotheses of `NS-FUB-A1C-COMP-Q`, a dovetailed exhaustive search through rational residual certificates eventually finds a PASS certificate whenever the strict positive finite margin is true.

### `NS-FUB-A1C-ENUM-Q`

For fixed rational polynomial finite dynamics, rational initial state, rational time and rational polynomial observable,

\[
\Phi(x(q))>b
\]

implies that exhaustive enumeration of finite rational residual certificates eventually emits a verified witness.

**Status:** DERIVED from certificate completeness plus decidability of the finite verifier.

This is a semidecision/existence result only. No useful runtime bound is claimed.

## 7. Navier--Stokes consequence under an explicit finite-data adapter

Combine:

1. `NS-FUB-A1E`: under the declared continuation and compact-time Galerkin convergence adapters, a finite-time singularity implies arbitrarily large finite Galerkin `H^3` exceedances at some finite cutoff and rational time;
2. `NS-FUB-A1C-COMP-Q`: a strict exceedance for a fixed rational finite Galerkin ODE admits a finite rational residual certificate;
3. `NS-FUB-A1C-ENUM-Q`: exhaustive certificate enumeration eventually finds such a certificate.

Then, **for the restricted case where the finite Galerkin initial state has an exact rational representation compatible with the declared dynamics**, a finite-time singularity implies that for every finite rational threshold `B` some dovetailed finite search eventually emits a verified A1V certificate with

\[
\|u_N(q)\|_{H^3}>B.
\]

Call this restricted conditional statement `NS-FUB-A1C-XQ`.

**Status:** DERIVED under the A1E analytic adapters plus the exact-rational finite-data hypothesis.

This does **not** establish the general Clay-facing `NS-FUB-A1C-X`, because arbitrary smooth continuum initial data need not arrive with exact rational finite-coordinate certificates. A representation/enclosure adapter for the full admissible initial-data class remains separate and OPEN.

## 8. What remains open after completeness

The following remain load-bearing:

- arbitrary admissible continuum initial-data representation/enclosure;
- arbitrary-`N` validated Galerkin construction with uniform statement discipline;
- an efficient or resource-controlled adaptive generator;
- a non-vacuous all-scale regularity-sensitive/tail theorem;
- the converse/exclusion bridge needed for global regularity;
- any theorem turning failure of a particular numerical/certificate search into a PDE singularity witness.

In particular,

\[
\text{certificate completeness at fixed finite }N
\not\Rightarrow
\text{uniform all-scale regularity}.
\]

## 9. Research consequence

The checker language is no longer the main logical risk for strict fixed-finite positive witnesses: under the stated rational finite hypotheses it is complete in the existence/semidecision sense.

The next high-leverage NS target is therefore not more fixed-N integration. It is the all-scale statement separating bounded smooth continuation from genuine finite obstruction:

\[
\text{uniform regularity-sensitive finite certificates}
+
\text{summable/all-refinement tail control}
\Longrightarrow
\text{global regularity},
\]

with a non-vacuity proof showing that the finite antecedent is not merely global regularity written in different words.
