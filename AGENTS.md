# Mandatory AI Startup Protocol — Clay Program

Any AI/coding/research agent working in this repository must orient itself before changing claims, code, experiments, or proof architecture.

## Mandatory first read

Read, in order:

1. `CLAY_READ_FIRST.md`
2. `CLAY_MULTI_PROBLEM_FINITE_BRIDGE_PROGRAM.md`
3. `CLAY_RESEARCH_TODO.md`
4. `CLAIMS.md`
5. relevant `README`/paper/reproduction files for the task

If working on P vs NP, also read `morrocwi/information-discrete-math` PR #117 and its branch `research/p-vs-np-readout`.

If working on shared bridge mathematics, read `morrocwi/information-discrete-math/docs/UNIVERSAL_FINITE_OBSTRUCTION_UNIFORM_BRIDGE_KERNEL.md`.

If changing theorem status/provenance, read `morrocwi/toledo/docs/CLAY_BRIDGE_PROGRAM_2026-09-11.md` before editing.

## Non-negotiable rules

- Do not promote fixed-N or finite diagnostic evidence into an all-N or continuum theorem.
- Do not promote existence of a local defect into an unrestricted constructive capture theorem.
- Do not claim one Clay problem reduces to another unless an actual reduction is proved.
- Separate finite theorem, uniform theorem, global bridge, and Clay conclusion.
- Search for counterexamples and hidden-target/vacuity before strengthening a theorem.
- Respect symmetry before uniqueness; quotient when the readout cannot distinguish an orbit.
- A failed analogy across Clay lanes is valid progress and must be recorded honestly.
- Use `PASS`, `DERIVED`, `OPEN`, and `HOLD` consistently with the evidence tier.
- Do not hand-edit generated Toledo registry outputs.

## Current highest-priority research fronts

1. Shared safe-core formalization: `morrocwi/information-discrete-math#124`.
2. Navier--Stokes finite singularity witness bridge: this repo issue #25 (`NS-FUB-A1`).
3. P vs NP unrestricted constructive defect capture: IDM PR #117 (`PNP-FUB-A1`).
4. Toledo canonicalization only after source statements stabilize: `morrocwi/toledo#11`.

Do not replace these with larger computations merely because they are easier to run.

## Before starting substantial work

Answer internally:

```text
What exact open statement am I attacking?
What source establishes its current status?
What evidence tier will my result have?
If successful, which global implication becomes easier?
Could my premise already contain the target theorem?
Where must the result be recorded (IDM / NS / Toledo / Genesis)?
```

If these cannot be answered, audit first.

## Before ending a session

Report:

- theorem/obstruction touched;
- evidence tier and status;
- tests/formal assumptions actually checked;
- Git files/commits/issues/PRs changed;
- Toledo status/provenance update needed or completed;
- one highest-leverage next target.

Core rule:

> **ONE SHARED CORE — MULTIPLE DOMAIN ADAPTERS — EXPLICIT BRIDGE BEFORE CLAY CLAIM.**
