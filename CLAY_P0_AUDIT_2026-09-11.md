# Clay P0 Audit — 2026-09-11

**Status:** frozen research-status snapshot for the shared Clay programme  
**Purpose:** complete P0 before new theorem work by auditing current repository heads, open bridges, CI/formal evidence, known refutations, and process blockers.  
**Claim effect:** status/provenance audit only; no Clay theorem is promoted by this document.

> P0 asks what is actually established at the audited Git state. It does not infer a global theorem from finite evidence, and it does not treat a failed proof script as a mathematical refutation unless the underlying statement is disproved.

---

## 1. Audited Git state

| Repository / lane | Audited ref | Audited SHA | State |
|---|---|---|---|
| `morrocwi/readout-problem-navier-stokes` | `main` | `0afa328d2f477283b00ead20371aafad4fd20f12` | shared programme + NS evidence source |
| `morrocwi/information-discrete-math` | `main` | `cda45522bfec909ac8bed50656a0353d7fd24928` | generic/shared-kernel source |
| `morrocwi/information-discrete-math` | `research/p-vs-np-readout` | `2e5466c6c3f3e403c4b84e65ffa6fb7174efbd1b` | P-vs-NP research head / PR #117 |
| `morrocwi/toledo` | `main` | `b223bd424aea32861714f4a874873489d74c0e4d` | theorem/provenance/status ledger |

The P-vs-NP branch is currently **diverged** from IDM `main`: 181 commits ahead and 27 commits behind, with merge base `69b0f3c079eb62c4633b02e021f7342a5520341b`. Claim-sensitive P-vs-NP work should first synchronize current `main` so the current shared-kernel/governance state is not bypassed.

---

## 2. Status vocabulary used in this audit

- **PASS** — executable finite verification passed for the declared artifact at the audited commit.
- **DERIVED** — mathematical consequence from explicitly declared assumptions.
- **OPEN** — the required theorem is not proved.
- **HOLD** — evidence/formal verification/process state is presently insufficient to promote the claim.
- **REFUTED** — a stated proposition has an explicit counterexample or contradiction under its declared formulation.

`HOLD` is not the same as `REFUTED`.

---

## 3. Shared finite-obstruction / uniform-bridge core

Primary source: `morrocwi/information-discrete-math/docs/UNIVERSAL_FINITE_OBSTRUCTION_UNIFORM_BRIDGE_KERNEL.md`.

| Item | P0 ruling |
|---|---|
| `PROP-FUB-01` finite certificate schema | **Definition / programme specification** |
| `PROP-FUB-02` robust certified margin gate | **Generic target; finite/domain instances exist** |
| `PROP-FUB-03` global failure -> finite witness | **OPEN** |
| `PROP-FUB-04` constructive uniform capture | **OPEN** |
| `PROP-FUB-05` cross-resolution compatibility / extension | **OPEN generic schema** |
| `PROP-FUB-06` non-vacuity / hidden-target audit | **Definition / mandatory gate** |
| IDM issue #124 safe-core formalization | **OPEN; work not yet closed** |

P0 conclusion: the shared core is a valid research specification and dependency architecture. It is **not yet a generic theorem that converts all finite certificates into a Clay conclusion**.

---

## 4. Navier--Stokes lane

Primary claim boundary: `CLAIMS.md`.

### Established/supporting finite and derived results

The current repository records, among other items:

- exact finite energy-observability rank/saturation certificates at selected fixed cutoffs;
- a certified full `N=1` translation-transverse 49-dimensional local inverse chain;
- exact characteristic-zero preconditioning and componentwise nonlinear enclosure;
- fixed-`N=1` state-space radius with reproduced bracket `10^-28 < r <= 10^-27`;
- finite direct-sample and finite-tape comparison constructions;
- analytic omitted-tail / relative-energy adapters under their declared hypotheses;
- conditional retained-plus-tail composition `sqrt(rho_N^2 + beta_N^2)`.

These are supporting mathematics. They do not close global regularity.

### Important OPEN frontiers already declared by the repository

- `PROP-NSOBS-07` — all-resolution earliest-order saturation;
- `PROP-EPSC-16` — scalable/tight outer comparison-path certification;
- `PROP-EPSC-24` — practical local/entrywise branch-stable measurement radius;
- `PROP-EPSC-19` — full noisy measurement-to-continuum propagation;
- arbitrary-`N` retained inverse beyond the certified fixed-cutoff cases;
- `NS-FUB-A1` — finite-time singularity implies a finite PDE-relevant certified failure;
- `NS-FUB-A2` — uniform exclusion of the admissible finite failures implies no finite-time singularity.

### Known NS-side refutations / guards

The following shortcuts are already ruled out by current claim boundaries:

- fixed-`N` inversion **does not imply** arbitrary-`N` inversion;
- finite nested agreement / boundary energy **does not imply** complete omitted-tail control;
- raw Galerkin values **cannot be silently identified** with continuum projections;
- shell-energy rank saturation is local quotient information, **not global injectivity**;
- reader/conditioning failure alone is **not automatically a PDE singularity witness**.

### P0 ruling

- finite/derived NS evidence: **usable supporting base**;
- exact Clay bridge: **OPEN**;
- Clay Navier--Stokes conclusion: **OPEN**.

The active NS load-bearing issue remains #25 (`NS-FUB-A1`).

---

## 5. P vs NP lane — audited PR #117

Research branch head: `2e5466c6c3f3e403c4b84e65ffa6fb7174efbd1b`.

### 5.1 Finite executable evidence

Focused workflow `p-vs-np-readout`, run `34560588733`:

- job `finite-fixtures`: **SUCCESS**;
- the recorded fixture/negative-control sequence completed through the AC0 baseline, including SAT restriction-defect, compressed negative closure, adaptive defect capture, robust margin, finite hitting-support probes, tiny genuine circuit calibration, clause-essentiality refuter, CEGIS baseline, and other declared finite checks.

P0 classification: **PASS for the focused finite fixture job at this exact head**.

This does not establish `PNP-FUB-A1`.

### 5.2 Actual formal failure at current head

The same workflow has `coq-intervention`: **FAILURE**.

Coq 8.20 reports in:

`formal/IDM_SATRestrictionDefect.v`, line 115

```text
Error: No such contradiction
```

inside the current proof of `wrong_root_forces_positive_defect`.

This is a real formal proof-script failure at the audited commit. It means the present branch cannot be described as lane-wide Coq-green. It is **not by itself a counterexample to the mathematical statement**.

### 5.3 Separate verifier lexical-guard failure

General `verify` run `34560588489` also concludes **FAILURE**. Its compute and install jobs pass, while the Coq job fails.

The no-`Admitted` scanner additionally matches the ordinary English word `admit` inside comments in:

- `formal/IDM_BackdoorSupportBudget.v` — comment says arbitrary SAT instances/circuits do not automatically *admit* logarithmic backdoors;
- `formal/IDM_OuterHittingSeparation.v` — comment says exact candidates never *admit* a verified defect.

Those two matches are a **verification-script lexical false positive / guard defect**, not evidence of hidden Coq `Admitted` in those comments. They must be repaired separately from the actual Coq proof-script failure above.

### 5.4 P-vs-NP mathematical frontier

The load-bearing statement remains:

```text
PNP-FUB-A1:
for every polynomial size bound p,
find an input length n such that every circuit C with |C| <= p(n)
has an efficiently constructible/samplable locally verifiable SAT defect
with inverse-polynomial capture probability,
without SAT/equivalence/MCSP/hidden exponential enumeration.
```

ADC form:

`1 - q_C >= 1/poly(n)`.

P0 ruling:

- focused finite executable evidence: **PASS**;
- lane-wide formal/Coq evidence: **HOLD** until CI is repaired and green;
- `PNP-FUB-A1`: **OPEN**;
- `SAT notin P/poly`: **OPEN from this programme**;
- `P != NP`: **OPEN**.

The previous PR-body wording that the newest CI was merely “pending” is stale; the audited focused runs have completed and failed for the reasons above. A P0 comment recording this was added to PR #117.

---

## 6. Toledo / provenance lane

Primary source: `morrocwi/toledo/docs/CLAY_BRIDGE_PROGRAM_2026-09-11.md`.

P0 confirms:

- `PROP-FUB-01..06`, `NS-FUB-A1/A2`, and `PNP-FUB-A1` remain **proposal identifiers**, not canonical Toledo codes;
- Toledo issue #11 remains **OPEN**;
- `PROP-FUB-03/04/05`, `NS-FUB-A1/A2`, and `PNP-FUB-A1` remain **OPEN**;
- no canonical registry promotion is justified by this P0 audit;
- P-vs-NP formal evidence should be recorded as **HOLD at the audited branch head**, while the unrestricted mathematical premise remains **OPEN**.

A P0 provenance/status comment was added to Toledo issue #11.

---

## 7. Governance / process audit

The repositories NS, IDM, and Toledo now contain the `clay-governance` PR workflow and fail-closed acknowledgement mechanism.

However, GitHub branch metadata at the audited state reports `main` as:

```text
protected: false
required status checks: enforcement off
```

for all three repositories.

Therefore:

- the governance workflow exists and can audit PRs;
- the repository process instructs agents to use PRs for Clay-sensitive work;
- but GitHub itself does **not yet hard-enforce** the check against a direct push to `main`.

P0 process classification: **HOLD until branch protection/ruleset makes `clay-governance` a required check**. This is a process/governance gap, not a mathematical claim failure.

---

## 8. P0 CLOSED / OPEN / HOLD / REFUTED matrix

| Research object | P0 status | Why |
|---|---|---|
| P0 source/HEAD audit itself | **CLOSED by this snapshot** | heads, claim ledgers, issues, PR and CI audited |
| NS selected fixed-cutoff exact certificates | **PASS where `CLAIMS.md` says PASS** | exact finite evidence |
| NS arbitrary-`N` inversion / all-resolution observability | **OPEN** | no all-`N` theorem |
| NS-FUB-A1 | **OPEN** | singularity -> finite PDE witness not proved |
| NS-FUB-A2 | **OPEN** | all-finite exclusion -> Clay regularity bridge not proved |
| PNP focused finite fixtures at `2e5466...` | **PASS** | finite-fixtures job green |
| PNP branch lane-wide formal verification | **HOLD** | Coq proof failure + verifier lexical guard defect |
| PNP-FUB-A1 | **OPEN** | unrestricted constructive capture theorem missing |
| `P != NP` | **OPEN** | load-bearing quantified premise missing |
| PROP-FUB-03/04/05 | **OPEN** | generic witness/capture/compatibility theorems not closed |
| Toledo canonicalization of FUB proposals | **OPEN** | issue #11; source statements/evidence must stabilize |
| Hard GitHub enforcement of Clay governance | **HOLD** | main branches unprotected / checks not required |
| “fixed finite success implies Clay theorem” shortcut | **REFUTED AS AN INFERENCE RULE** | programme explicitly separates finite uniformity and global bridge |

---

## 9. P0 exit decision

P0 is considered complete as an **audit phase** once this snapshot, TODO update, governance acknowledgement, and review PR exist.

It does **not** mean every CI lane is green. Instead it identifies the exact blockers that P1/P2/P3 must respect.

### Next work order after P0

1. **P1 — Shared safe core:** begin IDM issue #124 formalization on a current-main branch; prove only finite safe lemmas and stress-test against NS + PNP adapters.
2. **PNP formal hygiene blocker before P3:** synchronize PR #117 with current IDM `main`, repair `IDM_SATRestrictionDefect.v` under Coq 8.20, repair the lexical no-Admitted guard, and require a green formal rerun before promoting formal evidence.
3. **P2 — NS bridge:** continue `NS-FUB-A1` falsification/theorem-isolation work without waiting for PNP's unrestricted capture theorem; do not substitute larger fixed-N runs for the bridge.
4. **Process hardening:** require `clay-governance` in branch protection/rulesets for NS, IDM, Toledo when repository settings are available.
5. **P3 — P vs NP:** attack `PNP-FUB-A1` only after the branch is synchronized and the formal baseline is green.

---

## 10. Clay status after P0

```text
Navier--Stokes             OPEN
P vs NP                    OPEN
Yang--Mills + Mass Gap     exploratory candidate lane
Riemann Hypothesis         probe / no valid global adapter yet
Birch--Swinnerton--Dyer    probe / no valid global adapter yet
Hodge Conjecture           probe / no valid global adapter yet
```

The strongest immediate programme assets are finite certificates, exact/fail-closed verification discipline, explicit open-bridge isolation, and a shared dependency architecture. The load-bearing global implications remain to be proved.
