# OpenFOAM-13 cavity benchmark

`[SimulatedData] Simulation=Yes`

This benchmark is the first real-solver validation lane for ObservableFlow. It runs the **OpenFOAM Foundation v13** lid-driven cavity tutorial, instruments it with a sparse candidate probe grid and a denser reference probe grid, trains a POD/LTI observability bridge on the first 70% of the transient, selects sensor channels and temporal depth on the training interval only, then reconstructs the reduced reference state on the held-out final 30%.

It is intentionally narrower than a full CFD-state claim: the 7x7 reference grid samples `p` and `U` and acts as a dense observation surrogate. It is not the native full mesh and does not certify nonlinear/global observability.

## Pinned upstream case

- repository: `OpenFOAM/OpenFOAM-13`
- commit: `18870c24d21c6b982e2cdec27b2f59738cca5f90`
- case: `tutorials/incompressibleFluid/cavity`
- runtime image: `dicehub/openfoam@sha256:a891bb2da102378efc956fb00ff05fc1c686edf38e8343fb87f3603e081ca524`
- upstream `controlDict` declares `solver incompressibleFluid;`, `deltaT 0.005`, and OpenFOAM version 13.

The Docker image is third-party packaging of the Foundation release, not an OpenFOAM Foundation image. The solver case itself is pinned to the official OpenFOAM Foundation repository.

## Measurement architecture

- candidate grid: 4x4 interior locations, `p` and `U` recorded each time step;
- dense reference grid: 7x7 interior locations, `p` and `U` recorded each time step;
- default reduced state: rank-4 POD fit on training data only;
- pressure-only and pressure+velocity candidate designs are both reported;
- injected robustness test: Gaussian noise at 1% of each training channel's standard deviation;
- pressure channel cost = 1, velocity component channel cost = 2, temporal-depth cost = 0.25 per step.

These costs are declared benchmark weights, not market prices.

## Verified result — 2026-09-10

GitHub Actions real-solver run `34484321108` completed the pinned OpenFOAM solve, analysis, artifact validation, upload, and result commit successfully. The benchmark result is stored at `results/cavity_v13_result.json`.

The first rank-only result was a false positive for deployment. A single pressure channel with temporal depth 3 reaches rank 4, but its noise-whitened observability matrix has condition number about `2.06e6`. On the untouched 30% hold-out interval it gives NRMSE about `115.3` without injected sensor noise and about `1242.4` with 1% training-channel noise. It is therefore structurally rank-feasible but practically unstable in this benchmark.

The static multimodal design is much more stable. It selects four scalar channels, has condition number about `4.29`, and gives hold-out NRMSE about `0.5253` without injected noise and `0.5251` with the 1% noise test. This is a large improvement, but it narrowly misses the declared noiseless deployment gate of `NRMSE <= 0.50`.

Accordingly the v0.4 deployment verdict is **FAIL for the tested design family**. This is a valid negative engineering result, not a workflow failure. The declared gates are:

- condition number `<= 1000`;
- noiseless hold-out NRMSE `<= 0.50`;
- noisy hold-out NRMSE `<= 1.00`.

These are explicit engineering benchmark gates, not theorems or universal physical thresholds. They must not be relaxed post hoc merely to convert this result into a pass.

## Reproduce with Docker

```bash
python -m pip install -e 'software/observableflow[dev,api]'

# obtain the pinned upstream cavity tutorial, then:
python software/observableflow/benchmarks/openfoam13_cavity/prepare_case.py /path/to/cavity
chmod -R a+rwX /path/to/cavity

docker run --rm -v /path/to/cavity:/home/openfoam/data \
  dicehub/openfoam@sha256:a891bb2da102378efc956fb00ff05fc1c686edf38e8343fb87f3603e081ca524 \
  "cd /home/openfoam/data && blockMesh && foamRun"

python software/observableflow/benchmarks/openfoam13_cavity/analyze_case.py \
  /path/to/cavity \
  --output software/observableflow/benchmarks/openfoam13_cavity/results/cavity_v13_result.json
```

## Claim boundary

A successful workflow run establishes an executable engineering benchmark: real OpenFOAM solver output can be passed through the ObservableFlow train/select/hold-out reconstruction pipeline with pinned source/runtime provenance. It does **not** establish a universal sensor optimum, full-field CFD reconstruction, hardware performance, economic savings, or continuum Navier-Stokes observability.

The verified v0.4 result supports a narrower and scientifically useful conclusion: **finite-horizon rank sufficiency alone is not enough for deployable flow-state reconstruction; conditioning and untouched hold-out performance are necessary additional gates.** In this cavity test, the cheapest temporal rank-sufficient design fails badly, while a four-channel static multimodal design is stable but still slightly outside the declared accuracy gate.
