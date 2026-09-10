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

## What v0.2 includes

- local finite-horizon observability matrix construction;
- sensor-noise whitening;
- numerical rank, `sigma_min`, and conditioning metrics;
- exhaustive Pareto search for finite candidate sets;
- scalable greedy search for larger sets;
- finite-difference linearization of a nonlinear discrete simulator and scalar readers;
- Navier-Stokes cubic Galerkin structural-bound helpers reproducing the paper anchor values;
- optional FastAPI endpoints `/v1/analyze` and `/v1/optimize`;
- **OpenFOAM adapter** for standard `postProcessing` output:
  - reads scalar/vector/tensor-like `probes` files;
  - merges restart segments by physical time;
  - reads tabular sampled-state snapshots from time directories;
  - performs POD reduction of CFD snapshots;
  - fits an affine LTI Jacobian bridge `(A,C)` from reduced CFD state to probe channels;
  - sends the fitted model directly to the ObservableFlow Pareto/greedy optimizer;
  - generates a `probes` function-object block for `controlDict`;
  - exposes the `observableflow-openfoam` CLI.

## Install and test

```bash
cd software/observableflow
python -m pip install -e '.[dev]'
pytest -q
python examples/two_state_demo.py
python examples/openfoam_synthetic_demo.py
```

Optional API:

```bash
python -m pip install -e '.[api]'
uvicorn observableflow.api:app --reload
```

## OpenFOAM quick start

Generate a probes block:

```bash
observableflow-openfoam generate-probes \
  --field p --field U \
  --location 0,0,0 --location 0.05,0,0
```

Place the emitted block under `functions { ... }` in `system/controlDict`, run the solver (or OpenFOAM `postProcess`), then inspect the recorded channels:

```bash
observableflow-openfoam inspect-probes CASE --object observableFlowProbes --field p --field U
```

For a POD/ROM design run, provide a tabular sampled-state file produced at each OpenFOAM time directory:

```bash
observableflow-openfoam optimize CASE \
  --probe-object observableFlowProbes \
  --field p --field U \
  --snapshot-object stateSample \
  --snapshot-file state.raw \
  --snapshot-skip-columns 3 \
  --pod-rank 12 \
  --max-depth 20 \
  --max-sensors 8 \
  --depth-unit-cost 0.25 \
  --method greedy
```

See `OPENFOAM_ADAPTER.md` for the data contract, model assumptions and current limitations.

## Scope boundary

This package is an engineering algorithm, not a new theorem. The exact finite-field Navier-Stokes certificates remain in `reproduction/checks/`.

The OpenFOAM bridge currently fits a **local/data-driven affine LTI reduced model** from sampled CFD snapshots and probe signals. Its rank/conditioning output is therefore an engineering diagnostic, not a formal certificate for the continuous Navier-Stokes PDE. Native binary `volField` parsing, nonlinear/trajectory-varying Jacobians, physical-device grouping, reconstruction-error benchmarking, and direct OpenFOAM tutorial CI are later milestones.
