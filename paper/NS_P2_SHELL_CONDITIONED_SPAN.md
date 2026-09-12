# NS P2 — Shell-Conditioned Polarization-Span Obstruction

**Status:** NEW DERIVATION / PROPOSAL; exact finite corollary  
**Parent:** `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`  
**Four-anchor corollary:** `PROP-P3-MULTI-ANCHOR-SUPPRESSION-01`  
**Global OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  

## 0. Reuse-first path

This note introduces no new architecture. It reuses the exact anchor-cross nullity law

\[
\ker L_{p,q,a}\neq\{0\}
\iff
(a\cdot q=0)\vee(|q|=|p|)
\]

and asks only what simultaneous silence against a finite retained anchor set implies.

A Toledo lookup found no shell-conditioned span theorem. The result below is therefore a proposal.

## 1. Finite retained anchor family

Let

\[
\mathcal A=\{(p_i,a_i)\}_{i=1}^m
\]

with

\[
p_i\neq0,\qquad a_i\neq0,\qquad a_i\cdot p_i=0.
\]

Take a nonzero recruited source mode

\[
q\neq0
\]

with nonzero polarization

\[
b\in q^\perp,
\]

and assume the source is cross-silent against every retained anchor:

\[
\boxed{
\mathcal B_{p_i,q}(a_i,b)=0
\qquad\forall i.
}
\tag{SC-1}
\]

## 2. Off-shell anchors must be polarization-orthogonal

Set

\[
\rho:=|q|.
\]

For every anchor whose shell differs from the recruited shell,

\[
|p_i|\neq\rho,
\]

the equal-shell branch of the parent nullity theorem is unavailable. Therefore (SC-1) forces

\[
\boxed{a_i\cdot q=0.}
\tag{SC-2}
\]

Define the off-shell polarization span

\[
\boxed{
V_\rho
:=
\operatorname{span}
\{a_i:\ |p_i|\neq\rho\}.
}
\tag{SC-3}
\]

Then

\[
\boxed{q\in V_\rho^\perp.}
\tag{SC-4}
\]

Since `q != 0`, necessarily

\[
\boxed{\dim V_\rho\le2.}
\tag{SC-5}
\]

Thus complete cross-silence against a finite retained anchor family forces a **shell-conditioned polarization-rank defect**.

## 3. No-silent-recruitment criterion

The contrapositive is the useful reusable form:

\[
\boxed{
\left[
\dim\operatorname{span}\{a_i:|p_i|\neq\rho\}=3
\quad\forall\rho>0
\right]
\Longrightarrow
\text{no nonzero recruited mode can be cross-silent to all anchors.}
}
\tag{SC-6}
\]

It is enough to check only finitely many shell values:

- every distinct retained shell radius `|p_i|`;
- one generic `rho` not equal to any retained radius, for which the set in (SC-3) is simply all anchor polarizations.

Therefore this is a finite algebraic gate on a finite retained web.

## 4. Why this is stronger than the four-anchor corollary

The previous four-anchor result assumed pairwise-distinct anchor shells and triple-wise polarization independence.

The present statement allows arbitrary shell collisions. A shell collision is not by itself a loophole. A silent recruited mode at radius `rho` is possible only if, after deleting all anchors already on that shell, the remaining anchor polarizations fail to span `R^3`.

Hence the true exceptional branch is

\[
\boxed{
\exists\rho:\
\operatorname{rank}\{a_i:|p_i|\neq\rho\}\le2.
}
\tag{SC-7}
\]

not merely

```text
some shell collision exists.
```

This materially narrows the remaining OCSR degeneracy branch.

## 5. Interpretation in the current constraint-accumulation program

Every suppressed cross response contributes one exact branch condition:

\[
a_i\cdot q=0
\quad\vee\quad
|q|=|p_i|.
\]

Once the recruited shell `rho=|q|` is fixed, all off-shell anchors lose that disjunction: they must impose linear orthogonality constraints on `q`.

Therefore a compact zero-defect web that keeps recruiting silent modes must repeatedly preserve shell-conditioned polarization-rank defects.

This is precisely the type of lower-dimensional exceptional set that the existing FNW / OWR / OCSR machinery is intended to attack. No new global object is required.

## 6. Proposed result

`PROP-P3-SHELL-CONDITIONED-SPAN-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

Bounded statement:

```text
If one nonzero recruited mode is cross-silent to every anchor in a finite
retained anchor family, then after removing the anchors that lie on the same
shell as the recruited mode, the remaining anchor polarizations have rank at
most two. Equivalently, if the off-shell polarization span has rank three for
every retained shell choice (and for a generic non-retained shell), complete
cross-silence is impossible.
```

## 7. Claim boundary

This does not prove OCSR. It reduces the complete-suppression branch to the explicit exceptional condition (SC-7).

Still OPEN:

- rigidity of webs that preserve shell-conditioned polarization rank `<=2` under repeated full convolution;
- whether such webs must become planar/flat/degenerate, generate a nonzero retained descendant, or exit scale;
- global multi-source cancellation compatibility;
- Witness Soundness globally;
- G6/G7;
- Clay Navier–Stokes regularity.

## 8. Next reuse-first target

The next target is now sharply constrained:

```text
Assume a recurrent zero-defect web preserves
rank span{a_i : |p_i| != rho} <= 2
for every recruited silent shell rho.
Use existing flat-null-web / dispersion / full-convolution results to prove
that this rank-defect branch either degenerates further or creates a retained
nonzero descendant.
```

That is a specialization of the existing FNW/OCSR frontier, not a new theorem architecture.
