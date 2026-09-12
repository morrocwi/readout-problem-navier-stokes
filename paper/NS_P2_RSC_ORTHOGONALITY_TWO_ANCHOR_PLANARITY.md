# NS P2 — RSC-O Two-Anchor Orthogonality Suppression Forces Wavevector Planarity

**Status:** NEW DERIVATION / PROPOSAL; exact local linear-algebra theorem  
**Proposal id:** `PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01`  
**Parent:** `PROP-P3-RECURSIVE-SUPPRESSION-CHARGING-01` / RSC-O  
**Global RSC / OCSR / Witness Soundness / G4/G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_rsc_o_two_anchor_planarity.py`

## 0. Reuse-first path

A Toledo lookup found no matching two-anchor orthogonality-suppression planarity theorem. Reuse:

- the projected NSE bilinear interaction;
- `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`;
- the current RSC-O branch semantics.

No new global architecture is introduced.

---

## 1. Setup

Take two retained anchors

\[
(p_1,a_1),\qquad(p_2,a_2),
\]

with

\[
a_i\neq0,\qquad a_i\cdot p_i=0,
\]

and assume the retained polarization lines are independent:

\[
\boxed{a_1\times a_2\neq0.}
\]

Let a nonzero recruited mode / polarization pair satisfy

\[
q\neq0,\qquad b\neq0,\qquad b\cdot q=0.
\]

Assume the same recruited mode is cross-silent to both anchors **through the orthogonality branch**:

\[
\boxed{a_1\cdot q=0,\qquad a_2\cdot q=0,}
\tag{O-1}
\]

and

\[
\boxed{
\mathcal B_{p_1,q}(a_1,b)=0,
\qquad
\mathcal B_{p_2,q}(a_2,b)=0.
}
\tag{O-2}
\]

---

## 2. Orthogonality branch makes the kernel condition explicit

Let

\[
k_i=p_i+q.
\]

Because

\[
a_i\cdot p_i=0
\quad\text{and}\quad
a_i\cdot q=0,
\]

we have

\[
a_i\perp k_i.
\]

Therefore on the branch `a_i · q = 0`,

\[
\mathcal B_{p_i,q}(a_i,b)
=
\mathbb P_{k_i}\bigl((b\cdot p_i)a_i\bigr)
=
(b\cdot p_i)a_i.
\]

Since `a_i != 0`, exact cross silence implies

\[
\boxed{b\cdot p_1=0,\qquad b\cdot p_2=0.}
\tag{O-3}
\]

Thus the recruited polarization is simultaneously orthogonal to

\[
q,\ p_1,\ p_2.
\]

Because `b != 0` in `R^3`, those three wavevectors cannot span all of `R^3`:

\[
\boxed{
\det[p_1,p_2,q]=0.
}
\tag{O-4}
\]

Equivalently,

\[
\boxed{
\dim\operatorname{span}\{p_1,p_2,q\}\le2.
}
\]

So simultaneous O-labelled suppression against two independent retained polarization lines forces a planar wavevector triple.

---

## 3. Direction lock of the recruited mode

From (O-1) and `a_1 x a_2 != 0`, the orthogonal complement of

\[
W=\operatorname{span}\{a_1,a_2\}
\]

is one-dimensional. Therefore

\[
\boxed{
q\parallel a_1\times a_2.
}
\tag{O-5}
\]

Hence the same event pays two exact geometric charges at once:

```text
polarization-side charge: q is locked to W^perp;
wavevector-side charge:   p1,p2,q are coplanar.
```

This is stronger than the one-anchor nullity statement but remains local.

---

## 4. Consequence for an A1 two-line skeleton

In the surviving nonidentity A1 branch, recurrent returned polarizations lie on two fixed projective classes

\[
[\ell_+],[\ell_-].
\]

Choose nonzero representatives `a_+`, `a_-` with

\[
a_+\times a_-\neq0.
\]

Any recruited mode that is simultaneously O-silent to one retained anchor from each fixed line must satisfy

\[
\boxed{
q\parallel a_+\times a_-
}
\]

and its two anchor wavevectors plus `q` are planar.

Therefore repeated **double-O** suppression cannot roam through arbitrary 3D wavevector directions. It is confined to one normal direction determined by the two-line polarization skeleton and repeatedly creates planar wavevector certificates.

This is an exact local advance on RSC-O.

---

## 5. What is not proved

The theorem does not show that every O-labelled event is double-O. A web may attempt to alternate single-anchor orthogonality suppressions, mix `O` with `E` or `C`, replace anchors, or route descendants through other registered branches.

Therefore still OPEN:

- promotion from infinitely many O-labelled suppressions to infinitely many double-O events;
- compatibility of repeated planar triples across changing anchors;
- full RSC-O;
- recursive suppression charging globally;
- OCSR / Witness Soundness / FNW / G6;
- G4 / G7 / Clay regularity.

---

## 6. Proposed result

`PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01` — **NEW DERIVATION / PROPOSAL; exact local PASS**.

Bounded statement:

```text
If one nonzero recruited mode/polarization is exactly cross-silent through the
orthogonality branch to two retained anchors whose polarization lines are
independent, then the recruited mode is parallel to the normal of the two
polarization lines and the two anchor wavevectors together with the recruited
wavevector are coplanar.
```

This should be used as a charge certificate inside RSC-O, not as a global recurrence theorem.
