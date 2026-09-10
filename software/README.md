# Engineering software

## ObservableFlow

`observableflow/` is the engineering bridge from the repository's finite-resolution Navier--Stokes observability results to sensor × temporal-depth design.

Current version: **0.2.0**.

It includes:

- finite-horizon observability rank and conditioning analysis;
- Pareto and greedy sensor/time optimization;
- optional FastAPI endpoints;
- an OpenFOAM `postProcessing` adapter;
- scalar/vector/tensor-like `probes` parsing with restart merging;
- tabular sampled-state snapshot loading;
- POD reduction;
- affine LTI reduced-model fitting `(A,C)`;
- `controlDict` probes-block generation;
- `observableflow-openfoam` CLI;
- unit and end-to-end synthetic OpenFOAM-layout tests.

Start here: `observableflow/README.md`.

OpenFOAM data contract and scope boundary: `observableflow/OPENFOAM_ADAPTER.md`.

```bash
cd software/observableflow
python -m pip install -e '.[dev,api]'
pytest -q
observableflow-openfoam --help
```

The OpenFOAM bridge is an engineering diagnostic around a fitted reduced model. It is not a formal certificate for the continuous Navier--Stokes PDE, global reconstruction, physical sensor feasibility, or economic savings.
