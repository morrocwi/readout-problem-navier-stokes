# NS P2 — M3 Suppression-Label Checker: multi-label O/E/C/T + UNRESOLVED and the double-O rank counter

**Status:** NEW DERIVATION / PROPOSAL (checker / definition); exact finite labeling instrument  
**Proposal id:** `PROP-P3-M3-SUPPRESSION-LABELS-01` — not yet in Toledo  
**Parent:** `PROP-P3-RECURSIVE-SUPPRESSION-CHARGING-01` (M3 label-set interface, `paper/NS_P2_RECURSIVE_SUPPRESSION_CHARGING_CARD.md`)  
**Global FNW / OCSR / Witness Soundness / G4/G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_m3_suppression_labels.py`  
**Date:** 2026-09-13 (orthogonal-turn fixture added 2026-09-13)

## 0. Reuse-first path

A Toledo lookup (registry, canonical map, proposals for the NS P2 critical quotient) found no
suppression-label object, no multi-label suppression classifier, and no anchor-polarization rank
counter. Reused, not re-derived:

- **`PROP-P2-CANCELLATION-LEDGER-01`** (exact cancellation accounting) — the C label is exactly
  the ledger's "several nonzero contributions, net zero" row; it is an accounting entry there and
  remains one here.
- **`PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`** (`NS_P2_GENERAL_ANCHOR_CROSS_NULLITY.md`, (ACN-1),
  DERIVED / EXACT) — for anchor `a ∈ p^⊥` the cross map `b ↦ B_{p,q}(a,b)` on `q^⊥` has nontrivial
  kernel iff `a·q = 0` or `|q| = |p|`. The O and E labels are exactly its two branches, read
  per contributing pair.
- **Equal-shell direction lock** (`NS-P2-EQUAL-SHELL-DIRECTION-LOCK`, PASS, corollary of Standalone
  Section 14; `PROP-P3-EQUAL-SHELL-DIRECTION-LOCK-01`) — the E branch.
- **RSC-O two-anchor planarity** (`PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01`, PR #60) — fixes the
  anchor/recruit convention used by the double-O counter: an anchor `(p_i, a_i)` is O-silent to a
  recruit `(q, b)` through `a_i·q = 0`, and two anchors count as independent only when
  `a_1 × a_2 ≠ 0`.
- **Genesis readout-to-defect soundness** (fail-closed reading discipline): a suppression that is
  *observed* but not *provable* from the registered data must be reported as `UNRESOLVED`, never
  silently absorbed into a label.
- Fixtures W1, W2, W3 from `check_ns_p2_multisource_cancellation.py` /
  `NS_P2_MULTISOURCE_CANCELLATION_OCSR_GEN1.md` (`PROP-P3-MULTI-SOURCE-CANCELLATION-WITNESSES-01`).
- The orthogonal-turn chain geometry of `NS_P2_ORTHOGONAL_TURN_ALLSCALE_ESCAPE.md` /
  `check_ns_p2_orthogonal_turn_allscale_escape.py` (similitude `A`, seed `p0, q0`, axis exchange
  `T_1 = N_0`), used as the wavevector / polarization skeleton of the OT fixture below.

No new global architecture is introduced. This note only makes the M3 interface of the recursive
suppression charging card executable on exact fixtures.

---

## 1. Definition — the label set `L(e)`

Let a finite registered web be a set of real modes `(m, a_m)` with `a_m · m = 0` and
`u(−m) = u(m)`, together with a declared cell (a predicate on `|t|²`). One full local convolution
generation lands every unordered pair `{(p,a),(q,b)}` (repeats allowed) on the target `t = p+q ≠ 0`
with contribution

```text
g_{p,q}(a,b) = P_t( (a·q) b + (b·p) a ).
```

A target `e` is **suppressed** when at least one pair lands on it and the net forcing
`F_e = Σ g` is exactly zero. For each suppressed target the checker returns

```text
L(e) ⊆ {O, E, C, T}
```

with the four labels defined per contributing pair:

| Label | Name | Condition (exact, per pair landing on `e`) | Reused source |
|---|---|---|---|
| **O** | ORTH | some pair has `a·q = 0` or `b·p = 0` | (ACN-1) orthogonality branch |
| **E** | EQSHELL | some pair has `\|p\| = \|q\|` | (ACN-1) equal-shell branch / direction lock |
| **C** | MSCANCEL | at least two contributions are individually nonzero and the net is exactly zero | cancellation ledger |
| **T** | TED | `e` lies outside the declared cell (registered exit; terminal / named-defect status requires an external declaration and is not derived here) | Standalone exit accounting |

and the fail-closed complement

```text
UNRESOLVED :  suppression observed, L(e) = ∅   (no label provable from the registered data)
```

**Labels are not mutually exclusive.** `{O, E, T}`, `{E, C}`, `{O, E, C}` occur on the fixtures
below. A multi-label event belongs simultaneously to each atomic branch and therefore carries
more constraints, not fewer (card §4).

**C is an accounting label, never a physical loss.** It records that several individually
productive contributions sum to exactly zero at one target. Whether that cancellation is a
payable loss `D_cancel` or an amplitude constraint `F_e = 0` is exactly Witness Soundness
(Standalone §111.5), which is OPEN. The checker asserts this in its comments; nothing in this note
promotes C to a loss, a defect, or a phase tax.

## 2. Definition — the double-O rank counter

For each suppressed target `e` define the **anchor set**

```text
O(e) = { (m, a_m) : some pair {(m,a_m),(n,a_n)} lands on e with a_m · n = 0 }
```

— the retained anchors whose interaction with their recruit is O-suppressed, in the convention of
`PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01` (the anchor polarization annihilates the partner
wavevector). Then

```text
double-O(e)  :<=>  rank{ a_m : m ∈ O(e) } ≥ 2 .
```

"Double-O" means the same target is O-suppressed against **two independent anchor polarization
lines**; it is **not** "two O labels". Two O-suppressed pairs whose anchors have parallel
polarizations give rank 1. Per fixture the checker reports

```text
N_{O,1}  = #{ e suppressed : rank O(e) = 1 }
N_{O,≥2} = #{ e suppressed : rank O(e) ≥ 2 }
```

(suppressed targets with no O label have rank 0 and are counted in neither).

## 3. Fixtures

| Fixture | Modes | Cell | Source |
|---|---|---|---|
| W1 | `±p_i, ±q_i`, `i = 0,1` (8 modes), `k = (1,0,0)`, two-shell | `\|t\|² ≤ 3` | copied exactly from `check_ns_p2_multisource_cancellation.py` |
| W2 | `±p_i, ±q_i`, `i = 0,1,2` (12 modes), `k = (1,1,1)`, `p_i = e_i` | `\|t\|² ≤ 3` | copied exactly from `check_ns_p2_multisource_cancellation.py` |
| W3 point A | `±p_i, ±q_i`, `i = 0,1,2`, plus `±k`, `k = (0,0,1)` (14 modes, all on the unit shell), amplitudes `A1 = 1, A2 = 0, B1 = 0, B2 = −1`, `c = (1,0,0)` | `\|t\|² < 3` | exact literals over `Q(√3)` in the checker |
| OT gen-1 time-honest | `±p0, ±q0, ±p1, ±q1` (8 modes): `p0 = (1,0,0)`, `q0 = (2,4,0)`, `p1 = (3,4,0)`, `q1 = (6,8,20)`; polarizations `T0 = (0,1,0)`, `N0 = (0,0,1)`, `N0`, `N1 = (4,−3,0)/5`; amplitudes H1-flat `\|α_k\| = 1/\|k\|`, real, exact over `Q(√5)` (`p2 = (9,12,20)` not yet grown) | `\|t\|² ≤ 500 = \|q1\|²` | **EXACT FIXTURE / FINITE DIAGNOSTIC**; provenance: generator script `ot_chain_gen1_timehonest.py` (polarization chain also in `ot_chain_gen1_fullconv.py`) of the internal attack repository, commit `83d8b5bf0ed15ab81033e0ce92af6e80c9596c95`; wavevector/turn geometry as certified publicly by `check_ns_p2_orthogonal_turn_allscale_escape.py` |

All arithmetic is exact (sympy over `Q`, `Q(√3)` and `Q(√5)`). There is no randomness and no float in
any PASS decision. For the OT fixture the checker additionally asserts, mode by mode, `k·u_k = 0`,
that every amplitude entry is algebraic and free of floating-point atoms, and (symbolically) that
the interaction used is the same Fourier–Leray operator `B(p,q,a,b) = P_{p+q}[(a·q) b + (b·p) a]`
as the other checkers. The five-mode complex-phase variant of the generator (`p2` grown, `Z/4`
donor phases) is not registered because the web contract of §1 is real (`u(−m) = u(m)`).

## 4. Results

### 4.1 Per-fixture status and label counts

| Fixture | targets | SUPPRESSED | NOVELTY | UNRESOLVED | O | E | C | T |
|---|---|---|---|---|---|---|---|---|
| W1 | 26 | 10 | 16 | **0** | 8 | 8 | 2 | 8 |
| W2 | 56 | 14 | 42 | **0** | 12 | 12 | 2 | 12 |
| W3 point A | 82 | 26 | 56 | **0** | 16 | 26 | 2 | 16 |
| OT gen-1 time-honest (EXACT FIXTURE / FINITE DIAGNOSTIC) | 32 | 12 | 20 | **0** | 12 | 8 | 0 | 2 |

Label counts are per target (a target with `{O,E,T}` adds one to each of O, E, T).

### 4.2 Double-O rank counts

| Fixture | N_{O,1} | N_{O,≥2} | double-O targets |
|---|---|---|---|
| W1 | 8 | 0 | — |
| W2 | 12 | 0 | — |
| W3 point A | 14 | 2 | `±k = (0,0,±1)` |
| OT gen-1 time-honest | 12 | 0 | — |

On W1, W2 and the OT web every O-suppressed target is O-suppressed through a single polarization line. On
W3 point A the only double-O targets are `±k`: the three equal-shell pairs `(p_i, q_i)` each have
`a_i · q_i = 0` with `a_i = e_θi` horizontal, so the anchor polarizations span the plane `k^⊥`
(rank 2).

### 4.3 The `k` targets

| Fixture | `k` target | `L(k)` | n_contrib / n_nonzero | reading |
|---|---|---|---|---|
| W1 | `(1,0,0)` | `{C}` — **C without E** | 2 / 2 | two-shell exact cancellation; neither pair is equal-shell, neither is O-silent |
| W2 | `(1,1,1)` | `{C}` — C without E | 3 / 3 | rank-2 cancellation of three unequal-shell pairs |
| W3 point A | `(0,0,1)` | `{O, E, C}` — **C ∧ E** (and O) | 3 / 3 | three equal-shell, O-silent, individually nonzero locked contributions cancel exactly |

All three are asserted exactly by the checker, together with `UNRESOLVED = 0` on every fixture and
the counts in §4.1–§4.2.

### 4.4 Structure of the remaining suppressed targets

- W1 / W2: every suppressed target other than `±k` is a self-pair target `2m` (`|t|² = 4` or `8`),
  which is simultaneously O (`a·m = 0`), E (`|p| = |q|` trivially) and T (outside the cell). These
  are the `{O,E,T}` rows.
- OT gen-1 time-honest (12 suppressed, 20 novelty): every target of this web is single-source
  (exactly one unordered pair lands on it), so `C` cannot occur and every suppressed target is a
  projection zero of its only contribution. The selected forward channels `p1 = p0 + q0 = (3,4,0)`
  and `p2 = p1 + q1 = (9,12,20)` are NOVELTY, as the chain requires. The tree-return target
  `p0 = (1,0,0)` from `(−q0, p1)` is `{O}` only (`N0·p1 = 0`, `N0·q0 = 0`, unequal shells);
  `±(5,8,0)` from `(±p1, ±q0)`-type pairs are `{O}`; the six in-cell self-pair and equal-shell
  targets `±(2,0,0)`, `±(4,8,0)`, `±(6,8,0)` are `{O,E}`; `±2q1 = ±(12,16,40)` are `{O,E,T}`
  (`|t|² = 2000 > 500`). This reconciles O = 12, E = 8, T = 2, C = 0 and `N_{O,1} = 12`. The
  labels are identical under the generator's second (critical, `|α|² = 1/|k|`) normalization,
  as the checker asserts. **Reading:** this is a finite diagnostic of the four-label interface on
  one exact web; it is never evidence that RSC (O/E/C) passes globally, that the chain is
  compact or zero-novelty (it is not: 20 novelty targets), or anything about OCSR.
- W3 point A (26 suppressed): `±k` (`{O,E,C}`); six targets at `|t|² = 9/4` that are `{E}` only,
  two contributions each and both projection zeros (`n_nonzero = 0`), matching the depth-1 audit of
  `NS-P2-W3-FULLCONV-DEPTH1-NOT-LOSSLESS`; two single-contribution projection-zero targets at
  `|t|² = 1` (`{E}`); two at `|t|² = 3` (`{E,T}`, outside the cell); and fourteen self-pair targets
  `2m` at `|t|² = 4` (`{O,E,T}`). This reconciles O = 2 + 14 = 16, T = 2 + 14 = 16, E = 26 and
  `N_{O,1} = 14`.

## 5. Status

```text
PROP-P3-M3-SUPPRESSION-LABELS-01  definition + checker            PASS (exact; not yet in Toledo)
UNRESOLVED count on W1 / W2 / W3 point A / OT gen-1               0 / 0 / 0 / 0
W1 k target is C without E                                        PASS
W3 point A k target is C and E                                    PASS
double-O rank counter, N_{O,1} / N_{O,>=2} per fixture             PASS (8/0, 12/0, 14/2, 12/0)
orthogonal-turn gen-1 time-honest fixture (O12/E8/C0/T2)          EXACT FIXTURE / FINITE DIAGNOSTIC
```

## 6. Claim boundary

This note is a **labeling / accounting instrument**. It proves nothing about:

```text
OCSR (Standalone Section 117.5)                                   OPEN
Witness Soundness for D_cancel (Section 111.5)                    OPEN
RSC-O / RSC-E / RSC-C recursive charging                          OPEN
G6 / G7 (global gates of the charging card)                       OPEN
global multi-source cancellation compatibility (118.4)            OPEN
Clay Navier-Stokes regularity                                     OPEN
```

In particular: `UNRESOLVED = 0` on four exact fixtures is calibration of the four-label interface
on those webs, not evidence that the four labels are complete in general; a double-O count is a
count, not a charge certificate (the RSC-O planarity theorem is the only charge statement in the
repository and it is local); and C on `±k` in every fixture is the cancellation ledger's own row
under a new name, not a loss. Do not invent a fifth label unless an exact `UNRESOLVED` fixture
forces it (card §7).
