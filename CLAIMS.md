# Claim boundaries

This note follows this repository's own stated non-claim boundary (paper Remark on Theorem 1 /
the "boundary" remark before Section 5). Read it before citing this work.

| Claim | Status |
|---|---|
| There is a finite 8-state system with an admissible domain reading (exact commuting dynamical and observational welds) for which no finite observation horizon decides a nonconstant domain question | **Proved** (Theorem 1 in the paper), and independently re-verified by exact enumeration over all 8 states plus a period-2 structural check (`verification/verify_state_breakdown_math.py`) |
| Exact domain-dynamics welding and exact reader factorization imply, in general, that a declared finite reader decides an arbitrary domain question | **Refuted** by the same theorem — this is the whole point of the construction |
| The Navier-Stokes readout dichoromy (R)/(N) — whether Fefferman's breakdown predicate is finite-readout-determined for a given translation and reader | **Posed, not answered.** No Navier-Stokes translation `q_NS` satisfying the exact-weld identities is constructed in this paper. This is stated as open. |
| A finite retained-turbulence layer `tau_R dI_R/dt + L_R I_R = S_R + eta_R` (finite dimension, `tau_R>0`, fixed finite `L_R`, locally integrable drive) has a unique, bounded solution on every finite time interval | **Proved** (the paper's Global finite-interval continuation theorem, rendered as "Theorem 5" in the compiled `main.pdf`; via variation of constants — standard linear ODE theory, hand/algebraically re-checked, not machine-checked in Coq) |
| A continuum Navier-Stokes breakdown forces blow-up of this retained-turbulence layer | **Not claimed.** Any theorem transferring continuum blow-up onto this layer requires the layer's own finite-dimensional regularity hypotheses to fail first — a separate, unestablished claim |
| This paper proves or disproves any part of the Clay Millennium Navier-Stokes existence-and-smoothness problem | **Explicitly not claimed.** |
| The finite-witness theorem and the retained-turbulence continuation theorem are registered in Toledo | **Registered as Toledo proposals, pending canonical-code assignment.** |
| This repository has been through independent adversarial review and is ready for public release / Zenodo deposit | Public GitHub repo, release `v0.1.0`, and Zenodo deposit DOI `10.5281/zenodo.22673246` are already present. |

## Post-paper research lane: Discrete Epsilon-Completion (2026-09-10)

This lane is a later executable/analytic extension and is **not part of the deposited v0.1.0 paper claim** unless a future release explicitly incorporates it.

| Claim | Status |
|---|---|
| The declared finite Fourier-Galerkin NS recurrence can be executed directly on integer Fourier records and ordered triads without constructing a spatial x/y/z grid in the production path | **Supported as a finite implementation statement** by `reproduction/checks/check_discrete_epsilon_completion.py`; not a claim that continuum space has been disproved or eliminated mathematically |
| The independent direct-triad and padded-FFT implementations agree on the recorded K=2 smooth random finite state | **Supported numerical diagnostic**: max RHS difference `1.041e-16`, max one-RK4-step difference `8.674e-19`; finite floating-point evidence, not a universal proof |
| The short Taylor-Green run (`nu=0.01`, `dt=0.005`, `T=0.05`) satisfies the declared nested-refinement operational gate at K=4 and K=5 | **Supported numerical diagnostic.** K=4: overlap L2 `3.551e-08`, boundary energy `2.089e-12`; K=5: overlap L2 `7.741e-10`, boundary energy `1.031e-15` |
| K=5 therefore contains all continuum Navier-Stokes information to the declared tolerance | **Not established; HOLD.** Small nested defect and small boundary-shell energy do not prove a bound on the complete omitted infinite tail |
| Finite retained terminal Fourier coefficients alone determine a useful universal omitted-tail bound for arbitrary divergence-free L2 terminal states | **No. Analytic non-identifiability obstruction.** For any K, an arbitrary divergence-free conjugate pair may be added at `q=(K+1,0,0)` without changing `P_K u`; see `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` |
| A computable finite-to-infinite tail certificate exists for unforced Leray-Hopf trajectories in the declared spacetime norm `L2(0,T;L2_x)` | **Derived at analytic (`Dr`) tier.** On the `2*pi` periodic torus, `||(I-P_K)u||_{L2_tL2_x} <= ||u0||_2 / (sqrt(2 nu)(K+1))`; this tends to zero and does not require global smoothness |
| A forced spacetime analogue exists when `f in L2(0,T;H^{-1})` | **Derived at analytic (`Dr`) tier.** `beta_K <= (K+1)^(-1) sqrt(||u0||^2/nu + ||f||^2_{L2_tH^-1}/nu^2)` under the declared normalization |
| The spacetime tail certificate propagates through any readout Lipschitz in the certified norm | **Derived at analytic (`Dr`) tier.** In particular the time-averaged field has tail at most `beta_K/sqrt(T)` |
| A prescribed terminal-time tail certificate follows from a separately certified pointwise H^s bound | **Conditional analytic statement.** If `|| |nabla|^s u(T)||_2 <= M_s(T)`, then `||(I-P_K)u(T)||_2 <= M_s(T)/(K+1)^s` |
| The project now has an unconditional useful terminal-time `beta_K` for arbitrary 3-D Navier-Stokes states | **Still OPEN.** The missing object is a globally valid pointwise regularity bound or another admissible terminal certificate; this is where the classical 3-D difficulty re-enters |
| The epsilon-completion family is registered in Toledo | **Registered as proposals, not canonical theorems.** `PROP-EPSC-04` is now refined by terminal no-go, spacetime certificate, readout lift, and conditional terminal certificate proposals |
| These results solve the Clay Millennium problem | **No.** They neither prove global smoothness nor finite-time blow-up; they refine which finite readouts can be certified without answering the full regularity question |
| The finite refinement result overturns the existing negative external Taylor-Green validation at coarse turbulent resolution | **No.** The prior external-reference result remains in force: coarse K<=3 did not reproduce the published Re=1600 turbulent dissipation curve. Short-horizon nested stability and external physical/DNS adequacy are different claims. |

The governing distinction for this lane is now:

`finite algebra / nested stability` **does not imply** `terminal full-state completion`, while a separately proved tail estimate **can imply** `completion in a declared spacetime/readout norm`.
