# NS P2 — Rank-2 Plane-Switch Capacity and Two-Lineage Plane Lock

**Status:** NEW DERIVATION / PROPOSAL; exact retained-space corollary  
**Parents:** `PROP-P3-RANK2-SELFCLOSURE-PLANARITY-01`; existing Genesis/Toledo retention, sufficiency, lineage and no-silent-loss discipline  
**Global FNW / OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_plane_switch_capacity.py`

## 0. Reuse-first path

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

Lookup found no canonical Toledo theorem for rank-2 plane switching.  This note therefore derives only the missing finite linear-algebraic constraint and labels it PROPOSAL.

Reused objects:

- Genesis retention / lineage preservation: a future-relevant distinction cannot silently disappear;
- exact/declared cancellation, terminal, exit and defect channels;
- `PROP-P3-RANK2-SELFCLOSURE-PLANARITY-01`, which reduces a productive local rank-2 branch to polarization escape, wavevector planarity, or declared degeneration;
- the existing Flat Null-Web / Generative Constraint Accumulation architecture of the Standalone.

No new global proof architecture is introduced.

## 1. Plane-switch problem

Suppose a productive rank-2 patch is represented in a polarization plane

\[
W_j=n_j^\perp.
\]

The previous self-closure result says that a nonplanar productive branch emits a nonzero retained polarization novelty outside `W_j` unless it collapses to the planar / degenerate branch.

A possible recurrent loophole is therefore **plane switching**:

\[
W_j
\longrightarrow
\text{novel retained polarization(s)}
\longrightarrow
W_{j+1},
\]

where the new rank-2 plane attempts to absorb the escaped retained distinctions.

The question here is not whether switching is globally impossible.  It is: **what exact compatibility price must a zero-defect switch pay?**

## 2. Three retained novelties cannot fit a rank-2 plane generically

Let

\[
c_1,c_2,c_3\in\mathbb R^3
\]

be active future-relevant retained polarization vectors that must survive into the next rank-2 representation, with no registered cancellation, terminalization, exit or defect removing any one of them.

If all three are represented inside one next plane `W_{j+1}`, then

\[
\dim\operatorname{span}\{c_1,c_2,c_3\}\le2.
\]

Equivalently,

\[
\boxed{
\det[c_1\ c_2\ c_3]
=
c_1\cdot(c_2\times c_3)
=0.
}
\tag{PS-1}
\]

Thus three linearly independent retained novelties cannot be losslessly recompressed into a rank-2 plane.

If

\[
\det[c_1\ c_2\ c_3]\ne0,
\]

then at least one of the following is mandatory:

```text
registered cancellation / resolution
OR terminalization
OR exit
OR named defect / lost-information failure
OR abandon rank-2 representation.
```

This is a pure sufficiency/retention consequence; it does not reclassify cancellation as physical dissipation.

## 3. Two independent retained lineages lock the next plane

Assume

\[
c_1\times c_2\ne0.
\]

Any rank-2 plane containing both vectors is uniquely

\[
\boxed{
W_{j+1}=\operatorname{span}\{c_1,c_2\}.
}
\tag{PS-2}
\]

Its normal is fixed projectively by

\[
\boxed{
[n_{j+1}]=[c_1\times c_2].
}
\tag{PS-3}
\]

Therefore a third future-relevant retained novelty `c` can be absorbed without a registered resolution channel iff

\[
\boxed{
(c_1\times c_2)\cdot c=0.
}
\tag{PS-4}
\]

Once two independent lineages survive a switch, the next rank-2 plane is **not a free parameter**. Every further retained novelty adds an explicit algebraic compatibility constraint.

This is exactly the Generative Constraint Accumulation mechanism, now in a concrete plane-switch form.

## 4. Two-lineage recurrent plane lock

Consider a sequence of rank-2 representations

\[
W_0\to W_1\to\cdots\to W_m.
\]

Suppose two independent future-relevant lineage classes are retained across the whole segment without registered cancellation / replacement / terminalization / exit / defect, represented by nonzero vectors `c_1,c_2` up to the declared frame/projective transport.

At every stage the rank-2 plane must contain both transported lineage vectors. Hence each plane is uniquely fixed by their span.

In the exact identity/reanchor branch, if the two lineages return to the same projective classes, then

\[
\boxed{
W_m=W_0.
}
\tag{PS-5}
\]

More importantly, a **genuine change of rank-2 plane** cannot occur while carrying two independent lineage directions unchanged.  Every genuine switch must therefore do at least one of the following:

\[
\boxed{
\text{replace / resolve at least one basis lineage}
\quad\vee\quad
\text{register exit / defect}
\quad\vee\quad
\text{lose rank-2 closure}.
}
\tag{PS-6}
\]

This turns plane switching from a free geometric loophole into a lineage-turnover obligation.

## 5. Proposed result

`PROP-P3-PLANE-SWITCH-CAPACITY-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

Bounded statement:

```text
A zero-defect/no-exit rank-2 switch can retain at most a two-dimensional span of
future-relevant polarization distinctions. Two independent retained lineages
uniquely determine the next rank-2 plane. Therefore every additional retained
novelty must satisfy an exact determinant constraint, and every genuine plane
switch must replace/resolve at least one of the two independent basis lineages
(or register exit/defect / abandon rank-2 closure).
```

## 6. Why this advances the current bottleneck

The current local chain had already reached

```text
productive rank-2 patch
-> polarization escape OR wavevector planarity OR degeneration.
```

The unresolved loophole was

```text
escape from W_j -> recompress into a new W_{j+1} -> repeat forever.
```

The present result shows that this is possible only with repeated **lineage turnover** or repeated determinant constraints.  Plane switching is therefore no longer an unconstrained degree of freedom.

The new recurrent-web target is narrower:

```text
Can a compact productive zero-defect recurrent web repeatedly replace one of
its two plane-defining lineage directions, while all such replacements are
compatible with the exact cancellation ledger and projective-null lineage
transport?
```

That is now the load-bearing missing piece.

## 7. What remains OPEN

This proposal does **not** prove that lineage turnover costs a physical defect. Exact cancellation may legitimately resolve a future distinction if Witness Soundness certifies that it is no longer future-relevant.

Still OPEN:

- whether a recurrent zero-defect web can perform an infinite/closed sequence of basis-lineage replacements;
- compatibility of those replacements with the exact cancellation ledger;
- projective-null / holonomy consistency of a closed replacement loop;
- global Witness Soundness;
- FNW / OCSR;
- G6 / G7;
- Clay Navier–Stokes regularity.

## 8. Next reuse-first target

Do not derive another local pair theorem.  Reuse the existing projective-null connection (Standalone Section 114), cancellation ledger and lineage preservation to classify a **basis-replacement loop**:

```text
(c1,c2) -> (c2,c3) -> ... -> (cm,c1)
```

where each step is a genuine plane switch and therefore replaces at least one plane-defining lineage.  The goal is to determine whether a closed zero-defect loop forces

```text
registered cancellation/resolution
OR projective holonomy obstruction
OR planarity/degeneracy
OR scale/boundary escape.
```
