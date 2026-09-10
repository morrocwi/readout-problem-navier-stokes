# OpenFOAM Adapter — ObservableFlow v0.2

## Purpose

The adapter connects OpenFOAM post-processing output to ObservableFlow's sensor × temporal-depth optimizer. It does not modify or replace OpenFOAM. The intended chain is:

```text
OpenFOAM case
  -> probes / sampled state output
  -> aligned time series
  -> POD state coordinates
  -> fitted local affine ROM Jacobians A, C
  -> finite-horizon observability matrix
  -> rank + conditioning + sensor/time optimization
```

OpenFOAM function objects are designed to generate post-processing data at runtime or through `postProcess`. The `probes` function object samples fields at declared point locations. ObservableFlow uses that standard `postProcessing/<functionObject>/<time>/...` layout.

## 1. Candidate probes

Generate a block:

```bash
observableflow-openfoam generate-probes \
  --field p --field U \
  --location 0,0,0 \
  --location 0.05,0,0 \
  --location 0.10,0,0
```

The generated OpenCFD-style block is equivalent to:

```text
observableFlowProbes
{
    type                probes;
    libs                (sampling);
    writeControl        timeStep;
    writeInterval       1;
    fixedLocations      true;
    interpolationScheme cellPoint;
    fields              (p U);
    probeLocations
    (
        (0 0 0)
        (0.05 0 0)
        (0.1 0 0)
    );
}
```

Put it inside `functions { ... }` in `system/controlDict`. Library naming and some function-object syntax can differ between OpenFOAM distributions/releases; use the equivalent local syntax when needed.

## 2. Probe data contract

The parser expects the common function-object layout:

```text
CASE/
  postProcessing/
    observableFlowProbes/
      0/
        p
        U
      10/
        p
        U
```

A scalar file may contain:

```text
# Probe 0 (0 0 0)
# Probe 1 (1 0 0)
0.0 101325 101300
0.1 101320 101298
```

A vector file may contain:

```text
# Probe 0 (0 0 0)
# Probe 1 (1 0 0)
0.0 (1 0 0) (0.9 0.1 0)
0.1 (1.1 0 0) (1.0 0.1 0)
```

Vector components become independent optimization channels such as `U[p0].x`, `U[p0].y`, `U[p0].z`. Restart directories are processed in increasing start-time order; a later segment overwrites duplicate physical times.

## 3. State snapshots

Observability relative to a CFD state requires more than probe histories alone. v0.2 therefore accepts one tabular ASCII/CSV-like sampled-state file for every time directory:

```text
CASE/postProcessing/stateSample/0/state.raw
CASE/postProcessing/stateSample/0.1/state.raw
...
```

Each non-comment row is parsed numerically and flattened. `--snapshot-skip-columns N` drops coordinate columns on every row before flattening. This is suitable for sampled sets/surfaces or a custom function object that writes a fixed-layout state sample. Every time must have the same flattened width.

Native binary OpenFOAM `volField` files are deliberately not parsed in v0.2.

## 4. POD and fitted local model

Let the flattened sampled CFD state be `q_t`. ObservableFlow forms a rank-`r` POD basis and coordinates `x_t`. It then fits affine least-squares maps

```text
x_(t+1) ~= A x_t + a

y_t     ~= C x_t + c
```

Only the Jacobians `A` and `C` enter the observability calculation; affine offsets do not. The finite-horizon matrix is built from `C A^k` (or the equivalent time-indexed arrays accepted by the core engine).

The CLI reports POD captured energy plus state-transition and measurement fit RMSE before reporting an optimized design. These fit diagnostics must be inspected; a poor ROM fit invalidates engineering interpretation of the observability result.

## 5. Optimization

Example:

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
  --min-sigma 1e-4 \
  --method greedy
```

`greedy` is intended for larger candidate sets. `pareto` exhaustively enumerates small design spaces and returns nondominated feasible designs.

## Interpretation boundary

A successful design means the **fitted reduced model** meets the requested local rank and conditioning gate. It does not yet prove:

- global state reconstruction;
- stable reconstruction on unseen trajectories;
- correctness for the full PDE or continuum limit;
- physical sensor feasibility at a proposed point;
- lower total plant cost;
- robustness to model mismatch beyond the declared fit/noise model.

The next validation milestone is a real OpenFOAM benchmark with train/test trajectories, static sparse-sensor baselines, reconstruction error under noise, and physical device-level cost grouping.
