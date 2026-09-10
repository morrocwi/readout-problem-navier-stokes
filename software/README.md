# Engineering software

## ObservableFlow

`observableflow/` is the engineering bridge from the repository's finite-resolution Navier--Stokes observability results to **sensor × temporal-depth design**.

Current frozen version: **0.5.0**.

It includes:

- finite-horizon observability rank, singular-value and conditioning analysis;
- Pareto/greedy sensor-time optimization plus the v0.5 stability-aware search;
- optional FastAPI endpoints;
- an OpenFOAM `postProcessing` adapter;
- scalar/vector/tensor-like `probes` parsing with restart merging;
- sampled-state loading, POD reduction and affine reduced-model fitting;
- `controlDict` probes-block generation and `observableflow-openfoam` CLI;
- a real pinned OpenFOAM-13 cavity benchmark;
- a matched external head-to-head lane against pinned PySensors `SSPOR + QR`;
- train/validation/untouched-test evaluation with declared noise and deployment gates.

Start here: `observableflow/README.md`.

OpenFOAM data contract: `observableflow/OPENFOAM_ADAPTER.md`.

Frozen v0.5 head-to-head protocol and result:

- `observableflow/benchmarks/openfoam13_cavity/HEAD_TO_HEAD_V05.md`
- `observableflow/benchmarks/openfoam13_cavity/results/head_to_head_v05.json`

Canonical v0.5 closure package:

- `observableflow/closure/OBSERVABLEFLOW_V05_FINAL_MANIFEST.json`
- `observableflow/closure/OBSERVABLEFLOW_V05_CLOSURE_AUDIT.md`
- `observableflow/closure/OBSERVABLEFLOW_V05_TECHNICAL_NOTE.md`
- `observableflow/closure/CLOSED_V0.5.0.md`

```bash
cd software/observableflow
python -m pip install -e '.[dev,api]'
pytest -q
observableflow-openfoam --help
```

### Frozen result boundary

On the single frozen OpenFOAM-13 cavity head-to-head, ObservableFlow v0.5 uses 3 spatial channels plus temporal depth 4 and Pareto-dominates the pinned PySensors static baseline on the benchmark's declared acquisition-cost, noiseless-NRMSE and 1%-noise-NRMSE axes. Both methods fail the predeclared noiseless-NRMSE deployment gate.

Therefore v0.5 is closed as a **benchmark-specific research prototype**. It does not establish general market superiority, production readiness, physical sensor savings, multi-regime generalization, or any claim about the continuous Navier--Stokes existence/smoothness problem. New tuning or broader experiments belong to v0.6 or later.
