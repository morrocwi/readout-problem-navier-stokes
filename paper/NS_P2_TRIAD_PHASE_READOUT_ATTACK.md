# NS P2 reopened — phase-complete triad readout attack

**Date:** 2026-09-11  
**Tracker:** issue #46 (reopened).  
**Status:** OPEN mathematical attack.  

## 1. Correction of stopping rule

The earlier observation that an existential all-scale contraction criterion is equivalent to regularity is **not a refutation** of the contraction proposal. Equivalence does not justify rejecting or abandoning the mathematical statement. The active rule is now falsification-first: reject only a precisely stated candidate for which a matching counterexample or impossibility proof is supplied.

## 2. Why the shell-energy reader is missing a dynamical coordinate

The repository already contains an exact analytic vorticity triad embedded in periodic Navier--Stokes,

\[
a=(1,0,0),\qquad b=(1,1,0),\qquad c=(-2,-1,0),
\]

with

\[
|a|^2=1,\quad |b|^2=2,\quad |c|^2=5
\]

and exact transfer coefficients

\[
c_a=\frac3{10},\qquad c_b=-\frac45,\qquad c_c=\frac12.
\]

The reduced variables `(x,y,z,r)` satisfy

\[
\dot x=2c_a r-2\nu |a|^2x,
\]
\[
\dot y=2c_b r-2\nu |b|^2y,
\]
\[
\dot z=2c_c r-2\nu |c|^2z,
\]
\[
\dot r=c_a yz+c_bxz+c_cxy-\nu(|a|^2+|b|^2+|c|^2)r.
\]

Thus the signed coordinate `r` carries information that `(x,y,z)` does not contain.

At `nu=1/200` and `x=y=z=1`, the two admissible phase choices `r=+1` and `r=-1` have identical shell energies but

\[
\dot z\big|_{r=+1}=\frac{19}{20}>0,
\qquad
\dot z\big|_{r=-1}=-\frac{21}{20}<0.
\]

Therefore an actual NS triad can send the highest shell in opposite instantaneous directions while the shell-energy readout is identical.

### Ruling `NS-P2-TRIAD-PHASE-01`

```text
shell energies alone -> universal signed transfer / strict contraction
```

is **REFUTED for this precise reader class** by an actual finite NS triad.

This does **not** refute a phase-complete contraction theorem.

## 3. Viscosity does not automatically contract normalized phase coherence

Define, where nonzero,

\[
\chi:=\frac{r}{\sqrt{xyz}}.
\]

The viscous contribution to `d log |r| / dt` is

\[
-\nu(s_a+s_b+s_c),
\]

while the viscous contribution to

\[
\frac12\frac d{dt}\log(xyz)
\]

is the same number. Hence viscosity cancels exactly from the logarithmic derivative of `|chi|`.

### Ruling `NS-P2-TRIAD-PHASE-02`

```text
viscosity alone -> strict contraction of normalized triad phase coherence
```

is **REFUTED** even in the exact isolated triad reduction.

Again, this does not rule out contraction produced by the combined nonlinear triad network plus viscosity.

## 4. Readout-Genesis translation: minimal dynamically closed reader

For the isolated triad, `(x,y,z,r)` is dynamically closed whereas `(x,y,z)` is not. Therefore the next finite reader must retain signed phase-sensitive transfer information, not merely shell energies or unsigned transfer magnitudes.

For a general finite Fourier cutoff, a natural phase-complete finite record is

\[
\mathcal R_N(t)=\{E_k(t),\,r_\tau(t): |k|\le N,\ \tau=(p,q,k),\ p+q=k\},
\]

where each `r_tau` is the real signed triad product in a declared divergence-free/helical coordinate convention. Shell transfer is then a finite linear aggregation of the signed `r_tau` with exact triad coefficients.

The full finite Fourier state is of course sufficient; the research question is whether a substantially smaller phase-complete transfer record admits a closed inequality strong enough for all-scale contraction.

## 5. Exact N=1 H3 sign-frustration witness

The exact integer-scaled `N=1` 52-real-dimensional Galerkin tensor was used to form the nonlinear production polynomial of the inhomogeneous `H^3` squared norm,

\[
Q_3(x)=\sum_i W_i x_i\,(C B(x,x))_i,
\qquad
W_i=w_i(1+|k_i|^2)^3.
\]

After commutative aggregation the polynomial has exactly 432 nonzero cubic monomials: 218 positive coefficients and 214 negative coefficients.

Ask whether a coordinate sign assignment `x_i in {+1,-1}` can make **every** nonzero monomial contribution positive. This is an exact GF(2) linear system. The checker returns

```text
UNSAT_EXACT_SIGN_FRUSTRATION
```

and produces a four-equation contradiction trace. Therefore the exact N=1 H3 production polynomial has an unavoidable coordinate-monomial sign frustration.

The four conflicting monomials are, with `a=x_0`, `b=x_17`, `c=x_20`, `d=x_22`, `e=x_25`,

\[
-11400abc,
\qquad
+10800abd,
\qquad
-11400ace,
\qquad
-10800ade.
\]

Equivalently their sum is

\[
\boxed{
Q_{\rm cyc}
=600a\left[-19bc+18bd-19ce-18de\right].
}
\]

The relevant Fourier coordinates lie on the mode pattern

\[
(0,0,1),\quad (1,-1,-1),\quad (1,-1,0),\quad (1,-1,1),
\]

with the two declared transverse coordinate directions at the central mode `(1,-1,0)`.

The XOR of the four target-sign equations is `0=1`, so all four nonzero contributions cannot have the same sign.

### Status `NS-P2-N1-H3-SIGN-FRUSTRATION`

**PASS / exact finite witness.** This is a genuine algebraic cancellation obstruction in the actual N=1 Galerkin tensor. It is not yet an all-N theorem and not yet a quantitative scale contraction.

## 6. Exact local frustration tax

Let

\[
S_{\rm cyc}
:=11400|abc|+10800|abd|+11400|ace|+10800|ade|
\]

and

\[
m_{\rm cyc}
:=\min\{11400|abc|,10800|abd|,11400|ace|,10800|ade|\}.
\]

Because the product of the four signed term signs is negative whenever all five amplitudes are nonzero, at least one term must oppose the others. Hence by direct sign accounting,

\[
\boxed{
|Q_{\rm cyc}|\le S_{\rm cyc}-2m_{\rm cyc}.
}
\]

This is an exact quantitative **frustration tax**.

Removing the common `600a`, the cycle is the bilinear form

\[
[b,e]
\begin{bmatrix}
-19&18\\
-19&-18
\end{bmatrix}
\begin{bmatrix}c\\d\end{bmatrix}.
\]

Its two columns are exactly orthogonal:

\[
(-19,-19)\cdot(18,-18)=0,
\]

with squared column norms

\[
2\cdot19^2,\qquad 2\cdot18^2.
\]

This explains the four-term Hadamard-like sign cycle algebraically.

### Boundary of the tax

The ratio `m_cyc/S_cyc` can approach zero when one participating amplitude is small. Therefore the local tax alone does **not** give a cutoff-independent relative deficit

\[
|Q_{\rm cyc}|\le(1-\delta)S_{\rm cyc}
\]

with universal `delta>0`.

The next theorem must exploit the resulting dichotomy:

```text
balanced active cycle
    -> definite frustration tax
or
one participant is small
    -> that route through the transfer network is weak / broken.
```

Turning this local dichotomy into an all-scale statement is the current load-bearing problem.

## 7. New load-bearing candidate

The previous critical ratio remains

\[
R_j=\frac{(K_{N_j}^2)^{2p/(p-2)}}{\Lambda_j}.
\]

The active target is now **not** a contraction inferred from shell accounting alone. It is:

### `NS-P2-PHASE-COMPLETE-CONTRACTION` — OPEN

Construct from finite/checkable phase-complete triad records upper certificates `U_j` and a remainder `beta_j` such that

\[
R_j\le U_j,
\]
\[
U_{j+1}\le (1-\delta_j)U_j+\beta_j,
\]

with a proved cumulative strict margin sufficient to force `U_j -> 0`; for example one strong sufficient form is

\[
\delta_j\ge\delta_*>0,
\qquad
\beta_j\le B\rho^j,
\quad 0<\rho<1.
\]

A weaker nonuniform form is admissible if it still proves decay, e.g. a product/summability condition on `(1-delta_j)` and `beta_j`.

## 8. Candidate network theorem: frustration-or-cut

The N=1 cycle suggests a finite combinatorial/dynamical statement suitable for the project machinery.

For a declared shell boundary, let `A_tau` be the absolute contribution of each transfer-active signed triad term and let the exact signed-triad incidence constraints define a family of frustration cycles. Seek a certified inequality of the form

\[
|\Phi_j|
\le
\sum_{\tau\in\mathcal T_j}A_\tau
-2\,\mathfrak F_j,
\]

where `mathfrak F_j` is a finite computable frustration tax assembled from overlapping conflict cycles.

Then prove a dichotomy:

1. `mathfrak F_j` is a fixed fraction of the potential outward transfer, giving a strict contraction margin; or
2. the amplitudes responsible for making all cycle minima small form a cut/hitting set whose smallness itself bounds transmission to the next scale.

Call the desired uniform form

### `NS-P2-FRUSTRATION-OR-CUT` — OPEN

This is now a more precise target than generic "cancellation": it asks for a quantitative alternative that remains useful when individual cycle minima degenerate.

## 9. What must create the strict margin

The exact stress tests rule out obtaining the margin from shell energy plus viscosity alone. Any proof must use at least one genuinely phase-sensitive network fact, such as:

- cancellation between overlapping signed triads;
- divergence-free/helical polarization restrictions on simultaneous phase alignment;
- an incidence/phase-frustration theorem preventing critical coherent transfer across all scales;
- a time-window recurrence showing that coherence capable of feeding one shell cannot remain coherently aligned through an arbitrarily long scale chain;
- an exact finite completion budget that turns the preceding local statement into an all-scale statement.

## 10. Immediate next attack

The next finite algebraic task is no longer to ask whether frustration exists at N=1; that has passed. It is to determine whether the four-term conflict pattern extends as a parameterized family of actual Fourier triads at arbitrary cutoff, and whether overlapping copies give a frustration-or-cut inequality with constants that do not collapse as the cutoff grows.

If a parameterized family fails, record the matching counterexample. If it survives, derive its exact coefficient scaling and network coverage before attempting the continuum/all-scale composition.

## 11. Claim boundary

The exact isolated-triad controls prove two precise no-go results. The N=1 tensor additionally supplies an exact four-equation sign-frustration witness and a local frustration-tax inequality. `NS-P2-PHASE-COMPLETE-CONTRACTION` and `NS-P2-FRUSTRATION-OR-CUT` remain OPEN. No all-scale strict deficit has yet been proved.