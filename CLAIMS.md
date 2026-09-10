# Claim boundaries

This note follows this repository's own stated non-claim boundary (paper Remark on Theorem 1 / the "boundary" remark before Section 5). Read it before citing this work.

| Claim | Status |
|---|---|
| There is a finite 8-state system with an admissible domain reading (exact commuting dynamical and observational welds) for which no finite observation horizon decides a nonconstant domain question | **Proved** (Theorem 1 in the paper), and independently re-verified by exact enumeration over all 8 states plus a period-2 structural check (`verification/verify_state_breakdown_math.py`) |
| Exact domain-dynamics welding and exact reader factorization imply, in general, that a declared finite reader decides an arbitrary domain question | **Refuted** by the same theorem |
| The Navier-Stokes readout dichotomy (R)/(N) — whether Fefferman's breakdown predicate is finite-readout-determined for a given translation and reader | **Posed, not answered.** No Navier-Stokes translation `q_NS` satisfying the exact-weld identities is constructed in the deposited paper. |
| A finite retained-turbulence layer `tau_R dI_R/dt + L_R I_R = S_R + eta_R` (finite dimension, `tau_R>0`, fixed finite `L_R`, locally integrable drive) has a unique, bounded solution on every finite time interval | **Proved** in the paper by standard finite-dimensional linear ODE analysis; not machine-checked in Coq |
| A continuum Navier-Stokes breakdown forces blow-up of this retained-turbulence layer | **Not claimed.** |
| The deposited paper proves or disproves the Clay Millennium Navier-Stokes existence-and-smoothness problem | **Explicitly not claimed.** |

## Post-paper research lane: Discrete Epsilon-Completion (2026-09-10)

This lane is a later executable/analytic extension and is **not part of the deposited v0.1.0 paper claim** unless a future release explicitly incorporates it.

| Claim | Status |
|---|---|
| The declared finite Fourier-Galerkin NS recurrence can be executed directly on integer Fourier records and ordered triads without constructing a spatial x/y/z grid in the production path | **Supported as a finite implementation statement** by `reproduction/checks/check_discrete_epsilon_completion.py`; not a claim that continuum space has been disproved |
| Direct-triad and padded-FFT implementations agree on the recorded K=2 finite state | **Supported numerical diagnostic**: max RHS difference `1.041e-16`, max one-RK4-step difference `8.674e-19` |
| The short Taylor-Green run (`nu=0.01`, `dt=0.005`, `T=0.05`) satisfies the declared nested-refinement operational gate at K=4 and K=5 | **Supported numerical diagnostic.** K=4: overlap L2 `3.551e-08`, boundary energy `2.089e-12`; K=5: overlap L2 `7.741e-10`, boundary energy `1.031e-15` |
| K=5 therefore contains all continuum Navier-Stokes information to the declared tolerance | **Not established; HOLD.** Nested stability plus boundary-shell energy is not a complete omitted-tail proof |
| Finite retained terminal Fourier coefficients alone determine a useful universal omitted-tail bound for arbitrary divergence-free L2 terminal states | **No. Analytic non-identifiability obstruction.** A divergence-free conjugate pair can be placed wholly outside the cutoff without changing `P_Ku` |
| A computable finite-to-infinite tail certificate exists for unforced Leray-Hopf trajectories in `L2(0,T;L2_x)` | **Derived at analytic (`Dr`) tier.** On the `2*pi` periodic torus, `||(I-P_K)u||_{L2_tL2_x} <= ||u0||_2/(sqrt(2 nu)(K+1))` |
| A forced spacetime analogue exists when `f in L2(0,T;H^{-1})` | **Derived at analytic (`Dr`) tier** under the declared normalization |
| The spacetime certificate propagates through a Lipschitz readout | **Derived at analytic (`Dr`) tier.** The time-averaged field is one explicit corollary |
| A prescribed terminal-time tail certificate follows from a separately certified pointwise H^s bound | **Conditional analytic statement.** `|| |nabla|^s u(T)||_2 <= M_s(T)` implies terminal tail `<= M_s(T)/(K+1)^s` |
| A prescribed terminal-time L2 tail bound can be obtained from a richer certified retained energy tape | **Derived at analytic (`Dr`) tier.** For the actual unforced Leray-Hopf projection, `||(I-P_K)u(T)||_2^2 <= ||u0||_2^2 - ||P_Ku(T)||_2^2 - 2 nu int_0^T ||grad P_Ku||_2^2 dt`; see `paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md` |
| The terminal energy-budget bound is valid if raw finite-Galerkin values are substituted with no continuum adapter proof | **No. HOLD.** The terminal norm and retained dissipation must be exact or certified directional bounds for the actual continuum projection |
| The terminal energy-budget certificate necessarily tends to zero for every Leray-Hopf weak solution | **Not claimed.** Its exact-projection asymptotic squared floor is the energy-inequality slack `D_E(T)` |
| If energy equality is independently justified up to T, the exact-projection terminal energy-budget beta tends to zero | **Derived at analytic (`Dr`) tier.** Under zero energy defect, terminal tail and unresolved dissipation both vanish as K grows |
| The project already has the certified finite-Galerkin -> continuum energy-tape adapter required to drive the terminal theorem from its solver output | **OPEN.** Registered as `PROP-EPSC-12`; this is now the principal computational bridge obligation |
| The epsilon-completion family is registered in Toledo | **Registered as proposals, not canonical theorems.** `PROP-EPSC-01..09` cover the base/spacetime family; `PROP-EPSC-10..12` cover terminal energy-budget closure and the open adapter |
| These results solve the Clay Millennium problem | **No.** They neither prove global smoothness nor finite-time blow-up, and do not establish uniqueness of 3-D weak solutions |
| The finite refinement result overturns the existing negative external Taylor-Green validation at coarse turbulent resolution | **No.** Short-horizon nested stability and external physical/DNS adequacy remain distinct claims |

The current frontier is therefore:

```text
finite Galerkin record
    -> PROP-EPSC-12 certified adapter (OPEN)
actual continuum projected energy tape
    -> PROP-EPSC-10 terminal energy-budget theorem
rigorous terminal beta_K
```

The governing distinction remains: finite algebra and nested stability do not by themselves imply continuum completion; certification requires a proved bridge in the declared target norm.
