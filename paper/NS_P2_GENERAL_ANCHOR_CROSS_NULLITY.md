# NS P2 — General Anchor-Cross Nullity Locus

**Status:** NEW DERIVATION / PROPOSAL; exact local algebraic theorem  
**Global OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_general_anchor_cross_nullity.py`

## 0. Reuse-first path

This note follows the system rule

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

and introduces no new global architecture.

Reused objects:

- the existing symmetric projected NSE interaction `B`;
- the current full-convolution semantics;
- the equal-source-shell direction-lock result already present in the P2 Standalone branch;
- Genesis exact-domain / sufficiency discipline: retained distinctions and named defects are preserved rather than silently collapsed.

A Toledo lookup for an anchor-cross nullity theorem returned no matching object. The statement below is therefore a proposal.

## 1. Setup

Let

\[
p,q,k=p+q\in\mathbb R^3,
\qquad
p,q,k\neq0,
\]

and let the retained anchor polarization satisfy

\[
a\neq0,
\qquad
a\cdot p=0.
\]

For an incoming polarization

\[
b\in q^\perp,
\]

define the exact anchor-cross map

\[
\boxed{
L_{p,q,a}(b)
:=
\mathcal B_{p,q}(a,b)
\in k^\perp.
}
\]

The question is: when can a nonzero incoming polarization avoid producing any cross response against the retained anchor?

## 2. Exact kernel theorem

The kernel is nontrivial exactly on two algebraic loci:

\[
\boxed{
\ker L_{p,q,a}\neq\{0\}
\iff
\bigl(a\cdot q=0\bigr)
\ \vee\ 
\bigl(|q|=|p|\bigr).
}
\tag{ACN-1}
\]

Equivalently, off those two loci,

\[
\boxed{
 a\cdot q\neq0
 \quad\text{and}\quad
 |q|\neq|p|
 \Longrightarrow
 L_{p,q,a}:q^\perp\to k^\perp
 \text{ is invertible.}
}
\tag{ACN-2}
\]

This is the reusable statement needed after the first off-plane descendant: any newly recruited source that suppresses its cross interaction with a retained anchor must satisfy a declared exceptional constraint.

## 3. Coordinate-free proof

Write

\[
\lambda:=a\cdot q.
\]

Assume first that

\[
\lambda\neq0
\]

and that a nonzero

\[
b\in q^\perp
\]

satisfies

\[
L_{p,q,a}(b)=0.
\]

By definition of the Leray projection, the unprojected source

\[
\lambda b+(b\cdot p)a
\]

must be parallel to

\[
k=p+q.
\]

Hence for some scalar `c`,

\[
\lambda b+(b\cdot p)a=ck.
\tag{ACN-3}
\]

Set

\[
\beta:=b\cdot p.
\]

Taking the dot product of (ACN-3) with `p` and using `a\cdot p=0` gives

\[
\lambda\beta=c(k\cdot p).
\tag{ACN-4}
\]

Taking the dot product with `q` and using `b\cdot q=0` and `a\cdot q=\lambda` gives

\[
\lambda\beta=c(k\cdot q).
\tag{ACN-5}
\]

If `c=0`, then (ACN-3) and `lambda != 0` force `b=0`, contradiction. Therefore `c != 0`, and (ACN-4)–(ACN-5) imply

\[
k\cdot p=k\cdot q.
\]

Since

\[
k=p+q,
\]

this is exactly

\[
|p|^2+p\cdot q
=
|q|^2+p\cdot q,
\]

hence

\[
\boxed{|p|=|q|.}
\]

Conversely, assume

\[
|p|=|q|,
\qquad
\lambda\neq0.
\]

Define

\[
\boxed{
b_*
:=
k-\frac{k\cdot p}{\lambda}a.}
\tag{ACN-6}
\]

Then

\[
q\cdot b_*
=
k\cdot q-k\cdot p
=
|q|^2-|p|^2
=0,
\]

so `b_*` is an admissible `q`-polarization. Also

\[
\lambda b_*+(b_*\cdot p)a
=
\lambda k,
\]

whose projection to `k^perp` is zero. Thus

\[
L_{p,q,a}(b_*)=0.
\]

Finally, if

\[
\lambda=a\cdot q=0,
\]

then because also `a\cdot p=0`, we have

\[
a\perp k.
\]

For any nonzero

\[
b\in p^\perp\cap q^\perp
\]

(the intersection is always nontrivial in `R^3`),

\[
(a\cdot q)b+(b\cdot p)a=0,
\]

hence again

\[
L_{p,q,a}(b)=0.
\]

This proves (ACN-1).

## 4. Exact determinant factorization

In an adapted chart

\[
p=(P,0,0),
\qquad
 a=(0,A,C),
\qquad
 q=(x,y,z),
\]

the exact two-dimensional transverse determinant factors as

\[
\boxed{
\det L
=
\frac{(a\cdot q)^2\bigl(|q|^2-|p|^2\bigr)}{|p+q|^2},
}
\tag{ACN-7}
\]

up to the declared transverse coordinate chart. The checker verifies this identity exactly in `SymPy` with no floating arithmetic.

Thus the two exceptional loci are visible algebraically as the only determinant zeros:

\[
\boxed{
 a\cdot q=0
 \quad\text{or}\quad
 |q|=|p|.
}
\]

## 5. Constraint-accumulation interpretation

This theorem does **not** say that either exceptional locus is impossible.

It says that suppressing a full-convolution cross response is no longer a free event. Every suppression against a retained anchor must pay one of two exact algebraic constraints:

\[
\boxed{
\text{polarization orthogonality}
\quad\vee\quad
\text{equal-shell locking}.
}
\tag{ACN-8}
\]

Therefore a zero-defect compact web attempting to cancel successive descendants must accumulate a branch history of such constraints.

This is exactly the kind of reusable finite statement requested by the current OCSR / Generative Constraint Accumulation program. It does not by itself prove that an infinite compatible branch history is impossible.

## 6. Relation to the previous strip-boundary theorem

For the antipodal-strip anchor

\[
p=(0,P,0),
\qquad
a=e_3,
\]

and an external mode

\[
r=(x,y,z),
\]

the condition

\[
a\cdot r=0
\]

is simply

\[
z=0.
\]

So the previous special determinant

\[
\det L_r
=
\frac{z^2(|r|^2-|p|^2)}{|p+r|^2}
\]

is the direct specialization of (ACN-7).

The previous `planar OR equal-shell` split is therefore not an isolated trick. It is the first coordinate instance of the general reusable nullity law (ACN-1).

## 7. Proposed result

`PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01` — **NEW DERIVATION / PROPOSAL; exact algebraic PASS**.

Bounded statement:

```text
For the declared projected NSE bilinear interaction, fix any nonzero retained
anchor mode p with nonzero transverse polarization a.  For any source mode q
with k=p+q != 0, the cross map from q-polarizations to k-polarizations has a
nonzero kernel if and only if q is polarization-orthogonal to the anchor
(a·q=0) or q lies on the same shell as p (|q|=|p|).  Off this finite union of
exceptional algebraic loci, every nonzero q-polarization produces a nonzero
cross response.
```

## 8. Claim boundary

This closes only the local nullity classification for one retained anchor.

Still OPEN:

- compatibility of repeated exceptional choices across a large interaction web;
- whether repeated equal-shell / polarization-orthogonality constraints force planarity, degeneracy, scale escape, or positive registered defect;
- global multi-source cancellation compatibility;
- OCSR;
- Witness Soundness globally;
- G6/G7;
- Clay Navier–Stokes regularity.

## 9. Next reuse-first target

Use (ACN-1) simultaneously against **two retained parent anchors** of a forced descendant.

A newly recruited mode `q` that suppresses both cross interactions must satisfy

\[
(a_1\cdot q=0\ \vee\ |q|=|p_1|)
\]

and

\[
(a_2\cdot q=0\ \vee\ |q|=|p_2|).
\]

The next missing piece is therefore no longer an arbitrary cancellation theorem. It is a finite compatibility problem for intersections of two exceptional-locus constraints. That is the next place to reuse the present theorem before deriving anything else.
