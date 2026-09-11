# NS P2 — finite-to-continuum closure reduction

**Date:** 2026-09-11  
**Status:** P2 reduction theorem / frontier isolation.  
**Claim boundary:** this closes the finite-to-adapter translation architecture, not the Clay Navier--Stokes problem. One uniform finite-native dissipative-margin theorem remains OPEN.

## 1. Clay endpoint

The current attack targets the unforced periodic three-dimensional branch: for every smooth divergence-free periodic initial datum and every `nu>0`, obtain a smooth periodic Navier--Stokes solution for all finite times.

P2 does not require continuum mathematics to disappear. It requires the continuum layer to be isolated after a finite-native uniform theorem rather than being silently assumed inside the finite core.

## 2. Layers already removed from the bottleneck

The following are no longer the main obstruction.

1. `NS-FUB-A1E`: under the declared classical continuation and compact-time Galerkin adapters, a finite-time singularity forces arbitrarily large finite-Galerkin `H^3` exceedances.
2. `A1V`: a finite Galerkin `H^3` exceedance has an exact rational PASS/HOLD verifier.
3. `A1C-COMP-Q` / `A1C-ENUM-Q`: fixed finite rational polynomial/Galerkin strict witnesses admit finite rational residual certificates and exhaustive semidecision, with no useful runtime claim.
4. Adjacent/local compatibility alone is insufficient.
5. Instantaneous omitted `L2`/energy tail smallness does not control omitted `H^3` tail.
6. Failure of one fixed-`N` Galerkin trajectory/certificate construction is not a singularity witness; each unforced fixed finite Galerkin system extends globally.
7. Linear Stokes memory and nonlinear history separated from the endpoint by a positive time gap have explicit all-scale `H^3` tail envelopes.
8. A finite exact interface exists for shellwise absorption inequalities.
9. `NS-P2-HH-GEOM-LIFT` below converts one useful all-shell geometric defect envelope into a weighted `H^3` remainder bound.

The remaining issue is the **uniform recent nonlinear production**.

## 3. Adapter-neutral `H^3` energy margin

For the finite Fourier-Galerkin solution `u_N`, define

\[
X_N(t):=\|u_N(t)\|_{H^3}^2,
\]

and let

\[
\mathcal D_N(t):=\nu\|\nabla\Lambda^3u_N(t)\|_2^2
\]

be the `H^3` viscous dissipation. Define the signed nonlinear production so that the exact finite Galerkin identity is

\[
\boxed{
\frac12\frac{d}{dt}X_N(t)+\mathcal D_N(t)=\mathcal P_N(t).
}
\]

The precise Fourier normalization can be fixed once in the finite implementation; the reduction only needs the same normalization in `X_N`, `D_N`, and `P_N`.

### `NS-P2-H3-MARGIN`

Suppose there are constants

\[
0\le\theta<1,
\qquad C_T<\infty,
\]

independent of the cutoff `N`, such that for every retained cutoff and every `t in [0,T]`,

\[
\boxed{
\mathcal P_N(t)
\le
\theta\mathcal D_N(t)+C_T\bigl(1+X_N(t)\bigr).
}
\]

Then

\[
\frac12X_N'(t)+(1-\theta)\mathcal D_N(t)
\le C_T(1+X_N(t)),
\]

and hence

\[
X_N'(t)\le2C_T(1+X_N(t)).
\]

Gronwall gives the explicit uniform bound

\[
\boxed{
1+X_N(t)
\le
(1+X_N(0))e^{2C_Tt}
\le
(1+\|u_0\|_{H^3}^2)e^{2C_TT}.
}
\]

Thus a cutoff-independent dissipative margin yields a cutoff-independent finite-time `H^3` bound.

**Status:** DERIVED algebraic/Gronwall reduction. The difficult part is constructing `theta,C_T` by a non-vacuous finite mechanism.

## 4. Standard semantic adapter after the uniform margin

Once the cutoff-independent `H^3` bound is established on every finite interval, the remaining continuum step is the standard Galerkin compactness/strong-solution continuation adapter: extract/identify the periodic strong solution on `[0,T]`, use uniqueness in the strong class, and continue. Since `T` is arbitrary, this gives the periodic global-smoothness branch.

This semantic adapter is intentionally weaker and more standard than any special shellwise regularity preprint. The finite programme's Clay-bearing obligation is therefore concentrated before this adapter.

## 5. Exact finite certificate interface for the margin

For one finite cutoff/time cell, a fail-closed certificate may contain rational enclosures

\[
P^+\ge\mathcal P_N,
\quad
D^-\le\mathcal D_N,
\quad
X^+\ge X_N,
\]

and rational `theta,C` with

\[
0\le\theta<1,
\qquad C\ge0.
\]

The exact local checker may return PASS only if

\[
\boxed{
P^+\le\theta D^-+C(1+X^+).
}
\]

Enclosure soundness, complete time coverage, and cutoff-independent reuse of the same `theta,C` are separate obligations. A finite list of PASS cells is not silently upgraded to all times or all cutoffs.

## 6. High--High route retained only as a candidate subroute

For an `H^3` dyadic decomposition let the weight be

\[
w_j=2^{6j}=64^j
\]

and define a positive High--High excess

\[
d_j(t):=[T_j^{HH}(t)-\eta V_j(t)]_+.
\]

### `NS-P2-HH-GEOM-LIFT`

If a finite prefix satisfies

\[
d_j(t)\le c_j(1+X_3(t))\quad(j_0\le j\le J),
\]

and the true infinite tail satisfies

\[
d_j(t)\le Aq^j(1+X_3(t))\quad(j>J)
\]

with

\[
64q<1,
\]

then

\[
\sum_{j\ge j_0}64^jd_j(t)
\le C_R(1+X_3(t)),
\]

where

\[
\boxed{
C_R=
\sum_{j=j_0}^{J}64^jc_j
+A\frac{(64q)^{J+1}}{1-64q}.
}
\]

This closes the *weighted-tail lifting arithmetic*. It does not prove the nonlinear shell envelope itself, nor does it prove the missing Low--Low/Low--High continuum energy closure.

The externally tracked High--High preprint is now `HOLD` after independent audit. Therefore `NS-P2-HH-GEOM-LIFT` is retained only as one possible way to help prove the adapter-neutral `H^3` margin above.

## 7. The single main P2 load-bearing lemma

### `NS-P2-H3-MARGIN-UNIFORM` — OPEN

For every admissible smooth periodic divergence-free unforced datum, every `nu>0`, and every finite target time `T`, construct from finite/checkable information constants

\[
0\le\theta<1,
\qquad C_T<\infty,
\]

**independent of the Galerkin cutoff**, together with a finite/uniform certificate mechanism proving

\[
\boxed{
\mathcal P_N(t)
\le
\theta\mathcal D_N(t)
+C_T(1+X_N(t))
}
\]

for every finite cutoff `N` and every `t in [0,T]`.

The construction may use exact finite triad algebra, interval enclosures, symmetry, scale recursion, Stokes damping, shell-transfer decomposition, residual certificates, or another finite-native invariant. It may **not** obtain `C_T` by assuming the desired uniform `H^3` bound, nor hide an equivalent regularity theorem in an oracle/premise.

A stronger theorem such as `NS-P2-HH-UNIFORM` with a separately proved shell-energy closure may imply this margin, but High--High absorption is no longer assumed to be the unique route.

## 8. Why this is exactly the remaining Clay-strength point

If `NS-P2-H3-MARGIN-UNIFORM` is proved, then the chain is

```text
finite/checkable uniform dissipative-margin theorem
        |
        v
uniform all-N H^3 Gronwall bound
        |
        v
standard Galerkin/strong-solution semantic adapter
        |
        v
smooth periodic solution on every finite interval
        |
        v
periodic global smoothness.
```

Conversely, merely checking larger fixed cutoffs, increasing integration length at fixed `N`, controlling only `L^2` tails, or observing numerical transfer decay does not prove the uniform margin.

## 9. P2 status

P2 is **CLOSED AS A REDUCTION / OPEN AT ONE LOAD-BEARING LEMMA**:

```text
NS-P2-H3-MARGIN-UNIFORM = OPEN
```

The High--High preprint is `HOLD`, not a validated final adapter. The High--High geometric-tail theorem remains a valid supporting finite lemma.

No Clay solution is claimed. Proving `NS-P2-H3-MARGIN-UNIFORM` non-vacuously would close this P2 bridge and, with the standard semantic adapter, settle the periodic regularity branch; until then the Millennium problem remains OPEN.
