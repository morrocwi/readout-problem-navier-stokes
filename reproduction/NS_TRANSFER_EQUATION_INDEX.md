# NS energy-transfer observability equation index

This index links the new transfer bridge to Toledo proposal IDs. Proposal IDs are provenance/status records, not automatically canonical theorem codes.

| Toledo ID | Object | Tier/status in this project | Boundary |
|---|---|---|---|
| `PROP-NSOBS-09` | `dI_s/dt = T_s - 2 nu s I_s + F_s`, with `sum_s T_s=0` in the unforced closed finite system | standard finite identity / Definition | not an originality or continuum claim |
| `PROP-NSOBS-10` | `(I,T)` is an invertible affine reparameterization of `(I,dI/dt)` for prescribed forcing | `Dr` derived | same local rank; does not prove saturation |
| `PROP-NSOBS-11` | every boundary mode at cutoff `N>=2` has a constructive non-collinear triad connection to `K_{N-1}` | `Dr` derived; finite sweep through `N=8` | kinematic connectivity only; minor independence remains open |
| `PROP-EPSC-20` | explicit quantitative inverse radius for the existing analytic three-mode reduced subcase | `Dr` derived partial witness | does not close the full `N=1` cube inverse |
| `PROP-EPSC-21` | derivative-free window transfer identity and interval-radius propagation | `Dr` derived partial witness | removes differentiation from one noisy-observation substep; full EPSC-19 remains open |

## Relation to existing open items

`PROP-NSOBS-07` is **still OPEN**. The new connectivity lemma removes a structural disconnection obstruction, but earliest-order all-`N` saturation still requires a nonzero/minor-independence argument.

`PROP-EPSC-18` is **still OPEN** for the full finite Fourier quotient. `PROP-EPSC-20` closes only the already-isolated analytic triad subcase quantitatively.

`PROP-EPSC-19` is **still OPEN** end-to-end. `PROP-EPSC-21` supplies a noise-stable transfer-window input without numerical differentiation, but a certified noisy full-state inverse is still missing.

`PROP-EPSC-16` remains a separate outer-certificate scaling/tightness problem.

## Current reduced chain

```text
shell-energy measurements / finite windows
    -> transfer summaries with certified interval radii       [NSOBS-09/10, EPSC-21]
    -> full quotient-state inverse radius rho_N               [EPSC-18 OPEN]
    -> omitted-tail beta_N                                    [EPSC]
    -> sqrt(rho_N^2 + beta_N^2)                               [EPSC-17]
    -> continuum tolerance verdict
```

The existing triad subcase has a quantitative inner witness (`EPSC-20`), but the full chain remains fail-closed until the full `rho_N` exists.
