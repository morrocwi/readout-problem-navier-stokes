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

P0 audit phase status: **CLOSED as an audit**, with the blockers above explicitly carried into later phases. No Clay theorem was promoted by P0.

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
- IDM PR #127 / issue #126: negative controls refute naive FUB-03/04/05 forms while strengthened forms remain OPEN.

## P2 — Navier--Stokes load-bearing bridge

Primary home: this repository.

### FINAL phase ruling

```text
P2 = CLOSED AS A RESEARCH / REDUCTION PHASE
P2B finite-observation route = CLOSED AS REGULARITY-EQUIVALENT
NS-P2-H3-MARGIN-UNIFORM = RETIRED as an active separate bridge target
NS-P2B-SCALE-CONTRACTION-UNIFORM = REGULARITY-EQUIVALENT existentially
Clay Navier--Stokes global regularity = OPEN
```

Final closure theorem: `paper/NS_P2_FINAL_CLOSURE_EQUIVALENCE.md` (`NS-P2-FINAL-EQUIV`).  
P2B source merge: `9d6f516734d1a151bae987a8df33c05273bcd32b`.

### What P2 established before closure

- [x] `A1E`: finite-time singularity forces arbitrarily large finite-Galerkin `H^3` exceedances under explicitly declared continuation/Galerkin adapters.
- [x] `A1V`: exact finite rational PASS/HOLD verification of a certified finite Galerkin `H^3` exceedance.
- [x] Fixed-`N` validated trajectory/tube and rational certificate machinery.
- [x] Energy/`L2`-only omitted-tail control REFUTED as an `H^3` tail mechanism.
- [x] Fixed-`N` certificate breakdown REFUTED as a standalone singularity witness.
- [x] Positive-lag Stokes and old-Duhamel histories receive explicit all-scale `H^3` tail envelopes.
- [x] Finite shellwise High--High / full `H^3` margin interfaces implemented fail-closed.
- [x] External High--High preprint audited and held rather than promoted.
- [x] P2B: EPSC finite-tape error -> finite modal time-window observation lift (`NS-P2B-EPSC-OBS-LIFT`).
- [x] P2B: strict subcritical finite-observation scaling -> published finite-observation regularity gate (`NS-P2B-SUBCRITICAL-OBS`).
- [x] P2B: energy+dissipation-only strict exponent gain REFUTED by exact critical-spike accounting.
- [x] P2B: integrated shell window balance + total transfer conservation alone REFUTED as a source of strict contraction.
- [x] P2B: strict cross-scale recurrence -> eventual gate PASS (`NS-P2B-SCALE-CONTRACTION`).
- [x] Final non-vacuity audit: existential strict scale contraction is equivalent to regularity on `[0,T]` in the declared modal/dyadic adapter (`NS-P2-FINAL-EQUIV`).

### Final equivalence

For dyadic modal scales define

```text
R_j = (K_{N_j}^2)^(2p/(p-2)) / Lambda_j.
```

Let `SC(T)` assert finite nonnegative upper bounds `U_j` and constants `kappa,rho<1`, `B<infinity` satisfying

```text
R_j <= U_j
U_{j+1} <= kappa U_j + B rho^j
```

for all sufficiently large `j`.

Then, under the declared periodic modal finite-observation adapter,

```text
regularity on [0,T]  <=>  SC(T).
```

- Regularity gives a cutoff-independent `H1` bound, hence `R_j <= C_T/Lambda_j`; dyadic `Lambda_{j+1}=4 Lambda_j` gives the explicit contraction `U_{j+1}=(1/4)U_j`.
- `SC(T)` gives `R_j -> 0`; normalized fixed initial/forcing terms also vanish with scale, so a finite modal observation level satisfies the published regularity gate.

Therefore the last P2B residual is not a lower-strength intermediate theorem. An **effective finite constructor** for `SC(T)` from genuinely weaker information would be new regularity-level mathematics and must be treated as a future direct attack, not as unfinished P2 bookkeeping.

### Anti-reopening rule

P2 is complete as a research phase. Do **not** reopen it by renaming regularity as another known necessary-and-sufficient criterion. A future NS attack must first show a genuinely weaker, independently checkable premise or new structural theorem. Otherwise mark it `REGULARITY-EQUIVALENT / HOLD`.

Tracked issues #25 and #46 should be closed with the explicit note that the phase closed by reduction/equivalence, **not** by solving Clay.

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

For every Clay-bearing implication `A -> Target`:

- [x] Require the question whether proving `A` is genuinely more structured than proving `Target` directly.
- [x] P2 final audit: existential finite-observation scale contraction is regularity-equivalent; retire it as a separate bridge.
- [ ] Identify any imported theorem equivalent in strength to the desired conclusion for each remaining domain candidate.
- [x] Mark HOLD when a premise merely renames the Clay bottleneck.
- [ ] Continue registering counterexamples or vacuity findings in Toledo.

## P5 — Formal verification / adversarial testing

- [x] No `Admitted` in the promoted P1 safe finite kernels and audited formal negative controls.
- [x] Run `Print Assumptions` for the P1/P2 audited Coq theorems.
- [x] Add counterexample tests for naive generic bridge forms.
- [x] Add exact finite controls for NS A1V, validated tubes, residual localization, certificate completeness, H3-tail no-go, fixed-N extensibility, geometric-tail lifting, H3 margin, P2B criticality, scale contraction, and final equivalence algebra.
- [ ] Add further symmetry aliases and representation-redundancy tests as domain adapters mature.
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

Status: candidate third direct lane, not yet a Clay proof route.

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

- [x] Keep `PROP-FUB-01..06`, `NS-FUB-A1/A2`, `PNP-FUB-A1` and research sub-identifiers non-canonical until source statements stabilize.
- [ ] Pin final repo/commit/path for each stabilized proposal before canonicalization.
- [x] Attach P1/P2 exact tier/status evidence through Toledo provenance notes/issues.
- [ ] Add valid parent/relation structure.
- [ ] Map new Coq/Rocq identifiers only from actual formal evidence after canonical audit.
- [ ] Run normal Toledo build/checkers; do not hand-edit generated registry outputs.

Tracked by: `morrocwi/toledo#11`.

## Tasks that are deliberately lower priority

Do not spend a full session primarily on these unless tied to a specific open bridge:

- increasing NS cutoff only for a larger number;
- adding more fixed-N validated integration steps;
- retrying the held High--High preprint without a repaired continuum proof;
- reopening P2 through another regularity-equivalent criterion;
- more tiny-circuit enumeration;
- more RH zeros at finite height;
- more elliptic-curve examples;
- larger Yang--Mills simulations;
- runtime optimization with no theorem consequence;
- interpretation prose with no source/theorem change.

## Definition of meaningful progress

A session is high-value if it does at least one of the following:

1. proves a reusable finite theorem;
2. finds a counterexample that kills an invalid bridge;
3. narrows an OPEN statement to a precise load-bearing lemma;
4. formalizes a safe reusable kernel;
5. produces a domain adapter with explicit hypotheses;
6. closes a provenance/status ambiguity in Toledo.

The preferred next target is always the smallest statement carrying the most downstream dependencies.
