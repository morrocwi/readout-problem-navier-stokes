# Reproducing the Energy-Observability Results

This lane reproduces the finite-dimensional observability certificates used by
`paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex`.

**Simulation=No.** The principal checks are exact finite-field formal Taylor/tangent computations. They are not DNS, turbulence simulation, or a continuum Navier--Stokes proof.

## Environment

A known-good environment is recorded in `reproduction/requirements-energy-observability.txt`:

```bash
python3 -m pip install -r reproduction/requirements-energy-observability.txt
```

The package was assembled against Python 3.13.5, NumPy 2.3.5, and Numba 0.65.1. Other compatible versions may work, but the pinned versions define the recorded software environment.

## One-command reproduction

Full exact rerun:

```bash
bash reproduction/reproduce_energy_observability.sh
```

Quick integrity/manifest check without recomputing the expensive tangent series:

```bash
bash reproduction/reproduce_energy_observability.sh --quick
```

Fresh full-run logs are written under `reproduction/results/reproduced_energy_observability/` and are deliberately not part of the mathematical claim unless the invoked checkers exit successfully.

## Expected exact certificates

| Resolution | Reader | State dimension | Translation ceiling | Earliest possible order | Exact attained rank |
|---|---|---:|---:|---:|---:|
| K=1 | total energy | 52 | 49 | 48 | 49 |
| K=1 | 3 shell energies | 52 | 49 | 23 | 49 |
| K=2 | total energy | 248 | 245 | 244 | 245 |
| K=3 | 18 shell energies | 684 | 681 | 39 | 681 |

The K=2 witness uses `F_251`; the K=3 witness uses `F_683`. The earlier K=1 witness uses `F_1000003`. For the stated derivative orders the chosen primes are larger than the relevant Taylor orders, so factorial rescalings are invertible. The scripts also construct the declared rational transverse bases and finite Galerkin operators directly.

## Files

- `checks/check_volume6_ns_observability.py` -- K=1 total- and shell-energy exact witness.
- `checks/check_positive_viscosity_scaling.py` -- exact sanity check for the positive-viscosity scaling identity.
- `checks/check_k2_energy_observability.py` -- K=2 scalar total-energy witness.
- `checks/check_k3_shell_energy_observability.py` -- K=3 18-shell witness.
- `checks/check_energy_observability_manifest.py` -- quick deterministic consistency verifier.
- `results/k2_energy_observability_mod251.json` and `results/k3_shell_energy_observability_mod683.json` -- committed machine-readable certificates.
- `results/energy_observability_manifest_v1.json` -- provenance and expected-invariant manifest.

## Claim boundary

The reproducible statement is finite-dimensional and local: at the certified reader/resolution pairs the jet differential reaches the translation-limited generic local rank at the earliest structurally admissible order, and positive-viscosity scaling transfers each positive-viscosity rank statement across `nu>0` at fixed finite resolution.

This package does **not** prove continuum Navier--Stokes regularity or singularity formation, global injectivity, stable differentiation from noisy physical sensors, a physical sensor layout, or a cheaper reduced propagator. The all-resolution saturation statement in the final paper remains a conjecture outside the certified cases.
