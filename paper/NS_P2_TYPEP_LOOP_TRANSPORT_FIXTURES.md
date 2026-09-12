# NS P2 — Type-P Loop Transport: Shell Confinement and Identity-Monodromy Loop Fixtures

**Status:** NEW DERIVATION / PROPOSAL; exact finite PASS  
**Parents:** Standalone vNext Sections 114.1–114.2; `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`; `PROP-P3-PROJECTIVE-THREE-LINE-RIGIDITY-01`; `NS_P2_PROJECTIVE_HOLONOMY_TYPE_AUDIT.md`  
**Attack-map position:** inputs to targets A1 (nonidentity Type-P branch) and A3 (identity-monodromy equality branch) of the current typed attack map (2026-09-12)  
**Global FNW / OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Global A1 / A3 / G4 / G6 / G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_typeP_loop_transport.py`

## 0. Reuse-first path

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

Reused objects (no new architecture, no new equation):

- **Standalone (114.1)–(114.2)** — the zero-cross partial projective transport `T_e: P(k_1^perp) -> P(k_2^perp)` and the recurrent-loop condition `T_loop(lambda) = lambda`. This note uses exactly that definition: `T_e([a]) = [b]` with `b in k_2^perp` and `B_{k_1,k_2}(a,b) = 0`, where `B_{p,q}(a,b) = P_{p+q}[(a·q) b + (b·p) a]` is the existing symmetric projected interaction.
- **`PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`** (`NS_P2_GENERAL_ANCHOR_CROSS_NULLITY.md`, (ACN-1)) — for anchor `a in p^perp`, the cross map `b |-> B_{p,q}(a,b)` on `q^perp` has nontrivial kernel iff `a·q = 0` or `|q| = |p|`. Status of this reused object: **DERIVED / EXACT** (exact algebraic PASS in its own checker). It is reused verbatim with `p = k_1`, `q = k_2`.
- **`PROP-P3-PROJECTIVE-THREE-LINE-RIGIDITY-01`** (`NS_P2_PROJECTIVE_HOLONOMY_TYPE_AUDIT.md`, (PH-1)–(PH-2)) — a nonidentity `PGL(2,R)` monodromy fixes at most two projective lineage classes. Used only to classify concrete loop monodromies.
- The type boundary of the same audit: everything below is **Type P** (projective polarization/lineage holonomy). Nothing here is a Type-Phi scalar phase cycle, and the forbidden inference `Type P -> Type Phi -> packed tax` is not used.

A Toledo lookup found no canonical object for the shell-confinement corollary or for explicit Type-P loop monodromy fixtures. Both proposal identifiers below are therefore **not yet in Toledo**.

## 1. Setup

Fix a closed mode cycle `k_1 -> k_2 -> ... -> k_m -> k_1` of nonzero integer vectors with `k_i + k_{i+1} != 0`. On each edge `e = (k_1, k_2)` the transport relation is

\[
T_e([a]) = [b]
\quad\Longleftrightarrow\quad
a\in k_1^\perp,\ b\in k_2^\perp,\ \mathcal B_{k_1,k_2}(a,b)=0,\ b\neq0 .
\]

`T_e` is a **single-valued map on the whole fiber** exactly when, for every `a in k_1^perp \ {0}`, the kernel of `b |-> B_{k_1,k_2}(a,b)` on `k_2^perp` is a line. In a fixed exact rational basis of `k_1^perp` and `k_2^perp`, such a `T_e` is a `2x2` rational matrix; the loop monodromy

\[
M = T_{e_m}\circ\cdots\circ T_{e_1}\in PGL(2,\mathbb Q)
\]

is the exact product, expressed in the basis of `k_1^perp` at both ends.

## 2. Shell confinement (corollary of the reused nullity theorem)

Apply (ACN-1) with `p = k_1`, `q = k_2`, anchor `a in k_1^perp`:

```text
ker( b |-> B_{k1,k2}(a,b) ) != {0}   iff   a·k2 = 0   or   |k1| = |k2|.
```

Two branches follow, and they are kept **separate**:

**(i) Equal-shell edge, `|k_1| = |k_2|`.** The kernel is a line for every class `[a]` (the checker verifies that the transverse determinant vanishes identically in `a` and that each basis class has a one-dimensional kernel). `T_e` is a genuine projective map `P(k_1^perp) -> P(k_2^perp)`.

**(ii) Rank-0 edge, `a ⊥ k_2` with `|k_1| != |k_2|`: projective collapse to `[k_1 × k_2]`.** Assume `k_1 ∦ k_2` (automatic on an equal-shell edge with `k_1 != ±k_2`; on an unequal-shell parallel edge `k_2 = c k_1`, `c != -1`, every class has `a·k_2 = 0` and the kernel is all of `k_2^perp`, so `T_e` is not single-valued there either and (TP-1) below still holds). Since also `a ⊥ k_1`, the only class in `P(k_1^perp)` with `a·k_2 = 0` is `[k_1 × k_2]`; for it the kernel is the line `[k_1 × k_2]` in `k_2^perp`. Every other class has trivial kernel, hence **no** zero-cross partner. On such an edge the transport relation is the single point `[k_1 × k_2] |-> [k_1 × k_2]` — a rank-0 (constant) projective relation. It is never an invertible transport and is never treated as one below. (The cross map itself has rank 1 at that anchor; "rank-0" refers to the induced projective relation, not to the linear cross map.)

Hence the structural reduction:

\[
\boxed{
\text{non-rank-0 Type-P transport on an edge } k_1\to k_2
\ \Longrightarrow\
|k_1| = |k_2| .
}
\tag{TP-1}
\]

**Consequence for loops.** A closed Type-P loop whose every edge is a non-rank-0 transport lies on **one shell** `|k_1| = |k_2| = ... = |k_m|`. Equivalently: a recurrent Type-P web that does not collapse classes through rank-0 edges lives in the equal-shell sector. This connects the Type-P entrance of FNW back to the existing equal-shell material — the equal-shell direction lock of Section 113, the W3 equal-shell cancellation witness, and the equal-shell self-closure (NPSC) question — rather than to an arbitrary multi-shell web.

Status of (TP-1): **DERIVED / EXACT** as a corollary of the reused nullity theorem; the checker certifies it on three explicit unequal-shell edges (generic classes: kernel trivial; exceptional class `[k_1 × k_2]`: one-dimensional kernel spanned by `k_1 × k_2`; `T_e` not single-valued) and three equal-shell control edges (single-valued on the whole fiber).

**Finite diagnostic (not part of the theorem).** Forty random integer cycles (`m in {3,4}`, entries in `[-3,3]`, seed 1) were transported exactly; all forty contain an edge on which `T_e` is not single-valued. Status: **FINITE_DIAGNOSTIC** — consistent with (TP-1), evidence of nothing beyond it, and deliberately not reproduced in CI.

## 3. Equal-shell loop monodromy: exact fixtures

On the equal-shell sector the loop monodromy `M in PGL(2,Q)` is computable exactly. For an exact `2x2` representative, `M ~ I` iff `M` is a nonzero scalar matrix; otherwise the real fixed lines of `M` on `P^1` are the real roots of `M_{21} + M_{22}x - x(M_{11} + M_{12}x)` together with `[0:1]` when `M_{12} = 0`, so `#Fix_{P^1}(M) in {0,1,2}` — exactly the dichotomy (PH-2).

### 3.1 Equal-shell loop statistics — FINITE_DIAGNOSTIC

Random cycles of `m in {3,4,5}` distinct integer vectors on one shell (`|k|^2 in {9, 6, 5}`, entries in `[-3,3]`, antipodal consecutive pairs excluded, seed 7):

```text
shell |k|^2   loops   M ~ I   0 real fixed lines   1   2 real fixed lines
   9           48       1            2             0         45
   6           52       0            9             0         43
   5           52       1           11             0         40
```

Status: **FINITE_DIAGNOSTIC**. Read-out only: on these samples the monodromy is generically nonidentity with two real fixed lines (hyperbolic type), sometimes elliptic (no real fixed line), never parabolic (one), and identity loops occur. No rate, no genericity theorem and no all-shell statement is claimed. This table is not reproduced in CI; the deterministic fixtures below are.

### 3.2 Identity-monodromy loop fixtures — EXACT FIXTURE / PROPOSAL

Two explicit equal-shell loops with `M = I` exactly:

```text
shell 9  rectangle       [(2,-2,1), (2,-2,-1), (-2,-2,1), (-2,-2,-1)]      M = I
shell 5  planar 3-cycle  [(-1,-2,0), (-2,1,0), (2,1,0)]                     M = I   (z = 0: class P)
```

The shell-5 loop is planar (`z = 0` throughout), so it belongs to the planar branch `P` of the canonical target `CR_0 subset P u D`. The shell-9 rectangle is not planar.

**What these fixtures are.** They are **branch-B (identity monodromy) witnesses**: explicit Type-P loops on which the projective return map is the identity, so every lineage class returns. They show that the identity branch of the Type-P fork is non-empty at the level of the transport algebra.

**What these fixtures are not.** They are **not counterexamples to anything.** No productivity, zero-defect, full-convolution closure, phase or amplitude compatibility of the underlying webs has been tested; whether either loop supports a productive zero-defect recurrent web, or instead lands in the planar / degenerate / terminal / exit branch, is untested and OPEN. Identity monodromy is a necessary-type condition for branch B, not a construction of a recurrent web.

### 3.3 Nonidentity fixtures (branch A) — EXACT

Two explicit equal-shell loops with `M != I` and exactly two real fixed lines, plus one elliptic control:

```text
shell 5  [(1,0,2), (-2,1,0), (-1,2,0)]        M = [[1, 1], [5/2, -2]]      2 real fixed lines
shell 6  [(1,2,-1), (-2,1,1), (-1,-1,2)]      M = [[7, -3], [-1, 4]]       2 real fixed lines
shell 5  [(1,0,-2), (-2,1,0), (0,-1,2)]       M = [[1, 1], [-5/2, 2]]      0 real fixed lines
```

By (PH-2) a nonidentity monodromy fixes at most two classes; these fixtures realise both the two-line and the zero-line case on concrete integer loops, which is the exact input the A1 falsification search needs (a productive web returning on only the two fixed classes would refute the third-line target; none is exhibited here).

## 4. Proposed results

`PROP-P3-TYPE-P-SHELL-CONFINEMENT-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS; not yet in Toledo.**

```text
For the declared projected NSE interaction, the Standalone (114.1) zero-cross
transport T_e: P(k1^perp) -> P(k2^perp) is a single-valued projective map on
the whole fiber if and only if |k1| = |k2|.  On an unequal-shell edge the
zero-cross relation is the single point [k1 x k2] |-> [k1 x k2] (rank-0
projective collapse), never an invertible transport.  Hence every closed
Type-P loop with non-rank-0 edges lies on one shell, and a recurrent Type-P
web that does not collapse classes through rank-0 edges lies in the
equal-shell sector.
```

Tier: corollary of `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01` (DERIVED / EXACT); exact certification on explicit edges by the checker.

`PROP-P3-TYPE-P-IDENTITY-LOOP-FIXTURES-01` — **EXACT FIXTURE / PROPOSAL; not yet in Toledo.**

```text
The equal-shell integer loops
  shell 9: (2,-2,1) -> (2,-2,-1) -> (-2,-2,1) -> (-2,-2,-1) -> back
  shell 5: (-1,-2,0) -> (-2,1,0) -> (2,1,0) -> back   (planar, z = 0)
have identity Type-P loop monodromy, M = I in PGL(2,Q), exactly.
The equal-shell loops (1,0,2)->(-2,1,0)->(-1,2,0) and
(1,2,-1)->(-2,1,1)->(-1,-1,2) have nonidentity monodromy with exactly two
real fixed lines.
```

Derived consequence: **the identity branch (A3) is non-empty** at the transport level — DERIVED from the exact fixtures. **A3 is NOT closed**: productive identity-monodromy rigidity (`M = I` + productivity + `D = E = 0` ⇒ planar / degenerate / terminal) remains OPEN, and these fixtures neither prove nor refute it.

## 5. What this advances

- The Type-P entrance of FNW is no longer an arbitrary multi-shell object: non-rank-0 transport is shell-confined, so the Type-P loop question is an equal-shell question, in the same sector as the direction lock, W3 and the self-closure (NPSC) material.
- The rank-0 edge is isolated as its own branch (projective collapse to `[k_1 × k_2]`), so any future "escape to another shell" in a recurrent Type-P web must pass through such a collapse and be registered as one (resolution / terminalization / exit / lineage defect / collapse into a fixed class), consistent with the Genesis no-silent-loss discipline.
- Concrete integer loops now exist for both branches of the three-line-rigidity fork: two identity-monodromy witnesses (A3 non-empty) and explicit two-fixed-line and zero-fixed-line monodromies (inputs for the A1 falsification search).

## 6. Claim boundary

Still OPEN (nothing here changes any of these):

- A1: third-line generation/return, or its refutation, on the nonidentity Type-P branch;
- A3: productive identity-monodromy rigidity; productivity / zero-defect / full-convolution closure of the two identity fixtures is **untested**;
- Type-P recurrent lineage web -> registered full-convolution channel network -> Type-Phi conflict-cycle coverage or classified remainder ((PH-3));
- FNW / OCSR / Witness Soundness / global multi-source cancellation compatibility;
- WS for `D_cancel`;
- G4 / G6 / G7;
- Clay Navier–Stokes regularity.

No result here promotes cancellation to physical loss, and no projective-holonomy statement is promoted to a phase tax.

## 7. Next reuse-first target

Take the shell-9 rectangle and the shell-5 planar 3-cycle as seeds and run the existing equal-shell full-convolution closure audit (Section 113 direction lock, W3 generation-1 outward suppression, depth-1 full convolution) on them: either both land in the planar / degenerate / terminal branch, or one produces an explicit productive identity-monodromy candidate for A3. Do not build new holonomy machinery for this.
