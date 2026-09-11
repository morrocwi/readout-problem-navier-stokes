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
- IDM PR #127 / issue #126: P2 negative controls refute naive FUB-03/04/05 forms while strengthened forms remain OPEN.

## P2 — Navier--Stokes load-bearing bridge

Primary home: this repository.

### NS-FUB-A1

- [x] State a precise regularity-sensitive theorem decomposition in `paper/NS_FUB_A1_H3_FINITE_WITNESS.md`:

```text
A1E: finite-time singularity
     -> for every finite B, some finite Galerkin cutoff N and rational q<T* satisfy ||u_N(q)||_H3 > B
     [DERIVED under explicitly declared continuation + compact-interval Galerkin adapters]

A1V: certified rational interval enclosure of a finite Galerkin state
     -> exact finite PASS/HOLD verification of ||u_N(q)||_H3 > B
     [finite exact checker; CI PASS]

A1C: finite-time singularity
     -> constructible validated A1V certificate
     [general Clay-facing form OPEN]
```

#### A1C finite certificate layer already closed in restricted settings

- [x] `A1C-V/RV`: exact fixed-`N=1` absolute and residual-centered validated Galerkin tubes; residual localization passes exact CI.
- [x] `A1C-CV/G1`: finite tube-chain verification and pinned finite-step construction pass exact CI.
- [x] `A1C-COMP-Q`: for a fixed finite rational polynomial/Galerkin ODE with rational data and a strict finite observable margin, a finite rational residual certificate exists.
- [x] `A1C-ENUM-Q`: finite rational certificates are enumerable and exactly decidable, so exhaustive dovetailing eventually finds a certificate when the strict fixed-finite witness is true; **no useful runtime bound is claimed**.
- [x] `A1C-XQ`: restricted rational-finite-data singularity-to-certificate consequence DERIVED under the A1E adapters.
- [ ] General `A1C-X`: bridge arbitrary smooth/continuum initial data to constructive finite rational enclosures, arbitrary cutoffs, and the all-scale statement. This remains OPEN.

Evidence: NS PRs #29, #30, #32 and #33; latest completeness merge `df022097ea899bacb917238be7a69b40c15e2107`.

#### Candidate finite failure classes

- [x] Cross-resolution compatibility: **adjacent/local or L2 compatibility alone rejected as insufficient**; any useful form needs all-refinement Cauchy/tail control and regularity relevance.
- [x] Failure of a uniform regularity-sensitive bound: `H^3` finite Galerkin exceedance isolated as the A1E witness class.
- [ ] Finite scale-extension/tail suppression:
  - [x] **energy/L2-only tail smallness REFUTED** as an H3 tail mechanism. `paper/NS_FUB_A1_H3_TAIL_NO_GO.md` gives a one-mode divergence-free counterexample: for every `N`, `epsilon>0`, and finite `B`, an omitted tail can have `L2<=epsilon` but `H3>B`.
  - [x] finite-band L2-to-H3 bounds identified as insufficient for the all-scale bridge because the constant grows with the outer cutoff.
  - [ ] find a non-vacuous frequency-weighted / PDE-derived smoothing or decay mechanism that yields a summable/all-refinement H3-relevant tail envelope without assuming global regularity.
- [ ] Regularity-relevant energy-transfer concentration/growth: still requires a theorem showing why the chosen observable is forced by singularity and is not merely correlated with high-frequency activity.
- [ ] Certificate recursion/extensibility failure:
  - fixed-N verifier/generator failures alone are **not** accepted as PDE failure; a complete certificate class exists in the fixed rational finite setting.
  - [ ] determine whether any *uniform across N* certificate deterioration can be linked to regularity rather than algorithmic conditioning/resource growth.
- [x] Conditioning loss alone rejected as a singularity witness unless a separate PDE-regularity implication is proved.

#### Current P2 load-bearing frontier

- [x] Construct counterexamples to weak local/adjacent compatibility.
- [x] Construct counterexample to energy/L2-only H3 tail suppression (issue #34 / PR #37).
- [x] Reject premises that simply assume smoothness or an equivalent Clay criterion without new finite leverage.
- [ ] Extend the initial-data adapter from rational finite data to the actual admissible smooth/continuum data class with explicit certified projection/tail representation.
- [ ] Find a PDE-derived all-scale frequency-weighted tail mechanism that survives the non-vacuity audit.
- [ ] Formulate and test the strongest useful uniform extension theorem only after the required tail quantity is explicit.

Tracked by: `morrocwi/readout-problem-navier-stokes#25`, #31 and #34.

### NS-FUB-A2

- [ ] After the admissible all-scale tail mechanism stabilizes, formulate the converse exclusion theorem:

```text
uniform exclusion of every admissible finite regularity failure
+ certified all-scale tail/compatibility control
  -> no finite-time singularity.
```

- [x] Separate finite uniformity from the continuum/global semantic bridge.
- [ ] Audit the template `uniform all-N H3 bound -> strong solution` for non-vacuity: the implication may be classical while proving the antecedent remains the Clay-strength difficulty.
- [ ] Avoid treating a stronger uniform `H^{3+sigma}` bound as progress unless a new mechanism proves it; it is a mathematically sufficient tail repair but may simply strengthen the target premise.

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
- [x] Record the generic P2 negative control: defect existence alone does not imply efficient capture in an unstructured black-box family.
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

- [x] No `Admitted` in the promoted P1 safe finite kernels and P2 formal negative controls.
- [x] Run `Print Assumptions` for the P1/P2 audited Coq theorems.
- [x] Add counterexample tests for naive generic bridge forms.
- [x] Add exact finite controls for NS A1V, validated tubes, residual localization, certificate completeness, and energy-only H3-tail no-go.
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
- adding more fixed-N validated integration steps after the certificate-completeness result;
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
