# ObservableFlow v0.5.0

ObservableFlow is an observability-guided design engine for choosing **what to measure, how many spatial channels to retain, and how much temporal depth to use** before a declared reduced state becomes observable and practically reconstructable under explicit stability/error checks.

It is an engineering bridge from the finite-resolution Navier--Stokes observability work in this repository to sensor architecture. It does **not** turn spectral observability theorems into physical-sensor guarantees, and it does not claim that full rank alone implies stable reconstruction.

**v0.5.0 is CLOSED and frozen.** New tuning or broader experiments belong to v0.6 or later.

## Core design problem

For candidate sensors `S` and temporal depth `R`, form the local finite-horizon observation matrix

`O(S,R) = stack_k H_S(k) Phi_k`,

where `Phi_k = dx_k/dx_0`. ObservableFlow evaluates rank, singular values, condition number, sensor cost and temporal cost.

v0.5 adds a stability-aware search that continues past first rank saturation. Full-rank candidates can then be selected on held-out validation reconstruction rather than accepted solely because their Jacobian has full rank.

## What v0.5.0 includes

- local finite-horizon observability matrix construction;
- sensor-noise whitening;
- numerical rank, `sigma_min`, and condition-number diagnostics;
- exhaustive Pareto and scalable greedy search;
- stability-aware greedy candidate generation across temporal depths;
- finite-difference linearization helpers for nonlinear discrete systems;
- Navier--Stokes finite-resolution structural-bound helpers;
- optional FastAPI endpoints `/v1/analyze` and `/v1/optimize`;
- OpenFOAM `postProcessing` adapter with scalar/vector/tensor-like probe parsing and restart merging;
- sampled-state loading, POD reduction and affine LTI reduced-model fitting `(A,C)`;
- OpenFOAM probes-block generation and `observableflow-openfoam` CLI;
- real pinned OpenFOAM-13 cavity CI lane;
- frozen head-to-head comparison against real pinned PySensors `SSPOR + QR + Custom(shared POD basis)`;
- chronological train/validation/untouched-test evaluation and fixed 1%-noise test;
- machine-readable final manifest, closure audit and final technical note.

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

Place the emitted block under `functions { ... }` in `system/controlDict`, run the solver or `postProcess`, then inspect recorded channels:

```bash
observableflow-openfoam inspect-probes CASE \
  --object observableFlowProbes --field p --field U
```

See `OPENFOAM_ADAPTER.md` for the adapter contract and assumptions.

## Frozen v0.5 external benchmark

`[SimulatedData] Simulation=Yes`

The canonical protocol is `benchmarks/openfoam13_cavity/HEAD_TO_HEAD_V05.md`, and the canonical result is `benchmarks/openfoam13_cavity/results/head_to_head_v05.json`.

The final untouched-test comparison is:

| Quantity | ObservableFlow v0.5 | PySensors SSPOR/QR |
|---|---:|---:|
| Spatial channels | **3** | 8 |
| Temporal depth | 4 | 0 |
| Declared total cost | **4.0** | 8.0 |
| Rank | 8/8 | 8/8 |
| Condition number | 106.304 | **8.849** |
| Noiseless full-reference NRMSE | **0.6073** | 0.7676 |
| 1%-noise full-reference NRMSE | **0.6076** | 0.7676 |
| Deployment pass | No | No |

Under the predeclared three-axis Pareto rule `(cost, clean error, noisy error)`, ObservableFlow dominates in this single frozen benchmark. The result does **not** establish general superiority to PySensors or the market. PySensors also has substantially better conditioning in the selected comparison. Both methods fail the predeclared clean-NRMSE deployment gate of `0.50`.

## Canonical closure package

- `closure/OBSERVABLEFLOW_V05_FINAL_MANIFEST.json` — machine-readable frozen evidence and provenance;
- `closure/OBSERVABLEFLOW_V05_CLOSURE_AUDIT.md` — adversarial leakage/fairness/scope audit;
- `closure/OBSERVABLEFLOW_V05_TECHNICAL_NOTE.md` — final technical narrative;
- `closure/CLOSED_V0.5.0.md` — freeze marker and release wording.

## Claim boundary

ObservableFlow v0.5 is an engineering research prototype around a fitted reduced model. The frozen result supports a **benchmark-specific spatial-sensor/temporal-readout advantage** against one pinned static sparse-sensing baseline under one declared cost model.

It does not establish physical CAPEX/OPEX savings, industrial deployment readiness, performance across turbulence/geometry/Reynolds-number regimes, reconstruction of the complete native CFD mesh, closed-loop control performance, or a result on the continuum Navier--Stokes existence-and-smoothness problem.
