# NS P2 — Forced-Address Accounting Completeness (the forgotten-descendant loophole) and Three Exact RSC-O Skeleton Fixtures

**Status:** NEW DERIVATION / PROPOSAL; exact finite checker obligation + exact fixtures  
**Proposal ids:** `PROP-P3-FORCED-ADDRESS-ACCOUNTING-01` — not yet in Toledo; `PROP-P3-RSC-O-SKELETON-FIXTURES-01` — not yet in Toledo  
**Parent route:** merged PR #64 `PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01` (at `6f4d32e1`) / PR #63 `PROP-P3-RSC-O-ALTERNATION-TRANSFER-01` / PR #60 RSC-O / PR #62 M3 labels  
**Global RSC-O / RSC-E / RSC-C / OCSR / Witness Soundness / G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_forced_address_accounting.py`  
**Date:** 2026-09-13

## 0. Reuse-first audit

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

A Toledo lookup (registry, canonical map, the NS P2 critical-quotient proposals) found no canonical
object for a forced-address accounting obligation and none for the three skeleton fixtures below.

Reused objects (not re-derived):

- **The NPSC depth-1 sweep** (no productive self-closure on small negation-closed integer address
  sets, exact Gröbner over ℚ, 26,496 orbit representatives in `[-1,1]^3` and `[-2,2]^3`, 2–4 ± pairs).
  Its reading is the origin of the rule: 622 nominal SELF_CLOSED_PRODUCTIVE hits, all with **partial
  support** (exactly two populated ± pairs, every other registered address at amplitude 0; 25 ABSORBED,
  597 KERNEL), and the **fully-populated variant EMPTY for all 622** (Gröbner basis `[1]` after
  saturating every `‖a_m‖² ≠ 0`). The sweep is an internal working record; the numbers are quoted here
  as finite_diagnostic readouts of that record, not re-run in this repository.
- **RSC-O two-anchor planarity** (`PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01`, PR #60): the anchor /
  recruit convention, an anchor being O-silent to a recruit through `a·q = 0`.
- **(ALT-1)** of `paper/NS_P2_RSC_O_ALTERNATION_TRANSFER.md` (`PROP-P3-RSC-O-ALTERNATION-TRANSFER-01`,
  PR #63): a genuine nonparallel single-O recruit copies the suppressed anchor's polarization line.
- **The one-sided silent layer** (`PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01`, PR #64): under one-sided
  `O_+` persistence the recruit layer is quadratically silent to itself; all persistent productivity
  must cross the layer/core interface. Fixture F2 below is exactly the "next target box" that note
  left OPEN, on one skeleton.
- **The M3 labels** `O / E / C / T` and `UNRESOLVED` (`PROP-P3-M3-SUPPRESSION-LABELS-01`, PR #62): the
  outcome menu of the rule is stated in these names.
- **The cancellation ledger** (`PROP-P2-CANCELLATION-LEDGER-01`): exact multi-source cancellation is an
  accounting entry, never a physical loss.
- **Genesis lineage preservation / no silent loss** (Standalone §114.1, Readout Genesis
  `NoEarlyCollapse`, mandatory lineage preservation): a future-relevant distinction cannot silently
  disappear. The rule below is this discipline written as a constraint on an exact closure test.
- The exact projected NSE bilinear interaction `B_{p,q}(a,b) = P_{p+q}[(a·q) b + (b·p) a]`, the same
  operator as every other checker on `main`, here in its **denominator-cleared** form
  `P_k[v] = (k·k) v − (v·k) k` (same zero set as the Leray projection over the reals for `k ≠ 0`).

No new global architecture is introduced.

---

## 1. The loophole — a forced address left out of the state

An exact closure question in this route has the form: *given a registered address set with
amplitudes, do all forcings into unregistered addresses vanish (zero registered novelty / no exit)
while some forcing into a registered address is nonzero (productive)?* Every such question is posed to
a Gröbner solver as polynomial equations (outside forcing = 0) plus Rabinowitsch saturations (some
inside forcing ≠ 0, recruits ≠ 0, genuine single-O, …).

The solver answers about the amplitude variables it is given. If a registered address `t` **receives
nonzero forcing** but its amplitude is either absent from the variable list or allowed to be `0` with
no further condition, the solver may return a point in which `t` is *forced and empty*: a descendant
that the dynamics produces and the state has forgotten. Such a point is not a closure of the dynamics —
the forcing into `t` is a real quadratic source that the next generation must carry — yet it satisfies
every equation posed. This is the **forgotten-descendant loophole**. As recorded in the NPSC sweep, it is
the mechanism of all 622 nominal hits: the populated 2-pair sub-state forces a registered third address
(KERNEL: exactly one of `p ± q` registered; ABSORBED: both) that carries amplitude 0.

---

## 2. The rule — forced-address accounting completeness

**Rule (`PROP-P3-FORCED-ADDRESS-ACCOUNTING-01`).** In any exact closure question, every registered
address that receives nonzero *individual* forcing must be explicitly represented in the state or the
ledger and resolved with exactly one of the outcomes

```text
ACTIVE                          amplitude != 0 at the address (the address is populated);
EXACT-CANCELLED                 net forcing 0 while individual contributions != 0, entered in the
                                cancellation ledger (M3 label C; accounting only, never a loss);
NULL-BY-REGISTERED-GEOMETRY     every individual contribution 0 by ORTH (a.q = 0 or b.p = 0) or
                                EQSHELL nullity (M3 labels O / E);
TED                             the address is outside the declared cell (M3 label T).
```

A forced address absent from state and ledger is **UNRESOLVED**, and the closure test that produced
the point is an **INVALID CLOSURE TEST**: its SAT points are not closure points of the dynamics.

This is *not* the statement "every forced address must be populated". That stronger reading would
delete the legitimate exact-cancellation branch (EXACT-CANCELLED) and the geometric-nullity branch,
both of which are honest outcomes in which an address is forced by individual pairs but carries no net
source. The rule asks for **accounting completeness**, not population.

### Boxed checker obligation

For each registered address `t` with amplitude variables `c_t` and net forcing polynomial `F(t)`:

\[
\boxed{
\;(c_t \neq 0)\ \ \lor\ \ \big(F(t) = 0\big)\;
}
\qquad\text{run as two exact systems and reported separately:}
\]

```text
System A   :  c_t saturated nonzero (adjoin v.(c_t.c_t) - 1)            -> ACTIVE
System B   :  c_t = 0  and  F(t) = 0  (componentwise)                   -> EXACT-CANCELLED or
                                                                            NULL-BY-GEOMETRY
forgotten  :  c_t = 0  and  F(t) != 0 (adjoin v.(F(t).F(t)) - 1)         -> the loophole;
                                                                            any SAT here = INVALID CLOSURE TEST
```

A closure point is valid only if it lies in System A or System B for **every** forced registered
address. The forgotten system is run so that the loophole is *seen*, not merely excluded. (Where the
distinction between EXACT-CANCELLED and NULL-BY-GEOMETRY matters, System B is split further by the M3
label checker; the fixtures below do not need that split.)

Over the complex variety that a ℚ Gröbner basis certifies, the denominator-cleared projection
degenerates on an **isotropic** pair sum (`k·k = 0`, `k ≠ 0`, no real counterpart) to the rank-one map
`v ↦ −(v·k) k`, whose kernel `k^⊥` contains `k` itself; the outside-zero equation then reads `(v·k) k = 0`,
which is far weaker than the Leray zero set (undefined there). Every symbolic pair sum `t` is therefore
additionally saturated by `t·t ≠ 0` in every system. This is part of
the obligation whenever the projection is used in denominator-cleared form.

---

## 3. Evidence for the rule (finite_diagnostic)

1. **NPSC sweep.** All 622 nominal depth-1 self-closure hits on negation-closed integer sets have
   partial support — a forced registered address left at amplitude 0 (25 ABSORBED / 597 KERNEL) — and the
   variant that saturates every amplitude nonzero (System A on all addresses) is EMPTY for all 622. The
   per-address `A ∨ B` variant was not run in that sweep and is OPEN.
2. **Fixture F2 below** (one-sided `O_+` layer + active `O_-` core, one skeleton): the forgotten system
   is SAT with a real rational witness (`q_0 = (0,0,±1)`, `b_0 = a_+`, core `c = 0`, all outside forcing
   `0`, core forced by `(0,0,2)` and empty), while System A and System B are both UNSAT. The point that a
   solver without the obligation returns is exactly a forgotten descendant.
3. **Fixture F1 below** (single-O alternation) is a *negative control for the evidence, not for the
   rule*: its earlier "unpopulated SAT" is not a forgotten-descendant point but a complex isotropic
   artifact (`q_0 = (0,0,±i)`, `(p_+ + q_0)·(p_+ + q_0) = 0`); with `t·t ≠ 0` saturated the unpopulated
   single-O system is UNSAT for `m = 2, 3` before any population condition is imposed. The checker
   records this correction explicitly.

---

## 4. The fixed skeleton

```text
p+ = (1,0,0), a+ = (0,1,0)          O_+ anchor
p- = (0,1,0), a- = (0,0,1)          O_- anchor           (a+ not parallel to a-)
k  = p+ + p- = (1,1,0),  c = (c1,-c1,c3)  in k^perp     core address, free polarization
anchor-anchor forcing into k:  B_{p+,p-}(a+,a-) = (0,0,2)   (nonzero, independent of every recruit)
```

Recruits `(q_j, b_j)` are **new registered addresses** (`q_j ∉ {±p_±, ±k}`; a "recruit" on an anchor
address would modify the fixed skeleton and is excluded by definition). Every pair sum that is not a
numeric member of `{p_+, p_-, k}` must carry zero net forcing (zero registered novelty). Conventions
inherited from the source runs and declared here: only the `+` representatives of the real modes enter
the web (difference targets `p − q` are not part of this accounting); formally distinct symbolic
targets are constrained separately, so every verdict is a verdict on the coincidence-free stratum
(strata where two symbolic targets, or a symbolic target and an inside address, coincide are not
analysed here — OPEN). The recruit pair sums `q_i + q_j = k` are shown UNSAT under the recruit
constraints, so `F(k) = (0,0,2)` on the admissible set, and System B for the core is refuted by that
constant. The saturation `t·t ≠ 0` also removes the real antipodal pair sums `t = 0` (`q_i = −q_j`,
`q_j = −p_±`), so every verdict is on the stratum without antipodal pair sums, consistent with the
`+`-representative convention.

**System A is already refuted at `m = 0`.** The anchor–core pairs are not silent (`a_+·k = 1`;
`a_-·k = 0` but `c·p_- = −c_1`): they force the outside
targets `(2,1,0)` (source `(c_1, 0, c_3)`) and `(1,2,0)` (source `(0,0,−c_1)`), and the two outside-zero
equations reduce to `c_1 = c_3 = 0` (Gröbner basis `[c_1, c_3]`, asserted by the checker). On the
coincidence-free stratum no recruit target can land on those addresses, so a populated core is an exit
for every `m` and every recruit family. Consequently the "System A UNSAT" and "System B UNSAT" columns
below are properties of the skeleton, not of the recruit histories; the only recruit-dependent column is
the forgotten one. (Numbers such as `‖(0,0,2)‖² = 4` are denominator-cleared quantities; the Leray value
of the anchor–anchor forcing is `(0,0,1)`.)

---

## 5. The three fixtures (`PROP-P3-RSC-O-SKELETON-FIXTURES-01`)

### F1 — single-O alternation, double-O excluded, `m = 2, 3`

Recruits alternate `σ_j = +, −, +, …`; `a_{σ_j}·q_j = 0` (genuine single-O on anchor `σ_j`),
`z_j (a_{−σ_j}·q_j) − 1 = 0` (double-O excluded), `b_j·q_j = 0`, `b_j ≠ 0`,
`B_{p_{σ_j}, q_j}(a_{σ_j}, b_j) = 0` (suppression of the `σ_j`-anchor interaction), productivity
`u · Σ_{t ∈ {p_+,p_-,k}} ‖F(t)‖² − 1 = 0`, `t·t ≠ 0` on every symbolic pair sum.

```text
m = 2 :  System A UNSAT   System B UNSAT   forgotten UNSAT   (forgotten WITHOUT t.t != 0: SAT, isotropic)
m = 3 :  System A UNSAT   System B UNSAT   forgotten UNSAT   (forgotten WITHOUT t.t != 0: SAT, isotropic)
```

Reading: on this skeleton a single-O alternating history with double-O excluded admits no
zero-novelty productive closure at all, in any of the three accountings (A and B already at the
skeleton level, Section 4; the forgotten column is the recruit-dependent one); the only points a ℚ
solver finds are complex isotropic artifacts. This corrects the earlier reading of the raw run as
"SAT → UNSAT once the core is populated": the raw SAT was never a real point.

### F2 — one-sided `O_+` recruit layer + active `O_-` core, `m = 1, 2`

Recruits `q_j = (x_j, 0, y_j) ∈ a_+^⊥`, `b_j = s_j a_+` (ALT-1), `a_-·q_j ≠ 0` (genuine single-O),
`s_j ≠ 0`; the `O_+` suppression `B_{p_+,q_j}(a_+,b_j) = 0` holds identically (PR #64); otherwise as
F1.

```text
m = 1 :  System A UNSAT   System B UNSAT   forgotten SAT — real witness q0 = (0,0,+-1), b0 = a+, c = 0
m = 2 :  System A UNSAT   System B UNSAT   forgotten SAT — variety = {q0 = q1 = (0,0,+-1)} only
                                                          (coincident recruits; the m = 1 point with a
                                                          duplicated address)
```

The `m = 1` witness is re-verified by exact substitution: every outside forcing vanishes, the `O_+`
interaction is silent, the productivity polynomial equals `4 = ‖(0,0,2)‖²`, and the core carries
amplitude 0 while being forced by `(0,0,2)`. Under the rule this point is UNRESOLVED at `k` and the
test that returns it is an INVALID CLOSURE TEST. With the obligation imposed (`A ∨ B`) the one-sided
box on this skeleton has **no** valid zero-novelty productive closure for `m = 1, 2` — but, per
Section 4, that is because the skeleton's own anchor–core interactions exit (System A refuted at
`m = 0`) and the core is forced by a constant (System B refuted), not because of anything the layer
does. The PR #64 "next target box" is therefore *not* answered by the layer on this skeleton; what the
fixture shows is that a solver without the obligation returns a forgotten descendant here. It says
nothing about other skeletons, larger `m`, or the coincidence strata.

### F3 — A3 shell-9 identity-monodromy rectangle

`S = ±{(2,−2,1), (2,−2,−1), (−2,−2,1), (−2,−2,−1)}` (8 addresses, all on shell `|k|² = 9`; the
identity-monodromy fixture of `PROP-P3-TYPE-P-IDENTITY-LOOP-FIXTURES-01`).

```text
pair sums landing on S : 0          distinct outside targets : 18          verdict : NO_INSIDE_TARGET
```

Every interaction of the rectangle is a registered exit; the web has no pair sum on its own
addresses, so it cannot be a zero-exit productive web *as it stands* (structurally, before any
amplitude is chosen). This is the closure half of the open A3 item for the shell-9 fixture; the
shell-5 planar 3-cycle is not treated here, and A3 is NOT closed.

---

## 6. Proposed results

`PROP-P3-FORCED-ADDRESS-ACCOUNTING-01` — **NEW DERIVATION / PROPOSAL; checker obligation**.

```text
In an exact closure question every registered address that receives nonzero
individual forcing must be represented and resolved as ACTIVE, EXACT-CANCELLED,
NULL-BY-REGISTERED-GEOMETRY or TED; per address the checker runs
  System A (amplitude != 0)  and  System B (amplitude = 0 and net forcing = 0)
and reports both; a point with amplitude = 0 and net forcing != 0 at a registered
address is a forgotten descendant and the test is an INVALID CLOSURE TEST.
Symbolic pair sums are saturated by t.t != 0 whenever the projection is
denominator-cleared.
```

`PROP-P3-RSC-O-SKELETON-FIXTURES-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

```text
On the fixed skeleton of Section 4 (denominator-cleared projection, t.t != 0,
+ representatives, coincidence-free stratum):
  F1 single-O alternation, double-O excluded : A UNSAT, B UNSAT, forgotten UNSAT (m = 2, 3);
                                               raw unsaturated points are complex isotropic.
  F2 one-sided O_+ layer + active O_- core    : A UNSAT, B UNSAT (m = 1, 2) — skeleton-level
                                               (A refuted at m = 0 by the anchor-core exits,
                                               B by the constant anchor-anchor forcing);
                                               forgotten SAT with real witness q0 = (0,0,+-1), c = 0
                                               (m = 2: coincident-recruit copies only).
  F3 A3 shell-9 rectangle                     : NO_INSIDE_TARGET (structurally open).
```

---

## 7. Claim boundary

```text
forced-address accounting completeness (Section 2)                 PROPOSAL / checker obligation
F1, F2, F3 verdicts (Section 5)                                     exact finite PASS on ONE skeleton, m <= 3, finite_diagnostic
NPSC 622 partial-support reading                                    finite_diagnostic readout of an internal sweep record
per-address A v B rerun of the NPSC sweep                           OPEN
coincidence strata / difference targets / other skeletons / m > 3   OPEN
A3 shell-5 planar 3-cycle closure                                   OPEN; A3 is NOT closed
PR #64 next target box (passive O_+ layer + active O_- core)        OPEN (not answered by F2: A/B fail at skeleton level)
RSC-O branch B (one-sided persistence)                              reduced on this skeleton only; not closed
RSC-O branch C (parallel anchor/recruit degeneracy)                 OPEN
RSC-O global                                                     OPEN
RSC-E / RSC-C                                                    OPEN
OCSR / Witness Soundness / G6/G7                                 OPEN
Clay Navier-Stokes regularity                                    OPEN
```

The fixtures prove nothing about RSC-O globally. No cancellation label is promoted to physical loss.
The rule is an accounting obligation on exact closure tests, not a dynamical theorem; the phrase
"forgotten descendant" names an accounting omission, not a physical process.

---

## 8. Status

```text
PROP-P3-FORCED-ADDRESS-ACCOUNTING-01     checker obligation encoded (A / B / forgotten)     PASS (exact; not yet in Toledo)
PROP-P3-RSC-O-SKELETON-FIXTURES-01       F1 m=2,3 / F2 m=1,2 / F3 verdicts                  PASS (exact; not yet in Toledo)
System A refuted at m = 0 (anchor-core exits, Groebner basis [c1, c3])                        PASS
F2 m=1 forgotten witness re-verified by substitution                                        PASS
F1 isotropic-artifact markers (z0^2 + 1, q0_2 + z0) in the raw basis                        PASS
checker runtime                                                                            ~16 s (m = 3 retained)
```
