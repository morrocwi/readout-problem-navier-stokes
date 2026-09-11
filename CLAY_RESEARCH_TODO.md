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

### Phase ruling

```text
P2 = CLOSED AS A REDUCTION
NS-P2-H3-MARGIN-UNIFORM = OPEN / HOLD frontier
Clay Navier--Stokes global regularity = OPEN
```

Canonical P2 handoff: `paper/NS_P2_FINITE_TO_CONTINUUM_CLOSURE.md`.  
Latest reduction merge: NS PR #42, commit `83e966df251e548fd9574d9553d7f4bf5551877b`.

The phase is closed because the useful finite/continuum architecture has been reduced to one explicit uniform theorem target. It is **not** closed as a Millennium solution.

### P2 layers already closed or ruled out

- [x] `A1E`: finite-time singularity forces arbitrarily large finite-Galerkin `H^3` exceedances under explicitly declared classical continuation + compact-time Galerkin adapters.
- [x] `A1V`: exact finite rational PASS/HOLD verification of a certified finite Galerkin `H^3` exceedance.
- [x] `A1C-V/RV`: exact fixed-`N=1` validated absolute/residual tubes.
- [x] `A1C-CV/G1`: exact finite tube-chain verification.
- [x] `A1C-COMP-Q`: fixed finite rational polynomial/Galerkin strict witness -> finite rational residual certificate.
- [x] `A1C-ENUM-Q`: exhaustive rational certificate semidecision; no useful runtime claimed.
- [x] Adjacent/local or `L2` cross-resolution compatibility rejected as a global bridge.
- [x] Energy/`L2`-only omitted-tail control REFUTED as an `H^3` tail mechanism (issue #34 / PR #37, merge `af97fc84542dc042b3b6c386458fc0afbd797bef`).
- [x] Fixed-`N` certificate/trajectory breakdown REFUTED as a standalone singularity witness (issue #38 / PR #39, merge `72d7672ea1753794e452fd0bb5206dea7be21764`).
- [x] Positive-lag Stokes and old-Duhamel histories receive explicit all-scale `H^3` tail envelopes.
- [x] `NS-P2-HH-GEOM-LIFT`: finite prefix + true geometric High--High defect tail with `64q<1` gives an exact `H^3`-weighted remainder bound.
- [x] Exact finite shellwise absorption and full `H^3` dissipative-margin interfaces implemented fail-closed.
- [x] External High--High absorption preprint independently audited and placed on **HOLD** as a final semantic adapter; it is not a proof premise.

### Main derived reduction

For each finite Galerkin cutoff define

```text
X_N = ||u_N||_H3^2
D_N = nu ||grad Lambda^3 u_N||_2^2
(1/2) X_N' + D_N = P_N
```

If cutoff-independent constants `0 <= theta < 1` and `C_T < infinity` satisfy

```text
P_N(t) <= theta D_N(t) + C_T (1 + X_N(t))
```

for every cutoff and every `t in [0,T]`, then Gronwall gives a uniform all-`N` `H^3` bound. The final continuum layer is then the standard Galerkin/strong-solution continuation semantic adapter.

### Single main residual theorem — `NS-P2-H3-MARGIN-UNIFORM`

- [ ] For every admissible smooth periodic divergence-free unforced datum, every `nu>0`, and every finite `T`, construct from finite/checkable information constants `theta<1` and `C_T<infinity`, independent of cutoff, together with a sound finite/uniform certificate mechanism proving

```text
P_N(t) <= theta D_N(t) + C_T (1 + X_N(t))
```

for all finite `N` and all `t in [0,T]`.

Non-vacuity requirements:

- [ ] `C_T` may not be obtained by assuming the desired uniform `H^3` bound.
- [ ] no equivalent regularity oracle may be hidden in the certificate constructor.
- [ ] finite time cells must have a proved all-time coverage/modulus.
- [ ] finite cutoffs must have a proved uniform/all-`N` rule; a large maximum cutoff is not enough.
- [ ] any shellwise High--High route must separately prove the Low--Low/Low--High closure instead of importing the audited preprint's unresolved step.

**Handoff rule:** do not spend another P2 session on larger fixed cutoffs, more fixed-`N` integration steps, energy-only tails, adjacent compatibility, reader conditioning, or the held external adapter unless new mathematics directly advances `NS-P2-H3-MARGIN-UNIFORM`.

Tracked by master issue #25. Issues #40 and #41 are closed after PR #42; #41 is closed `not_planned` because the external preprint is HOLD as a final adapter.

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
- [ ] Identify any imported theorem equivalent in strength to the desired conclusion for each domain candidate.
- [x] Mark HOLD when a premise merely renames the Clay bottleneck.
- [ ] Continue registering counterexamples or vacuity findings in Toledo.

## P5 — Formal verification / adversarial testing

- [x] No `Admitted` in the promoted P1 safe finite kernels and audited formal negative controls.
- [x] Run `Print Assumptions` for the P1/P2 audited Coq theorems.
- [x] Add counterexample tests for naive generic bridge forms.
- [x] Add exact finite controls for NS A1V, validated tubes, residual localization, certificate completeness, H3-tail no-go, fixed-N extensibility, geometric-tail lifting, and the H3 margin interface.
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
