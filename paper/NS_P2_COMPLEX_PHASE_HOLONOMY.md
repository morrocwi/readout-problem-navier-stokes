# NS P2 — exact complex phase holonomy and local frustration-or-cut

**Date:** 2026-09-11  
**Programme:** finite-first / readout-based Navier–Stokes attack  
**Active parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**New exact checker:** `reproduction/checks/check_ns_p2_phase_holonomy.py`

## 1. Result in one line

The real-coordinate four-term sign motif can be lifted to a genuine overlapping **complex Fourier phase-incidence obstruction** for every integer scale parameter `n>=1`.

The resulting four actual Fourier–Leray scalar channels have an exact phase holonomy mismatch of

\[
\Delta=\pi,
\]

so they cannot all achieve their outward-saturation phases simultaneously.

This gives a local quantitative complex-network frustration tax and an exact local frustration-or-amplitude-cut dichotomy. It does **not** yet prove dyadic boundary coverage, time-window persistence, or scale contraction.

---

## 2. Fixed Fourier–Leray channel convention

Use the same unnormalised real divergence-free basis convention as the existing all-`n` P2 checkers. For every nonzero Fourier wavevector `k`, choose real basis vectors

\[
h_{k,1},h_{k,2}\perp k.
\]

For one scalar complex polarization slot write

\[
u_k=z_k h_{k,s}.
\]

For `p+q=k`, including both ordered convection contributions `(p,q)` and `(q,p)`, the scalar coefficient in the `k`-slot is

\[
\boxed{
c_\tau=
\frac{
(h_{p,s_p}\!\cdot q)(h_{k,s_k}\!\cdot h_{q,s_q})
+
(h_{q,s_q}\!\cdot p)(h_{k,s_k}\!\cdot h_{p,s_p})
}{
|h_{k,s_k}|^2
}.
}
\]

Because `h_{k,s_k}\perp k`, testing the Leray-projected output against `h_{k,s_k}` is exactly the same as testing the pre-projected vector; the formula is therefore an actual Fourier–Leray scalar channel coefficient, not an abstract shell model.

The channel contribution to the complex scalar ODE is

\[
\dot z_k\big|_\tau=-i\,c_\tau z_pz_q.
\]

Hence

\[
\frac{d}{dt}|z_k|^2\Big|_\tau
=
2c_\tau\operatorname{Im}(z_pz_q\overline{z_k}).
\]

Writing

\[
z_\ell=a_\ell e^{i\phi_\ell},
\qquad
\Theta_\tau=\phi_p+\phi_q-\phi_k,
\]

and

\[
A_\tau=2|c_\tau|a_pa_qa_k,
\]

the outward-oriented channel contribution is

\[
T_\tau
=
A_\tau
\cos(\Theta_\tau-\Theta_\tau^*),
\]

with exact saturation target

\[
\boxed{
\Theta_\tau^*=\operatorname{sgn}(c_\tau)\frac{\pi}{2}
\pmod{2\pi}.
}
\]

Thus the target phase is derived from the actual coefficient sign; it is not imposed universally in advance.

---

## 3. The all-`n` overlapping channel motif

For every positive integer `n`, define

\[
p=(0,0,1),\qquad
k_-=(n,-n,-1),\qquad
k_0=(n,-n,0),\qquad
k_+=(n,-n,1).
\]

Take the following four scalar channels:

\[
\begin{aligned}
A:\;&p/e_1+k_-/e_1\to k_0/e_1,\\
B:\;&p/e_1+k_-/e_1\to k_0/e_2,\\
C:\;&p/e_2+k_0/e_1\to k_+/e_1,\\
D:\;&p/e_2+k_0/e_2\to k_+/e_1.
\end{aligned}
\]

Direct exact symbolic Fourier–Leray calculation gives

\[
\boxed{
c_A=-n,\qquad
c_B=-\frac1n,\qquad
c_C=-\frac{n^3}{n^2+1},\qquad
c_D=+\frac{n^3}{n^2+1}.
}
\]

Therefore their saturation targets, measured in quarter turns `pi/2`, are

\[
(-1,-1,-1,+1).
\]

All four coefficients are nonzero for every integer `n>=1`.

### Status

`NS-P2-COMPLEX-CHANNEL-COEFF-ALLN` — **PASS** for the exact symbolic checker.

---

## 4. Exact phase holonomy obstruction

Let each incidence row represent

\[
\phi_p+\phi_q-\phi_k.
\]

The four rows satisfy the exact integer relation

\[
\boxed{
r_A-r_B+r_C-r_D=0.
}
\]

Indeed, `A-B` leaves only the difference between the two `k_0` polarization phases, while `C-D` gives the opposite difference.

If all four channels were simultaneously outward-saturated, the same linear combination of their requested target angles would have to vanish modulo `2pi`. Instead,

\[
-\frac{\pi}{2}
-\left(-\frac{\pi}{2}\right)
-\frac{\pi}{2}
-\left(+\frac{\pi}{2}\right)
=
-\pi
\not\equiv0\pmod{2\pi}.
\]

Therefore the four saturation equations are exactly inconsistent:

\[
\boxed{
\text{no complex phase assignment saturates }A,B,C,D\text{ simultaneously}.
}
\]

This is a genuine shared-mode/shared-polarization **complex phase holonomy** obstruction. It is stronger in interpretation than the earlier real-coordinate monomial parity witness because the contradiction now lives directly in the complex Fourier phase-incidence system.

### Status

`NS-P2-COMPLEX-HOLONOMY-ALLN` — **DERIVED**, with exact symbolic checker support.

---

## 5. Quantitative angular deficit

Let

\[
\varepsilon_i
=
\Theta_i-\Theta_i^*
\]

be the principal circular phase error for `i=A,B,C,D`.

Because the incidence combination vanishes while the target combination has holonomy `pi`,

\[
\varepsilon_A-\varepsilon_B+\varepsilon_C-\varepsilon_D
\equiv\pi\pmod{2\pi}.
\]

If all four circular errors had magnitude strictly less than `pi/4`, the absolute value of a lifted left-hand side would be strictly less than `pi`, which cannot represent the class `pi mod 2pi`.

Hence

\[
\boxed{
\max_i
\operatorname{dist}_{\mathbb T}(\Theta_i,\Theta_i^*)
\ge\frac{\pi}{4}.
}
\]

For at least one channel `j`,

\[
T_j
=
A_j\cos\varepsilon_j
\le
\frac{A_j}{\sqrt2}.
\]

All other channels satisfy `T_i<=A_i`. Therefore

\[
\boxed{
\sum_{i=A}^D T_i
\le
\sum_{i=A}^D A_i
-
\left(1-\frac1{\sqrt2}\right)
\min_{i=A,\ldots,D} A_i.
}
\]

This is the first local quantitative tax in this programme derived from a genuine complex overlapping-channel holonomy rather than from a real-coordinate sign cycle.

### Status

`NS-P2-COMPLEX-HOLONOMY-TAX` — **DERIVED**.

---

## 6. Exact local frustration-or-cut lemma

Fix any threshold `lambda>0` and let

\[
m_C=\min_i A_i.
\]

Then exactly one of the following useful branches holds:

### Cut branch

\[
m_C\le\lambda.
\]

At least one channel needed by this motif has amplitude prefactor at most `lambda`.

### Frustration branch

\[
m_C>\lambda,
\]

and therefore

\[
\boxed{
\sum_iT_i
<
\sum_iA_i
-
\left(1-\frac1{\sqrt2}\right)\lambda.
}
\]

So the complex holonomy gives the desired logical form

\[
\boxed{
\text{amplitude cut}
\quad\text{or}\quad
\text{strict phase-frustration tax}.
}
\]

### Status

`NS-P2-LOCAL-FRUSTRATION-OR-CUT` — **DERIVED**.

This is local to the declared four-channel motif. It must not be promoted to the parent all-boundary theorem.

---

## 7. What this closes and what remains open

This result closes the first missing step identified in `FUTURE_WORK_P2_TRIAD_ATTACK.md`:

```text
real-coordinate sign frustration
    -> genuine complex shared-mode phase holonomy
```

It also supplies a concrete FW-3/FW-4 style quantitative local deficit.

It does **not** prove:

```text
one motif -> positive weighted fraction of all boundary flux
all dyadic boundaries -> covered by such motifs
static tax -> time-window tax
local amplitude cut -> onward cascade cut
local tax -> R_{j+1} <= (1-delta_j) R_j + beta_j
```

Therefore the parent theorem remains

```text
NS-P2-FRUSTRATION-OR-CUT — OPEN
```

and no Clay/global regularity claim changes status.

---

## 8. Immediate next attack

The most useful next step is not to search for another isolated frustration motif.

The new motif contains the polarization slot

\[
k_0/e_2=(n,-n,0)/e_2,
\]

which is also one of the input slots in the existing dyadic high–high family

\[
(n,n,0)+(n,-n,0)=(2n,0,0).
\]

So the next exact search should glue:

```text
complex holonomy motif at scale n
        +
dyadic high-high channel n -> 2n
```

and ask whether a shared-slot network crossing the dyadic boundary remains fully phase-satisfiable.

The falsification test is:

```text
SAT with full outward saturation
    -> record a matching escape network and sharpen the theorem

UNSAT
    -> extract the smallest exact cross-boundary holonomy cycle,
       then derive its weighted tax and amplitude-cut consequence
```

Only after that should the programme attempt boundary coverage or time-window aggregation.
