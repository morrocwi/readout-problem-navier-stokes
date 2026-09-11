# NS P2 — exact dyadic fresh-donor tree escape

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_dyadic_fresh_donor_tree.py`

## 1. Why this attack is load-bearing

The current P2 programme has genuine gauge-robust holonomy cycles and a non-overcounted packing theorem.  The next question is whether the conflict-free remainder is automatically weak.

It is not.

This note gives an exact all-scale family of dyadic-reaching Fourier--Leray channels which is

```text
phase SAT,
acyclic at the selected channel-incidence level,
conflict-free for every finite prefix,
and H1-coupling-nondegenerate uniformly in scale.
```

Therefore a proof of P2 cannot close the small-packing branch by asserting

```text
no holonomy cycle => weak coupling / no dyadic transfer.
```

The missing control must use additional NSE structure such as amplitude budget, dissipation, induced off-tree interactions, or time-window dynamics.

---

## 2. Two-step self-similar dyadic geometry

Let

\[
n_m=4^m,
\qquad m=0,1,2,\ldots
\]

and define backbone modes

\[
P_{2m}=n_m(1,0,0),
\qquad
P_{2m+1}=n_m(2,0,1),
\qquad
P_{2m+2}=n_m(4,0,0).
\]

Introduce fresh donor modes

\[
Q_{2m}=n_m(1,0,1),
\qquad
Q_{2m+1}=n_m(2,0,-1).
\]

Then exactly

\[
P_j+Q_j=P_{j+1}.
\]

In max-coordinate scale,

\[
\|P_{2m}\|_\infty=n_m,
\quad
\|P_{2m+1}\|_\infty=2n_m,
\quad
\|P_{2m+2}\|_\infty=4n_m.
\]

Thus every selected interaction advances the backbone by one dyadic boundary.

All wavevectors lie in the `xz` plane.  Use the common unit normal

\[
N=(0,1,0)
\]

and, for every nonzero planar mode `ell`, the unit tangential polarization

\[
T_\ell=\frac{N\times\ell}{|\ell|}.
\]

Select one scalar channel per triad:

\[
\boxed{
P_j/N+Q_j/T_{Q_j}\longrightarrow P_{j+1}/N.
}
\]

---

## 3. Exact Fourier--Leray coefficients

For a channel `p/N+q/T_q -> k/N`, because `N` is orthogonal to every planar wavevector,

\[
c(p,q;k)=T_q\cdot p.
\]

For the two self-similar shapes the checker obtains

\[
\boxed{
c_{2m}=\frac{n_m}{\sqrt2}}
\]

and

\[
\boxed{
c_{2m+1}=-\frac{4n_m}{\sqrt5}}.
\]

Both are nonzero at every scale.

### Status

`NS-P2-DYADIC-FRESH-DONOR-COEFF-ALLN` — **PASS** for the exact symbolic identities.

---

## 4. Exact phase satisfiability and absence of holonomy

Let `phi_j` be the phase of the backbone coordinate `P_j/N` and `psi_j` the phase of the fresh donor coordinate `Q_j/T_{Q_j}`.

The outward-saturation equation is

\[
\phi_j+\psi_j-\phi_{j+1}
=\operatorname{sgn}(c_j)\frac\pi2
\pmod{2\pi}.
\]

Choose

\[
\boxed{\phi_j=0\quad\text{for all }j}
\]

and

\[
\boxed{
\psi_{2m}=+\frac\pi2,
\qquad
\psi_{2m+1}=-\frac\pi2.
}
\]

Every selected dyadic channel is then exactly outward-saturated.

More generally, for any finite prefix, each incidence row contains the fresh donor phase `psi_j`, and that donor phase appears in no other selected row.  Hence the incidence rows are linearly independent over the integers: any integer linear dependency must have zero coefficient on the row containing the last fresh donor, and induction removes every row.

Therefore no finite prefix contains a phase-holonomy cycle in this selected channel family.

### Status

`NS-P2-FRESH-DONOR-TREE-SAT` — **DERIVED**.

This is a constructive SAT result, not merely failure to find a contradiction.

---

## 5. Cutoff-uniform H1 coupling

Use homogeneous physical H1-normalized scalar coordinates.  With unit polarizations,

\[
\Gamma^{H^1,hom}
=2c\frac{|k|}{|p||q|}.
\]

For the two repeating shapes,

\[
\boxed{
\Gamma_{2m}^{H^1,hom}=\sqrt5
}
\]

and

\[
\boxed{
\Gamma_{2m+1}^{H^1,hom}=-\frac{32}{5\sqrt5}.
}
\]

Consequently

\[
\boxed{
|\Gamma_j^{H^1,hom}|\ge\sqrt5
}
\]

for every selected channel and every scale.

For inhomogeneous physical H1 weights, the normalization correction satisfies

\[
\frac{|\Gamma^{H^1,inh}|}{|\Gamma^{H^1,hom}|}
=\frac{R_1(|k|)}{R_1(|p|)R_1(|q|)},
\qquad
R_1(L)=\frac{\sqrt{1+L^2}}{L},
\]

and `1 <= R_1(L) <= sqrt(2)` for every nonzero integer mode.  Therefore

\[
\boxed{
|\Gamma_j^{H^1,inh}|\ge\frac{\sqrt5}{2}
}
\]

uniformly in the dyadic depth.

### Status

`NS-P2-DYADIC-FRESH-DONOR-H1-FLOOR` — **DERIVED**.

Thus the conflict-free selected chain is not made harmless by coefficient decay in the same H1 normalization used by `K_N`.

---

## 6. Matching refutations

The exact family is a matching counterexample to the following over-broad spatial claims:

```text
phase-satisfiable / cycle-free channel remainder
    -> no dyadic scale advance;

phase-satisfiable / cycle-free channel remainder
    -> H1 coupling decays with cutoff;

absence of holonomy cycles alone
    -> strict P2 scale contraction.
```

Record:

`NS-P2-CONFLICT-FREE-REMAINDER-GEOMETRICALLY-WEAK` — **REFUTED**.

`NS-P2-SPATIAL-HOLONOMY-ALONE-FORCES-CONTRACTION` — **REFUTED** as an inference from phase incidence plus coupling geometry alone.

These refutations do **not** produce an NSE blow-up trajectory.  A state containing many such modes may generate additional off-tree convolution channels, and a time-dependent cascade must obey the full NSE dynamics.  The result says precisely that the residual P2 theorem cannot discard the conflict-free branch by static phase/coupling geometry alone.

---

## 7. What this does to the P2 frontier

The spatial programme has now separated into two exact branches.

### Conflict-rich branch

The holonomy packing theorem gives

\[
\sum_eT_e\le\sum_eA_e-c_0P,
\qquad
c_0=1-1/\sqrt2,
\]

so a positive packed fraction gives strict loss.

### Conflict-poor branch

The fresh-donor family proves that the remaining cycle-free network can still contain dyadic, phase-saturated, uniformly H1-coupled channels.

Therefore the next load-bearing theorem must control the conflict-poor branch by genuinely dynamical structure:

\[
\boxed{
\text{fresh-donor / conflict-free critical transfer}
\Longrightarrow
\text{amplitude/dissipation cost, induced interactions, or time-window loss}.
}
\]

Current boundary:

```text
large packed holonomy mass -> strict pointwise tax                DERIVED
conflict-free dyadic H1-nondegenerate selected tree exists       DERIVED / exact family
conflict-free remainder automatically weak                       REFUTED
window/dynamical control of fresh-donor remainder                 OPEN
constructive R_j recurrence                                      OPEN
NS-P2-FRUSTRATION-OR-CUT                                         OPEN
NS-P2B-SCALE-CONTRACTION-UNIFORM                                 OPEN
Clay Navier-Stokes regularity                                    OPEN
```
