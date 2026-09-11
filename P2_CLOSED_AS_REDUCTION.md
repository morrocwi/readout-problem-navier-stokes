# P2 handoff — Navier--Stokes

**Date:** 2026-09-11  
**Status:** `CLOSED AS A REDUCTION`; Clay Navier--Stokes remains `OPEN`.

Canonical detailed handoff: `paper/NS_P2_FINITE_TO_CONTINUUM_CLOSURE.md`.

Source reduction merge: `83e966df251e548fd9574d9553d7f4bf5551877b` (PR #42).

Single main residual theorem:

```text
NS-P2-H3-MARGIN-UNIFORM = OPEN / HOLD frontier
```

Do not restart P2 by increasing a fixed cutoff, adding fixed-N integration steps, relying on L2/energy-only tails, adjacent compatibility, reader conditioning, or the held external High--High preprint. Re-enter P2 only with mathematics that directly advances the cutoff-independent H3 dissipative-margin theorem or a strictly stronger non-vacuous alternative.

Next active phase: P3 / P vs NP, after its branch-sync and formal-CI blockers are repaired.
