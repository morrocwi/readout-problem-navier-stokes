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

- [ ] Formalize strict-margin soundness and fail-closed HOLD semantics.
- [ ] Formalize finite error-budget composition.
- [ ] Formalize finite cross-resolution compatibility-budget composition.
- [ ] Formalize quotient/symmetry-respecting certificate transport.
- [ ] Formalize local finite-defect checker soundness under declared laws.
- [ ] Add negative controls showing why tested finite cases do not imply all-finite or global claims.
- [ ] Stress-test each generic statement against both NS and P vs NP adapters.

Tracked by: `morrocwi/information-discrete-math#124`.

## P2 — Navier--Stokes load-bearing bridge

Primary home: this repository.

### NS-FUB-A1

- [ ] State a precise theorem candidate:

```text
FiniteTimeSingularity
  -> exists finite certified PDE-relevant failure.
```

- [ ] Audit candidate witness classes:
  - [ ] cross-resolution incompatibility
  - [ ] failure of a uniform regularity-sensitive bound
  - [ ] failure of extension/tail suppression
  - [ ] regularity-relevant energy-transfer concentration/growth
  - [ ] certificate recursion/extensibility failure
  - [ ] conditioning loss only if PDE relevance is proved
- [ ] Try to construct counterexamples to each candidate witness class.
- [ ] Reject any premise that already assumes smoothness or an equivalent Clay criterion without new finite leverage.

Tracked by: `morrocwi/readout-problem-navier-stokes#25`.

### NS-FUB-A2

- [ ] After A1 stabilizes, formulate the converse exclusion theorem:

```text
uniform exclusion of every admissible finite failure mode
  -> no finite-time singularity.
```

- [ ] Separate finite uniformity from the continuum/global semantic bridge.

## P3 — P vs NP load-bearing bridge

Primary home: `morrocwi/information-discrete-math`, branch `research/p-vs-np-readout`, PR #117.

**Entry gate:** do not promote new P3 formal claims until the P0 branch-sync and formal-CI blockers above are cleared.

### PNP-FUB-A1

- [ ] Construct or refute an unrestricted efficient defect/hitting-support theorem.
- [ ] Require inverse-polynomial capture probability.
- [ ] Audit for hidden SAT oracle.
- [ ] Audit for hidden equivalence oracle.
- [ ] Audit for MCSP-like hardness.
- [ ] Audit for exponential enumeration disguised as support generation.
- [ ] Keep tiny-circuit enumeration as calibration/negative control only, not the main frontier.
- [ ] Preserve the explicit transfer:

```text
verified unrestricted defect capture
  -> SAT notin P/poly
  -> P != NP.
```

## P4 — Non-vacuity / hidden-target audit

For every Clay-bearing implication `A -> Target`:

- [ ] Ask whether proving `A` is genuinely more structured than proving `Target` directly.
- [ ] Identify any imported theorem equivalent in strength to the desired conclusion.
- [ ] Mark HOLD if the premise merely renames the Clay bottleneck.
- [ ] Register counterexamples or vacuity findings in Toledo.

## P5 — Formal verification / adversarial testing

- [ ] No `Admitted` in promoted finite kernels.
- [ ] Run `Print Assumptions` for audited formal theorems.
- [ ] Add counterexample tests for every proposed generic bridge.
- [ ] Add symmetry aliases and representation-redundancy tests.
- [ ] Keep finite diagnostic claims separate from formal theorem status.
- [ ] Keep CI status attached to exact commit SHA.

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

- [ ] Keep `PROP-FUB-01..06`, `NS-FUB-A1/A2`, `PNP-FUB-A1` as non-canonical proposal IDs until source statements stabilize.
- [ ] Pin repo/commit/path for each proposal before canonicalization.
- [ ] Attach exact tier/status evidence.
- [ ] Add valid parent/relation structure.
- [ ] Map Coq/Rocq identifiers only from actual formal evidence.
- [ ] Run normal Toledo build/checkers; do not hand-edit generated registry outputs.

Tracked by: `morrocwi/toledo#11`.

## Tasks that are deliberately lower priority

Do not spend a full session primarily on these unless tied to a specific open bridge:

- increasing NS cutoff only for a larger number;
- more tiny-circuit enumeration;
- more RH zeros at finite height;
- more elliptic-curve examples;
- larger Yang--Mills simulations;
- runtime optimization with no theorem consequence;
- new interpretation prose with no source/theorem change.

## Definition of meaningful progress

A session is high-value if it does at least one of the following:

1. proves a reusable finite theorem;
2. finds a counterexample that kills an invalid bridge;
3. narrows an OPEN statement to a precise load-bearing lemma;
4. formalizes a safe reusable kernel;
5. produces a domain adapter with explicit hypotheses;
6. closes a provenance/status ambiguity in Toledo.

The preferred next target is always the smallest statement carrying the most downstream dependencies.
