# OpenFOAM-13 cavity benchmark

`[SimulatedData] Simulation=Yes`

This benchmark is the first real-solver validation lane for ObservableFlow. It runs the **OpenFOAM Foundation v13** lid-driven cavity tutorial, instruments it with a sparse candidate probe grid and a denser reference probe grid, trains a POD/LTI observability bridge on the first 70% of the transient, selects sensor channels and temporal depth on the training interval only, then reconstructs the reduced reference state on the held-out final 30%.

It is intentionally narrower than a full CFD-state claim: the 7x7 reference grid samples `p` and `U` and acts as a dense observation surrogate. It is not the native full mesh and does not certify nonlinear/global observability.

## Pinned upstream case

- repository: `OpenFOAM/OpenFOAM-13`
- commit: `18870c24d21c6b982e2cdec27b2f59738cca5f90`
- case: `tutorials/incompressibleFluid/cavity`
- upstream `controlDict` declares `solver incompressibleFluid;`, `deltaT 0.005`, and OpenFOAM version 13.

## Measurement architecture

- candidate grid: 4x4 interior locations, `p` and `U` recorded each time step;
- dense reference grid: 7x7 interior locations, `p` and `U` recorded each time step;
- default reduced state: rank-4 POD fit on training data only;
- pressure-only and pressure+velocity candidate designs are both reported;
- injected robustness test: Gaussian noise at 1% of each training channel's standard deviation;
- pressure channel cost = 1, velocity component channel cost = 2, temporal-depth cost = 0.25 per step.

These costs are declared benchmark weights, not market prices.

## Reproduce with Docker

The GitHub workflow uses a containerized v13 runtime and records the resolved image digest in the result JSON. A local equivalent is:

```bash
python -m pip install -e 'software/observableflow[dev,api]'

# obtain the pinned upstream cavity tutorial, then:
python software/observableflow/benchmarks/openfoam13_cavity/prepare_case.py /path/to/cavity

docker run --rm -v /path/to/cavity:/home/openfoam/data dicehub/openfoam:13 \
  "blockMesh && foamRun"

python software/observableflow/benchmarks/openfoam13_cavity/analyze_case.py \
  /path/to/cavity \
  --output software/observableflow/benchmarks/openfoam13_cavity/results/cavity_v13_result.json
```

The Docker image is a third-party packaging of the Foundation release, not an OpenFOAM Foundation image. The **solver case itself is pinned to the official OpenFOAM Foundation repository**. The CI result records the exact pulled image digest so the environment can be pinned after the first successful run.

## Claim boundary

A successful run establishes an executable engineering benchmark: OpenFOAM solver output can be passed through the ObservableFlow train/select/hold-out reconstruction pipeline. It does **not** establish a universal sensor optimum, full-field CFD reconstruction, hardware performance, economic savings, or continuum Navier-Stokes observability.
