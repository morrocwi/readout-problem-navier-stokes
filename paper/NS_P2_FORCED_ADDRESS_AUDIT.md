# NS P2 — Per-Address Forced-Address Audit: an Exact Classifier, the Isotropic-Saturation Invariant, and a Pre-Threshold Audit of the T0-02 Runtime Record

**Status:** NEW DERIVATION / PROPOSAL; instrument + finite diagnostic  
**Proposal ids:** `PROP-P3-FORCED-ADDRESS-AUDIT-01` — not yet in Toledo; `PROP-P3-ISOTROPIC-SATURATION-INVARIANT-01` — not yet in Toledo  
**Parent route:** merged PR #66 `PROP-P3-FORCED-ADDRESS-ACCOUNTING-01` (at `0bdf9df`, `paper/NS_P2_FORCED_ADDRESS_ACCOUNTING_RULE.md`) / PR #64 / PR #63 / PR #62 M3 labels  
**Global RSC-O / RSC-E / RSC-C / OCSR / Witness Soundness / G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checkers:** `reproduction/checks/check_ns_p2_forced_address_audit.py`, `reproduction/checks/check_ns_p2_t0_02_forced_address_prethreshold.py`  
**Data:** `reproduction/data/ns_p2_t0_02_A_d2_prethreshold.json` (compact export of the internal T0-02 record, point A, depth 2)  
**Date:** 2026-09-13

## 0. Reuse-first audit

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

A Toledo lookup (registry, canonical map, the NS P2 proposals) found no canonical object for a
per-address accounting classifier and none for the isotropic-saturation invariant as a checker
obligation. Reused objects (not re-derived):

- **The accounting rule** `PROP-P3-FORCED-ADDRESS-ACCOUNTING-01` (PR #66): every registered address
  that receives nonzero individual forcing must be resolved as ACTIVE, EXACT-CANCELLED,
  NULL-BY-REGISTERED-GEOMETRY or TED; absent ⇒ UNRESOLVED ⇒ INVALID CLOSURE TEST. That note stated the
  obligation as two Gröbner systems per address (System A / System B / forgotten). This note gives the
  *evaluated* form: a classifier that takes a concrete web (addresses with amplitudes), aggregates every
  contribution per address, and assigns exactly one state.
- **The two corrections recorded in the PR #66 paper**, referred to here as R1 and R2:
  R1 — the raw "unpopulated SAT" of the single-O fixture F1 was retracted as a complex isotropic
  artifact (`q_0 = (0,0,±i)`, `(p_+ + q_0)·(p_+ + q_0) = 0`); with `t·t ≠ 0` saturated the system is
  UNSAT, which also corrects the earlier reading "SAT → UNSAT once the core is populated" (the raw SAT
  was never a real point). R2 — the System A / System B UNSAT columns of F2 are skeleton-level (System A
  refuted at `m = 0` by the anchor–core exits, System B by the constant anchor–anchor forcing), so F2
  does not answer the PR #64 target box. R1 is the origin of the invariant in Section 3.
- **The NPSC depth-1 sweep** (internal run record; exact Gröbner over ℚ on negation-closed integer
  address sets, box `[-2,2]^3`, 2–4 ± pairs): 610 nominal SELF_CLOSED_PRODUCTIVE hits with an explicit
  rational point (20 with three ± pairs, 590 with four). Its amplitude construction
  `a_m = x_m e_1(m) + y_m e_2(m)` with `(e_1, e_2) = perp_basis(m)` is reused **verbatim** (Section 4.2).
- **The T0-02 runtime record** `T0-2026-09-12-02` (internal; frozen 14-mode seed on the √3-lattice,
  point A, ν = 1/200, integrating-factor RK4, active set `A_d`, registered exit `S_{d+1} \ S_d`,
  retention threshold `1e-12 · B(T0)`). Its report states `Dropped = T = 0` in every reader window. The
  present note audits the layer beneath that readout.
- **The M3 labels** `O / E / C / T` and `UNRESOLVED` (PR #62) and the **cancellation ledger**
  (`PROP-P2-CANCELLATION-LEDGER-01`): EXACT_CANCELLED is an accounting entry, never a physical loss.
- The exact projected bilinear interaction `B_{p,q}(a,b) = P_{p+q}[(a·q) b + (b·p) a]`, the same operator
  as every other checker on `main`; here in its Leray form (exact division by `k·k`) for classification
  and in its denominator-cleared form `P_k[v] = (k·k) v − (v·k) k` for the symbolic invariant.

No new global architecture is introduced.

---

## 1. The instrument — one address, one state

The accounting unit is **one address after aggregation**: every unordered pair `{p, q}` of registered
modes (self-pairs included; `p + q = 0` skipped) contributes `B_{p,q}(a_p, a_q)` to the address
`t = p + q`, and the classifier decides on the aggregate `F(t) = Σ B`, with the individual contributions
retained for the ledger split. Each record carries `(a, N_terms, F(a), registered, state)`.

States are mutually exclusive and decided in this precedence order:

```text
ISOTROPIC_TARGET      t.t = 0, t != 0 (complex only)          flagged first; never counted as zero
                                                              or nonzero (R1 guard)
ACTIVE                a registered, amplitude != 0
EXACT_CANCELLED       F(a) = 0 exactly, >= 2 individually nonzero contributions
NULL_BY_GEOMETRY      F(a) = 0 exactly, every contribution individually 0
TED                   F(a) != 0, a unregistered, a outside the declared cell   (registered exit)
FORGOTTEN_REGISTERED  F(a) != 0, a registered, amplitude = 0                   -> INVALID CLOSURE TEST
FORGOTTEN_INSIDE      F(a) != 0, a unregistered, a inside the declared cell    -> INVALID CLOSURE TEST
```

Exact inputs (sympy rationals and algebraic numbers) are decided exactly: there is no tolerance in any
exact decision. Float inputs go through a separate path whose only zero state is
`NUMERICAL_ZERO(eps)`, reported with its `eps`; it is never renamed `EXACT_CANCELLED` or
`NULL_BY_GEOMETRY`, and a bitwise-zero float is reported as a sub-count inside it, not as an exact zero.

### Boxed invariant

Let `W` be the set of populated addresses (amplitude ≠ 0) of the web under test. Then

\[
\boxed{\;\forall\, a \notin W:\qquad F(a) = 0 \;\;\lor\;\; a \text{ enters the ledger}\;}
\]

— *no empty forced address may disappear from the accounting.* "Enters the ledger" means the address
receives a state that names what happened to its forcing: TED (a registered exit, its load recorded) or
one of the two FORGOTTEN states (which invalidate the closure test that produced the web). An empty
forced address that appears in no record at all is the loophole of PR #66; the classifier makes it
impossible to leave one out because it enumerates every pair sum. Cancelled and geometrically null
addresses satisfy the left disjunct and are ledgered as `EXACT_CANCELLED` / `NULL_BY_GEOMETRY` for the
M3 split.

The invariant is an accounting obligation on closure tests and runtime readouts. It is not a
dynamical statement and does not say that forcing must be integrated.

---

## 2. Semantics that the checker enforces

- **Aggregation before classification.** Two contributions that cancel at the same address give one
  record with `N_terms = 2`, `F = 0`, state `EXACT_CANCELLED`; they are not two records.
- **Registered exit versus forgotten inside.** The declared cell is part of the input (a bound on
  `|t|²`; for the NPSC hits the box itself, `|t|² ≤ 3·box²`). A nonzero forced address outside the cell is
  a TED entry; inside the cell it is FORGOTTEN_INSIDE. Moving the cell moves addresses between these two
  states and nothing else.
- **Registered but empty.** An address that is in the web's address list with amplitude 0 and receives
  `F ≠ 0` is FORGOTTEN_REGISTERED regardless of the cell.
- **Real field.** `a_{−m} = a_m` for every fixture, as in the source runs.
- **Self-pairs.** The pair enumeration includes `{p, p}`; for a divergence-free amplitude
  `B_{p,p}(a,a) ∝ (a·p) a = 0`, so every `2p` address collects an identically zero contribution and, if
  nothing else lands there, is `NULL_BY_GEOMETRY`. This inflates that count by construction and is
  part of the calibrated totals.
- **Order of the last two decisions.** TED requires an unregistered address and FORGOTTEN_REGISTERED a
  registered one, so the two are disjoint; the checker tests `registered` before the cell bound, which
  changes no outcome.

---

## 3. The isotropic-saturation invariant (`PROP-P3-ISOTROPIC-SATURATION-INVARIANT-01`)

Over the complex variety that a ℚ Gröbner basis certifies, the denominator-cleared projection
`P_k[v] = (k·k) v − (v·k) k` degenerates on an isotropic pair sum (`k·k = 0`, `k ≠ 0`) to the rank-one map
`v ↦ −(v·k) k`; the outside-zero equation then reads `(v·k) k = 0`, far weaker than the Leray zero set,
which is undefined there. The R1 retraction in PR #66 is exactly this failure on the single-O fixture.

**Invariant (checker form).** In every denominator-cleared symbolic closure test, every symbolic pair
sum `t` is saturated:

```text
adjoin   u_t · (t·t) − 1 = 0     for every symbolic target t        (Rabinowitsch form)
   or    assert t·t != 0          numerically, for every concrete target
```

The numeric form is the `ISOTROPIC_TARGET` precedence of the classifier (Section 1): an isotropic
target is flagged before any zero / nonzero decision is attempted and is never counted on either side.
The checker verifies both forms on `p = (1,0,0)`, `q = (0,i,0)`: `t = (1,i,0)`, `t·t = 0`, the classifier
returns `ISOTROPIC_TARGET`, the saturation polynomial evaluates to `−1` for every `u`, and
`P_dc[t] = 0` (rank-one degeneracy); on a real lattice target the polynomial is satisfiable with
`u = 1/(t·t)`. On the real integer lattice `t·t = 0` forces `t = 0`, which is skipped as "no target", so
the guard never fires on the fixtures of Section 4 (asserted).

---

## 4. Results — exact fixtures (finite_diagnostic)

### 4.1 The three open seeds W1, W2, W3 point A

| fixture | cell | addresses | NULL_BY_GEOMETRY | EXACT_CANCELLED | ACTIVE | TED | FORGOTTEN_INSIDE | verdict |
|---|---|---|---|---|---|---|---|---|
| W1 (two-shell N = 2) | `\|t\|² ≤ 3` | 26 | 8 | 2 | 0 | 6 | **10** | INVALID (10) |
| W2 (rank-2, three ± pairs) | `\|t\|² ≤ 3` | 56 | 12 | 2 | 12 | 18 | **12** | INVALID (12) |
| W3 point A (T0-02 seed, 14 modes) | `\|t\|² < 29/10` | 82 | 22 | 0 | 14 | 28 | **18** | INVALID (18) |

These are the expected outcomes: W1, W2 and W3 are *open* seeds whose descendants were never claimed to
be closed, so their INVALID verdicts calibrate the classifier against the internal record (the same
address totals and state counts; per-address records are printed, not asserted) rather than establish anything about the seeds. W3 point A has no
EXACT_CANCELLED address at generation 1 under this cell; the `±k` datum address is ACTIVE (registered
with amplitude `(1,0,0)`), so its exact cancellation is not visible in this table.

### 4.2 NPSC box-2 hits: 20 of 610 in CI, 610/610 as a record

Each SELF_CLOSED_PRODUCTIVE hit is reconstructed as a concrete web: registered set `S = ±S_reps`, amplitude
`a_m = x_m e_1(m) + y_m e_2(m)` with `(e_1, e_2) = perp_basis(m)` **copied verbatim from the sweep**, point
coordinates from the hit record, declared cell `|t|² ≤ 12`. A deterministic subset of 20 hits (index
`(k·610)//20`, `k = 0..19`, over the box-2 hit list in file order — the 20 three-pair hits first, then the
590 four-pair hits) runs in CI; each must be INVALID with at least one FORGOTTEN_REGISTERED address.

```text
CI subset (20 hits)  : 20/20 INVALID; address states  NULL_BY_GEOMETRY 506  ACTIVE 80  FORGOTTEN_REGISTERED 40
                       (every hit: exactly 2 forgotten registered addresses = one +- pair; 4 ACTIVE = the
                        two populated +- pairs; every unregistered target NULL_BY_GEOMETRY)
Internal full record : 610/610 INVALID, 0 valid; address states  NULL_BY_GEOMETRY 15186  ACTIVE 2440
                       FORGOTTEN_REGISTERED 1260    [FINITE_DIAGNOSTIC record of the internal run; not re-run in CI]
Box-1 hits (12)      : not re-audited
```

Reading: on every audited hit the populated two ± pairs force exactly one registered ± pair that carries
amplitude 0 — the KERNEL / ABSORBED partial-support mechanism of PR #66, now seen address by address — and
no outside target carries any nonzero contribution. No hit has an EXACT_CANCELLED or TED address: the
"closure" of these points is the trivial one in which the only nonzero interactions land on a forgotten
registered address.

**Lesson — point coordinates are basis-dependent; reuse the generator's basis.** The first internal
pass reconstructed the points with a *different* basis of `m^⊥` and reported 10 of the 610 hits as valid
closure points; re-running with the sweep's own `perp_basis` gave 0. The intermediate log was not
retained, so this is carried as a process lesson, not a result: a hit record `(S, x, y)` is meaningless
without the basis that defined `x, y`, and a checker that re-derives a basis is auditing a different web.
The checker therefore embeds the generator's function verbatim and cites the sweep record.

---

## 5. Results — pre-threshold audit of the T0-02 runtime record (finite_diagnostic)

The T0-02 report classifies an address as energised when its retained load `w |k|² |u|²` exceeds
`1e-12 · B(T0)` (`B(T0) = 14`) and reports `Dropped = T = 0` in every window. The question posed here is
whether the pipeline respects the per-address accounting *before* that threshold: is there any registered
address (the active set `A_2`, 289 canonical-half addresses) that carries forcing while its amplitude is
zero?

**Export.** At the four stored reader-window boundaries the forcing `N_k` on every registered address was
recomputed in float64 from the stored full state with the stepper's own pair table (no threshold); a
fifth sample at the first record (`t = rec·dt = 0.003`) is taken from the run's recorded `Nhist`
(complex64) / `load_hist` (float64) arrays and labelled as such. Every float is written with 6 significant
digits; `0.0` is kept exactly; **no rational rounding is applied** to any decided value.
`Fraction.limit_denominator(10⁹)` is reported only as a comparison: it would rename 18 of the 1 726
nonzero float forcing components to exactly 0 at each window boundary `t > 0` (18 of 78 at `t = 0`;
214 of 1 726 at `t = 0.003`),
which is why a rational rounding cannot be used to decide "exact zero".

**Float semantics (declared).** Amplitude zero = bitwise zero (`max_c |u_c| = 0.0`); "below the retention
threshold" (`0 < load ≤ 1.4e-11`) is a separate sub-count and is *not* amplitude zero. Forcing zero =
`NUMERICAL_ZERO(eps)` with `eps = 1e-12` on `max_c |F_c|`, bitwise-zero sub-count inside it. A second,
stricter reader ("threshold semantics": amplitude := load > threshold) is tabulated beside it for
comparison; it is not the accounting semantics.

| sample | t | ACTIVE | of which below threshold | NUMERICAL_ZERO(1e-12) | of which bitwise 0 | FORGOTTEN_REGISTERED | threshold-reader FORGOTTEN | source |
|---|---|---|---|---|---|---|---|---|
| snap_0 | 0 | 7 | 0 | 259 | 256 | **23** | 23 | stored state, float64 recompute |
| record_1 | 0.003 | 289 | 187 | 0 | 0 | **0** | 187 | recorded Nhist (complex64) / load_hist |
| snap_1 | 5.350 | 289 | 0 | 0 | 0 | **0** | 0 | stored state, float64 recompute |
| snap_2 | 10.701 | 289 | 0 | 0 | 0 | **0** | 0 | stored state, float64 recompute |
| snap_3 | 16.050 | 289 | 0 | 0 | 0 | **0** | 0 | stored state, float64 recompute |

Exit layer (unregistered, outside the declared cell = TED by construction): 1 874 exit half addresses,
1 867 with nonzero Duhamel window load in each of the three windows (max `|I|` 0.975 / 0.711 / 0.703).

**Reading.**

1. **At `t > 0` the pipeline respects the accounting: FORGOTTEN_REGISTERED = 0 at every sample.** Every
   registered address that carries forcing carries amplitude; nothing forced is empty.
2. **At `t = 0` the datum itself leaves 23 addresses forced and empty**, all of generation 1 (the 46 full
   addresses the first step populates; the equal-shell class and the `±k` datum address carry zero net
   forcing there). This is the definition of an initial condition, not an omission: under the strict
   instantaneous semantics of Section 1 these 23 addresses *are* FORGOTTEN_REGISTERED at the instant
   `t = 0`, and the table says so rather than hiding it. Three further generation-1 addresses show
   `|F| = 1.1e-16`: geometrically null datum targets (`NULL_BY_GEOMETRY` in the exact W3A fixture of
   Section 4.1, every contribution individually zero) whose float recompute leaves roundoff; they are
   read as NUMERICAL_ZERO, not as exact zero.
3. **The threshold reader is not the accounting.** At `t = 0.003` the retention threshold would call 187
   sub-threshold addresses "not energised" although every one of them carries nonzero amplitude and the
   integrator carries it forward; under threshold semantics these would be 187 forgotten addresses. The
   report's `Dropped = T = 0` is therefore a statement about the *count* reader; the accounting statement
   underneath it (no forced address is empty at any `t > 0`) is what this audit adds, and it holds.
4. Nothing here is a statement about depth `d ≥ 3`, point B, other `ν`, `λ_0`, or the continuum; the
   `d = 2` exit carries load comparable to the interior after `t ≈ 0.3` (T0-02 report, validation (3)) and
   is ledgered here as TED, not integrated.

---

## 6. Proposed results

`PROP-P3-FORCED-ADDRESS-AUDIT-01` — **NEW DERIVATION / PROPOSAL; instrument, exact finite PASS on the fixtures**.

```text
Per-address classifier for the forced-address accounting rule: unit = one address after
aggregation; states ISOTROPIC_TARGET > ACTIVE > EXACT_CANCELLED > NULL_BY_GEOMETRY > TED >
FORGOTTEN_REGISTERED / FORGOTTEN_INSIDE (=> INVALID CLOSURE TEST); exact decisions only on
exact inputs; NUMERICAL_ZERO(eps) as the sole zero state on float inputs, never renamed EXACT.
Invariant: for every a outside the populated set, F(a) = 0 or a enters the ledger.
  W1 / W2 / W3A : INVALID with 10 / 12 / 18 FORGOTTEN_INSIDE (calibration against the record)
  NPSC box-2    : 20/20 CI subset INVALID (>= 1 FORGOTTEN_REGISTERED each); 610/610 internal record
  T0-02 A d=2   : FORGOTTEN_REGISTERED = 0 at every t > 0 sample; 23 at t = 0 (the datum's
                  generation-1 targets); 187 threshold-reader artefacts at t = 0.003
```

`PROP-P3-ISOTROPIC-SATURATION-INVARIANT-01` — **NEW DERIVATION / PROPOSAL; checker invariant**.

```text
Every denominator-cleared symbolic closure test saturates every symbolic pair sum t by
u_t (t.t) - 1 = 0 (or asserts t.t != 0 numerically); the classifier flags an isotropic target
before any zero / nonzero decision.  Origin: the R1 retraction of PR #66.
```

---

## 7. Claim boundary

```text
per-address classifier (Sections 1-2)                              PROPOSAL / instrument
isotropic-saturation invariant (Section 3)                          PROPOSAL / checker invariant
W1 / W2 / W3A verdicts                                              calibration on open seeds, finite_diagnostic
NPSC box-2: 20-hit CI subset                                        exact finite PASS (INVALID each), depth 1
NPSC box-2: 610/610                                                 FINITE_DIAGNOSTIC record of an internal run, not re-run here
NPSC box-1 hits (12)                                                not re-audited
T0-02 pre-threshold audit                                           point A, depth 2, five samples, float semantics declared;
                                                                    d >= 3 / point B / other readers        OPEN
basis-dependence lesson (Section 4.2)                               process lesson; intermediate log not retained
coincidence strata / difference targets / m > 3 (PR #66)            OPEN
RSC-O global / RSC-E / RSC-C                                        OPEN
OCSR / Witness Soundness / G6/G7                                    OPEN
Clay Navier-Stokes regularity                                       OPEN
```

The instrument proves nothing about OCSR, Witness Soundness, G6/G7 or Clay. No cancellation label is
promoted to physical loss; "forgotten" names an accounting omission, not a physical process. An INVALID
verdict on a closure test says the test's point is not a closure point of the dynamics; it does not say
the dynamics has no closure.

---

## 8. Status

```text
PROP-P3-FORCED-ADDRESS-AUDIT-01              classifier + fixtures + NPSC subset + T0-02 audit    PASS (not yet in Toledo)
PROP-P3-ISOTROPIC-SATURATION-INVARIANT-01    guard + saturation polynomial verified                PASS (not yet in Toledo)
W1 / W2 / W3A calibration                    26 / 56 / 82 addresses, state counts as recorded      PASS
NPSC box-2 CI subset                         20/20 INVALID, 40 FORGOTTEN_REGISTERED                PASS
T0-02 pre-threshold                          FORGOTTEN_REGISTERED = 0 for t > 0; 23 at t = 0       PASS (finite_diagnostic)
checker runtime                              ~1.3 s (classifier), < 0.1 s (pre-threshold)
```
