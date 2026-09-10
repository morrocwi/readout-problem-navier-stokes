# Semantic Closure Accounting for Boolean Circuits

**Preprint v0.1 — 2026-09-10; route-closure corrigendum 2026-09-11**  
**Author:** Yaoharee Lahtee  
**Status:** research architecture / conditional complexity framework; **not a proof of `P != NP`**.

This directory is deliberately separated from the Navier–Stokes papers in this repository. It records the P-versus-NP research lane derived from the Readout / IDM architecture, while preserving a fail-closed claim boundary.

## Contents

- `Semantic_Closure_Accounting_P_vs_NP_v0.1.tex` — self-contained arXiv-style LaTeX manuscript.
- `Semantic_Closure_Accounting_P_vs_NP_v0.1.pdf` — reproducibly built PDF.
- `ROUTE_CLOSURE.md` — final audit of what the architecture proves, the exact asymptotic correction, and why the remaining `H_n/K_n` step is already the unrestricted circuit lower-bound breakthrough.
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
- `formal/IDM_DemandCircuitDominance.v`

## Route-closure theorem

If an admissible semantic accounting is valid for every correct circuit,

```text
H_n(f_n) <= |C| K_n,
```

then applying it to a minimum-size circuit gives

```text
H_n(f_n) <= CC(f_n) K_n.
```

Thus any certified gap `B K_n < H_n(f_n)` is already a certificate that `B < CC(f_n)`. The `H_n/K_n` architecture therefore organizes an unrestricted circuit lower bound; it does not bypass one. See `ROUTE_CLOSURE.md` for the precise statement and implications.

## Exact open load-bearing theorem

The architecture does **not** establish an unrestricted lower bound for SAT. The remaining target is to construct a non-circular, sharing-aware semantic demand `H_n` and per-gate capacity scale `K_n` such that universal accounting holds for every shared bounded-fan-in Boolean circuit and the ratio is not polynomially bounded.

A multiplication-only formulation of the required asymptotic gap is:

```text
for every polynomial p and every N,
there exists n >= N such that
H_n(SAT_n) > p(n) K_n.
```

This is weaker and more exact than the original v0.1 wording “for every polynomial p, eventually for all n.” If the displayed condition and universal accounting are established under the admissibility conditions in the paper, then `SAT notin P/poly`, hence `P != NP`. This SAT-specific lower-bound premise is **OPEN**.

## Corrigendum

The v0.1 manuscript contains one logical wording error after the conditional separation theorem: the phrase **“if and only if”** should read **“provided that”** (or simply **“if”**). The proof establishes sufficiency only; no converse is proved. The source/PDF is being corrected without changing the claim boundary.

## Toledo

The equations introduced or newly assembled in this manuscript are registered Toledo-first in:

`morrocwi/toledo/registry/proposals/semantic_closure_accounting_p_vs_np_v0_1.json`

Canonical Toledo codes are intentionally left as `A3/M.??.v1` proposals until Toledo's deduplication, lineage, and canonical-code build pipeline promotes them. Existing Toledo equations are not renumbered. The route-closure refinement is recorded separately so that the original proposal provenance is not silently rewritten.
