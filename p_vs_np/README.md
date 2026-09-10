# P vs NP Research Lane

This directory is a deliberately separated complexity-theory lane inside `readout-problem-navier-stokes`. It does not alter the Navier–Stokes claims or the Clay-status language of the root project.

## Current lane

[`semantic_closure_accounting_v0.1/`](./semantic_closure_accounting_v0.1/)

**Final route status:** the CGSL + Retain/Recompute/Resolve semantic-accounting architecture is structurally closed as a proof interface, but it does **not** prove `P != NP`.

The decisive route-closure relation is

```text
universal accounting: H_n(f_n) <= |C| K_n for every correct C

=> H_n(f_n) <= CC(f_n) K_n

=> any B K_n < H_n(f_n) is already a circuit lower-bound certificate B < CC(f_n).
```

So the remaining SAT-specific `H_n/K_n` theorem is not a small missing bookkeeping lemma. If proved under the required non-circularity, sharing, recomputation, basis, and barrier guards, it would itself constitute the unrestricted Boolean-circuit lower-bound breakthrough.

See:

- [`ROUTE_CLOSURE.md`](./semantic_closure_accounting_v0.1/ROUTE_CLOSURE.md) — final mathematical/status audit.
- [`Semantic_Closure_Accounting_P_vs_NP_v0.1.pdf`](./semantic_closure_accounting_v0.1/Semantic_Closure_Accounting_P_vs_NP_v0.1.pdf) — corrected reproducible preprint.
- [`TOLEDO_EQUATIONS.md`](./semantic_closure_accounting_v0.1/TOLEDO_EQUATIONS.md) — original and route-closure Toledo proposal crosswalk.

Formal finite kernels and negative controls are maintained in `morrocwi/information-discrete-math`, draft PR #117, branch `research/p-vs-np-readout`.
