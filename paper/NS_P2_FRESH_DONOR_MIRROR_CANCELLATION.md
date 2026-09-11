# NS P2 — exact mirror cancellation of the fresh-donor induced target

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_fresh_donor_mirror_cancellation.py`

## 1. Purpose

The fresh-donor window charge shows that overlap of two consecutive donors must be paid by target response or by other nonlinear contributions to the same target coordinate.

A proof must not assume that the cancellation branch is automatically expensive.  This note gives a matching exact counterexample to that shortcut: one reflected donor pair produces the same target with exactly the opposite Fourier--Leray coefficient.

Thus cancellation itself can be supplied by a simple symmetry.  The useful structural observation is that this exact escape remains inside one Fourier plane, pointing the next P2 attack toward a planar/2D3C branch versus genuinely non-planar interaction geometry.

---

## 2. Original and reflected donor pairs

Use the common `xz` Fourier plane and normal

\[
N=(0,1,0),
\qquad
T_\ell=\frac{N\times\ell}{|\ell|}.
\]

The original donor pair is

\[
q_0=n(1,0,1),
\qquad
q_1=n(2,0,-1),
\]

with target

\[
r=q_0+q_1=n(3,0,0).
\]

Reflect the donors across the `x` axis in Fourier space:

\[
\widetilde q_0=n(1,0,-1),
\qquad
\widetilde q_1=n(2,0,1).
\]

Then

\[
\widetilde q_0+\widetilde q_1=r.
\]

---

## 3. Exact opposite coefficients

For tangential input and output polarizations, the exact ordered-pair-combined Fourier--Leray coefficients are

\[
\boxed{
c(q_0,q_1;r)=+\frac{3\sqrt{10}}{10}n}
\]

and

\[
\boxed{
c(\widetilde q_0,\widetilde q_1;r)=-\frac{3\sqrt{10}}{10}n.}
\]

All four donor modes have paired equal lengths under the reflection, so their physical inhomogeneous H1 normalization factors also agree pairwise.  Hence the normalized amplitude-equation coefficients satisfy

\[
\boxed{
\widetilde\alpha_n=-\alpha_n.
}
\]

### Status

`NS-P2-FRESH-DONOR-MIRROR-COEFF-CANCEL` — **PASS** for the exact symbolic identities.

---

## 4. Exact target cancellation

The two contributions to the normalized target equation are

\[
-i\alpha_nX_{q_0}X_{q_1}
-i\widetilde\alpha_nX_{\widetilde q_0}X_{\widetilde q_1}.
\]

If

\[
X_{\widetilde q_0}X_{\widetilde q_1}
=X_{q_0}X_{q_1},
\]

then, because `tilde alpha_n=-alpha_n`, the two contributions cancel exactly:

\[
\boxed{
-i\alpha_nX_{q_0}X_{q_1}
-i\widetilde\alpha_nX_{\widetilde q_0}X_{\widetilde q_1}=0.
}
\]

No small coefficient or high-frequency decay is involved.

### Status

`NS-P2-FRESH-DONOR-SIMPLE-CANCELLATION-EXISTS` — **DERIVED**.

This is a cancellation of one target equation, not a claim that all other convolution outputs cancel or that the finite set is dynamically invariant.

---

## 5. Matching refutation

The construction is a matching counterexample to the over-broad inference

```text
large cancellation term in the induced target equation
    -> cancellation necessarily requires complicated/high-cost geometry.
```

Record:

`NS-P2-FRESH-DONOR-CANCELLATION-AUTOMATICALLY-COSTLY` — **REFUTED**.

Therefore the donor-window theorem must not close its cancellation branch merely by naming it `complexity`.

---

## 6. Structural fact that survives the red-team

Every wavevector in the cancelling construction satisfies

\[
k_y=0.
\]

The same is true for the full fresh-donor selected tree.  Moreover, a Fourier plane through the origin is closed under the wavevector addition in the NSE convolution.

Hence the exact mirror cancellation points to a sharper branch decomposition:

```text
planar Fourier ancestry / cancellation
    versus
non-planar ancestry, where shared-mode polarization frames must turn.
```

The next theorem should exploit the fact that an exactly plane-supported incompressible NSE solution is a 2D3C flow: the in-plane velocity solves a two-dimensional NSE system and the normal component is an advected-diffused scalar.  Such a branch is regular by the classical two-dimensional theory.

This note does not yet prove that every conflict-free/cancelling ancestry network is planar or close to planar.

Current boundary:

```text
simple exact donor cancellation exists                           DERIVED
cancellation automatically costs complexity                      REFUTED
exact mirror cancellation geometry is planar                     PASS geometric fact
full planar-support invariant/regular branch                     next theorem target
non-planar conflict-poor ancestry classification                 OPEN
K_N / R_j contraction                                            OPEN
NS-P2-FRUSTRATION-OR-CUT                                         OPEN
Clay Navier-Stokes regularity                                    OPEN
```
