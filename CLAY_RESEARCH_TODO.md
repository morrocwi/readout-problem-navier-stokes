# Clay Research TODO — Priority by Mathematical Leverage

**Status:** live cross-repository task queue  
**Date:** 2026-09-11  
**Rule:** priority is determined by how much a task advances an explicit global bridge, not by how interesting or computationally large it is.

## P0 — Orientation / audit gate

- [x] Read `CLAY_READ_FIRST.md` before substantive work.
- [x] Read `CLAY_MULTI_PROBLEM_FINITE_BRIDGE_PROGRAM.md`.
- [x] Check NS `CLAIMS.md` for current claim boundaries.
- [x] Check IDM P-vs-NP PR #117 and issue #124.
- [x] Check Toledo `docs/CLAY_BRIDGE_PROGRAM_2026-09-11.md` and issue #11.
- [x] Record current branch/commit/CI/formal status before changing a theorem claim.
- [x] Freeze the P0 snapshot in `CLAY_P0_AUDIT_2026-09-11.md`.
- [x] Record the P-vs-NP formal/CI HOLD finding in PR #117 and Toledo issue #11.

### P0 findings / blockers carried forward

- [ ] **PNP baseline blocker before P3:** synchronize `research/p-vs-np-readout` with current IDM `main`; at the P0 snapshot it is 181 commits ahead and 27 behind.
- [ ] **PNP formal blocker before P3:** repair the Coq 8.20 failure in `formal/IDM_SATRestrictionDefect.v` (`wrong_root_forces_positive_defect`) and rerun focused formal CI green.
- [ ] **PNP verifier blocker:** repair the no-`Admitted` lexical guard so ordinary English `admit` in comments is not reported as hidden formal assumptions.
- [ ] **Governance hardening:** require `clay-governance` through branch protection/rulesets for NS, IDM and Toledo; the audited `main` branches currently report `protected:false`.

P0 audit phase status: **CLOSED as an audit**, with the blockers above explicitly carried into later phases.

## P1 — Shared finite obstruction / uniform bridge core

Primary home: `morrocwi/information-discrete-math`.

- [x] Formalize strict-margin soundness and fail-closed HOLD semantics.
- [x] Formalize finite error-budget composition.
- [x] Formalize finite cross-resolution compatibility-budget composition.
- [x] Formalize quotient/symmetry-respecting certificate transport under declared invariance.
- [x] Formalize local finite-defect checker soundness under declared laws.
- [x] Add negative controls showing why tested/local finite conditions do not imply global claims.
- [ ] Continue stress-testing strengthened generic statements against both NS and P vs NP adapters.

Evidence:

- IDM PR #125 merged as `1ddf295ea6fd9c504a10e6296fdea5bb97cf78fd`: 11 Coq 8.20 safe-core theorems axiom-free.
- IDM P2 negative controls refute naive FUB-03/04/05 forms while strengthened forms remain OPEN.

## P2 — Navier--Stokes direct bridge attack

Primary home: this repository.

### Read-first handoff

Before new P2 work, read:

```text
CLAY_P0_P2_RESEARCH_HANDOFF_2026-09-11.md
FUTURE_WORK_P2_TRIAD_ATTACK.md
paper/NS_P2_TRIAD_PHASE_READOUT_ATTACK.md
```

### Corrected status rule

The theorem `NS-P2-FINAL-EQUIV` remains **DERIVED** under its declared adapter:

```text
regularity on [0,T] <=> existential SC(T)
```

However, the earlier workflow inference

```text
regularity-equivalent => stop attacking the proposal
```

is withdrawn. Equivalence is not refutation. A constructive proof of `SC(T)` from genuinely weaker finite/checkable NSE structure remains a valid direct attack.

Current ruling:

```text
P2 historical reduction architecture = established
P2 constructive direct attack = REOPENED / ACTIVE
NS-P2-FINAL-EQUIV = DERIVED
NS-P2B-SCALE-CONTRACTION-UNIFORM = OPEN as constructive target
NS-P2-FRUSTRATION-OR-CUT = OPEN load-bearing structural target
```

### P2 established results retained

- [x] `A1E`: finite-time singularity forces arbitrarily large finite-Galerkin `H^3` exceedances under declared adapters.
- [x] `A1V`: exact finite rational PASS/HOLD verification of finite `H^3` exceedance.
- [x] Fixed-`N` validated tube, tube chain, residual tube and finite rational certificate-completeness machinery.
- [x] `L2`/energy-only omitted-tail control REFUTED as an `H^3` tail mechanism.
- [x] Fixed-`N` certificate/trajectory breakdown REFUTED as a standalone singularity witness.
- [x] Positive-lag Stokes and old-Duhamel histories have explicit all-scale `H^3` tail envelopes.
- [x] Adapter-neutral `H^3` dissipative-margin implication -> uniform `H^3` Gronwall bound DERIVED.
- [x] `NS-P2-HH-GEOM-LIFT` weighted geometric-tail arithmetic DERIVED.
- [x] External High--High preprint held rather than promoted.
- [x] `NS-P2B-EPSC-OBS-LIFT` DERIVED.
- [x] `NS-P2B-SUBCRITICAL-OBS` DERIVED.
- [x] Energy+dissipation-only strict critical exponent gain REFUTED as an inference by critical-spike accounting.
- [x] Integrated shell balance + total transfer conservation alone REFUTED as sufficient source of strict contraction.
- [x] `NS-P2B-SCALE-CONTRACTION`: strict recurrence -> `R_j -> 0` -> eventual observation-gate PASS DERIVED.
- [x] `NS-P2-FINAL-EQUIV`: regularity <-> existential `SC(T)` DERIVED under declared adapter.

### Reopened exact triad attack — current results

- [x] Shell-energy-only signed transfer/contraction REFUTED by an actual exact NSE triad with identical `(x,y,z)` and opposite phase coordinate `r`.
- [x] Viscosity-only contraction of normalized phase coherence REFUTED; viscous contribution cancels from `d log|r/sqrt(xyz)|/dt`.
- [x] Exact isolated-triad identity `D=xyz-r^2`, `D'=-16 nu D`; perfect phase locking `D=0` can persist.
- [x] Exact N=1 H3 nonlinear-production polynomial: 432 nonzero cubic monomials and GF(2) all-sign alignment is UNSAT.
- [x] Exact four-term finite frustration tax `|Q_cycle| <= S_cycle - 2 m_cycle`.
- [x] Symbolic all-n ladder frustration family constructed.
- [x] Symbolic dyadic high-high motif `q=(n,n,0)`, `r=(n,-n,0)`, `t=(2n,0,0)` derived with

```text
Q_n = C_n Im(z_q z_r conjugate(z_t))
C_n = 8 n^7 (28 n^4 + 18 n^2 + 3)
Gamma_n <= 7 sqrt(2)/(8 n^2)
```

- [x] Claim correction: one complex triad's four-real-monomial sign pattern is not by itself genuine network frustration; a single triad can choose a maximizing phase.

### Current P2 load-bearing frontier

#### `NS-P2-FRUSTRATION-OR-CUT` — OPEN

For overlapping transfer-active complex triads crossing dyadic boundaries, prove or refute a quantitative dichotomy:

```text
phase-holonomy incompatibility -> strict cancellation tax
OR
required amplitude becomes small -> transfer-chain cut
```

Strong enough to imply a recurrence

```text
R_{j+1} <= (1-delta_j) R_j + beta_j
```

with a uniform or nonuniform decay condition sufficient for `R_j -> 0`.

Immediate work order is specified in `FUTURE_WORK_P2_TRIAD_ATTACK.md`:

- [ ] build exact complex phase-incidence/holonomy checker for overlapping triads;
- [ ] search counterexample/SAT assignments before asserting frustration;
- [ ] extract the smallest genuine complex UNSAT holonomy cycle if one exists;
- [ ] turn holonomy mismatch into quantitative phase deficit;
- [ ] prove frustration-or-amplitude-cut lemma;
- [ ] prove dyadic boundary cycle coverage/decomposition;
- [ ] control temporal phase switching in the finite-observation time window;
- [ ] aggregate to all-scale recurrence and explicit recent-nonlinear remainder decay;
- [ ] formalize stable finite lemmas and rerun fail-closed CI.

### Canonical P2 architecture upgrade — Standalone vNext (2026-09-11, later than PR #52)

`paper/NS_P2_STANDALONE_VNEXT.md` supersedes the framing (not the statements) of the holonomy-era
notes. Its Sections 109–118 replace fixed-point/viable-set rigidity by the chain-recurrent core target
and organise the interior around constraint accumulation:

```text
CR_0(Q-bar^sc_P2) subset P u D                         CANONICAL TARGET / OPEN      (109.3, 118.3)
IRR  interior recurrent rigidity                        OPEN                          (111.2)
OWR / FNW  orthogonal-web / flat null-web rigidity      OPEN                          (112.3, 114.3)
OCSR outward-channel suppression rigidity               OPEN; shortest IRR route      (117.5)
Witness Soundness                                       OPEN / conceptually essential (111.5)
current preferred move: OCSR + global multi-source cancellation compatibility + Witness Soundness (118.4)
```

`NS-P2-FRUSTRATION-OR-CUT` is retained as an OPEN statement; phase holonomy is now one component
(`d_hol`) of the defect vector of the constraint web rather than the organising principle.

Exact results recorded against this architecture (`paper/NS_P2_MULTISOURCE_CANCELLATION_OCSR_GEN1.md`):

- [x] (113.1)–(113.3) certified exactly; equal source shells lock the interaction direction (Section 14 corollary); rank 1 iff `|p|=|q|` (exact instances PASS, generic statement DERIVED via Section 14).

Which order governs: the holonomy work list above (FW-1…FW-12) remains valid as checker material; the
standalone's (118.4) move — OCSR + global multi-source cancellation compatibility + Witness Soundness —
is the current canonical priority for the interior.
- [x] Exact multi-source cancellation witnesses W1/W2/W3 (two-shell N=2, rank-2 genericity, equal-shell N=3); reality constraint vacuous on all three.
- [x] W3 generation 1: suppressing both outward descendants forces a non-productive parent; W3 depth-1 full convolution is not lossless (36 nonzero targets, 30 single-source).
- [ ] Witness Soundness for `D_cancel` on the three witnesses (is `C_k > 0` a payable loss or a constraint?).
- [ ] OCSR at generation 2 on any seed; antipodal-source configurations; symmetry-free two-shell N=2.
- [ ] Supply or downgrade the unstated "zero-cancellation source-ray alignment — DERIVED" lemma.

### Current typed attack map (2026-09-12) — Type-P inputs to A1 / A3

Sources: `paper/NS_P2_PROJECTIVE_HOLONOMY_TYPE_AUDIT.md` (three-line rigidity, Type-P / Type-Phi boundary),
`paper/NS_P2_TYPEP_LOOP_TRANSPORT_FIXTURES.md`, checker `reproduction/checks/check_ns_p2_typeP_loop_transport.py`.

- [x] `PROP-P3-TYPE-P-SHELL-CONFINEMENT-01`: non-rank-0 Type-P transport on an edge forces `|k1| = |k2|` (corollary of the anchor-cross nullity theorem, DERIVED / EXACT); a closed Type-P loop with non-rank-0 edges lies on one shell. The rank-0 edge (`a ⊥ k2`) is a separate projective-collapse branch to `[k1 × k2]`, never an invertible transport.
- [x] `PROP-P3-TYPE-P-IDENTITY-LOOP-FIXTURES-01`: shell-9 rectangle and shell-5 planar 3-cycle have identity Type-P loop monodromy exactly (EXACT FIXTURE / PROPOSAL); explicit two-fixed-line and zero-fixed-line nonidentity loops recorded. Identity branch A3 is non-empty at the transport level (DERIVED from the fixtures); A3 is NOT closed.
- [ ] A3: run the existing equal-shell full-convolution closure audit (direction lock, W3 generation-1 suppression, depth-1 full convolution) on the two identity-monodromy fixtures; productivity / zero-defect closure of those webs is untested.
- [ ] A1: third-line generation/return search, or refutation, on the explicit two-fixed-line loops; equal-shell loop statistics remain FINITE_DIAGNOSTIC only.
- [x] `PROP-P3-M3-SUPPRESSION-LABELS-01` (`paper/NS_P2_M3_SUPPRESSION_LABELS.md`, checker `reproduction/checks/check_ns_p2_m3_suppression_labels.py`, not yet in Toledo): M3 label-set checker — per suppressed target `L(e) ⊆ {O, E, C, T}` or `UNRESOLVED` (fail-closed), labels not mutually exclusive, C an accounting label never a physical loss; double-O rank counter (`rank{a_i : i ∈ O(e)} ≥ 2`, not two O labels). Exact: `UNRESOLVED = 0` on W1 / W2 / W3 point A; W1 `k` is C without E; W3 `k` is C ∧ E; `N_{O,1}/N_{O,≥2}` = 8/0, 12/0, 14/2. Instrument only — OCSR / Witness Soundness / RSC / G6 / G7 unchanged.
- [x] M3 calibration on the orthogonal-turn generation-1 chain (2026-09-13): the time-honest gen-1 web (`±p0, ±q0, ±p1, ±q1`, H1-flat real amplitudes exact over `Q(√5)`, cell `|t|² ≤ 500`) is registered in `check_ns_p2_m3_suppression_labels.py` as an EXACT FIXTURE / FINITE DIAGNOSTIC with provenance (internal generator script `ot_chain_gen1_timehonest.py`, commit `83d8b5bf`). Result: `UNRESOLVED = 0`, O12/E8/C0/T2, `N_{O,1}/N_{O,≥2}` = 12/0; every target single-source, so no C; selected channels `p1`, `p2` NOVELTY. Not evidence that RSC passes globally.
- [ ] M3 on the five-mode complex-phase OT web (`p2` grown, `Z/4` donor phases): requires extending the web contract from real `u(−m) = u(m)` to Hermitian `u(−m) = conj u(m)`; not registered.

### RSC-O frontier after PR #63 (2026-09-13)

- [x] `PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01` (`paper/NS_P2_RSC_O_ONE_SIDED_SILENT_LAYER.md`, checker `reproduction/checks/check_ns_p2_rsc_o_one_sided_silent_layer.py`, not yet in Toledo): under one-sided `O_+` persistence every recruit has `q_j ∈ a_+^⊥`, `[b_j] = [a_+]` (ALT-1, PR #63), hence `b_i·q_j = b_j·q_i = 0` and `B_{q_i,q_j}(b_i,b_j) = 0` for all `i, j` — the recruit layer is a 2D3C-like passive layer with respect to internal recruit–recruit interactions only (not a full 2D3C branch; layer/core interactions unconstrained). Reduction: all persistent productivity must cross the layer/core interface. Exact symbolic PASS + two rational fixtures + off-line control. RSC-O branch B is reduced, not closed.
- [ ] Next target box (OPEN): passive `O_+` layer + active `O_-` core ⇒ double-O ∨ E ∨ C ∨ novelty/exit, for a compact productive full-convolution-closed zero-novelty one-sided history.
- [ ] RSC-O branch C: parallel anchor/recruit degeneracy (`p × q = 0`) — classify as scale-ray / rank / terminal structure; OPEN.

Audit of the single-target candidate `NS-P2-UNIFORM-FULLCONV-SCALE-LOSS` (`T_j ≤ (1−δ)νD_j + Cρ^j`),
`paper/NS_P2_UNIFORM_SCALE_LOSS_AUDIT.md`:

- [x] Recurrence identity `R_{j+1} ≤ κR_j + C_η R^sh_{j+1}` DERIVED; content = shell-own critical ratio geometric.
- [x] Universal-constant form REFUTED (exact triad witness `T/D = 20` at the datum; `n⁶` excess and 2.5-D fillers are analytic `Dr` scalings; windowed numbers are on the 3-mode Galerkin truncation only).
- [x] Solution-dependent form REGULARITY-EQUIVALENT / HOLD per FINAL-EQUIV §8.
- [x] Budget ratio `∫T_j/∫D_j = 1 + 1/(2ν)` DERIVED: accounting in the P2C-3 critical budget cannot give `δ > 0`.
- [ ] Only residue: constructive generator of `R^sh_j ≤ Bρ^j` from finite records (= `NS-P2B-SCALE-CONTRACTION-UNIFORM`).

### P2 anti-shortcut rules

Do not substitute any of the following for the open theorem:

```text
larger fixed N
longer finite integration
L2 tail for H3 tail
fixed-N solver failure
adjacent compatibility
energy accounting alone
window balance alone
single-triad decoherence
single-triad real-coordinate sign frustration
another regularity criterion with no new constructive mechanism
```

A candidate is REFUTED only by a matching counterexample/impossibility proof.

## P3 — P vs NP load-bearing bridge

Primary home: `morrocwi/information-discrete-math`, branch `research/p-vs-np-readout`, PR #117.

**Entry gate:** clear the P0 branch-sync/formal-CI blockers before promoting new P3 formal claims.

### PNP-FUB-A1

- [ ] Synchronize `research/p-vs-np-readout` with current IDM `main` without losing the research lane.
- [ ] Repair `wrong_root_forces_positive_defect` under Coq 8.20 and restore focused formal CI.
- [ ] Repair the no-`Admitted` lexical guard false-positive on ordinary English `admit` in comments.
- [ ] Construct or refute an unrestricted efficient defect/hitting-support theorem.
- [ ] Require inverse-polynomial capture probability.
- [ ] Audit for hidden SAT oracle.
- [ ] Audit for hidden equivalence oracle.
- [ ] Audit for MCSP-like hardness.
- [ ] Audit for exponential enumeration disguised as support generation.
- [x] Record the generic negative control: defect existence alone does not imply efficient capture in an unstructured black-box family.
- [ ] Keep tiny-circuit enumeration as calibration/negative control only, not the main frontier.
- [ ] Preserve the explicit transfer:

```text
verified unrestricted defect capture
  -> SAT notin P/poly
  -> P != NP.
```

## P4 — Non-vacuity / hidden-target audit

For every target-bearing implication `A -> Target`:

- [x] Require the question whether proving `A` is genuinely more structured than proving `Target` directly.
- [x] Record `NS-P2-FINAL-EQUIV` as an equivalence theorem.
- [x] Correct the stopping rule: equivalence alone does not refute or prohibit a constructive attack on `A`.
- [ ] Identify any hidden regularity oracle or equivalent premise inside each proposed constructor.
- [ ] Continue registering matching counterexamples and status/provenance changes in Toledo.

## P5 — Formal verification / adversarial testing

- [x] No `Admitted` in promoted P1 safe finite kernels and audited formal negative controls.
- [x] Run `Print Assumptions` for promoted P1/P2 audited Coq theorems.
- [x] Add counterexample tests for naive generic bridge forms.
- [x] Add exact finite controls for NS A1V, validated tubes, residual localization, certificate completeness, H3-tail no-go, fixed-N extensibility, geometric-tail lifting, H3 margin, P2B criticality, scale contraction and final equivalence algebra.
- [x] Add exact triad phase stress, coherence-defect, N=1 sign-frustration, finite frustration-tax, all-n ladder and dyadic high-high motif controls.
- [ ] Add exact overlapping-complex-triad phase-holonomy controls.
- [ ] Formalize stable finite holonomy/frustration-or-cut lemmas after statement stabilization.
- [x] Keep finite diagnostic claims separate from formal theorem status.
- [x] Keep CI status attached to exact commit SHA.

## P6 — Yang--Mills adapter

Start only after the shared kernel has at least one stable formal layer.

- [ ] Define finite regulated object/lattice state.
- [ ] Declare gauge symmetry and quotient target.
- [ ] Define refinement/comparison maps.
- [ ] Define finite observables/certificates.
- [ ] Define a finite spectral-gap certificate candidate.
- [ ] Identify the required uniform lower-gap statement.
- [ ] Identify the separate continuum existence/limit bridge.
- [ ] Search for failure modes showing the NS analogy is insufficient.

Status: candidate third direct lane, not yet a proof route.

## P7 — RH / BSD / Hodge probes

Use these as stress tests of the shared core, not equal-priority direct attacks yet.

### RH
- [ ] Search for an `off-critical zero -> finite obstruction` formulation.
- [ ] Reject mere finite-height verification as a global bridge.

### BSD
- [ ] Specify arithmetic and analytic readouts precisely.
- [ ] Search for a generic invariant-bridge theorem, not curve-by-curve agreement.

### Hodge
- [ ] Specify finite positive witness verification.
- [ ] Search for a genuine finite obstruction to nonrepresentability.
- [ ] Record `NO VALID ADAPTER` if no mathematically meaningful transfer exists.

## P8 — Toledo integration

- [x] Keep research proposal identifiers non-canonical until source statements stabilize.
- [ ] Pin final repo/merge commit/path for PR #48 results after merge.
- [x] Preserve previous P1/P2 exact tier/status provenance.
- [ ] Add the reopened P2 triad findings to Toledo after NS merge, including the methodological correction that equivalence is not refutation.
- [ ] Add valid parent/relation structure.
- [ ] Map new Coq/Rocq identifiers only from actual formal evidence after canonical audit.
- [ ] Run normal Toledo build/checkers; do not hand-edit generated registry outputs.

Tracked by: `morrocwi/toledo#11`.

## Tasks that are deliberately lower priority

Do not spend a full session primarily on these unless tied to a specific open bridge:

- increasing NS cutoff only for a larger number;
- adding more fixed-N validated integration steps;
- retrying the held High--High preprint without a repaired proof;
- more tiny-circuit enumeration;
- more RH zeros at finite height;
- more elliptic-curve examples;
- larger Yang--Mills simulations;
- runtime optimization with no theorem consequence;
- interpretation prose with no source/theorem change.

## Definition of meaningful progress

A session is high-value if it does at least one of the following:

1. proves a reusable finite theorem;
2. finds a matching counterexample that kills an invalid bridge;
3. narrows an OPEN statement to a precise load-bearing lemma;
4. formalizes a safe reusable kernel;
5. produces a domain adapter with explicit hypotheses;
6. proves a genuine overlapping-triad phase-holonomy/frustration-or-cut result;
7. closes a provenance/status ambiguity in Toledo.

The preferred current NS target is the smallest statement carrying the most downstream dependencies:

```text
overlapping complex triad phase incidence
  -> quantitative frustration-or-cut ?
```
