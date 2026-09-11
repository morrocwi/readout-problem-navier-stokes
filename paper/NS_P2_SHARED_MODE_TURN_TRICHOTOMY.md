# NS P2 — shared-mode plane-turn trichotomy

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Uses:** shared-mode projective-frame mismatch theorem and planar 2D3C branch.  
**Checker:** `reproduction/checks/check_ns_p2_shared_mode_turn_trichotomy.py`

## 1. Purpose

After the polarization-gauge correction, projective frame dispersion is the basis-invariant local geometry at a mode shared by two triads.  After the planar-branch theorem, an exact same-plane escape is regular rather than singularity-producing.

This note classifies the remaining zero-dispersion geometry exactly.  There is only one genuinely non-planar projectively compatible case: an **orthogonal turn** between the two triad planes.

Thus the conflict-poor P2 frontier is reduced from arbitrary plane changes to a discrete orthogonal-turn ancestry problem.

---

## 2. Two triads sharing one mode

Let two non-collinear triads share the nonzero Fourier mode `p`:

\[
p+q_1=k_1,
\qquad
p+q_2=k_2.
\]

Define nonzero triad-plane normals

\[
n_1=p\times q_1,
\qquad
n_2=p\times q_2.
\]

Both normals lie in the two-dimensional polarization fiber

\[
p^\perp.
\]

Introduce the exact squared line correlation

\[
\boxed{
c^2=
\frac{(n_1\cdot n_2)^2}
{|n_1|^2|n_2|^2}
\in[0,1].}
\]

The sign of either normal is irrelevant because only the projective line matters.

Define the projective turn invariant

\[
\boxed{
\mu=4c^2(1-c^2).
}
\]

If `theta in [0,pi/2]` is the acute angle between the normal lines, then

\[
\mu=\sin^2(2\theta).
\]

For equal incident weights this is exactly the two-frame dispersion quantity.

### Status

`NS-P2-SHARED-MODE-TURN-INVARIANT` — **DERIVED**.

---

## 3. Exact zero-dispersion classification

Because `0<=c^2<=1`,

\[
\mu=0
\quad\Longleftrightarrow\quad
c^2\in\{0,1\}.
\]

There are exactly two cases.

### Case A — same plane

If

\[
c^2=1,
\]

then `n_1` and `n_2` are parallel, so the two triad planes have the same normal and therefore are the same plane through the shared line `p`.

This is a planar continuation.

### Case B — orthogonal turn

If

\[
c^2=0,
\]

then

\[
n_1\cdot n_2=0.
\]

The two triad planes are distinct and their normals are orthogonal.  Their adapted polarization frames at `p` are the same unordered pair of projective axes with the two axes exchanged.

This is the unique non-planar zero-dispersion transition.

### Status

`NS-P2-ZERO-DISPERSION-SAME-OR-ORTHOGONAL` — **DERIVED**.

---

## 4. Positive dispersion returns to the existing frustration/cut branch

If

\[
0<c^2<1,
\]

then

\[
\mu>0.
\]

Equivalently, the adapted projective frames are neither identical nor related by an exact quarter-turn.  The previously derived shared-mode frame theorem then applies: every common polarization basis misaligns at least one triad by a positive projective angle, producing the exact four-channel `pi`-holonomy face unless the corresponding coefficients are driven into the quantitative weak-coupling/cut regime.

Therefore the local geometry has the exact trichotomy

\[
\boxed{
\text{same plane}
\quad\text{or}\quad
\text{orthogonal turn}
\quad\text{or}\quad
\text{frame-mismatch frustration/cut}.
}
\]

### Status

`NS-P2-SHARED-MODE-PLANE-TURN-TRICHOTOMY` — **DERIVED**.

This combines an exact algebraic classification with the already-derived frame-mismatch theorem; it does not newly strengthen the coefficient floor in that theorem.

---

## 5. P2 consequence after closing the planar branch

The planar escape theorem gives

```text
same plane forever
    -> plane-supported 2D3C NSE
    -> globally regular branch.
```

The positive-dispersion branch is already assigned a quantitative frustration/cut cost.

Hence an exact conflict-poor non-planar ancestry network that avoids the existing mismatch tax at every shared-mode transition must be assembled from orthogonal plane turns.

This gives the sharpened unresolved branch:

\[
\boxed{
\text{singularity-relevant conflict-poor escape}
\Longrightarrow
\text{recent nonlinear ancestry containing orthogonal-turn transitions}
}
\]

unless it pays the already-certified frame-mismatch cut/tax.

### Status

`NS-P2-NONPLANAR-ZERO-DISPERSION-REDUCES-TO-ORTHOGONAL-TURNS` — **DERIVED**.

---

## 6. Exact fixtures

The checker verifies three integer configurations.

### Same-plane fixture

\[
p=(1,0,0),
\quad q_1=(0,0,1),
\quad q_2=(1,0,1).
\]

Both normals are parallel and `mu=0` with `c^2=1`.

### Orthogonal-turn fixture

\[
p=(2,0,1),
\quad q_1=(-1,0,0),
\quad q_2=(2,4,1).
\]

The normals are proportional to `(0,1,0)` and `(-1,0,2)`, which are orthogonal; hence `mu=0` with `c^2=0` while the triad planes are distinct.

### Positive-dispersion fixture

\[
p=(1,0,0),
\quad q_1=(0,0,1),
\quad q_2=(0,1,1).
\]

The normal-line angle is `pi/4`, so

\[
c^2=1/2,
\qquad
\mu=1.
\]

### Checker status

`NS-P2-SHARED-MODE-TURN-FIXTURES` — **PASS**.

---

## 7. Remaining load-bearing target

The next attack must now focus specifically on orthogonal-turn ancestry networks:

1. search for an all-scale phase-SAT orthogonal-turn tree with nondegenerate H1 coupling;
2. if one exists, red-team its full NSE convolution and recent-ancestry closure;
3. if every sufficiently rich orthogonal-turn network creates cross-triad holonomy, extract the exact finite cycle theorem;
4. aggregate that theorem with the existing window packing and recent-ancestry bounds.

Current boundary:

```text
same-plane exact branch regular                              DERIVED
positive frame dispersion -> frustration/cut                DERIVED previously
zero dispersion -> same plane or orthogonal turn             DERIVED
non-planar zero-dispersion -> orthogonal-turn network         DERIVED
all-scale orthogonal-turn escape classification              OPEN
orthogonal-turn window packing/recurrence                    OPEN
K_N / R_j contraction                                        OPEN
NS-P2-FRUSTRATION-OR-CUT                                     OPEN
Clay Navier-Stokes regularity                                OPEN
```
