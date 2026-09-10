# Toledo Equation Crosswalk

Original Toledo registration source:

`morrocwi/toledo/registry/proposals/semantic_closure_accounting_p_vs_np_v0_1.json`

Route-closure refinement source:

`morrocwi/toledo/registry/proposals/semantic_closure_accounting_p_vs_np_v0_1_route_closure.json`

The canonical registry was checked first. Existing reader-equivalence / readout-sufficiency machinery is treated as prior Toledo/Readout-Genesis structure rather than re-registered under a new equation number. The entries below are manuscript-specific derivations or assembled complexity-theoretic readings.

| Proposal ID | Working code | Manuscript object | Tier / status |
|---|---|---|---|
| `PROP-SCA-PNP-01` | `A3/M.??.v1` | Circuit-to-Genesis ledger size preservation, `LedgerSize(CGSL(C)) = CircuitSize(C)` | `Dr`, unverified proposal |
| `PROP-SCA-PNP-02` | `A3/M.??.v1` | Retain–Recompute–Resolve semantic trichotomy | formal candidate / unverified proposal |
| `PROP-SCA-PNP-03` | `A3/M.??.v1` | RRR demand-versus-gate-capacity inequality | formal candidate / unverified proposal |
| `PROP-SCA-PNP-04` | `A3/M.??.v1` | Semantic-ledger lower-bound transfer to Boolean circuits | formal candidate / unverified proposal |
| `PROP-SCA-PNP-05` | `A3/M.??.v1` | Original stronger conditional SAT-to-`P/poly` separation schema | `Dr`, conditional; refined by `-07` |
| `PROP-SCA-PNP-06` | `A3/M.??.v1` | Original stronger SAT Semantic Demand target, `H_n/(K_n n^c) -> infinity` | `Open`; refined by `-09` |
| `PROP-SCA-PNP-07` | `A3/M.??.v1` | Exact `P/poly`-strength separation condition: no eventual polynomial upper bound on `H_n/K_n` | `Dr`, conditional |
| `PROP-SCA-PNP-08` | `A3/M.??.v1` | Demand–Circuit Dominance: `H <= CC(f)K`; `BK < H => B < CC(f)` | finite formal candidate |
| `PROP-SCA-PNP-09` | `A3/M.??.v1` | Exact SAT Semantic Demand target: for every polynomial `p` and cutoff `N`, some `n>=N` has `H_n > p(n)K_n` | `Open` |

## Route-closure interpretation

`PROP-SCA-PNP-08` closes a conceptual ambiguity in the original manuscript. Once universal accounting is valid for every correct circuit, any demand/capacity gap beyond a gate budget is already a circuit lower-bound certificate. The semantic-accounting layer therefore organizes the unrestricted circuit lower bound; it does not bypass it.

The original `PROP-SCA-PNP-05` and `PROP-SCA-PNP-06` remain in the proposal history rather than being silently overwritten. `PROP-SCA-PNP-07` and `PROP-SCA-PNP-09` record the weaker exact asymptotic condition needed to exclude `P/poly`.

## Claim boundary

Proposal registration is not canonical promotion. The placeholder sequence `??` is deliberate: Toledo's own code scheme says existing numbering must be reused and canonical codes must be assigned by the registry build/dedup/lineage process rather than guessed manually.

In particular, `PROP-SCA-PNP-09` remains the unresolved load-bearing statement. Registering it records the research target; it does not change its tier from `Open` and does not establish `P != NP`.

Pinned Toledo route-closure proposal commit: `c5331e733d83357a45284229c3a65a954cf0c2e2`.
