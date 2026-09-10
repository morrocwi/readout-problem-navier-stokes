# K=3 shell-energy observability saturation

## Status

For the cubic Fourier--Galerkin truncation

\[
K_3=\{-3,\ldots,3\}^3\setminus\{0\},
\]

there are 342 nonzero Fourier modes and 684 real divergence-free degrees of freedom. Spatial translations provide a three-dimensional continuous symmetry invisible to shell-energy readouts, so the generic local observability rank is at most

\[
684-3=681.
\]

The exact squared-wavenumber shells are

\[
1,2,3,4,5,6,8,9,10,11,12,13,14,17,18,19,22,27,
\]

so the shell-energy reader has 18 components.

## Structural lower bound on jet depth

Let

\[
\mathcal J_R=(I,L_FI,\ldots,L_F^RI).
\]

The exact shell balance and total nonlinear energy conservation give one scalar dependence in every new 18-component shell block. Therefore

\[
\operatorname{rank}D\mathcal J_R\le \min(18+17R,681).
\]

Consequently rank 681 is impossible before

\[
R=39.
\]

Thus 39 is the earliest mathematically possible shell-jet order for local completeness modulo translation.

## Exact modular witness

`checks/check_k3_shell_energy_observability.py` uses the rational K=3 projected Galerkin operator at viscosity `nu=1/200`, the prime

\[
p=683,
\]

and 681 projected tangent directions. It propagates formal Taylor state/tangent series and computes exact ranks over `F_683`. Since `683>39` and all declared Galerkin, basis, and viscosity denominators are invertible modulo 683, Taylor-block and Lie-jet ranks agree through order 39 up to invertible factorial row scalings.

The exact ranks at selected milestones are

| R | rank |
|---:|---:|
| 0 | 18 |
| 5 | 103 |
| 10 | 188 |
| 20 | 358 |
| 30 | 528 |
| 35 | 613 |
| 38 | 664 |
| 39 | **681** |

Every recorded value equals

\[
\min(18+17R,681).
\]

In particular,

\[
\boxed{\operatorname{rank}_{\mathbb F_{683}}D\mathcal J_{39}=681.}
\]

A nonzero 681-by-681 projected minor modulo this good prime implies that the corresponding characteristic-zero minor polynomial is not identically zero. Combined with the translation upper bound,

\[
\boxed{\operatorname{rank}_{\rm gen}D\mathcal J_{39}=681}
\]

at `nu=1/200`.

The positive-viscosity scaling conjugacy

\[
F_\nu(\nu y)=\nu^2F_1(y)
\]

and quadratic homogeneity of each shell energy preserve jet rank for every `nu>0`. Hence

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal J_{39}=681,
\qquad \forall\nu>0.
}
\]

The order 39 is optimal because all smaller orders are excluded by the structural rank bound.

## Device interpretation

This is not yet a physical 18-sensor device. The 18 outputs are exact Fourier shell energies of the finite Galerkin state. The result is nevertheless a useful sensor-design benchmark: compared with one total-energy scalar, whose coordinate-count lower bound at K=3 would require order 680 to have any chance of reaching rank 681, the 18-channel shell reader reaches the same translation-limited local dimension at order 39.

Thus the finite model exhibits an exact trade-off between simultaneous measurement dimension and temporal jet depth:

\[
\text{more informative channels}\quad\Longleftrightarrow\quad\text{shallower time history}.
\]

The next engineering problem is to replace ideal Fourier shell energies by physically measurable pressure, velocity, wall-shear, force, vibration, or spectral-probe channels and minimize the jet order required for the same rank.

## Scope

Simulation=No. This is an exact finite-field observability computation for a fixed finite Fourier--Galerkin truncation. It does not prove scalar total-energy saturation at K=3, continuum Navier--Stokes regularity, global state reconstruction, noise robustness, or a realizable sensor architecture.

Machine-readable result: `results/k3_shell_energy_observability_mod683.json`.
