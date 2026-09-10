# NS Discrete Epsilon-Completion — Equation and Implementation Index

Status: **post-paper EPSC research lane**. This index separates proposal provenance, analytic (`Dr`) statements, and executed finite diagnostics. It does not promote any Toledo proposal to a canonical verified theorem.

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
| `PROP-EPSC-16` | Tight/scalable high-cutoff certified enclosure | not yet optimized | future benchmark/validated-numerics work | **OPEN** |

## EPSC-15 construction

For each stored binary64 node, the implementation takes every real/imaginary component as its **exact IEEE-754 dyadic rational**, applies the Leray projector in exact rational arithmetic, and joins consecutive nodes by

\[
v_h(t_n+\theta h)=(1-\theta)v_n+\theta v_{n+1},\qquad 0\le\theta\le1.
\]

The path is continuous, `K`-supported and exactly divergence-free. Its full Navier--Stokes residual is degree at most two in `theta`; therefore its homogeneous `H^{-1}` norm squared is degree at most four and its time integral is an exact rational finite computation. A coefficientwise Fourier `l1` majorant yields a rigorous upper bound for `int ||grad v_h||_inf`, and a rational Taylor/geometric remainder bounds the exponential from above.

The executed `K=1`, `nu=0.01`, `dt=0.01`, `T=0.05` Taylor--Green witness reports approximately

\[
\overline A_T=0.599550229412277,
\qquad
\overline B_T=9.736386925864618\times10^{-5},
\qquad
\beta_T\le0.1331648457569634.
\]

These values certify the declared short comparison path; they are not a DNS-resolution claim.

## Source-of-truth order

1. **Toledo** owns proposal identifiers, status and equation provenance under `registry/proposals/discrete_epsilon_completion*.json`.
2. **Information Discrete Mathematics** owns reusable algorithms and certificate APIs.
3. **This Navier--Stokes repository** owns domain-specific proofs, reproduction checks, generated ledger and manuscript evidence.
4. **Readout Genesis** records the interpretation/application map only; application evidence does not automatically become Genesis root ontology.

## Mandatory claim fence

The following implication remains forbidden:

```text
small nested defect + small outer-shell energy
    => all omitted continuum information is small
```

The supported chain is instead

```text
finite node tape
  -> declared exact comparison path
  -> certified A_bar/B_bar residual summaries
  -> standard relative-energy theorem (Dr)
  -> terminal L2/tail beta
  -> epsilon gate for that declared target
```

This does **not** imply global 3-D regularity, finite-time blow-up, physical turbulence adequacy of a tested cutoff, or a Clay Millennium solution. The current open engineering problem is `PROP-EPSC-16`: tightness and cost at larger `K` and longer `T`.
