# NS P2 — multi-source cancellation, equal-shell direction lock, and W3 generation-1 closure

**Date:** 2026-09-11  
**Canonical architecture:** `paper/NS_P2_STANDALONE_VNEXT.md` (Sections 109–118: CR₀ chain-recurrent target, OWR/FNW/OCSR, Generative Constraint Accumulation)  
**Parent targets:** `NS-P2-OCSR` — **OPEN**; `NS-P2-MULTISOURCE-CANCELLATION-COMPAT` — **OPEN**; `NS-P2-WITNESS-SOUNDNESS` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_multisource_cancellation.py`  
**Clay Navier–Stokes regularity:** OPEN

## 1. Purpose

Section 112 of the standalone requires every dangerous cross interaction of a zero-defect web to be *null or exactly cancelled*; Section 116 (SBX) leaves an explicit *exact global cancellation obligation*; Section 118.4 names *global multi-source cancellation compatibility* as one of three current targets. This note records exact finite facts about that branch. Nothing here refutes a statement of the standalone; the results sharpen which obligation actually carries weight.

## 2. Direction lock — Section 14 read at equal source shells

Section 14 gives the adapted-basis components `B_N = A(−xv/Q + yu/P)`, `B_T = A(Q²−P²)/(PQK)·yv`. Hence:

```text
|p| = |q|  =>  B_T = 0  =>  B_{p,q}(a,b) is parallel to p x q for every admissible (a,b)
|p| != |q| =>  B_N, B_T independent  =>  image of (a,b) -> B_{p,q}(a,b) is all of k-perp
```

The checker certifies (113.1) exactly with discrepancy factor 1 — no normalization convention is needed — and confirms rank 1 iff `|p|=|q|` on exact rational instances, including `|p|=|k|≠|q|` (rank 2): the only exceptional locus is source–source shell equality.

### Status

`NS-P2-EQUAL-SHELL-DIRECTION-LOCK` — **PASS** (exact CAS; corollary of Section 14, not a new lemma).  
`NS-P2-SEC113-PROJECTIVE-NULL` — (113.1)–(113.3) **PASS**; the "normalization convention" hedge can be dropped.

## 3. Exact multi-source cancellation witnesses

| Witness | Geometry | Result |
|---|---|---|
| W3 | `k=(0,0,1)`, equal-shell `θ ∈ {0, 2π/3, 4π/3}`, `(a,b)=(e_θ, −q×e_θ)` | `g_i = (√3/2)e_θi`, `Σg_i = 0` exactly; sources rank 3; N=2 equal-shell impossible (two independent locked directions) |
| W1 | `k=(1,0,0)`, two-shell (`|p|²=2`, `|q|²=1`) | `g₁=(0,1,−2)`, `g₂=(0,−1,2)`; both productive before projection; amplitudes and wavevectors span ℝ³; the two triads are congruent (90° about k) |
| W2 | `k=(1,1,1)`, `p_i=e_i` | system rank 2 for any number of triads (dim `k⊥`); each single non-equal-shell source map is already onto `k⊥`; real and genuine complex-phase exact solutions |

The Fourier reality constraint `û(−p)=conj û(p)` is **vacuous** on all three (no antipodal sources, no source equals `±k`); configurations with an antipodal source pair are not covered.

### Status

`NS-P2-MULTISOURCE-CANCELLATION-WITNESSES` — **PASS**.

### What this does and does not mean

- Two-triad exact cancellation with both terms nonzero is impossible **iff** both triads are equal-source-shell with non-parallel normals; it is generic otherwise. Non-coplanarity of wavevectors is not the mechanism.
- In the standalone's own accounting every witness has net response `0` and cancellation deficit `C_k = Σ‖g_α‖ > 0` (Section 9). Whether `C_k > 0` is a payable physical loss (`D_cancel`) or a constraint `F_e = 0` on amplitudes (Section 114.1) is exactly Witness Soundness (Section 111.5). The witnesses convert that obligation into three concrete test cases.
- Direction lock gives **no** phase frustration at a single shared target: the energy transfers `⟨c,g_i⟩ = (√3/2)C_i(c·e_θi)` can all be made positive by choosing `sign(C_i)`.

## 4. W3 generation 1 through k — outward suppression kills the parent

With free `c ⊥ k` at the target, the descendants `D1_i = B_{p_i,k}(a_i,c)`, `D2_i = B_{q_i,k}(b_i,c)` land on six **distinct** targets with `|s|² = 3` (Section 115), so suppression must be nullity, not cancellation. Both are direction-locked and share one invertible 2×2 matrix `M_i` (`det = 3/4`, `M2 = −M1`). Nullity of both pins `(A_i)` and `(B_i)` to the same line, so the parent determinant `C_i = A_{2i}B_{1i} − A_{1i}B_{2i}` vanishes identically (checker: substitution argument with `det M_i = 3/4`); a scratch Gröbner computation (not in-repo) additionally shows `c₁C_i, c₂C_i ∈ ⟨D1·e, D2·e⟩` while `C_i ∉`, i.e. `c = 0` is exactly the escape.

This is Section 13–14 at `K = P = Q`: the conditions `(K²−P²)yt = 0` become vacuous and the two remaining conditions share one linear form. It is strictly stronger than the self-closure lemma on this configuration (that lemma controls only `⟨c,B_pq⟩`, vacuous when `c ⊥ e_θ`; this kills `B_pq` itself).

### Status

`NS-P2-W3-OUTWARD-SUPPRESSION-GEN1` — **PASS** (one configuration, one generation, through `k` only).

## 5. W3 depth-1 full convolution with dead k-mode — not lossless

Taking `û(k)=0` and the 12 real modes `±p_i, ±q_i`, one full local convolution generation (Section 35) gives 60 pairs on 44 targets: `±k` exactly cancelled; six targets at `|t|² = 9/4` are projection zeros (raw vector parallel to `t`); **36 targets with `F_t ≠ 0`, 30 of them single-source** (forced novelty, eq. (111.7)) and six at `|t|² = 3/4` with only partial cancellation (analytic value `C_t = √39/4 − √3/2`, not asserted by the checker). Analytic remark (not asserted by the checker): no rescaling within the `Σg_i = 0` family kills the off-`k` forcings except the zero field, because the `(p_i,p_j)` and `(q_i,q_j)` forcings scale as `λ_iλ_j`, `μ_iμ_j` and never see the `k`-balance.

### Status

`NS-P2-W3-FULLCONV-DEPTH1-NOT-LOSSLESS` — **PASS**.

Net: **W3 is not a zero-defect web at depth 1 in any branch** — with `c ≠ 0` it dies by outward suppression forcing non-productive parents; with `c = 0` it dies by forced novelty. This is one exact instance of the Section 16 conjecture at depth 1 on one seed. It proves nothing general.

## 6. Source gap recorded

"zero-cancellation source-ray alignment — DERIVED" is cited five times in the standalone (Sections 49, 56, 66, 67, 112) but is never stated or derived. It must be supplied or downgraded before it can be registered.

## 7. Boundary

```text
(113.1)-(113.3) exact certification                       PASS
equal-shell direction lock (corollary of Section 14)      PASS
two-triad cancellation iff-characterization               PASS on instances / DERIVED generically
W1, W2, W3 exact witnesses, reality constraint vacuous    PASS
W3 gen-1 outward suppression => non-productive parent     PASS (one seed)
W3 depth-1 full convolution not lossless                  PASS (one seed)
antipodal-source configurations                           OPEN
Witness Soundness for D_cancel                            OPEN
OCSR (Section 117.5)                                      OPEN
global multi-source cancellation compatibility (118.4)    OPEN
CR_0(Q-bar^sc_P2) subset P u D                            OPEN
NS-P2-FRUSTRATION-OR-CUT                                  OPEN (framing superseded by the standalone, statement retained)
Clay Navier-Stokes regularity                             OPEN
```
