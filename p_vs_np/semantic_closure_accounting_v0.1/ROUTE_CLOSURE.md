# Route Closure — Semantic Closure Accounting for P vs NP

**Date:** 2026-09-11  
**Status:** the accounting route is structurally closed; the unrestricted SAT circuit lower bound remains open.  
**Claim boundary:** this note does **not** claim `P != NP`. It records the exact theorem boundary after auditing the manuscript, the IDM formal lane, negative controls, and the fusion/readout alternatives.

## 1. Final conclusion

The CGSL + Retain/Recompute/Resolve (RRR) architecture is a valid **proof interface** for a Boolean-circuit lower bound. It is not, by itself, a shortcut around that lower bound.

The finite chain is:

```text
Boolean circuit
  -> size-preserving semantic ledger
  -> Retain / Recompute / Resolve accounting
  -> demand <= gates * per-gate-capacity
  -> circuit lower bound, if an independent demand gap is proved
```

The first, second, arithmetic, and transfer steps have finite formal candidates in `morrocwi/information-discrete-math`, branch `research/p-vs-np-readout`. The missing SAT-specific step is exactly the unrestricted circuit lower bound in a new coordinate system.

## 2. Demand–Circuit Dominance (route-closure theorem)

Let `f_n` be a Boolean function and let `CC(f_n)` denote the minimum size of a correct circuit in the declared circuit model. Suppose a proposed semantic demand `H_n(f_n)` and capacity scale `K_n >= 0` satisfy the universal accounting statement

```text
H_n(f_n) <= |C| K_n
```

for **every** correct circuit `C` computing `f_n`.

Applying the same statement to a minimum-size correct circuit gives

```text
H_n(f_n) <= CC(f_n) K_n.
```

Therefore, whenever `K_n > 0`, informally

```text
H_n(f_n) / K_n <= CC(f_n).
```

More importantly, without using division, for every budget `B`:

```text
B K_n < H_n(f_n)  =>  B < CC(f_n).
```

This implication is formalized as the finite arithmetic kernel `formal/IDM_DemandCircuitDominance.v` in the IDM research branch.

### Consequence

A proof that `H_n(SAT_n)/K_n` escapes every polynomial, **while universal accounting remains valid for every shared Boolean circuit**, is already a proof that SAT has no polynomial-size circuit family. The semantic accounting has organized the proof obligation but has not reduced its mathematical strength.

The tautological choice

```text
H_n(f_n) = CC(f_n),   K_n = 1
```

would make the inequality perfectly tight, but is circular and is explicitly forbidden by the manuscript's admissibility rules. Hence the decisive research problem is not to name a larger `H_n`; it is to construct a non-circular invariant whose universal per-gate accounting theorem can actually be proved.

## 3. Corrigendum to v0.1: sufficiency, not “if and only if”

The sentence following the conditional separation theorem in preprint v0.1 used the phrase **“if and only if.”** The proof establishes only a sufficient route:

```text
admissible H_n,K_n + universal accounting + a non-polynomial demand/capacity gap
    => SAT notin P/poly
    => P != NP.
```

No converse was proved. The source manuscript is corrected to say **“provided that” / “if”** rather than “if and only if.”

## 4. Corrigendum to the asymptotic target

The v0.1 manuscript asks for the stronger condition that, for every polynomial `p`,

```text
H_n(SAT_n) > p(n) K_n
```

for all sufficiently large `n` (and elsewhere phrases this as a ratio tending beyond every polynomial).

That is sufficient but stronger than necessary for excluding `P/poly`.

The exact condition needed is that `H_n(SAT_n)/K_n` is **not eventually bounded by any polynomial**. A multiplication-only statement is:

```text
for every polynomial p and every N,
there exists n >= N such that
H_n(SAT_n) > p(n) K_n.
```

If a polynomial-size circuit family existed, one polynomial `p` would bound its size for every sufficiently large input length (indeed under the usual definition, all lengths after harmless adjustment). Universal accounting would then force `H_n <= p K_n` on those lengths, contradicting the displayed condition.

This weaker exact target is now the preferred formulation. It does not make the core lower-bound problem easier; it merely removes an unnecessary asymptotic strengthening.

## 5. Negative controls permanently retained

The route must continue to reject all of the following shortcuts:

- **Residual-count / future-width counting alone:** equality has `2^m` block-ordered residuals but a linear-size shared circuit.
- **Retained-bit counting alone:** the whole input is only `O(n)` bits and computation can be postponed to the decoder.
- **Elimination width alone:** it lower-bounds the declared elimination model, not arbitrary shared circuits without a transfer theorem.
- **Provenance counting:** circuit complexity is extensional; harmless lineage duplication cannot be charged as hardness.
- **A single fixed fusion/semi-filter distribution:** the standard probabilistic-counting limitation gives only an `O(n)` ceiling in the general non-monotone setting. A candidate-adaptive distribution can evade that fixed-distribution ceiling, but proving that such an adaptive adversary defeats every small circuit is itself the hard lower-bound step.

## 6. The only remaining unrestricted frontier

Two equivalent-looking research interfaces remain useful, but neither is currently closed:

### A. Non-circular demand/capacity invariant

Construct `H_n,K_n` such that:

1. `H_n` is defined without minimum circuit size, SAT/equivalence/MCSP oracle access, or the complete SAT truth table;
2. every correct shared bounded-fan-in circuit satisfies `H_n(SAT_n) <= |C| K_n`;
3. `H_n(SAT_n)/K_n` is not polynomially bounded;
4. the proof survives sharing, recomputation, basis simulation, harmless rewrites, and the standard complexity barriers.

### B. Candidate-adaptive uniform refuter

For every polynomial gate bound `B`, construct from the syntax/lineage of each candidate circuit `C` with `|C| <= B(n)` an input `x` satisfying

```text
C(x) != SAT_n(x),
```

without computing the target answer through an oracle or hidden truth table.

A successful construction would be a genuine unrestricted circuit lower bound. The current repository does not contain such a construction.

## 7. Final status table

| Component | Final status |
|---|---|
| Circuit -> CGSL ledger | finite formal candidate |
| DAG sharing preserved | finite formal candidate |
| RRR no-collapse | finite formal candidate |
| RRR demand/capacity arithmetic | finite formal candidate |
| Ledger lower bound -> circuit lower bound | finite formal candidate |
| Demand–Circuit Dominance meta-theorem | finite formal candidate |
| Equality / sharing negative control | exact finite diagnostic |
| Fixed-distribution fusion route | asymptotically blocked as a general super-linear route |
| Non-circular universal SAT `H_n,K_n` | **OPEN** |
| Candidate-adaptive unrestricted SAT refuter | **OPEN** |
| `SAT notin P/poly` | **NOT PROVED** |
| `P != NP` | **NOT PROVED** |

## 8. What “closed” means here

This research lane is now **closed as an architectural reduction**: there is no remaining bookkeeping bridge whose completion would automatically settle P vs NP. Any further decisive advance must prove a new unrestricted Boolean-circuit lower bound, either directly or through an invariant/refuter strong enough to imply one.

That is the correct stopping point for Semantic Closure Accounting v0.1. Future work should not claim that filling in `H_n` is a small technical step; it is the central lower-bound breakthrough itself.
