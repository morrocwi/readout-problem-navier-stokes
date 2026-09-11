# NS P2 — non-overcounted holonomy packing or small hitting set

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_holonomy_packing_dichotomy.py`

## 1. Why this lemma is needed

A collection of local phase-holonomy cycles cannot simply have its local taxes added: cycles may share scalar channels, so naive summation double-counts the same amplitude budget.

This note removes that obstruction for any finite family of four-channel `pi`-holonomy cycles.  It gives an exact deterministic alternative:

```text
large non-overcounted fractional cycle packing
    -> global quantitative phase tax

or

small packed mass
    -> small weighted hitting set whose removal intersects every declared conflict cycle.
```

Thus the remaining P2 spatial problem is not generic overcounting.  It is domain-specific coverage of the actual dyadic critical-flux network and control of the conflict-free/hitting-set remainder.

---

## 2. Finite channel model

Let `E` be a finite set of scalar Fourier--Leray channels.  Each channel has a positive amplitude prefactor

\[
A_e>0,
\qquad e\in E,
\]

and phase error `epsilon_e` from its outward-saturation target, so

\[
T_e=A_e\cos\varepsilon_e.
\]

Let `C` be a declared finite family of four-channel exact `pi`-holonomy cycles.  For every cycle `C in C`, the four phase errors obey a signed relation congruent to `pi`, hence

\[
\max_{e\in C}|\varepsilon_e|_{\mathbb T}\ge\frac\pi4.
\]

Therefore

\[
\boxed{
\sum_{e\in C}\cos\varepsilon_e
\le
3+\frac1{\sqrt2}
=4-c_0,
}
\]

where

\[
\boxed{c_0=1-\frac1{\sqrt2}>0.}
\]

This is the phase-only form of the local holonomy tax.

---

## 3. Greedy fractional cycle packing

Initialize residual channel capacities

\[
r_e^{(0)}=A_e.
\]

While there exists a declared conflict cycle `C` for which every member has strictly positive residual capacity, set

\[
x_C=\min_{e\in C}r_e
\]

and replace

\[
r_e\leftarrow r_e-x_C
\qquad(e\in C).
\]

Leave all other residuals unchanged and continue.

Every iteration makes at least one previously positive residual exactly zero, so the algorithm terminates after at most `|E|` iterations.

Let `P` denote the total packed mass:

\[
\boxed{P=\sum_C x_C.}
\]

For every channel,

\[
\boxed{
A_e=r_e+\sum_{C\ni e}x_C,
\qquad r_e\ge0.
}
\]

Thus the construction is an exact non-overcounting fractional allocation of channel amplitude to conflict cycles.

### Status

`NS-P2-HOLONOMY-GREEDY-PACKING` — **DERIVED**.

---

## 4. Aggregate transfer tax without double counting

Using the exact amplitude decomposition,

\[
\sum_{e\in E}T_e
=
\sum_C x_C\sum_{e\in C}\cos\varepsilon_e
+
\sum_{e\in E}r_e\cos\varepsilon_e.
\]

Each packed cycle satisfies

\[
\sum_{e\in C}\cos\varepsilon_e\le4-c_0,
\]

and every residual term satisfies

\[
\cos\varepsilon_e\le1.
\]

Therefore

\[
\sum_eT_e
\le
(4-c_0)\sum_Cx_C+\sum_er_e.
\]

But

\[
\sum_eA_e
=4\sum_Cx_C+\sum_er_e.
\]

Subtracting gives the exact global finite inequality

\[
\boxed{
\sum_{e\in E}T_e
\le
\sum_{e\in E}A_e
-c_0P.
}
\]

Hence overlapping cycles may share channels arbitrarily; the tax is still additive on the **fractionally allocated** cycle mass.

### Status

`NS-P2-HOLONOMY-NONOVERLAP-TAX` — **DERIVED**.

---

## 5. The saturated channels form a hitting set

At termination define

\[
H=\{e\in E:r_e=0\}.
\]

If some declared conflict cycle avoided `H`, then every edge of that cycle would have positive residual capacity and the greedy procedure would not have terminated.  Therefore

\[
\boxed{
H\cap C\ne\varnothing
\quad\text{for every declared conflict cycle }C.
}
\]

So `H` is a hitting set for the entire declared cycle family.

Moreover, for every saturated edge

\[
A_e=\sum_{C\ni e}x_C.
\]

Since every selected cycle has four edges,

\[
\sum_{e\in H}A_e
=
\sum_{e\in H}\sum_{C\ni e}x_C
\le
4\sum_Cx_C.
\]

Thus

\[
\boxed{
A(H):=\sum_{e\in H}A_e\le4P.
}
\]

### Status

`NS-P2-HOLONOMY-HITTING-SET` — **DERIVED**.

---

## 6. Exact packing-or-cut dichotomy

Let

\[
S=\sum_{e\in E}A_e
\]

and choose any threshold

\[
0<\eta<\frac14.
\]

There are two branches.

### Branch A — substantial packed conflict mass

If

\[
P\ge\eta S,
\]

then the aggregate tax gives

\[
\boxed{
\sum_eT_e
\le
(1-c_0\eta)S.
}
\]

This is a strict relative deficit independent of cycle overlap.

### Branch B — small cycle-hitting cut

If

\[
P<\eta S,
\]

then the saturated hitting set satisfies

\[
\boxed{
A(H)<4\eta S.
}
\]

Removing a channel set carrying less than a `4 eta` fraction of the total amplitude budget intersects every declared four-channel `pi`-holonomy cycle.

Therefore

\[
\boxed{
\text{strict non-overcounted frustration tax}
\quad\text{or}\quad
\text{small weighted conflict-hitting cut}.
}
\]

### Status

`NS-P2-HOLONOMY-PACKING-OR-HITTING-CUT` — **DERIVED**.

This is a finite aggregation theorem.  It is materially closer to the parent P2 target because it resolves the overlap/packing obstruction once a relevant cycle family and its actual amplitude weights have been identified.

---

## 7. Exact rational checker fixture

The checker uses channel amplitudes

\[
(A_0,\ldots,A_5)=(5,4,6,3,7,2)
\]

and three overlapping four-cycles

```text
C1=(0,1,2,3)
C2=(2,3,4,5)
C3=(0,1,4,5).
```

The greedy allocation is exactly

\[
x_{C1}=3,
\qquad
x_{C3}=1,
\qquad
P=4.
\]

The residual saturated set is

\[
H=\{1,3\},
\]

with

\[
A(H)=7\le16=4P.
\]

Every declared cycle meets `H`, and the checker verifies every per-channel decomposition exactly with rational arithmetic.

### Status

`NS-P2-HOLONOMY-PACKING-FIXTURE` — **PASS**.

---

## 8. What this removes from the P2 frontier

Before this lemma, one unresolved spatial concern was:

```text
many local holonomy cycles may overlap so strongly that their local taxes
cannot be aggregated without double counting.
```

For a finite declared family of four-channel `pi` cycles, that obstruction is now removed.  The greedy fractional allocation gives an exact aggregate tax or a small weighted hitting set.

What remains is more specific and therefore closer to the PDE bridge:

1. define `E_j` using the actual channels contributing to the critical outward dyadic flux;
2. define `A_e` from the actual positive channel amplitude prefactors relevant to that flux;
3. build a sufficiently complete **gauge-robust** conflict-cycle catalogue on `E_j`;
4. in the small-hitting-set branch, prove the conflict-free remainder plus the cut cannot still carry critical onward transfer;
5. aggregate the resulting spatial inequality across the dyadic boundary;
6. only then control temporal switching and derive the `R_j` recurrence.

Thus the current load-bearing statement has narrowed to

\[
\boxed{
\text{actual dyadic critical-flux network}
\Longrightarrow
\text{large packable gauge-robust conflict mass}
\quad\text{or}\quad
\text{small cut + quantitatively controlled conflict-free remainder}.
}
\]

### Current claim boundary

```text
non-overcounted fractional holonomy aggregation          DERIVED
packing -> strict relative tax                           DERIVED
small packing -> small weighted hitting set              DERIVED
actual critical-flux cycle catalogue/coverage            OPEN
conflict-free remainder control                          OPEN
temporal switching                                       OPEN
constructive R_j recurrence                              OPEN
NS-P2-FRUSTRATION-OR-CUT                                 OPEN
Clay Navier-Stokes regularity                            OPEN
```
