# Claim boundaries

This note follows this repository's own stated non-claim boundary (paper Remark on Theorem 1 /
the "boundary" remark before Section 5). Read it before citing this work.

| Claim | Status |
|---|---|
| There is a finite 8-state system with an admissible domain reading (exact commuting dynamical and observational welds) for which no finite observation horizon decides a nonconstant domain question | **Proved** (Theorem 1 in the paper), and independently re-verified by exact enumeration over all 8 states plus a period-2 structural check (`verification/verify_state_breakdown_math.py`) |
| Exact domain-dynamics welding and exact reader factorization imply, in general, that a declared finite reader decides an arbitrary domain question | **Refuted** by the same theorem — this is the whole point of the construction |
| The Navier-Stokes readout dichoromy (R)/(N) — whether Fefferman's breakdown predicate is finite-readout-determined for a given translation and reader | **Posed, not answered.** No Navier-Stokes translation `q_NS` satisfying the exact-weld identities is constructed in this paper. This is stated as open. |
| A finite retained-turbulence layer `tau_R dI_R/dt + L_R I_R = S_R + eta_R` (finite dimension, `tau_R>0`, fixed finite `L_R`, locally integrable drive) has a unique, bounded solution on every finite time interval | **Proved** (the paper's Global finite-interval continuation theorem, rendered as "Theorem 5" in the compiled `main.pdf` — the paper's `\newtheorem` counters are flat, not section-scoped, so this does not match the "Theorem 6.1" numbering used in the two source PDFs this note was drafted from; via variation of constants — standard linear ODE theory, hand/algebraically re-checked, not machine-checked in Coq) |
| A continuum Navier-Stokes breakdown forces blow-up of this retained-turbulence layer | **Not claimed, and the paper's own Corollary (bridge-failure) states the opposite direction**: any theorem transferring continuum blow-up onto this layer requires the layer's own finite-dimensional regularity hypotheses to fail first — a separate, unestablished claim |
| This paper proves or disproves any part of the Clay Millennium Navier-Stokes existence-and-smoothness problem | **Explicitly not claimed.** Restated at the end of the paper's introduction, at the boundary remark before Section 5, and in the conclusion. |
| The finite-witness theorem and the retained-turbulence continuation theorem are registered in the workspace's own Toledo equation library | **Registered as Toledo proposals, pending canonical-code assignment** — `PROP-NS-WITNESS-01` (tier `finite_diagnostic`) and `PROP-NS-CONTINUATION-01` (tier `Dr`, parented to `weld/P.05.v1` and `EQ-008`). Neither has yet been merged into Toledo's canonical registry (both still carry placeholder, not final, codes). `weld/P.05.v1` itself is registered in the canonical registry but carries `status: unverified` / `coq_status: open_prop` for the underlying turbulence-physics claim — a status that does not transfer to the present theorem's own linear-ODE mathematics, which does not depend on that physical claim. |
| This repository has been through independent adversarial review and is ready for public release / Zenodo deposit | An independent adversarial review has run (three reviewers: math correctness, overclaim/Toledo-first, leak/attribution) and its blocking findings have been fixed in this pass. Public GitHub repo (`github.com/morrocwi/readout-problem-navier-stokes`), release `v0.1.0`, and Zenodo deposit (DOI `10.5281/zenodo.22673246`) are done, per founder instruction. |

## Post-paper finite diagnostic: Discrete Epsilon-Completion (2026-09-10)

This lane is a later executable research extension and is **not part of the deposited v0.1.0 paper claim** unless a future release explicitly incorporates it.

| Claim | Status |
|---|---|
| The declared finite Fourier-Galerkin NS recurrence can be executed directly on integer Fourier records and ordered triads without constructing a spatial x/y/z grid in the production path | **Supported as a finite implementation statement** by `reproduction/checks/check_discrete_epsilon_completion.py`; not a claim that continuum space has been disproved or eliminated mathematically |
| The independent direct-triad and padded-FFT implementations agree on the recorded K=2 smooth random finite state | **Supported numerical diagnostic**: max RHS difference `1.041e-16`, max one-RK4-step difference `8.674e-19`; finite floating-point evidence, not a universal proof |
| The short Taylor-Green run (`nu=0.01`, `dt=0.005`, `T=0.05`) satisfies the declared nested-refinement operational gate at K=4 and K=5 | **Supported numerical diagnostic**. K=4: overlap L2 `3.551e-08`, boundary energy `2.089e-12`; K=5: overlap L2 `7.741e-10`, boundary energy `1.031e-15`. Frozen record: `reproduction/results/discrete_epsilon_completion_v01.json` |
| K=5 therefore contains all continuum Navier-Stokes information to the declared tolerance | **Not established; HOLD.** Small nested defect and small boundary-shell energy do not prove a bound on the complete omitted infinite tail |
| A rigorous finite-to-infinite completion certificate exists in the form `||(I-P_K)u|| <= beta_K(records_K)` with computable `beta_K -> 0` for the required 3D NS class | **Open target**, registered Toledo-first as `PROP-EPSC-04`; no such universal/useful bound is claimed here |
| The epsilon-completion family is registered in Toledo | **Registered as proposals, not canonical theorems**: `PROP-EPSC-01` Nested Readout Consistency Defect; `PROP-EPSC-02` NS boundary-energy diagnostic; `PROP-EPSC-03` fail-closed epsilon gate; `PROP-EPSC-04` open omitted-information certificate target. Source: `morrocwi/toledo/registry/proposals/discrete_epsilon_completion.json` |
| The finite refinement result overturns the existing negative external Taylor-Green validation at coarse turbulent resolution | **No.** The prior external-reference result remains in force: coarse K<=3 did not reproduce the published Re=1600 turbulent dissipation curve. Short-horizon nested stability and external physical/DNS adequacy are different claims. |

The governing distinction for this lane is:

`finite algebra / nested stability` **does not imply** `continuum completion` **does not imply** `physical turbulence validation`.
