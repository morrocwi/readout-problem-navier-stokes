# NS P2 reopened — phase-complete triad readout attack

**Date:** 2026-09-11  
**Tracker:** issue #46 (reopened).  
**Status:** OPEN mathematical attack.  

## 1. Correction of stopping rule

The earlier observation that an existential all-scale contraction criterion is equivalent to regularity is **not a refutation** of the contraction proposal.  Equivalence does not justify rejecting or abandoning the mathematical statement.  The active rule is now falsification-first: reject only a precisely stated candidate for which a matching counterexample or impossibility proof is supplied.

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

is the same number.  Hence viscosity cancels exactly from the logarithmic derivative of `|chi|`.

### Ruling `NS-P2-TRIAD-PHASE-02`

```text
viscosity alone -> strict contraction of normalized triad phase coherence
```

is **REFUTED** even in the exact isolated triad reduction.

Again, this does not rule out contraction produced by the combined nonlinear triad network plus viscosity.

## 4. Readout-Genesis translation: minimal dynamically closed reader

For the isolated triad, `(x,y,z,r)` is dynamically closed whereas `(x,y,z)` is not.  Therefore the next finite reader must retain signed phase-sensitive transfer information, not merely shell energies or unsigned transfer magnitudes.

For a general finite Fourier cutoff, a natural phase-complete finite record is

\[
\mathcal R_N(t)=\{E_k(t),\,r_\tau(t): |k|\le N,\ \tau=(p,q,k),\ p+q=k\},
\]

where each `r_tau` is the real signed triad product in a declared divergence-free/helical coordinate convention.  Shell transfer is then a finite linear aggregation of the signed `r_tau` with exact triad coefficients.

The full finite Fourier state is of course sufficient; the research question is whether a substantially smaller phase-complete transfer record admits a closed inequality strong enough for all-scale contraction.

## 5. New load-bearing candidate

The previous critical ratio remains

\[
R_j=\frac{(K_{N_j}^2)^{2p/(p-2)}}{\Lambda_j}.
\]

The active target is now **not** a contraction inferred from shell accounting alone.  It is:

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

## 6. What must create the strict margin

The exact triad stress test rules out obtaining the sign or margin from shell energy plus viscosity alone.  Any proof must use at least one genuinely phase-sensitive network fact, such as:

- cancellation between overlapping signed triads;
- divergence-free/helical polarization restrictions on simultaneous phase alignment;
- an incidence/phase frustration theorem preventing critical coherent transfer across all scales;
- a time-window recurrence showing that coherence capable of feeding one shell cannot remain coherently aligned through an arbitrarily long dyadic chain;
- an exact finite completion budget that turns the preceding local statement into an all-scale statement.

The highlighted candidate suggested by the project architecture is therefore a **phase-frustration / coherence-budget theorem** for the actual triad hypergraph, not another energy-only estimate.

## 7. Immediate next falsification target

Before attempting an all-scale proof, test the following finite statement on exact Galerkin triad networks:

> Can all transfer-active triads crossing two adjacent dyadic shell boundaries be simultaneously phase-aligned so that the signed outward flux saturates the triangle-inequality bound?

If yes, the naive phase-frustration margin is REFUTED and the theorem must include additional time/dynamical information.  If no, compute an exact deficit and identify whether that deficit is uniform in cutoff.

This is a finite algebraic question and is the next executable attack.

## 8. Claim boundary

The exact isolated-triad controls above prove only the two stated no-go results and identify the missing phase coordinate.  `NS-P2-PHASE-COMPLETE-CONTRACTION` remains OPEN.  No all-scale strict deficit has yet been proved.