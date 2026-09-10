# ObservableFlow MVP

ObservableFlow is an observability-guided design engine for choosing **what to measure, how many channels to retain, and how much temporal depth to use** before a local dynamical state becomes observable to a declared rank/conditioning target.

It is the engineering bridge from the finite-resolution energy-observability results in `paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.*` to practical sensor architecture. It does **not** claim that the current spectral shell readers are deployable physical sensors, nor that rank alone guarantees stable state reconstruction.

## Core design problem

For candidate sensors `S` and finite temporal depth `R`, build the local finite-horizon observability matrix

`O(S,R) = stack_k H_S(k) Phi_k`,

where `Phi_k = dx_k/dx_0`. The engine evaluates rank, smallest retained singular value, condition number, sensor cost, and temporal cost, then searches for low-cost feasible designs.

The practical optimization target is approximately

`min C_sensor(S) + C_time(R)`

subject to

`rank O(S,R) >= target_rank` and `sigma_min(O(S,R)) >= epsilon`.

## What v0.1 includes

- local finite-horizon observability matrix construction;
- sensor-noise whitening;
- numerical rank, `sigma_min`, and conditioning metrics;
- exhaustive Pareto search for finite candidate sets;
- scalable greedy search for larger sets;
- finite-difference linearization of a nonlinear discrete simulator and scalar readers;
- Navier-Stokes cubic Galerkin structural-bound helpers reproducing the anchor values:
  - K=1: d=52, 3 shells, scalar Rmin=48, shell Rmin=23;
  - K=2: d=248, 9 shells, scalar Rmin=244;
  - K=3: d=684, 18 shells, scalar Rmin=680, shell Rmin=39;
- optional FastAPI endpoints `/v1/analyze` and `/v1/optimize`.

## Install and test

```bash
cd software/observableflow
python -m pip install -e '.[dev]'
pytest -q
python examples/two_state_demo.py
```

Optional API:

```bash
python -m pip install -e '.[api]'
uvicorn observableflow.api:app --reload
```

## Scope boundary

This MVP is an engineering algorithm, not a new theorem. The exact finite-field Navier-Stokes certificates remain in `reproduction/checks/`. The current optimizer uses local linearized finite-horizon observability and SVD conditioning. A later CFD adapter should supply trajectory Jacobians/readers from OpenFOAM or another solver and should be benchmarked against static sparse-sensor baselines.
