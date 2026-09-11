# Clay Program — READ FIRST

**Status:** mandatory orientation map for AI/research agents  
**Date:** 2026-09-11  
**Purpose:** prevent context drift, duplicated work, source confusion, and accidental promotion of OPEN claims.

> Any AI working on the Clay program should read this file before proposing, proving, coding, benchmarking, reviewing, or editing research claims.

## 1. Program invariant

The program is **one shared finite-certificate / uniform-bridge core with multiple domain adapters**, not six unrelated projects.

```text
finite/local object
  -> finite law / defect
  -> independently checkable certificate
  -> uniform theorem over the admissible finite family
  -> explicit domain bridge
  -> global / Clay statement
```

Never collapse these stages.

## 2. Mandatory source order

Read in this order unless a task is explicitly narrower.

### A. Shared program map — start here

1. This file: `CLAY_READ_FIRST.md`
2. `CLAY_MULTI_PROBLEM_FINITE_BRIDGE_PROGRAM.md`
3. `CLAY_RESEARCH_TODO.md`

### B. Navier--Stokes source of truth

4. `README.md`
5. `CLAIMS.md`
6. `paper/`
7. `reproduction/`
8. `verification/`

Rule: `CLAIMS.md` controls claim boundaries. Fixed-N evidence, numerical saturation, local inversion, or finite reconstruction is not automatically all-N or continuum regularity.

### C. Shared finite mathematics / P vs NP

Repository: `morrocwi/information-discrete-math`

Read:

1. `AGENTS.md`
2. `docs/UNIVERSAL_FINITE_OBSTRUCTION_UNIFORM_BRIDGE_KERNEL.md`
3. `docs/DISCRETE_EPSILON_COMPLETION.md`
4. `docs/FINITE_DIRECT_SAMPLE_BRANCH.md`
5. P-vs-NP branch `research/p-vs-np-readout`
6. PR #117 — barrier-aware computational readout lane for P vs NP

Rule: PR #117 does **not** prove `P != NP`. Its load-bearing unrestricted constructive defect-capture premise remains OPEN.

### D. Toledo theorem/provenance ledger

Repository: `morrocwi/toledo`

Read:

1. `AGENTS.md` when present
2. `docs/CLAY_BRIDGE_PROGRAM_2026-09-11.md`
3. `docs/NS_OBSERVABILITY_TO_EPSC_BRIDGE.md`
4. `registry/SCHEMA.md`
5. `docs/EQ_CODE_SCHEME.md`

Rule: proposal identifiers such as `PROP-FUB-*`, `NS-FUB-*`, and `PNP-FUB-*` are **not canonical Toledo codes** until canonical audit is completed.

### E. Readout Genesis

Repository: `morrocwi/readout_genesis`

Use it for interpretation/application structure only. It is **not** proof evidence unless a statement is independently backed by a theorem/certificate source.

### F. Optional supporting repositories

Use only when directly relevant:

- `morrocwi/zero-readout-certifies` — machine-checked finite distinction/kernel results.
- `morrocwi/retained-sturm` — spectral/inertia/readout machinery.
- `morrocwi/readout_universe` — wider readout architecture.

## 3. Active direct Clay lanes

### Navier--Stokes

Primary open bridge target:

```text
NS-FUB-A1:
FiniteTimeSingularity
  -> exists finite certified PDE-relevant failure.
```

Then:

```text
NS-FUB-A2:
all admissible finite failures excluded uniformly
  -> no finite-time singularity.
```

GitHub issue: `morrocwi/readout-problem-navier-stokes#25`.

### P vs NP

Primary open bridge target:

```text
PNP-FUB-A1:
for every polynomial size bound p,
there exists n such that every circuit C with |C| <= p(n)
has an efficiently constructible locally verifiable SAT defect,
with inverse-polynomial capture probability,
without SAT/equivalence/MCSP/exponential hidden oracle.
```

Primary work item: `morrocwi/information-discrete-math#117`.

## 4. Candidate / exploratory lanes

- **Yang--Mills:** strongest candidate third lane. First build a valid finite lattice/gauge/cross-scale adapter; do not infer a mass gap from finite lattice numerics.
- **Riemann Hypothesis:** supporting probe until an all-height structural bridge or finite obstruction theorem exists.
- **BSD:** supporting probe; arithmetic/analytic readout bridge not yet established.
- **Hodge:** supporting probe; no domain-specific finite obstruction / universal representability bridge yet.

## 5. Mandatory startup checklist for every AI

Before doing substantive work, answer internally:

- [ ] What exact repo/branch/commit/PR contains the current source of truth?
- [ ] What is already CLOSED / OPEN / HOLD / REFUTED?
- [ ] Which theorem or issue does this task advance?
- [ ] Is the result finite, uniform, bridge-level, or Clay-level?
- [ ] Does the proposed premise secretly assume the target conclusion?
- [ ] Is there a formal theorem, exact certificate, finite diagnostic, or only analogy?
- [ ] Could the result be generic enough to move into IDM?
- [ ] Does Toledo need a proposal/status/provenance update?

If these questions cannot be answered, do not create a new Clay claim. First perform an audit.

## 6. Evidence hierarchy

Keep these categories distinct:

- `Th_coqc` / machine-checked theorem
- exact finite computation
- finite diagnostic
- derived analytic theorem under declared assumptions
- OPEN bridge
- HOLD / insufficient evidence
- exploratory analogy

Never upgrade one category into another by prose.

## 7. Anti-drift rule

Before a long calculation or code run, ask:

> **If this succeeds, which missing global implication becomes easier?**

If the answer is none, lower the task priority unless it is a deliberate falsification/negative control.

## 8. Required end-of-session report

Every research session should end with:

```text
SHARED CORE
- theorem/obstruction touched:
- status:

NAVIER--STOKES
- progress:
- open bridge:

P VS NP
- progress:
- open bridge:

OTHER CLAY LANES
- valid transfer only; no forced analogy:

FORMAL / CI
- tests:
- Coq/Rocq:
- assumptions:

TOLEDO
- proposal/status/provenance changes:

GIT
- files/commits/PRs/issues:

NEXT HIGHEST-LEVERAGE TARGET
- one item only:
```

## 9. Core sentence

```text
ONE SHARED CORE — MULTIPLE DOMAIN ADAPTERS — EXPLICIT BRIDGE BEFORE CLAY CLAIM.
```
