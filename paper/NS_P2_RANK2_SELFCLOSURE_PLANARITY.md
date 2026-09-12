# NS P2 — Rank-2 Self-Closure Forces Planarity or Polarization Escape

**Status:** NEW DERIVATION / PROPOSAL; exact finite corollary  
**Parents:** existing productive-triad self-closure lemma; `PROP-P3-RANK2-POLARIZATION-PLANE-RIGIDITY-01`  
**Global FNW / OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_rank2_selfclosure_planarity.py`

## 0. Reuse-first path

This note uses the standing rule

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

and introduces no new architecture.

The previous rank-2 polarization-plane result left one local concern: perhaps a productive interaction graph can remain too sparse to form a three-pair patch, thereby avoiding the planar conclusion. The existing productive-triad self-closure lemma removes that concern locally.

A Toledo lookup found no existing rank-2 self-closure/planarity theorem. The result below is therefore a new proposal.

## 1. Setup

Fix a retained polarization plane

\[
W=n^\perp.
\]

Consider a productive triad

\[
p+q=k
\]

with nonzero retained source polarizations

\[
a\in W\cap p^\perp,
\qquad
b\in W\cap q^\perp,
\]

and suppose its nonzero parent response is retained in the same plane:

\[
c:=\mathcal B_{p,q}(a,b)\neq0,
\qquad c\in W.
\tag{RS-1}
\]

The scalar transfer into `c` is automatically productive:

\[
\langle c,\mathcal B_{p,q}(a,b)\rangle=\|c\|^2>0.
\]

Thus the existing exact self-closure lemma applies.

## 2. Parent W-closure fixes the target wavevector in W

On the nonalignment branch, `PROP-P3-RANK2-POLARIZATION-PLANE-RIGIDITY-01` says a productive pair with output retained in `W` must satisfy

\[
 n\cdot(p+q)=0.
\]

Therefore

\[
\boxed{n\cdot k=0,\qquad k\in W.}
\tag{RS-2}
\]

## 3. Exact self-closure supplies the missing neighboring interaction

The existing productive-triad exact self-closure lemma gives

\[
\boxed{
\max\left\{
\|\mathcal B_{p,k}(a,c)\|,
\|\mathcal B_{q,k}(b,c)\|
\right\}>0.
}
\tag{RS-3}
\]

So at least one neighboring full-convolution interaction is nonzero. No triangle-completeness assumption on the productive interaction graph is needed.

## 4. If the forced self-closure remains in W, all wavevectors become planar

Suppose the nonzero self-closure channel is `(p,k)` and its output also remains in `W`.

Because both retained polarizations `a,c` lie in `W`, the reused rank-2 pair theorem gives

\[
 n\cdot(p+k)=0
\]

on the productive nonalignment branch.

Using (RS-2),

\[
 n\cdot k=0,
\]

hence

\[
\boxed{n\cdot p=0.}
\]

Since `k=p+q` and `n\cdot k=0`, it follows that

\[
\boxed{n\cdot q=0.}
\]

Thus

\[
\boxed{p,q,k\in W.}
\tag{RS-4}
\]

The same argument applies if the forced nonzero channel is `(q,k)`.

## 5. Exact dichotomy

Therefore a productive triad whose retained polarizations stay in a common rank-2 plane satisfies

\[
\boxed{
\begin{aligned}
&\mathcal B_{p,q}(a,b)=c\neq0,\quad a,b,c\in W
\\
&\Longrightarrow
\text{a nonzero self-closure descendant leaves }W
\\
&\qquad\vee\quad p,q,k\in W
\\
&\qquad\vee\quad \text{declared alignment / degeneracy branch}.
\end{aligned}
}
\tag{RS-5}
\]

This is stronger than the previous three-mode patch formulation: **one productive triad plus its already-established self-closure is enough.**

## 6. Exact non-vacuity control

The checker uses

\[
p=(1,0,1),
\qquad
q=(0,2,-1),
\qquad
k=(1,2,0),
\]

with

\[
a=e_3\times p,
\qquad
b=e_3\times q.
\]

The parent response is exactly

\[
\boxed{
\mathcal B_{p,q}(a,b)=\left(-\frac{12}{5},\frac65,0\right)\in W,
}
\]

and is nonzero. Using this response as the retained `k`-polarization, both exact self-closure descendants have nonzero `e_3` component. Thus the nonplanar branch genuinely produces polarization escape from `W`.

## 7. Proposed result

`PROP-P3-RANK2-SELFCLOSURE-PLANARITY-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

Bounded statement:

```text
For a productive triad whose source and retained target polarizations lie in a
common rank-2 plane W, the existing exact self-closure lemma forces a nonzero
neighboring interaction. If that forced descendant also remains in W, then the
three triad wavevectors lie in W (apart from declared alignment degeneracies).
Otherwise the rank-2 polarization defect is broken by an explicit descendant
outside W.
```

## 8. Consequence for the sparse-web concern

The previous open concern was that a rank-2 recurrent web might avoid a three-pair productive patch indefinitely by keeping its productive graph sparse.

For any productive triad, (RS-3) supplies a neighboring productive edge automatically. Therefore the local rank-2 branch no longer needs an independently assumed dense/triangular interaction graph:

```text
productive triad
-> exact self-closure edge
-> polarization escape OR wavevector planarity OR declared degeneration.
```

This directly reuses the existing Standalone self-closure mechanism.

## 9. Relation to existing planar branch

The Standalone already records

```text
Parallel-normal branch -> P
```

as geometrically DERIVED, while global FNW/OCSR remain OPEN. The present corollary is only an entrance lemma into that existing planar branch; it does not reclassify the global recurrent web by itself.

## 10. What remains OPEN

The remaining local load-bearing question is no longer generic rank-2 closure. It is whether a recurrent web can repeatedly:

- emit polarization novelty outside the current rank-2 plane and then cancel/recompress it into another rank-2 plane;
- move between different shell-conditioned planes without accumulating an incompatible lineage/cancellation constraint;
- or stay inside the planar/degenerate branch in a way not already covered by the existing FNW/OCSR targets.

Thus global multi-source cancellation compatibility, Witness Soundness, FNW/OCSR, G6/G7 and Clay regularity remain OPEN.

## 11. Next reuse-first target

The next pass should track **plane switching** rather than invent another local pair theorem:

```text
rank-2 plane W_j
-> forced descendant outside W_j
-> any later rank-2 plane W_{j+1} retaining/cancelling that descendant
```

and ask whether repeated plane switching is compatible with the existing lineage, projective-null and cancellation ledgers on a compact zero-defect recurrent web.
