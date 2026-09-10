# Semantic Closure Accounting for Boolean Circuits

**Preprint v0.1 — 2026-09-10**  
**Author:** Yaoharee Lahtee  
**Status:** research architecture / conditional complexity framework; **not a proof of `P != NP`**.

This directory is deliberately separated from the Navier–Stokes papers in this repository. It records the P-versus-NP research lane derived from the Readout / IDM architecture, while preserving a fail-closed claim boundary.

## Contents

- `Semantic_Closure_Accounting_P_vs_NP_v0.1.tex` — self-contained arXiv-style LaTeX manuscript.
- `BUILD.md` — reproducible local build instructions.
- `TOLEDO_EQUATIONS.md` — equation crosswalk to the Toledo proposal registry.
- `MANIFEST.json` — provenance, source hashes, and upstream formal-artifact anchors.

## Main finite architecture

The manuscript isolates the chain

```text
Boolean circuit
  -> one-entry-per-gate semantic ledger (CGSL)
  -> Retain / Recompute / Resolve accounting (RRR)
  -> finite demand-versus-capacity inequality
  -> semantic-ledger lower bound
  -> circuit lower bound
```

The associated formal candidates live in `morrocwi/information-discrete-math`, branch `research/p-vs-np-readout`, especially:

- `formal/IDM_CircuitGenesisBridge.v`
- `formal/IDM_RetainRecomputeResolve.v`
- `formal/IDM_RRRCostLowerBound.v`
- `formal/IDM_CircuitLedgerTransfer.v`

## Open load-bearing theorem

The architecture does **not** establish an unrestricted lower bound for SAT. The remaining target is to construct a non-circular, sharing-aware semantic demand `H_n` and per-gate capacity scale `K_n` such that the demand/capacity ratio outgrows every polynomial while remaining valid for every shared bounded-fan-in Boolean circuit.

In schematic form:

```text
H_n(SAT_n) > p(n) K_n   for every polynomial p, eventually,
```

combined with the universal accounting inequality for every size-`s` circuit:

```text
H_n(SAT_n) <= s K_n.
```

If both are established under the admissibility conditions in the paper, the standard implication is `SAT notin P/poly`, hence `P != NP`. The first inequality is **OPEN**.

## Toledo

The equations introduced or newly assembled in this manuscript are registered Toledo-first in:

`morrocwi/toledo/registry/proposals/semantic_closure_accounting_p_vs_np_v0_1.json`

Canonical Toledo codes are intentionally left as `A3/M.??.v1` proposals until Toledo's deduplication, lineage, and canonical-code build pipeline promotes them. Existing Toledo equations are not renumbered.
