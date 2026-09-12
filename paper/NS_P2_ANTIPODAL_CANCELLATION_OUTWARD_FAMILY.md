# NS P2 — Antipodal Cancellation Forces Outward Descendants in an Exact Family

**Status:** NEW DERIVATION / PROPOSAL; exact symbolic family  
**Global OCSR / Witness Soundness:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Family class (claim boundary):** every wavevector of this family has `k_z = 0` and every generated polarization is `e_3`, so the family lies in the 2D3C reduction (terminal class P, where regularity is classical). The results below exhibit the exact constraint-propagation / outward mechanism inside that class; they are not evidence about the productive non-planar sector, and the cross-family question (`NS_P2_CROSS_FAMILY_BOUNDARY_CANCELLATION.md`) is where a `k_z ≠ 0` recruit first enters.  
**Checker:** `reproduction/checks/check_ns_p2_antipodal_cancellation_outward.py`

## 0. Reuse-first path

This note uses only the existing P2 bilinear interaction, cancellation ledger, full-convolution closure rule, Genesis lineage/sufficiency requirements, and the already-open antipodal-source branch.

No new proof architecture is introduced.

## 1. Family

Take nonzero real parameters `K,P` and real amplitudes `x,z,w`. Define

\[
k=(K,0,0),\qquad p=(0,P,0),\qquad p'=-p,
\]

\[
q=k-p=(K,-P,0),\qquad q'=k+p=(K,P,0).
\]

Use the reality-coupled polarization on the antipodal pair

\[
a_{p}=a_{-p}=e_3,
\]

and

\[
b_q=(Px,Kx,z),\qquad d_{q'}=(-Px,Kx,w).
\]

The divergence-free conditions hold exactly:

\[
p\cdot a=(-p)\cdot a=q\cdot b=q'\cdot d=0.
\]

## 2. Exact shared-target cancellation

For the existing symmetric projected NSE interaction `B`, direct symbolic reduction gives

\[
\boxed{B_{p,q}(a,b)=KP x\,e_3,}
\]

\[
\boxed{B_{-p,q'}(a,d)=-KP x\,e_3.}
\]

Hence the two productive contributions cancel exactly at the common target `k`:

\[
\boxed{B_{p,q}(a,b)+B_{-p,q'}(a,d)=0.}
\]

For `x\neq0`, both parent interactions are nonzero.

This is a genuine reality-active / antipodal-source cancellation family, unlike W1/W2/W3 where the reality constraint was vacuous.

## 3. Cross descendants

Full convolution also contains the crossed pairs

\[
p+q'=(K,2P,0),
\qquad
-p+q=(K,-2P,0).
\]

The same exact symbolic calculation gives

\[
\boxed{B_{p,q'}(a,d)=KP x\,e_3,}
\]

\[
\boxed{B_{-p,q}(a,b)=-KP x\,e_3.}
\]

Therefore

\[
\boxed{x\neq0\Longrightarrow
B_{p,q'}\neq0\ \text{and}\ B_{-p,q}\neq0.}
\]

The nuisance parameters `z,w` cancel out of these conclusions.

## 4. Strict outward geometry

Let

\[
s_+=(K,2P,0),\qquad s_-=(K,-2P,0).
\]

Then

\[
|s_\pm|^2=K^2+4P^2,
\]

while

\[
|q|^2=|q'|^2=K^2+P^2,
\quad |p|^2=P^2,
\quad |k|^2=K^2.
\]

Thus for `K,P\neq0`,

\[
\boxed{|s_\pm|^2>|q|^2,\ |p|^2,\ |k|^2.}
\]

So productive exact cancellation at the shared target forces two strictly outward descendants in this entire symbolic family.

## 5. Proposed local result

`PROP-P3-ANTIPODAL-CANCEL-OUTWARD-01` — **NEW DERIVATION / PROPOSAL; exact symbolic PASS**.

Statement:

```text
For the declared antipodal family above, exact cancellation of two nonzero
parent contributions at k cannot suppress full-convolution closure. If the
parent is productive (x != 0), two crossed descendants at (K,+/-2P,0) are
nonzero and strictly farther out in wavevector magnitude than every parent
or shared target.
```

## 6. Consequence for the current open branch

This does not prove global OCSR, because a larger web may recruit additional sources to cancel the two outward descendants.

It does remove one previously untouched loophole:

```text
Fourier reality + an antipodal source pair
```

is not, by itself, a lossless cancellation mechanism. In this exact family, cancelling the shared target merely transfers the burden to two outward targets.

Under the existing Genesis/Standalone rule, any larger zero-defect web attempting to suppress those targets must register additional null/cancellation constraints rather than silently deleting them.

## 7. Next reuse-first target

The next missing piece is no longer "does an antipodal cancellation example exist?" It does.

The smallest remaining question is:

```text
Can a larger antipodal/full-convolution web cancel both forced outward
descendants without either (i) creating another outward descendant,
(ii) accumulating an incompatible cancellation constraint,
(iii) becoming degenerate/planar, or (iv) exiting the interior?
```

That is a concrete subcase of global multi-source cancellation compatibility / OCSR, not a new architecture.
