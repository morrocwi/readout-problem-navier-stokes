# NS P2 — geometric frustration-or-cut in a 3-parameter Fourier–Leray family

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_geometric_frustration_cut_family.py`

## 1. Why this family matters

The preceding all-`n` dyadic holonomy result proves a strict local phase deficit for one exact `n -> 2n` polarization network, but it does not yet explain how a cascade might try to avoid that deficit.

This note enlarges the motif to a three-parameter actual Fourier–Leray family and obtains a sharper alternative:

```text
phase frustration
        or
phase compatibility forces geometry toward a weak-coupling regime.
```

This is still a family theorem, not a boundary coverage theorem.

---

## 2. Fourier geometry

Let `a,b,c` be positive integers and define

\[
p=(0,0,a),\qquad
q=(b,-b,c),\qquad
k=(b,-b,a+c),
\]

so that

\[
p+q=k.
\]

Use the repository's standard real divergence-free basis

\[
h_{\ell,1},h_{\ell,2}\perp \ell
\]

and fix the `p` input in its first polarization.  Let the `q` and `k` slots vary over both polarizations.  This gives the four-channel rectangle

\[
\begin{aligned}
A:\;&p/e_1+q/e_1\to k/e_1,\\
B:\;&p/e_1+q/e_2\to k/e_1,\\
C:\;&p/e_1+q/e_1\to k/e_2,\\
D:\;&p/e_1+q/e_2\to k/e_2.
\end{aligned}
\]

For a scalar channel `p+q=k`, including both ordered convection contributions, the actual Fourier–Leray scalar coefficient is

\[
c_\tau=
\frac{
(h_p\!\cdot q)(h_k\!\cdot h_q)
+(h_q\!\cdot p)(h_k\!\cdot h_p)
}{|h_k|^2}.
\]

The associated complex scalar contribution is

\[
\dot z_k=-i c_\tau z_pz_q,
\]

and hence the maximizing phase target is

\[
\Theta_\tau^*=\operatorname{sgn}(c_\tau)\frac\pi2
\pmod{2\pi}.
\]

---

## 3. Exact coefficient formulas

Set

\[
D_1=a^2+2ac+b^2+c^2,
\qquad
D_2=a^2+2ac+2b^2+c^2,
\]

and

\[
P=
 a^2b^2+a^2c^2+4ab^2c+2ac^3
 +2b^4+3b^2c^2+c^4.
\]

The exact channel coefficients are

\[
\boxed{
\begin{aligned}
c_A&=\frac{ab(a^2-b^2-c^2)}{D_1},\\
 c_B&=\frac{a^2b(ac+b^2+c^2)}{D_1},\\
 c_C&=-\frac{2a^2b^3}{D_1D_2},\\
 c_D&=-\frac{abP}{D_1D_2}.
\end{aligned}}
\]

For positive `a,b,c`,

\[
c_B>0,\qquad c_C<0,\qquad c_D<0,
\]

whereas the sign of `c_A` is exactly the sign of

\[
a^2-b^2-c^2.
\]

Indeed the exact product factorization is

\[
\boxed{
 c_Ac_Bc_Cc_D
=
\frac{
2a^6b^6(a^2-b^2-c^2)(ac+b^2+c^2)P
}{D_1^4D_2^2}.
}
\]

Thus the four-channel sign parity is controlled by one geometric scalar.

### Status

`NS-P2-GEOMETRIC-CHANNEL-FACTOR` — **PASS** for the exact symbolic identities in the checker.

---

## 4. Exact phase compatibility classification

Let each phase-incidence row represent

\[
\phi_p+\phi_q-\phi_k.
\]

For the rectangle above,

\[
\boxed{
r_A-r_B-r_C+r_D=0.}
\]

Each target is `sign(c_i) pi/2`.  For four signs `s_i in {+1,-1}`, the target combination

\[
(s_A-s_B-s_C+s_D)\frac\pi2
\]

vanishes modulo `2pi` exactly when

\[
s_As_Bs_Cs_D=+1.
\]

Therefore this family has an exact trichotomy.

### Frustration branch

If

\[
\boxed{a^2<b^2+c^2,}
\]

then

\[
c_Ac_Bc_Cc_D<0,
\]

so the four maximizing phase constraints have a `pi` holonomy mismatch.  They cannot be simultaneously saturated.

Exactly as in the preceding holonomy notes, the mismatch implies

\[
\max_i
\operatorname{dist}_{\mathbb T}(\Theta_i,\Theta_i^*)
\ge\frac\pi4
\]

and hence

\[
\boxed{
\sum_iT_i
\le
\sum_iA_i
-
\left(1-\frac1{\sqrt2}\right)\min_i A_i.
}
\]

### Exact cut boundary

If

\[
\boxed{a^2=b^2+c^2,}
\]

then

\[
\boxed{c_A=0.}
\]

One member of the rectangle is deleted exactly by geometry.

### Phase-compatible branch

If

\[
\boxed{a^2>b^2+c^2,}
\]

then the sign product is positive, and the four maximizing phase equations are compatible.  Therefore **phase frustration alone cannot control this branch**.

This is an exact counterexample to any over-broad claim that every member of this geometric family is phase-frustrated.

### Status

`NS-P2-GEOMETRIC-PHASE-TRICHOTOMY` — **DERIVED**.

---

## 5. What phase compatibility costs geometrically

Introduce the dimensionless ratios

\[
x=\frac ba,
\qquad
y=\frac ca.
\]

On the phase-compatible or exact-cut side,

\[
a^2\ge b^2+c^2,
\]

so

\[
\boxed{x^2+y^2\le1.}
\]

The max-frequency gain in the vertical output coordinate is

\[
\frac{a+c}{a}=1+y.
\]

Therefore an attempt to make the interaction nearly dyadic forces `y` close to one, and then the phase-compatible inequality forces `x` to zero:

\[
x\le\sqrt{1-y^2}.
\]

More explicitly, if

\[
a+c\ge(2-\eta)a,
\qquad 0\le\eta\le\frac12,
\]

then

\[
y\ge1-\eta
\]

and hence

\[
\boxed{
 x^2\le1-(1-\eta)^2
 =2\eta-\eta^2
 \le2\eta.
}
\]

Thus

\[
\boxed{
\frac ba\le\sqrt{2\eta}.}
\]

This is already a geometric cut: avoiding the phase holonomy while approaching factor-two scale gain squeezes the transverse component `b`.

---

## 6. Physical `H^3` normalized coupling also collapses

The preceding statement must not rely on the unnormalised polarization coordinates, because their basis vectors themselves change with geometry.  Therefore we normalize each channel by the physical homogeneous `H^3` coordinate weight

\[
W^{\rm hom}_{\ell,s}=|h_{\ell,s}|^2|\ell|^6.
\]

For a channel coefficient `c_i`, define

\[
\Gamma_i^{\rm hom}
=
2c_i\frac{\sqrt{W^{\rm hom}_{k,s_k}}}
{\sqrt{W^{\rm hom}_{p,e_1}W^{\rm hom}_{q,s_q}}}.
\]

After substituting

\[
b=ax,\qquad c=ay,
\]

every normalized coefficient has the exact form

\[
\boxed{
\Gamma_i^{\rm hom}=\frac{x}{a^2}F_i(x,y),
}
\]

with explicit rational/algebraic functions `F_i` verified by the checker.

Write

\[
 r=x^2+y^2,
\quad u=2x^2+y^2,
\quad v=x^2+y^2+2y+1,
\quad w=2x^2+y^2+2y+1.
\]

The exact dimensionless factors are

\[
\begin{aligned}
a^2\Gamma_A^{\rm hom}
&=
\frac{2x(1-r)w^{3/2}}
{\sqrt r\,u^{3/2}\sqrt v},\\[1mm]
a^2\Gamma_B^{\rm hom}
&=
\frac{2x(r+y)w^{3/2}}
{\sqrt r\,u^2\sqrt v},\\[1mm]
a^2\Gamma_C^{\rm hom}
&=
-\frac{4x^3w}
{\sqrt r\,u^{3/2}\sqrt v},\\[1mm]
a^2\Gamma_D^{\rm hom}
&=
-\frac{2xw\,P_*(x,y)}
{\sqrt r\,u^2\sqrt v},
\end{aligned}
\]

where

\[
P_*=2x^4+3x^2y^2+4x^2y+x^2+y^4+2y^3+y^2.
\]

Now restrict to

\[
y\ge\frac12,
\qquad x^2+y^2\le1.
\]

The following elementary bounds hold:

\[
 r\ge\frac14,
\qquad u\ge\frac14,
\qquad v\ge\frac94,
\qquad w\le4,
\qquad x^2\le\frac34,
\qquad P_*\le14.
\]

Applying these directly gives the conservative component bounds

\[
\frac{|a^2\Gamma_A^{\rm hom}|}{x}\le\frac{512}{3},
\]

\[
\frac{|a^2\Gamma_B^{\rm hom}|}{x}\le\frac{2048}{3},
\]

\[
\frac{|a^2\Gamma_C^{\rm hom}|}{x}\le128,
\]

and

\[
\frac{|a^2\Gamma_D^{\rm hom}|}{x}\le\frac{7168}{3}.
\]

Therefore all four satisfy the single envelope

\[
\boxed{
|\Gamma_i^{\rm hom}|
\le
3072\frac{x}{a^2}.
}
\]

For the repository's inhomogeneous `H^3` weight

\[
W^{\rm inh}_{\ell,s}
=|h_{\ell,s}|^2(1+|\ell|^2)^3,
\]

write

\[
R(L)=\frac{(1+L^2)^{3/2}}{L^3}.
\]

Because all nonzero integer wavevectors here have `L>=1`,

\[
1\le R(L)\le2\sqrt2.
\]

The normalized coefficient ratio is

\[
\frac{|\Gamma_i^{\rm inh}|}{|\Gamma_i^{\rm hom}|}
=
\frac{R(|k|)}{R(|p|)R(|q|)}
\le2\sqrt2.
\]

Hence

\[
\boxed{
|\Gamma_i^{\rm inh}|
\le
6144\sqrt2\frac{x}{a^2}.
}
\]

Combining this with the near-dyadic phase-compatible estimate

\[
x\le\sqrt{2\eta}
\]

gives

\[
\boxed{
|\Gamma_i^{\rm inh}|
\le
\frac{12288\sqrt\eta}{a^2}
\qquad
\text{for every }i=A,B,C,D.
}
\]

Thus, inside this family, escaping the phase-frustration branch while demanding scale gain approaching two forces **all four physically normalized channel couplings** to collapse like `sqrt(eta)/a^2`.

### Status

`NS-P2-GEOMETRIC-NEAR-DYADIC-CUT` — **DERIVED**.

---

## 7. Family theorem

For the declared Fourier–Leray family with positive integers `a,b,c`, the following exact/quantitative alternative holds.

If

\[
a^2<b^2+c^2,
\]

then the four-channel phase rectangle has a `pi` holonomy and the local frustration tax

\[
\sum_iT_i
\le
\sum_iA_i
-
\left(1-\frac1{\sqrt2}\right)\min_i A_i.
\]

If

\[
a^2=b^2+c^2,
\]

then `c_A=0` exactly.

If

\[
a^2>b^2+c^2
\]

and the scale gain obeys

\[
a+c\ge(2-\eta)a,
\qquad0\le\eta\le\frac12,
\]

then all four inhomogeneous `H^3` normalized couplings obey

\[
\boxed{
|\Gamma_i^{\rm inh}|
\le
\frac{12288\sqrt\eta}{a^2}.
}
\]

So within this actual NSE family, near-dyadic transfer cannot simultaneously have

```text
no phase frustration
and
nondegenerate normalized coupling.
```

### Status

`NS-P2-GEOMETRIC-FRUSTRATION-OR-CUT-FAMILY` — **DERIVED**.

---

## 8. Claim boundary

This is materially stronger than a single all-`n` motif because it classifies a three-parameter geometric family and identifies the escape branch quantitatively.

It still does **not** establish:

```text
all boundary-crossing Fourier triads
    -> this family or a symmetry copy;

general high-flux network
    -> positive weighted mass in covered geometric sectors;

small normalized coupling in one local family
    -> global onward-cascade suppression;

instantaneous family dichotomy
    -> time-window recurrence.
```

Therefore

```text
NS-P2-FRUSTRATION-OR-CUT — OPEN
```

and the Clay Navier–Stokes global regularity problem remains OPEN.

---

## 9. Next theorem target

The next load-bearing question is now a geometric coverage question rather than merely finding another sign cycle:

\[
\boxed{
\text{critical boundary flux}
\Longrightarrow
\text{enough mass in frustrated sectors}
\ \text{or}\
\text{enough mass in quantitatively weak-coupling sectors}.
}
\]

The correct next falsification search is to enumerate symmetry classes of actual boundary-crossing triads and try to construct a high-weight phase-compatible network that avoids every sector covered by this family and its lattice symmetries.  A matching escape network would refute over-broad coverage; failure should be converted into an exact finite sector/packing lemma before any PDE-scale claim is promoted.
