# NS P2 — cutoff-uniform H1 floor for the gauge-compatible dyadic holonomy

**Date:** 2026-09-11  
**Parent route:** `NS-P2B-SCALE-CONTRACTION-UNIFORM` — **OPEN**  
**Structural parent:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_frame_compatible_dyadic_h1_floor.py`

## 1. Purpose

The finite-observation quantity in the P2B route is

\[
K_N=
\sup_t
\left(
\int_t^{t+\tau_0}
\|P_Nu(s)\|_{H^1}^{2p}\,ds
\right)^{1/(2p)}.
\]

Therefore an `H^3`-normalized coupling estimate, while useful for the older `H^3` margin lane, is not by itself the correct normalization for the scale readout

\[
R_N=\frac{(K_N^2)^{2p/(p-2)}}{\Lambda_N}.
\]

This note recomputes the exact four-channel gauge-compatible dyadic holonomy cycle in **physical H1-normalized scalar coordinates**.

The result is stronger for the P2B route: the cycle coefficient floor is cutoff-uniform rather than decaying like `n^-2`.

---

## 2. Reused exact all-n cycle

Use the frame-compatible network from `NS_P2_FRAME_COMPATIBLE_DYADIC_HOLONOMY.md`:

\[
p=n(1,0,1),
\qquad
c=n(0,1,0),
\qquad
q=n(1,1,1),
\qquad
k=n(2,1,2).
\]

The minimal `pi`-holonomy cycle is

```text
T1B: p0+c1 -> q1
T1C: p1+c1 -> q0
T2A: p0+q0 -> k0
T2C: p1+q1 -> k0
```

with raw Fourier--Leray coefficients

\[
-\frac n3,
\qquad
-2n,
\qquad
+n,
\qquad
-2n.
\]

Its incidence rows satisfy

\[
r_{T1C}-r_{T1B}+r_{T2A}-r_{T2C}=0,
\]

while outward target phases have a `pi` mismatch.

---

## 3. Homogeneous H1 normalization

For scalar coordinate `z_{ell,s}` in the declared unnormalised physical polarization vector `h_{ell,s}`, define

\[
W_{\ell,s}^{H^1,hom}
=|h_{\ell,s}|^2|\ell|^2.
\]

For a channel `p+q=k`, set

\[
\Gamma^{H^1,hom}
=
2c_\tau
\frac{\sqrt{W_{k}^{H^1,hom}}}
{\sqrt{W_{p}^{H^1,hom}W_q^{H^1,hom}}}.
\]

The checker derives exactly

\[
\boxed{
\begin{aligned}
\Gamma_{T1B}^{H^1,hom}&=-\sqrt2,\\
\Gamma_{T1C}^{H^1,hom}&=-2\sqrt3,\\
\Gamma_{T2A}^{H^1,hom}&=+\sqrt6,\\
\Gamma_{T2C}^{H^1,hom}&=-2.
\end{aligned}}
\]

Thus every member of the exact holonomy cycle obeys

\[
\boxed{
|\Gamma_i^{H^1,hom}|\ge\sqrt2
}
\]

for **every** positive integer `n`.

### Status

`NS-P2-FRAME-COMPATIBLE-DYADIC-H1-HOM-FLOOR` — **DERIVED**.

---

## 4. Inhomogeneous physical H1 floor

The actual inhomogeneous Fourier weight is

\[
W_{\ell,s}^{H^1,inh}
=|h_{\ell,s}|^2(1+|\ell|^2).
\]

Write

\[
R_1(L)=\frac{\sqrt{1+L^2}}{L}.
\]

For every nonzero integer Fourier mode, `L>=1`, so

\[
1\le R_1(L)\le\sqrt2.
\]

Therefore

\[
\frac{|\Gamma^{H^1,inh}|}{|\Gamma^{H^1,hom}|}
=
\frac{R_1(|k|)}{R_1(|p|)R_1(|q|)}
\ge\frac12.
\]

Combining with the homogeneous floor gives the cutoff-uniform physical bound

\[
\boxed{
|\Gamma_i^{H^1,inh}|
\ge
\frac1{\sqrt2}
}
\]

for every member of the cycle and every `n>=1`.

### Status

`NS-P2-FRAME-COMPATIBLE-DYADIC-H1-INH-FLOOR` — **DERIVED**.

This matters because the coefficient floor now lives in the same Sobolev normalization as the P2B observation quantity `K_N`.

---

## 5. H1 channel amplitude weights for the packing theorem

Let `X_{ell,s}` denote the scalar modal coordinate normalized by the inhomogeneous H1 weight.  A cycle channel then has the schematic cubic transfer form

\[
T_e^{H^1}
=
A_e^{H^1}\cos\varepsilon_e,
\]

where

\[
\boxed{
A_e^{H^1}
=|\Gamma_e^{H^1,inh}|
\,|X_{in,1}X_{in,2}X_{out}|.
}
\]

For the exact compatible-frame cycle,

\[
|\Gamma_e^{H^1,inh}|\ge1/\sqrt2.
\]

Therefore the small-amplitude branch of the local frustration-or-cut lemma cannot be caused by scale decay of the coefficient itself.  It must come from an actual small modal amplitude product.

This makes `A_e^{H^1}` a natural candidate weight for the non-overcounted holonomy packing theorem.

### Status

`NS-P2-H1-CYCLE-WEIGHT-ADAPTER` — **DERIVED as a finite algebraic coordinate identity**.

It is **not** yet an all-boundary coverage theorem.

---

## 6. What is now closer to P2 closure

The older H3-normalized cycle floor decays like `n^-2`.  In contrast, the H1-normalized cycle used by the finite-observation route has a uniform coefficient floor:

```text
cutoff scale n -> infinity
    does not weaken the four-channel H1 coupling coefficient.
```

Thus one possible scale-escape mechanism is removed for this exact family.

The remaining spatial theorem can now be stated in the correct P2B normalization:

\[
\boxed{
\text{H1 critical shell-production envelope at }N_j\to N_{j+1}
\Longrightarrow
\text{packable gauge-robust holonomy mass}
\quad\text{or}\quad
\text{small H1 amplitude cut + controlled conflict-free remainder}.
}
\]

If the packed mass is a fixed positive fraction of the relevant H1 channel envelope, `NS_P2_HOLONOMY_PACKING_DICHOTOMY.md` gives a cutoff-independent strict phase deficit because `c_0=1-1/sqrt(2)` is fixed and the cycle coefficient floor above is cutoff-uniform.

What remains OPEN is the actual NSE shell-production coverage and the later time-window step converting an instantaneous spatial deficit into a recurrence for `K_N` / `R_j`.

### Claim boundary

```text
H1 homogeneous cycle coefficient floor                    DERIVED
H1 inhomogeneous cutoff-uniform floor                      DERIVED
finite H1 cycle-weight coordinate identity                 DERIVED
actual H1 critical-flux/shell-production coverage          OPEN
time-window persistence/switching                          OPEN
constructive R_j recurrence                                OPEN
NS-P2-FRUSTRATION-OR-CUT                                   OPEN
NS-P2B-SCALE-CONTRACTION-UNIFORM                           OPEN
Clay Navier-Stokes regularity                              OPEN
```
