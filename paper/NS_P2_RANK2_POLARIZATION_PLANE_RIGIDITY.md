# NS P2 — Rank-2 Polarization-Plane Rigidity

**Status:** NEW DERIVATION / PROPOSAL; exact symbolic local theorem  
**Parents:** `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`, `PROP-P3-SHELL-CONDITIONED-SPAN-01`  
**Global OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_rank2_polarization_plane_rigidity.py`

## 0. Reuse-first path

This note applies the standing rule

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

No new global architecture is introduced.

The preceding shell-conditioned-span result reduces complete multi-anchor silence to a branch in which the off-shell retained polarizations span a space of dimension at most two. The present note attacks that existing rank-defect branch directly.

Reused objects:

- the existing projected symmetric NSE interaction `B`;
- full-convolution closure;
- `PROP-P3-SHELL-CONDITIONED-SPAN-01`;
- the existing planar / dispersion / flat-null-web direction of the P2 Standalone;
- Genesis no-silent-loss and dynamically sufficient retained-state discipline.

A Toledo lookup found no existing rank-2 polarization-plane rigidity theorem. The result below is therefore a new proposal.

## 1. Rank-2 polarization plane

Fix a two-dimensional polarization plane

\[
W=n^\perp,
\qquad |n|\neq0.
\]

Take two source modes `p,q` with nonzero polarizations constrained to `W`:

\[
a\in W\cap p^\perp,
\qquad
b\in W\cap q^\perp.
\]

When `p` and `q` are not parallel to `n`, these one-dimensional intersections have the exact form

\[
\boxed{
a=\alpha(n\times p),
\qquad
b=\beta(n\times q).
}
\tag{RP-1}
\]

The omitted cases `p || n` or `q || n` are already lower-dimensional alignment branches and are kept as declared degeneracies rather than silently folded into the generic branch.

## 2. Exact escape identity

Let

\[
k=p+q.
\]

For the existing projected bilinear interaction,

\[
\mathcal B_{p,q}(a,b)
=P_{k^\perp}\left[(a\cdot q)b+(b\cdot p)a\right],
\]

direct exact reduction gives

\[
\boxed{
 n\cdot \mathcal B_{p,q}(a,b)
 =
 \frac{
 2\alpha\beta\,[n\cdot(p+q)]\,[n\cdot(p\times q)]^2
 }{|p+q|^2}.
}
\tag{RP-2}
\]

The checker verifies (RP-2) symbolically with exact arithmetic.

Thus, on a productive nondegenerate pair `alpha beta != 0`, if

\[
n\cdot(p\times q)\neq0
\]

and

\[
n\cdot(p+q)\neq0,
\]

then

\[
\boxed{
 n\cdot\mathcal B_{p,q}(a,b)\neq0,
}
\]

so the output polarization necessarily leaves `W`.

Equivalently, preserving the rank-2 polarization plane across this interaction forces

\[
\boxed{
 n\cdot(p+q)=0
 \quad\vee\quad
 n\cdot(p\times q)=0
 \quad\vee\quad
 \alpha\beta=0.
}
\tag{RP-3}
\]

For a productive pair the last branch is excluded. Therefore every productive `W`-closed interaction pays one of two exact geometric constraints:

```text
vertical-sum cancellation
OR
projected-direction collision.
```

## 3. Three-mode rigidity

Now take three productive retained source modes

\[
p_1,p_2,p_3
\]

whose polarizations all lie in the same plane `W=n^perp`.

Assume their projected directions are pairwise nonparallel:

\[
\boxed{
 n\cdot(p_i\times p_j)\neq0
 \qquad(i\neq j).
}
\tag{RP-4}
\]

Suppose all three pair interactions remain in `W`:

\[
 n\cdot\mathcal B_{p_i,p_j}(a_i,a_j)=0
 \qquad\forall i<j.
\]

By (RP-2) and productivity, (RP-4) removes the projected-collision branch and leaves

\[
 n\cdot(p_1+p_2)=0,
\]

\[
 n\cdot(p_1+p_3)=0,
\]

\[
 n\cdot(p_2+p_3)=0.
\]

Writing

\[
z_i:=n\cdot p_i,
\]

we obtain

\[
z_1+z_2=0,
\qquad
z_1+z_3=0,
\qquad
z_2+z_3=0.
\]

Hence

\[
\boxed{z_1=z_2=z_3=0.}
\tag{RP-5}
\]

Therefore

\[
\boxed{
p_1,p_2,p_3\in W.
}
\tag{RP-6}
\]

So a rank-2 polarization plane can remain closed on a productive three-mode general-position patch only if the wavevectors themselves collapse into the same plane.

## 4. Exact dichotomy for persistent rank-2 closure

Combining the pair and triple statements gives the reusable form:

\[
\boxed{
\begin{aligned}
&\text{productive rank-2 polarization closure}\
&\Longrightarrow
\text{wavevector planarity}
\ \vee\ 
\text{projected-direction collision}
\ \vee\ 
\text{alignment / nonproductive degeneration}.
\end{aligned}
}
\tag{RP-7}
\]

The important point is that the shell-conditioned rank-defect branch from the previous note is not a featureless residual set. Full convolution forces it into explicit lower-dimensional geometry unless it emits polarization novelty outside `W`.

## 5. Non-vacuity control

The checker uses the exact rational modes

\[
p_1=(1,0,1),
\qquad
p_2=(0,1,-1),
\qquad
p_3=(1,1,1),
\]

with

\[
a_i=e_3\times p_i.
\]

Their horizontal projected directions are pairwise nonparallel. The vertical components are not all zero, so the three-mode `W`-closed conditions cannot all hold. The exact checker confirms that at least one pair interaction has nonzero `e_3` component and therefore escapes `W`.

## 6. Proposed result

`PROP-P3-RANK2-POLARIZATION-PLANE-RIGIDITY-01` — **NEW DERIVATION / PROPOSAL; exact symbolic PASS**.

Bounded statement:

```text
For a common rank-2 polarization plane W=n^perp, a productive pair with
polarizations in W has output outside W unless either n.(p+q)=0 or the
projections of p and q onto W are parallel. Consequently, for three productive
modes with pairwise nonparallel projected directions, closure of all three pair
interactions inside W forces all three wavevectors themselves to lie in W.
```

## 7. What this advances

The current chain is now:

```text
complete multi-anchor silence
-> shell-conditioned polarization rank <= 2
-> rank-2 polarization plane
-> polarization escape
   OR wavevector planarity
   OR projected-direction collision
   OR lower-dimensional degeneration.
```

This is a direct reuse-first narrowing of the existing FNW / OWR / OCSR branch. It does not introduce a new proof architecture.

## 8. Claim boundary

Still OPEN:

- rigidity of the wavevector-planar branch under full convolution;
- rigidity of repeated projected-direction collisions;
- whether every compact productive zero-defect recurrent web eventually creates the three-mode general-position patch needed above or falls into one of the declared degeneracies;
- global multi-source cancellation compatibility;
- Witness Soundness globally;
- OCSR / G6 / G7;
- Clay Navier–Stokes regularity.

## 9. Next reuse-first target

The next pass should reuse existing Standalone dispersion / orthogonal-web / flat-null-web material on the two surviving branches of (RP-7):

```text
A. wavevector planarity
B. projected-direction collision
```

The goal is to decide whether either branch can support a compact productive zero-defect recurrent web without producing a registered descendant or boundary exit.
