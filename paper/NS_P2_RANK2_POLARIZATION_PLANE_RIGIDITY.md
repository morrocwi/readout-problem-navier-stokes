# NS P2 — Rank-2 Polarization-Plane Rigidity

**Status:** NEW DERIVATION / PROPOSAL; exact symbolic local theorem  
**Parents:** `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`, `PROP-P3-SHELL-CONDITIONED-SPAN-01`  
**Global FNW / OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_rank2_polarization_plane_rigidity.py`

## 0. Reuse-first path

This note applies the standing rule

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

No new global architecture is introduced. The preceding shell-conditioned-span result reduces complete multi-anchor silence to a branch in which the off-shell retained polarizations span a space of dimension at most two. The present note attacks that existing rank-defect branch directly using the existing projected interaction and the Standalone planar/FNW structure.

## 1. Rank-2 polarization plane

Fix

\[
W=n^\perp,
\qquad n\neq0.
\]

For source modes `p,q` not parallel to `n`, nonzero polarizations in the common plane satisfy

\[
\boxed{
a=\alpha(n\times p),
\qquad
b=\beta(n\times q).
}
\tag{RP-1}
\]

The omitted alignments `p || n` or `q || n` are retained as explicit lower-dimensional degeneracy branches.

## 2. Exact interaction identities

Let

\[
k=p+q,
\qquad
\Delta:=n\cdot(p\times q).
\]

For the existing projected symmetric NSE interaction, exact reduction gives

\[
\boxed{
 n\cdot \mathcal B_{p,q}(a,b)
 =
 \frac{2\alpha\beta\,[n\cdot(p+q)]\,\Delta^2}{|p+q|^2}.
}
\tag{RP-2}
\]

The unprojected source also has an overall factor `Delta`. In the chart `n=e_3`,

\[
(a\cdot q)b+(b\cdot p)a
=
\alpha\beta\Delta
\bigl(p_y-q_y,\,-p_x+q_x,\,0\bigr).
\tag{RP-3}
\]

Hence

\[
\boxed{
\Delta=0
\Longrightarrow
\mathcal B_{p,q}(a,b)=0.
}
\tag{RP-4}
\]

So the previously apparent `projected-direction collision` escape is not a productive branch at all: it kills the parent interaction itself.

Therefore, for a **productive** pair,

\[
\Delta\neq0.
\]

Combining this with (RP-2), if the output polarization remains in `W`, then necessarily

\[
\boxed{
 n\cdot(p+q)=0.
}
\tag{RP-5}
\]

Thus a productive rank-2 `W`-closed pair has only one nondegenerate geometric option: the normal components of its two wavevectors cancel exactly.

## 3. Three-mode rigidity

Take three retained modes `p_1,p_2,p_3` whose nonzero polarizations lie in the same plane `W`, and assume each of the three pair interactions is productive and remains in `W`.

Productivity excludes projected-direction collision for every pair by (RP-4). Therefore (RP-5) gives

\[
 n\cdot(p_1+p_2)=0,
\qquad
 n\cdot(p_1+p_3)=0,
\qquad
 n\cdot(p_2+p_3)=0.
\]

Writing `z_i=n\cdot p_i`,

\[
z_1+z_2=z_1+z_3=z_2+z_3=0,
\]

hence

\[
\boxed{z_1=z_2=z_3=0.}
\tag{RP-6}
\]

Therefore

\[
\boxed{
p_1,p_2,p_3\in W.
}
\tag{RP-7}
\]

So a productive three-mode patch whose retained polarizations remain in one rank-2 plane can stay closed only by collapsing the wavevectors themselves into that plane.

## 4. Reuse of the existing planar branch

The P2 Standalone already records the geometrical branch

```text
Parallel-normal branch -> P
```

as DERIVED geometrically, while FNW/OCSR globally remain OPEN.

The present result does not re-prove or strengthen that global statement. It supplies a finite algebraic entrance condition into the existing planar branch:

\[
\boxed{
\text{rank-2 retained polarization closure}
+\text{three productive pair interactions}
\Longrightarrow
\text{wavevector-planar patch}.
}
\tag{RP-8}
\]

If the three productive pair interactions are not all present, that absence is itself a registered nonproductivity / interaction-graph sparsity condition rather than silent closure.

## 5. Non-vacuity control

The checker uses

\[
p_1=(1,0,1),
\quad
p_2=(0,1,-1),
\quad
p_3=(1,1,1),
\]

with

\[
a_i=e_3\times p_i.
\]

The vertical components are not all zero; exact evaluation confirms that the productive interactions cannot all remain in `W`.

## 6. Proposed result

`PROP-P3-RANK2-POLARIZATION-PLANE-RIGIDITY-01` — **NEW DERIVATION / PROPOSAL; exact symbolic PASS**.

Bounded statement:

```text
For a common rank-2 polarization plane W=n^perp, projected-direction collision
n.(p×q)=0 makes the declared pair nonproductive. Hence every productive pair
whose output remains in W must satisfy n.(p+q)=0. If three retained modes have
all three pair interactions productive and W-closed, all three wavevectors lie
in W. This is a finite algebraic entrance into the existing planar branch.
```

## 7. What this advances

The reuse-first chain is now

```text
complete multi-anchor silence
-> shell-conditioned polarization rank <= 2
-> common rank-2 polarization plane W
-> interaction escapes W
   OR interaction is nonproductive/aligned
   OR a productive three-pair patch forces wavevector planarity.
```

Compared with the previous version, `projected-direction collision` is no longer an unresolved productive branch: exact algebra shows it is nonproductive.

## 8. Claim boundary

Still OPEN:

- proving that every compact productive zero-defect recurrent web in the shell-conditioned rank-2 branch necessarily contains the required three-pair productive patch, or otherwise falls into a classified sparse/degenerate web;
- global FNW / OCSR;
- global multi-source cancellation compatibility;
- Witness Soundness globally;
- G6 / G7;
- Clay Navier–Stokes regularity.

## 9. Next reuse-first target

The missing piece is now very narrow:

```text
In the shell-conditioned rank<=2 recurrent branch, can the web avoid a
three-mode all-pairs-productive patch indefinitely by keeping the productive
interaction graph sparse?
```

The next pass should reuse existing full-convolution self-closure, two-neighbor off-shell incompatibility, and constraint-accumulation results to attack that sparse-web possibility before proposing anything broader.
