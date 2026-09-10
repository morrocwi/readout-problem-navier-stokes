# NS Discrete Epsilon-Completion and Energy-Observability Index

Status: **post-paper research lane**. This index separates proposal provenance, analytic (`Dr`) statements, executed finite diagnostics, and open frontiers. It does not promote any Toledo proposal to a canonical verified theorem.

## EPSC family

| Toledo proposal | Role | General implementation | NS evidence | Current status |
|---|---|---|---|---|
| `PROP-EPSC-01` | Nested readout defect `delta_K` | `information-discrete-math:idm/ns_epsilon.py` | `check_discrete_epsilon_completion.py` | Definition + finite witness |
| `PROP-EPSC-02` | Outer retained-shell energy diagnostic | `idm/ns_epsilon.py` | frozen discrete-epsilon result JSON | finite diagnostic proxy |
| `PROP-EPSC-03` | Fail-closed epsilon gate | `idm/ns_epsilon.py` | discrete-epsilon checker | Definition |
| `PROP-EPSC-04` | Target-indexed omitted-information certificate `beta_(K,Y)` | certificate family below | proof notes + Volume-7 checkers | resolved for declared target/record classes; not universal |
| `PROP-EPSC-05` | Terminal retained-mode non-identifiability | analytic obstruction | `check_volume7_spacetime_tail.py` high-mode witness | Dr + finite witness |
| `PROP-EPSC-06` | Spectral `H^s -> L2` tail inequality | `idm/ns_tail_certificate.py` | `check_volume7_spacetime_tail.py` | Dr + finite algebra witness |
| `PROP-EPSC-07` | Leray-Hopf spacetime tail certificate | `idm/ns_tail_certificate.py` | `paper/NS_SPACETIME_TAIL_CERTIFICATE.md` | Dr derived |
| `PROP-EPSC-08` | Lipschitz readout lift | `idm/ns_tail_certificate.py` | spacetime proof note | Dr derived |
| `PROP-EPSC-09` | Conditional terminal `H^s` certificate | `idm/ns_tail_certificate.py` | spacetime proof note | Dr conditional |
| `PROP-EPSC-10` | Terminal energy-budget certificate | `idm/ns_terminal_certificate.py` | `check_volume7_terminal_energy_budget.py` | Dr + finite algebra witness |
| `PROP-EPSC-11` | Energy-defect floor / equality closure | `idm/ns_terminal_certificate.py` | terminal-energy proof note | Dr derived |
| `PROP-EPSC-12` | Broad finite-trajectory to continuum retained-record adapter | refined by 13--15 | Volume-7 adapter lane | resolved for the declared residual-based path construction |
| `PROP-EPSC-13` | Relative-energy adapter `exp(A)(e0^2+B/nu)` | `idm/ns_relative_energy_adapter.py` | `check_volume7_relative_energy_adapter.py`; proof note | Dr derived |
| `PROP-EPSC-14` | Finite Fourier residual tape / `H^-1` summary | `idm/ns_relative_energy_adapter.py` | relative-energy checker | Definition + finite witness |
| `PROP-EPSC-15` | Exact continuous-time enclosure of a stored binary64 RK4 tape | `idm/ns_rk4_path_certificate.py` | `check_volume7_rk4_continuous_enclosure.py` | **finite_diagnostic PASS + Dr continuum implication** |
| `PROP-EPSC-16` | Tight/scalable high-cutoff certified enclosure | open optimization | future validated-numerics work | **OPEN** |
| `PROP-EPSC-17` | Observable-to-continuum orthogonal composition `sqrt(rho_N^2+beta_N^2)` | `idm/ns_observable_to_continuum.py` | `check_volume7_observable_continuum_bridge.py`; synthesis paper | **Dr derived + finite algebra witness** |
| `PROP-EPSC-18` | Certified inverse from energy jets to retained-state radius `rho_N` | no implementation allowed to fake this | synthesis paper | **OPEN** |
| `PROP-EPSC-19` | Noise-stable measurement-to-continuum certificate | fail-closed placeholder only | synthesis paper | **OPEN** |

## NS energy-observability family

| Toledo proposal | Role | NS source/evidence | Status |
|---|---|---|---|
| `PROP-NSOBS-01` | finite real phase-space dimension `d_N=2((2N+1)^3-1)` | `paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex` | Definition |
| `PROP-NSOBS-02` | scalar total-energy Lie-jet ceiling and `R_E^min=d_N-4` | same paper | Dr |
| `PROP-NSOBS-03` | shell-energy Lie-jet ceiling and `R_I^min` | same paper | Dr |
| `PROP-NSOBS-04` | positive-viscosity rank universality | same paper | Dr |
| `PROP-NSOBS-05` | exact saturation records `(N,E/I,R,rank)` at four cases | exact modular certificates + reproduction | finite_diagnostic evidence |
| `PROP-NSOBS-06` | measurement-channel versus temporal-depth tradeoff | structural ceilings | Dr |
| `PROP-NSOBS-07` | generic earliest-order saturation for every finite `N` | conjecture in observability paper | **OPEN** |
| `PROP-NSOBS-08` | local finite-state completeness modulo translation at certified saturation | rank + free translation action | Dr |

## Inner completeness + outer completeness

The combined architecture is

```text
energy observations / Lie jets
    -> retained-state quotient reconstruction radius rho_N   [inner completeness]
    -> retained Fourier state / certified comparison path
    -> omitted-tail radius beta_N                             [outer completeness]
    -> sqrt(rho_N^2 + beta_N^2)
    -> continuum L2 tolerance verdict modulo translation
```

The orthogonal composition is sharper than the generic triangle bound. If

\[
\inf_{g\in G}\|P_Nu(T)-g\widehat x_N\|_2\le\rho_N,
\qquad
\|(I-P_N)u(T)\|_2\le\beta_N,
\]

then, because the two terms lie in orthogonal Fourier subspaces,

\[
\boxed{
\inf_{g\in G}\|u(T)-g\widehat x_N\|_2
\le\sqrt{\rho_N^2+\beta_N^2}.
}
\]

For the energy-reader application `G=T^3` is spatial translation. Rank saturation provides local qualitative identifiability modulo this symmetry, but it does **not** by itself provide the quantitative `rho_N` required by the composition theorem.

## What is now closed and what remains open

`PROP-EPSC-15` is supplied for the declared exact-dyadic piecewise-linear reconstruction of recorded RK4 nodes. The executed `K=1`, `nu=0.01`, `dt=0.01`, `T=0.05` Taylor-Green witness reports approximately

\[
\overline A_T=0.599550229412277,
\qquad
\overline B_T=9.736386925864618\times10^{-5},
\qquad
\beta_T\le0.1331648457569634.
\]

The new combined frontiers are deliberately separated:

- `PROP-NSOBS-07`: prove or refute earliest-order generic saturation for every finite resolution;
- `PROP-EPSC-18`: turn saturated energy jets into a certified retained-state inverse radius `rho_N`;
- `PROP-EPSC-19`: make that inverse robust to measurement/noise/differentiation uncertainty;
- `PROP-EPSC-16`: independently improve cost/tightness of outer EPSC certification at larger cutoff/horizon.

These are related parts of one measurement-to-continuum programme, but they are not the same mathematical problem.

## Source-of-truth order

1. **Toledo** owns proposal identifiers, status and equation provenance under `registry/proposals/ns_energy_observability.json` and `registry/proposals/discrete_epsilon_completion*.json`.
2. **Information Discrete Mathematics** owns reusable algorithms and fail-closed composition APIs.
3. **This Navier-Stokes repository** owns domain-specific proofs, observability certificates, reproduction checks, generated ledger and manuscripts.
4. **Readout Genesis** records the interpretation/application map only; application evidence does not automatically become Genesis root ontology.

## Mandatory claim fence

Neither of the following shortcuts is allowed:

```text
small nested defect + small outer-shell energy
    => all omitted continuum information is small

full local observability rank
    => globally/stably reconstructed finite state with known error radius
```

The supported combined chain requires **both** a certified `rho_N` and a certified `beta_N`. This does not imply global 3-D regularity, finite-time blow-up, physical turbulence adequacy of a tested cutoff, or a Clay Millennium solution.
