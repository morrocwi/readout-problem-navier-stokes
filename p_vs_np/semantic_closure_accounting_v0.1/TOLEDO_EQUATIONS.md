# Toledo Equation Crosswalk

Toledo registration source:

`morrocwi/toledo/registry/proposals/semantic_closure_accounting_p_vs_np_v0_1.json`

Registration commit:

`0b17d60321f0a8ffaa0ebdd9f845fce05b347f30`

The canonical registry was checked first. Existing reader-equivalence / readout-sufficiency machinery is treated as prior Toledo/Readout-Genesis structure rather than re-registered under a new equation number. The entries below are manuscript-specific derivations or assembled complexity-theoretic readings.

| Proposal ID | Working code | Manuscript object | Tier / status |
|---|---|---|---|
| `PROP-SCA-PNP-01` | `A3/M.??.v1` | Circuit-to-Genesis ledger size preservation, `LedgerSize(CGSL(C)) = CircuitSize(C)` | `Dr`, unverified proposal |
| `PROP-SCA-PNP-02` | `A3/M.??.v1` | Retain–Recompute–Resolve semantic trichotomy | formal candidate / unverified proposal |
| `PROP-SCA-PNP-03` | `A3/M.??.v1` | RRR demand-versus-gate-capacity inequality | formal candidate / unverified proposal |
| `PROP-SCA-PNP-04` | `A3/M.??.v1` | Semantic-ledger lower-bound transfer to Boolean circuits | formal candidate / unverified proposal |
| `PROP-SCA-PNP-05` | `A3/M.??.v1` | Conditional SAT-to-`P/poly` separation schema | `Dr`, conditional |
| `PROP-SCA-PNP-06` | `A3/M.??.v1` | SAT Semantic Demand target, `H_n(SAT_n)/(K_n n^c) -> infinity` for every fixed `c` | `Open` |

## Claim boundary

Proposal registration is not canonical promotion. The placeholder sequence `??` is deliberate: Toledo's own code scheme says existing numbering must be reused and canonical codes must be assigned by the registry build/dedup/lineage process rather than guessed manually.

In particular, `PROP-SCA-PNP-06` is the unresolved load-bearing statement. Registering it records the research target; it does not change its tier from `Open`.
