# NS P2 — fresh-donor window response-or-cancellation charge

**Date:** 2026-09-11  
**Parent structural target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Parent scale target:** `NS-P2B-SCALE-CONTRACTION-UNIFORM` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_fresh_donor_window_charge.py`

## 1. Why this is the next load-bearing lemma

The previous P2 merge established two complementary facts.

1. Conflict-rich transfer pays a non-overcounted holonomy tax, and that tax survives arbitrary switching of which cycle edge is frustrated across the observation window.
2. A conflict-free selected fresh-donor tree can be phase-SAT and uniformly H1-coupled, but it is not dynamically closed: two consecutive donors generate an off-tree Fourier mode.

The remaining question is therefore dynamical rather than purely geometric:

\[
\boxed{
\text{if consecutive fresh donors overlap in time, where must that nonlinear forcing go?}
}
\]

This note gives an exact answer for the self-similar donor pair.  The forcing must appear either as response of the induced mode or as cancellation by other NSE interactions.  The statement integrates over arbitrary time windows and over any finite set of dyadic blocks.

It does not yet bound those two cost buckets by `K_N` or dissipation strongly enough to close the recurrence; that adapter remains the next target.

---

## 2. Self-similar donor pair

For any positive integer scale `n`, take the consecutive donors from the exact fresh-donor tree:

\[
q_0=n(1,0,1),
\qquad
q_1=n(2,0,-1),
\]

and their induced target

\[
r=q_0+q_1=n(3,0,0).
\]

All three lie in the `xz` plane.  Use the common unit normal

\[
N=(0,1,0)
\]

and unit tangential polarization

\[
T_\ell=\frac{N\times\ell}{|\ell|}.
\]

The exact Fourier--Leray coefficient of

\[
q_0/T_{q_0}+q_1/T_{q_1}\to r/T_r
\]

is

\[
\boxed{
c_n=\frac{3\sqrt{10}}{10}n.}
\]

---

## 3. Exact physical inhomogeneous H1 amplitude coefficient

For this unit-polarization scalar coordinate define the physical inhomogeneous H1 coordinate

\[
X_k=\sqrt{1+|k|^2}\,z_k.
\]

The donor term in the normalized **amplitude equation** has coefficient

\[
\alpha_n
=c_n
\frac{\sqrt{1+|r|^2}}
{\sqrt{1+|q_0|^2}\sqrt{1+|q_1|^2}}.
\]

Substituting the exact lengths gives

\[
\boxed{
\alpha_n=
\frac{3\sqrt{10}}{10}n
\frac{\sqrt{1+9n^2}}
{\sqrt{1+2n^2}\sqrt{1+5n^2}}.
}
\]

Its square satisfies the exact factorization

\[
\boxed{
\alpha_n^2-\frac12
=
\frac{(n^2-1)(31n^2+5)}
{10(1+2n^2)(1+5n^2)}
\ge0.
}
\]

Hence for every integer `n>=1`,

\[
\boxed{
\alpha_n\ge\frac1{\sqrt2}.
}
\]

This is stronger than the earlier generic inhomogeneous comparison because it uses the exact wavevector family.

### Status

`NS-P2-FRESH-DONOR-H1-AMPLITUDE-FLOOR` — **DERIVED** from the exact symbolic identity.

The factor `alpha_n` is the normalized amplitude-ODE coefficient, not the energy-transfer coefficient with the extra factor `2`.

---

## 4. Exact response-or-cancellation inequality

Let `R_r(t)` denote the sum of **all other** normalized nonlinear contributions to the same scalar `r/T_r` equation after removing the declared `q_0,q_1` donor pair.  The exact projected NSE coordinate equation is

\[
\boxed{
\dot X_r+\nu |r|^2X_r
=-i\alpha_nX_{q_0}X_{q_1}+R_r.
}
\]

Define the target-mode response density

\[
D_r(t)=\dot X_r(t)+\nu |r|^2X_r(t).
\]

Rearranging and using the triangle inequality gives

\[
\alpha_n|X_{q_0}X_{q_1}|
\le |D_r|+|R_r|.
\]

Using the cutoff-uniform coefficient floor,

\[
\boxed{
\frac1{\sqrt2}|X_{q_0}X_{q_1}|
\le
|\dot X_r+\nu|r|^2X_r|+|R_r|.
}
\]

This is an exact dynamical charge: large simultaneous donor amplitude cannot disappear.  It must be paid by induced-mode response or by nonlinear cancellation from other channels.

### Status

`NS-P2-FRESH-DONOR-RESPONSE-OR-CANCELLATION` — **DERIVED**.

---

## 5. Window charge

Let `I=[t_0,t_1]` be any finite interval on which the relevant Fourier coordinates are absolutely continuous.  Integrating gives

\[
\boxed{
\frac1{\sqrt2}
\int_I|X_{q_0}X_{q_1}|\,dt
\le
\int_I|\dot X_r+\nu|r|^2X_r|\,dt
+
\int_I|R_r|\,dt.
}
\]

No assumption is made that the donor phases, the target phase, or the cancelling channels are time-independent.

### Status

`NS-P2-FRESH-DONOR-WINDOW-CHARGE` — **DERIVED**.

---

## 6. Quiet-target implies cancellation charge

The response term has the elementary upper bound

\[
\int_I|\dot X_r+\nu|r|^2X_r|\,dt
\le
\operatorname{TV}_I(X_r)
+
\nu|r|^2\int_I|X_r|\,dt,
\]

where

\[
\operatorname{TV}_I(X_r)=\int_I|\dot X_r|\,dt.
\]

Therefore

\[
\boxed{
\int_I|R_r|\,dt
\ge
\frac1{\sqrt2}\int_I|X_{q_0}X_{q_1}|\,dt
-
\operatorname{TV}_I(X_r)
-
\nu|r|^2\int_I|X_r|\,dt.
}
\]

So if the induced mode remains both small and dynamically quiet, the donor overlap must be cancelled by other Fourier interactions of comparable integrated strength.

### Status

`NS-P2-FRESH-DONOR-QUIET-TARGET-CANCELLATION` — **DERIVED**.

This does not yet say that the cancellation term is harmful; the next recursive step must charge those cancelling interactions rather than allowing an infinite free cancellation cascade.

---

## 7. High-amplitude donor overlap has a time-measure cost

For any threshold `lambda>0`, define

\[
E_\lambda
=
\{t\in I:
|X_{q_0}(t)|\ge\lambda,
\ |X_{q_1}(t)|\ge\lambda\}.
\]

On `E_lambda`,

\[
|X_{q_0}X_{q_1}|\ge\lambda^2.
\]

Hence

\[
\boxed{
\frac{\lambda^2}{\sqrt2}|E_\lambda|
\le
\int_I|D_r|\,dt+
\int_I|R_r|\,dt.
}
\]

Equivalently, if the dynamic response/cancellation budget is small, two consecutive donors cannot both remain large for a large fraction of the observation window.

### Status

`NS-P2-FRESH-DONOR-HIGH-OVERLAP-MEASURE` — **DERIVED**.

---

## 8. Finite multiscale composition

For the self-similar tree let

\[
n_m=4^m,
\]

\[
q_{m,0}=n_m(1,0,1),
\qquad
q_{m,1}=n_m(2,0,-1),
\qquad
r_m=n_m(3,0,0).
\]

The target modes `r_m` are distinct for distinct `m`.  Applying the window charge to each block and summing over any finite index set `M` gives

\[
\boxed{
\frac1{\sqrt2}
\sum_{m\in M}
\int_I|X_{q_{m,0}}X_{q_{m,1}}|\,dt
\le
\sum_{m\in M}
\int_I|D_{r_m}|\,dt
+
\sum_{m\in M}
\int_I|R_{r_m}|\,dt.
}
\]

This is an exact finite composition across arbitrarily many dyadic blocks.  It does not assume that the remainder terms on the right are disjoint; recursive non-overcounting of those cancellation channels is still OPEN.

### Status

`NS-P2-FRESH-DONOR-MULTISCALE-WINDOW-CHARGE` — **DERIVED** for every finite set of self-similar blocks.

---

## 9. What this removes and what remains

Before this lemma the conflict-poor branch could be described only qualitatively as

```text
donor amplitude cut
or temporal separation
or induced interaction
or cancellation complexity.
```

The new exact inequality gives one common quantitative currency for all four possibilities:

\[
\boxed{
\text{donor-overlap mass}
\lesssim
\text{induced-mode response}
+
\text{other-channel cancellation mass}.
}
\]

with explicit all-scale constant `sqrt(2)`.

The next load-bearing P2 theorem is now:

\[
\boxed{
\text{bound / recursively pack the summed response and cancellation terms}
\Longrightarrow
\text{window loss for conflict-poor transfer}
\Longrightarrow
\text{channel-envelope contraction for }K_N/R_j.
}
\]

Current claim boundary:

```text
exact inhomogeneous H1 donor amplitude floor                 DERIVED
pointwise response-or-cancellation charge                    DERIVED
window donor-overlap charge                                  DERIVED
quiet-target cancellation lower bound                        DERIVED
high-amplitude overlap time-measure bound                    DERIVED
finite multiscale window composition                         DERIVED
recursive non-overcounting of cancellation channels          OPEN
response/cancellation budget -> K_N inequality               OPEN
constructive R_j recurrence                                  OPEN
NS-P2-FRUSTRATION-OR-CUT                                     OPEN
NS-P2B-SCALE-CONTRACTION-UNIFORM                             OPEN
Clay Navier-Stokes regularity                                OPEN
```
