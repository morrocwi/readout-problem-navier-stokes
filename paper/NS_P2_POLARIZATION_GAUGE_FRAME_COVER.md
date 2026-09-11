# NS P2 — polarization-gauge red-team and shared-frame coverage reduction

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_polarization_gauge_frame.py`

## 1. Why this attack is load-bearing

The preceding P2 work found exact channel-level phase holonomies in the repository's declared real divergence-free polarization basis.  Before using those holonomies as a physical cross-scale mechanism, they must survive a more basic red-team question:

> does the obstruction survive a change of polarization basis inside each two-dimensional divergence-free Fourier fiber?

The answer is **no for a single wavevector triad, and no for the previous coplanar two-triad ladder as an unavoidable statement**.

That does not invalidate the exact coefficient calculations in their declared basis.  It changes their role:

```text
standard-basis scalar-channel holonomy
    = exact coordinate statement
    != basis-invariant P2 transfer obstruction.
```

This correction sharpens the active frontier.  A load-bearing P2 mechanism must use geometry that cannot be removed by modewise polarization-frame choices.  The natural invariant object is the incompatibility of the **triad-adapted frames** carried by distinct non-coplanar triads sharing a Fourier mode.

---

## 2. Every non-collinear triad has an adapted sparse tensor

Let

\[
p+q=k,
\qquad p\times q\ne0.
\]

Write

\[
A=|p\times q|,
\qquad P=|p|,
\qquad Q=|q|,
\qquad K=|k|.
\]

Choose the unit normal to the triad plane

\[
N=\frac{p\times q}{A},
\]

and, at every mode \(\ell\in\{p,q,k\}\), the in-plane divergence-free unit direction

\[
T_\ell=N\times\frac{\ell}{|\ell|}.
\]

Then \((N,T_\ell)\) is an orthonormal basis of \(\ell^\perp\).

For the Fourier--Leray scalar coefficient

\[
c(h_p,h_q;h_k)
=(h_p\cdot q)(h_k\cdot h_q)
 +(h_q\cdot p)(h_k\cdot h_p),
\]

with unit output polarization, the exact adapted-frame tensor has only three nonzero entries:

\[
\boxed{
\begin{aligned}
c(N,T_q;N)&=-\frac{A}{Q},\\
 c(T_p,N;N)&=+\frac{A}{P},\\
 c(T_p,T_q;T_k)&=
 \frac{A(Q^2-P^2)}{PQK}.
\end{aligned}}
\]

All other five entries of the \(2\times2\times2\) polarization tensor vanish.

### Status

`NS-P2-TRIAD-ADAPTED-SPARSE-TENSOR` — **DERIVED**, with exact symbolic checker support.

This already proves that no single wavevector triad carries an unavoidable eight-channel polarization holonomy: there is always a real divergence-free basis in which its tensor is sparse.

---

## 3. Exact matching counterexample to basis-invariant single-triad holonomy

Rotate only the \(p\)-fiber basis by

\[
E_1=\cos\theta\,N+\sin\theta\,T_p,
\qquad
E_2=-\sin\theta\,N+\cos\theta\,T_p,
\]

while keeping the \(q\)- and \(k\)-fibers adapted.

The four channels into \(k/N\) are

\[
\begin{aligned}
c(E_1,T_q;N)&=-\frac{A}{Q}\cos\theta,\\
 c(E_1,N;N)&=+\frac{A}{P}\sin\theta,\\
 c(E_2,T_q;N)&=+\frac{A}{Q}\sin\theta,\\
 c(E_2,N;N)&=+\frac{A}{P}\cos\theta.
\end{aligned}
\]

Their product is

\[
\boxed{
-\frac{A^4}{P^2Q^2}
\sin^2\theta\cos^2\theta.
}
\]

Thus any non-adapted generic rotation creates a four-channel \(\pi\)-holonomy face, whereas at an adapted axis \(\theta\in(\pi/2)\mathbb Z\) two members of the face vanish and the obstruction disappears.

Therefore the precise candidate statement

```text
single-wavevector-triad scalar-channel holonomy is unavoidable under
all real divergence-free polarization-basis choices
```

is **REFUTED** by an exact general construction.

### Status

`NS-P2-SINGLE-TRIAD-HOLONOMY-BASIS-INVARIANT` — **REFUTED**.

This ruling does not retract the old exact standard-basis coefficient identities.  It retracts only the stronger interpretation that such a channel holonomy is by itself a basis-independent physical obstruction.

---

## 4. The previous all-n coplanar ladder is also gauge-removable

The earlier all-\(n\) overlapping ladder used modes

\[
p=(0,0,1),
\quad
k_-=(n,-n,-1),
\quad
k_0=(n,-n,0),
\quad
k_+=(n,-n,1).
\]

Every mode lies in the same plane spanned by

\[
(0,0,1)
\quad\text{and}\quad
(1,-1,0).
\]

Hence both wavevector triads share one plane normal and admit one common adapted frame field

\[
(N,T_k)
\]

on all participating modes.

In that common adapted gauge each triad has the sparse three-channel form above.  For \(n\ge1\), both have adapted coefficient signs

\[
(-,+,+).
\]

The six outward-saturation equations are simultaneously satisfiable.  In quarter-turn units modulo four, one explicit assignment is

```text
(pN,pT,k_-N,k_-T,k_0N,k_0T,k_+N,k_+T)
=
(0,0,0,2,3,1,2,0).
```

The checker verifies all six equations exactly.

### Consequence

The previously recorded `NS-P2-COMPLEX-HOLONOMY-ALLN` remains an exact theorem **in the declared repository standard basis**, but it is not a basis-invariant load-bearing P2 obstruction.

The same caution applies to the single-wavevector-triad dyadic and three-parameter geometric holonomy notes: their coefficient identities remain exact in the declared basis, but the holonomy component is not by itself invariant under polarization-frame changes.

This correction is necessary before any boundary coverage claim is promoted.

---

## 5. What survives the gauge red-team: shared-mode frame mismatch

Consider two non-collinear triads

\[
\tau_1=(p,q_1,k_1),
\qquad
\tau_2=(p,q_2,k_2),
\]

sharing the mode \(p\), with

\[
k_r=p+q_r.
\]

Each triad defines a unit normal direction in the shared polarization plane \(p^\perp\):

\[
N_r=\frac{p\times q_r}{|p\times q_r|}.
\]

The adapted frame at \(p\) is the unordered orthogonal pair

\[
\{N_r,T_{p,r}\},
\qquad
T_{p,r}=N_r\times\frac p{|p|}.
\]

Because swapping the two axes gives the same frame, the correct invariant separation is the projective-frame angle

\[
\boxed{
\delta
=
\operatorname{dist}
\bigl(\angle(N_1,N_2),(\pi/2)\mathbb Z\bigr)
\in[0,\pi/4].
}
\]

For any chosen orthonormal basis of \(p^\perp\), let \(d_r\) be its distance from the adapted axes of \(\tau_r\), again modulo \(\pi/2\).  The triangle inequality on the projective circle gives

\[
\boxed{
\max(d_1,d_2)\ge\frac\delta2.
}
\]

So if \(\delta>0\), no shared-mode polarization basis can adapt both triads simultaneously.

### Status

`NS-P2-SHARED-MODE-FRAME-MISMATCH` — **DERIVED**.

This is basis-invariant geometry: \(\delta\) depends only on the two wavevector triad planes.

---

## 6. Quantitative coefficient floor from frame mismatch

Choose the private \(q_r\)- and \(k_r\)-fibers in their triad-adapted frames.  For whichever triad satisfies

\[
d_r\ge\delta/2,
\]

the four-face coefficients in Section 3 all obey

\[
\boxed{
|c_i|
\ge
\frac{|p\times q_r|}{\max(|p|,|q_r|)}
\sin\frac\delta2.
}
\]

The same four coefficients have negative product, so their saturation targets carry a \(\pi\) holonomy.

For unit polarization vectors, the homogeneous \(H^3\)-normalized coefficient is

\[
\Gamma_i^{hom}
=2c_i\frac{|k_r|^3}{|p|^3|q_r|^3}.
\]

Hence the selected triad has the coefficient floor

\[
\boxed{
|\Gamma_i^{hom}|
\ge
2\frac{|p\times q_r|\,|k_r|^3}
{|p|^3|q_r|^3\max(|p|,|q_r|)}
\sin\frac\delta2.
}
\]

For nonzero integer modes, the inhomogeneous/homogeneous \(H^3\) normalization ratio is at least \(1/8\), so

\[
\boxed{
|\Gamma_i^{inh}|
\ge
\frac{|p\times q_r|\,|k_r|^3}
{4|p|^3|q_r|^3\max(|p|,|q_r|)}
\sin\frac\delta2.
}
\]

This is not yet a global transfer tax because scalar amplitude products may still be small.  But it turns the local alternative into the correct form:

```text
large projective frame mismatch
  -> a four-channel pi holonomy with an explicit coefficient floor

or

some required scalar amplitude product is small
  -> amplitude cut.
```

### Status

`NS-P2-FRAME-MISMATCH-COEFFICIENT-FLOOR` — **DERIVED**.

---

## 7. Explicit all-n non-coplanar pair with maximal frame mismatch

Take

\[
p=(0,0,n),
\qquad
q_1=(n,0,0),
\qquad
q_2=(n,n,0),
\qquad n\ge1.
\]

Then

\[
k_1=(n,0,n),
\qquad
k_2=(n,n,n).
\]

The two triad normals are

\[
p\times q_1=(0,n^2,0),
\qquad
p\times q_2=(-n^2,n^2,0),
\]

so

\[
\angle(N_1,N_2)=\frac\pi4.
\]

Thus

\[
\boxed{\delta=\frac\pi4}
\]

is the maximal projective-frame separation.

For every shared-mode basis, at least one triad has

\[
d_r\ge\frac\pi8.
\]

For both triads

\[
\frac{|p\times q_r|}{\max(|p|,|q_r|)}=n,
\]

so every member of the selected frustrated face has raw coefficient magnitude at least

\[
\boxed{
n\sin\frac\pi8.
}
\]

The checker also verifies the uniform all-\(n\) homogeneous \(H^3\) floor

\[
\boxed{
|\Gamma_i^{hom}|
\ge
\frac{3\sqrt6}{2n^2}\sin\frac\pi8
}
\]

and the conservative inhomogeneous floor

\[
\boxed{
|\Gamma_i^{inh}|
\ge
\frac{3\sqrt6}{16n^2}\sin\frac\pi8.
}
\]

This is a genuine non-coplanar shared-mode obstruction to simultaneous triad adaptation.

---

## 8. From one pair to a weighted incident-frame cover

The next coverage step can be stated without choosing a polarization basis.

At one shared mode \(p\), let active incident triads be indexed by \(r\), with nonnegative weights \(w_r\), total weight

\[
W=\sum_r w_r.
\]

Let \(\theta_r\) denote the adapted-frame angle in \(p^\perp\), modulo \(\pi/2\).  Define the projective frame order parameter

\[
\boxed{
Z_p
=\frac1W\sum_r w_r e^{i4\theta_r}
}
\]

and frame dispersion

\[
\boxed{
D_p=1-|Z_p|^2.
}
\]

This is invariant under a common polarization-basis rotation at the mode.

Expanding the square gives the exact finite identity

\[
\boxed{
D_p
=
\frac{4}{W^2}
\sum_{r<s}w_rw_s
\sin^2\bigl(2\delta_{rs}\bigr),
}
\]

where \(\delta_{rs}\in[0,\pi/4]\) is the projective-frame separation of the two incident triads.

Therefore frame dispersion is exactly a weighted count of non-simultaneously-adaptable triad pairs.

### Status

`NS-P2-FRAME-DISPERSION-IDENTITY` — **DERIVED**.

---

## 9. Quantitative pair-mass lower bound

Fix \(a\in[0,1)\) and call a pair separated if

\[
\sin^2(2\delta_{rs})\ge a.
\]

Let

\[
S_a
=\sum_{r<s:\,\sin^2(2\delta_{rs})\ge a}w_rw_s.
\]

Since

\[
\sum_{r<s}w_rw_s\le\frac{W^2}{2},
\]

the dispersion identity implies

\[
\frac{D_pW^2}{4}
\le
\frac{aW^2}{2}+(1-a)S_a.
\]

Hence whenever \(D_p>2a\),

\[
\boxed{
S_a
\ge
\frac{W^2}{1-a}
\left(\frac{D_p}{4}-\frac a2\right)
>0.
}
\]

Thus positive frame dispersion forces a positive weighted mass of incident triad pairs with a definite projective mismatch.  Every such pair is eligible for the coefficient-floor/frustration-or-amplitude-cut lemma in Section 6.

### Status

`NS-P2-FRAME-DISPERSION-PAIR-MASS` — **DERIVED**.

The checker audits the identity and lower bound on an exact rational fixture with

\[
(\theta_1,\theta_2,\theta_3)
=(0,\pi/8,\pi/4),
\qquad
(w_1,w_2,w_3)=(1,2,3),
\]

for which

\[
D_p=\frac79.
\]

---

## 10. What this changes in the P2 attack

The previous immediate target was phrased as a symmetry-orbit coverage theorem for standard-basis holonomy motifs.  The gauge red-team shows that this is not the right invariant formulation.

The stronger and safer decomposition is now:

```text
at a boundary-active shared mode p:

D_p bounded below
    -> positive weighted mass of non-coplanar/non-orthogonal frame pairs
    -> explicit shared-frame mismatch
    -> local coefficient-floor + phase-frustration-or-amplitude-cut candidates

D_p small
    -> incident triad planes concentrate near one orthogonal projective frame
    -> geometric frame-concentration remainder branch.
```

This is closer to the P2 parent theorem because it applies to an arbitrary finite incident triad family at one mode rather than one hand-picked wavevector family.

---

## 11. Remaining load-bearing gaps

This note does **not** close `NS-P2-FRUSTRATION-OR-CUT`.

The exact remaining spatial tasks are now narrower:

1. choose the weights \(w_r\) from the actual dyadic critical-transfer envelope, not an arbitrary diagnostic weight;
2. convert weighted pair mass \(S_a\) into a non-overcounted transfer deficit or a controlled finite packing;
3. prove that the low-dispersion frame-concentration branch is either quantitatively weak, effectively lower-dimensional, or otherwise summable;
4. aggregate the per-mode estimate across one dyadic boundary.

Only after those are proved should the programme move to temporal switching and the recurrence

\[
R_{j+1}\le(1-\delta_j)R_j+\beta_j.
\]

### Current status

```text
single-triad unavoidable basis-invariant channel holonomy     REFUTED
old coplanar ladder unavoidable holonomy interpretation       REFUTED
old standard-basis coefficient/holonomy identities            retained in declared basis only
triad-adapted sparse tensor                                    DERIVED
shared-mode projective frame mismatch                          DERIVED
frame-mismatch coefficient floor                               DERIVED
weighted frame-dispersion identity                             DERIVED
weighted separated-pair mass bound                            DERIVED
actual dyadic flux weighting / non-overcounted packing         OPEN
low-dispersion frame-concentration remainder                   OPEN
temporal switching                                             OPEN
constructive R_j recurrence                                    OPEN
NS-P2-FRUSTRATION-OR-CUT                                       OPEN
Clay Navier--Stokes regularity                                 OPEN
```

The next attack should therefore target the **low-dispersion frame-concentration escape branch** and the conversion of \(D_p\) to actual flux weights.  Any future attack that does not reduce one of those two gaps does not materially approach P2 closure.
