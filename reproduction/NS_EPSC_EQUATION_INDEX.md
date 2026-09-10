# NS Discrete Epsilon-Completion — Equation and Implementation Index

Status: **post-paper finite-diagnostic supplement**. This file does not alter the six-volume ledger and does not promote any proposal to a canonical Toledo theorem.

| Toledo proposal | Role | General implementation | NS reproduction evidence | Status |
|---|---|---|---|---|
| `PROP-EPSC-01` | Nested Readout Consistency Defect `delta_K = ||R_K x_(K+1)-x_K||` | `morrocwi/information-discrete-math:idm/ns_epsilon.py::nested_readout_consistency_defect` | `reproduction/checks/check_discrete_epsilon_completion.py::overlap_difference`; `reproduction/NS_DISCRETE_EPSILON_COMPLETION.md` | `Definition / unverified` |
| `PROP-EPSC-02` | NS Fourier boundary energy `E_partialK = 1/2 sum_{||k||_inf=K}|u_hat_k|^2` | `morrocwi/information-discrete-math:idm/ns_epsilon.py::boundary_energy` | checker `diagnostics`; frozen values in `reproduction/results/discrete_epsilon_completion_v01.json` | `Definition / finite diagnostic proxy` |
| `PROP-EPSC-03` | Fail-closed epsilon-completion gate | `morrocwi/information-discrete-math:idm/ns_epsilon.py::epsilon_completion_verdict` | NS report explicitly records finite diagnostic PASS but continuum certificate HOLD | `Definition / unverified` |
| `PROP-EPSC-04` | Computable omitted-information bound `||(I-P_K)x|| <= beta_K(records_K)`, `beta_K -> 0` | **No implementation is allowed to pretend this exists.** The IDM API accepts a beta only as a separately supplied proved bound. | NS report marks the continuum/infinite-object certificate `HOLD` | **Open** |

## Source-of-truth order

1. **Toledo** owns proposal identifiers, status, and equation provenance: `morrocwi/toledo/registry/proposals/discrete_epsilon_completion.json`.
2. **Information Discrete Mathematics** owns the general executable definitions/API: `idm/ns_epsilon.py` and `docs/DISCRETE_EPSILON_COMPLETION.md`.
3. **This Navier-Stokes repository** owns the domain-specific reproduction and frozen numerical evidence.
4. **Readout Genesis** may map the application in `APPLICATIONS.md`; it does not own or upgrade these mathematical claims.

## Mandatory claim fence

The following implication is forbidden by the current evidence:

```text
small nested defect + small outer-shell energy
    => all omitted continuum information is small
```

A theorem-level epsilon completion requires an actual `PROP-EPSC-04` certificate (or a future canonical successor) under explicit hypotheses. Until then:

```text
finite diagnostic: may PASS
continuum / infinite-object completion: HOLD
```
