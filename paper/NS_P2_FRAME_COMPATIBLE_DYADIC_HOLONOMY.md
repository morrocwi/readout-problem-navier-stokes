# NS P2 — exact frame-compatible 3D dyadic holonomy

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_frame_compatible_dyadic_holonomy.py`

## 1. Why this closes a real escape attempt

The polarization-gauge red-team shows that a scalar-channel holonomy confined to one wavevector triad, or to a coplanar ladder that admits one common adapted frame, is not a basis-invariant P2 obstruction.

That creates an immediate escape candidate:

```text
all incident triads remain projectively frame-compatible (D_p=0)
    -> choose one global compatible polarization frame
    -> perhaps all outward phase targets become satisfiable.
```

The all-`n` network below kills that implication exactly.

It is simultaneously:

- genuinely three-dimensional;
- projectively frame-compatible at every shared mode;
- generated from modes at scale `n` without importing a pre-existing `2n` mode;
- reaches max-coordinate scale `2n` at its final output;
- and nevertheless contains an exact four-channel `pi` phase holonomy with a physical `H^3` coefficient floor.

Thus zero frame dispersion is **not** by itself a phase-satisfiable escape.

---

## 2. The all-`n` wavevector network

For every positive integer `n`, define

\[
a=n(1,0,0),
\qquad
b=n(0,0,1),
\qquad
c=n(0,1,0).
\]

Build

\[
p=a+b=n(1,0,1),
\]

\[
q=p+c=n(1,1,1),
\]

and finally

\[
k=p+q=n(2,1,2).
\]

The three exact triads are

\[
\tau_0:a+b=p,
\qquad
\tau_1:p+c=q,
\qquad
\tau_2:p+q=k.
\]

The seed vectors `a,b,c` are linearly independent, so the network is not coplanar.  The final mode has

\[
\|k\|_\infty=2n,
\]

while all three seeds satisfy

\[
\|a\|_\infty=\|b\|_\infty=\|c\|_\infty=n.
\]

Hence the network reaches an exact max-coordinate dyadic boundary from scale-`n` seeds.

---

## 3. Exact projective-frame compatibility

The triad-plane normals are

\[
a\times b=n^2(0,-1,0),
\]

\[
p\times c=n^2(-1,0,1),
\]

and

\[
p\times q=n^2(-1,0,1).
\]

At the shared mode `p`, the normal for `tau_0` is orthogonal to the common normal of `tau_1` and `tau_2`.

But an adapted polarization frame is an unordered orthogonal pair in `p^perp`, so rotating its normal axis by `pi/2` leaves the same projective frame.  Therefore the projective frame separation at `p` is exactly

\[
\boxed{\delta_p=0.}
\]

At the shared mode `q`, `tau_1` and `tau_2` have parallel normals, so

\[
\boxed{\delta_q=0.}
\]

Consequently, for any positive incident weights,

\[
\boxed{D_p=D_q=0}
\]

for the projective frame-dispersion quantity introduced in `NS_P2_POLARIZATION_GAUGE_FRAME_COVER.md`.

This network therefore lies exactly in the low-dispersion/frame-compatible branch.

### Status

`NS-P2-FRAME-COMPATIBLE-3D-DYADIC-NETWORK` — **PASS** for the exact wavevector/frame identities.

---

## 4. One global compatible polarization frame

Let

\[
y=(0,1,0),
\qquad
d=(-1,0,1).
\]

Choose the following unnormalised orthogonal divergence-free pairs:

```text
a : y , (0,0,-1)
b : y , (1,0,0)
p : y , d
c : d , (-1,0,-1)
q : d , (-1,2,-1)
k : d , (-1,4,-1)
```

The checker verifies exactly, at every mode `ell`, that both declared vectors are perpendicular to `ell` and to each other.

This is one global real polarization gauge compatible with all three projective adapted frames.

---

## 5. Exact Fourier--Leray coefficients

Using the same scalar coefficient convention as the rest of the P2 attack,

\[
c(h_1,h_2;h_o)
=
\frac{
(h_1\cdot v_2)(h_o\cdot h_2)
+(h_2\cdot v_1)(h_o\cdot h_1)
}{|h_o|^2},
\]

all nonzero channels in this global frame are:

\[
\begin{array}{c|c}
\text{channel} & c_\tau \\
\hline
T0A & +n\\
T0B & -n\\
T1A & +n\\
T1B & -n/3\\
T1C & -2n\\
T2A & +n\\
T2B & +n/9\\
T2C & -2n
\end{array}
\]

The checker derives every entry directly from the wavevectors and declared polarization vectors.

### Status

`NS-P2-FRAME-COMPATIBLE-CHANNEL-COEFF-ALLN` — **PASS**.

---

## 6. Minimal cross-triad phase holonomy

Use phase variables for the scalar slots appearing in

```text
T1B: p0 + c1 -> q1      coefficient -n/3
T1C: p1 + c1 -> q0      coefficient -2n
T2A: p0 + q0 -> k0      coefficient +n
T2C: p1 + q1 -> k0      coefficient -2n
```

Let the corresponding incidence rows be `r_T1B`, `r_T1C`, `r_T2A`, `r_T2C`, where every row has the form

\[
\phi_{in,1}+\phi_{in,2}-\phi_{out}.
\]

They satisfy the exact integer relation

\[
\boxed{
r_{T1C}-r_{T1B}+r_{T2A}-r_{T2C}=0.}
\]

The outward-saturation target for a real coefficient `c` is

\[
\Theta^*=\operatorname{sgn}(c)\frac\pi2.
\]

Therefore the same combination of target phases is

\[
-\frac\pi2
-
\left(-\frac\pi2\right)
+
\frac\pi2
-
\left(-\frac\pi2\right)
=
\pi.
\]

Hence

\[
\boxed{
\text{the four outward-saturation equations are exactly UNSAT.}
}
\]

This holonomy lives across **two distinct wavevector triads** and survives inside a single global polarization frame that is projectively adapted to the entire three-triad network.

It therefore survives the main gauge-removability objection that killed the stronger interpretation of the earlier coplanar standard-basis motif.

### Status

`NS-P2-FRAME-COMPATIBLE-DYADIC-HOLONOMY-ALLN` — **DERIVED**.

---

## 7. Quantitative phase tax

The cycle has four channels and target holonomy `pi`.  The same circle-distance argument used in the earlier local holonomy note yields

\[
\boxed{
\max_{i\in C}
\operatorname{dist}_{\mathbb T}(\Theta_i,\Theta_i^*)
\ge\frac\pi4.
}
\]

If

\[
A_i=2|c_i|\,|z_{in,1}z_{in,2}z_{out}|
\]

denotes the positive amplitude prefactor in the chosen scalar coordinates, then

\[
\boxed{
\sum_{i\in C}T_i
\le
\sum_{i\in C}A_i
-
\left(1-\frac1{\sqrt2}\right)
\min_{i\in C}A_i.
}
\]

Thus the network gives an exact local frustration-or-amplitude-cut dichotomy even though its incident projective frame dispersion is zero.

### Status

`NS-P2-FRAME-COMPATIBLE-DYADIC-TAX` — **DERIVED**.

---

## 8. Physical `H^3` coefficient floor

Using the homogeneous physical coordinate weight

\[
W_{\ell,s}^{hom}=|h_{\ell,s}|^2|\ell|^6,
\]

the exact normalized coefficients of all eight nonzero channels are

\[
\begin{array}{c|c}
\text{channel} & \Gamma_\tau^{hom} \\
\hline
T0A & 4\sqrt2/n^2\\
T0B & -4\sqrt2/n^2\\
T1A & 3\sqrt6/(2n^2)\\
T1B & -3\sqrt2/(2n^2)\\
T1C & -3\sqrt3/n^2\\
T2A & 3\sqrt6/(2n^2)\\
T2B & \sqrt2/(2n^2)\\
T2C & -3/n^2.
\end{array}
\]

The four-channel holonomy cycle uses `T1B,T1C,T2A,T2C`, so every member obeys

\[
\boxed{
|\Gamma_i^{hom}|
\ge
\frac{3\sqrt2}{2n^2}.
}
\]

For nonzero integer wavevectors, the inhomogeneous/homogeneous `H^3` normalization ratio is at least `1/8`, hence conservatively

\[
\boxed{
|\Gamma_i^{inh}|
\ge
\frac{3\sqrt2}{16n^2}
\qquad(i\in C).
}
\]

So the holonomy does not arise from an exactly vanishing or arbitrarily smaller channel within this all-`n` shape family.

### Status

`NS-P2-FRAME-COMPATIBLE-DYADIC-H3-FLOOR` — **DERIVED**.

---

## 9. What this refutes

The network is a matching counterexample to the candidate implication

```text
exact projective frame compatibility / zero frame dispersion
    -> all outward phase targets can be simultaneously satisfied.
```

Therefore

`NS-P2-ZERO-FRAME-DISPERSION-IMPLIES-PHASE-SAT` — **REFUTED**.

It also refutes the stronger escape claim

```text
low-dispersion branch = necessarily coplanar or unable to reach a dyadic boundary.
```

The exact zero-dispersion family above is 3D and reaches `||k||_infty=2n`.

`NS-P2-ZERO-FRAME-DISPERSION-IS-LOWER-DIMENSIONAL` — **REFUTED**.

---

## 10. Updated spatial frontier

This result materially narrows the remaining spatial coverage problem.

We now have two complementary invariant mechanisms:

```text
positive projective frame dispersion
    -> weighted mass of frame-mismatched incident pairs
    -> coefficient-floor frustration-or-cut candidates;

zero projective frame dispersion
    does NOT imply phase SAT:
    an exact 3D dyadic-reaching compatible-frame family still carries
    cross-triad pi holonomy.
```

But this is not yet an exhaustive dichotomy for arbitrary boundary flux.  The remaining load-bearing spatial theorem is:

\[
\boxed{
\text{actual critical dyadic flux}
\Longrightarrow
\text{positive weighted mass captured by a gauge-robust holonomy/cut network}
\quad\text{or}\quad
\text{a quantitatively controlled remainder}.
}
\]

In particular, the next attack should classify **frame-concentrated networks that avoid the explicit compatible-frame four-cycle**, rather than merely classifying coplanar versus non-coplanar triads.

Only after that coverage/decomposition survives red-team should the programme move to temporal switching.

### Current claim boundary

```text
frame-compatible all-n 3D dyadic holonomy                    DERIVED
frame-compatible local phase tax                             DERIVED
cycle H3 coefficient floor                                   DERIVED
zero frame dispersion -> phase SAT                           REFUTED
zero frame dispersion -> lower-dimensional/non-dyadic        REFUTED
full actual-flux boundary coverage/decomposition              OPEN
temporal switching                                            OPEN
constructive R_j recurrence                                   OPEN
NS-P2-FRUSTRATION-OR-CUT                                      OPEN
Clay Navier-Stokes regularity                                 OPEN
```
