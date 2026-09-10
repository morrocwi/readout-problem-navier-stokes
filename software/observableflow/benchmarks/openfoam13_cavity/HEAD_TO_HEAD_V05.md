# ObservableFlow v0.5 vs PySensors — head-to-head protocol and verified result

`[SimulatedData] Simulation=Yes`

This lane asks a narrower question than market superiority:

> On the same OpenFOAM-13 cavity trajectory, the same standardized measurement channels, and the same POD basis, can a stability-aware **sensor x temporal-depth** design outperform a mature static sparse-sensor baseline on held-out reconstruction cost and error?

A positive result is benchmark-specific. A negative result is retained unchanged.

## Verified result

GitHub Actions run: `34487277000`

Result artifact committed at:

`software/observableflow/benchmarks/openfoam13_cavity/results/head_to_head_v05.json`

The real-solver workflow completed successfully through external-baseline installation, pinned OpenFOAM execution, head-to-head analysis, result validation, artifact upload, and commit-back to `main`.

On the untouched final test interval:

| Method | Spatial scalar channels | Temporal depth | Declared total cost | Rank | Condition number | Noiseless NRMSE | 1%-noise NRMSE | Deployment gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ObservableFlow v0.5 | 3 | 4 | 4.0 | 8/8 | 106.304 | 0.607257 | 0.607581 | FAIL |
| PySensors SSPOR/QR | 8 | 0 | 8.0 | 8/8 | 8.849 | 0.767630 | 0.767581 | FAIL |

ObservableFlow selected two pressure channels and one y-velocity channel, with depth 4 (five consecutive time samples including the initial sample). PySensors selected eight simultaneous scalar channels and its validation-selected regularized reconstruction.

Under the **predeclared three-coordinate Pareto rule** (declared total cost, noiseless NRMSE, noisy NRMSE), ObservableFlow Pareto-dominates PySensors on this test: it has lower declared cost and lower reconstruction error in both noise conditions. Relative to the PySensors result, the declared total cost is 50% lower and NRMSE is about 20.9% lower in the noiseless test and 20.8% lower in the noisy test.

This does **not** mean ObservableFlow dominates on every property. PySensors has substantially better conditioning (`8.849` versus `106.304`). Both are below the declared condition-number ceiling of 1000, but ObservableFlow still fails the deployment gate because its noiseless full-reference NRMSE (`0.607257`) exceeds the predeclared `0.50` threshold. PySensors fails the same accuracy gate at `0.767630`.

Therefore the verified conclusion is:

> **Benchmark-specific advantage: YES. Deployment-ready: NO. General market superiority: NOT ESTABLISHED.**

The threshold was not changed after observing the result.

## External baseline pin

The baseline is the real external project [`dynamicslab/pysensors`](https://github.com/dynamicslab/pysensors), pinned to commit:

`65400cd12e2f2b79e8a24d16852dd1371c14aa4e`

The benchmark uses PySensors `SSPOR` with its native `QR` optimizer and its native `Custom` basis interface. The custom basis is set to the **exact same training POD basis** used by ObservableFlow. Both PySensors unregularized and regularized reconstruction are evaluated on validation data; the better validation-selected method is frozen before final test evaluation.

## Common data and representation

The real solver lane reruns the pinned OpenFOAM Foundation v13 cavity tutorial and reads the 7x7 reference probe grid already defined by this repository.

- fields: `p` and `U`;
- scalar channels: 196;
- standardization: per-channel mean/std from **training data only**;
- reduced state: rank-8 POD from standardized training data only;
- common candidate channels: all 196 standardized scalar channels;
- common POD basis: exactly the same matrix for both methods;
- channel cost: 1 per scalar channel;
- ObservableFlow temporal-depth cost: 0.25 per step;
- injected measurement noise: Gaussian sigma = 0.01 in training-standardized units.

The 7x7 probe grid is a dense sampled reference surrogate, not the native CFD mesh.

## Anti-leakage split

The 401-sample transient is split chronologically:

- first 60%: **train** — fit standardization, POD, ROM, ObservableFlow structural search, and PySensors sensor ranking;
- next 20%: **validation** — choose the final ObservableFlow design and PySensors reconstruction method;
- final 20%: **test** — untouched until the final comparison.

No test metric is used for sensor selection, model fitting, hyperparameter choice, or method selection.

## ObservableFlow v0.5

The v0.5 stability-aware search differs from the original rank-first greedy lane in one important way: it does **not stop when rank first reaches the target**. It continues adding channels and retains full-rank designs across temporal depths so that conditioning can improve.

Structural candidate score:

```text
sensor_cost + depth_cost + 0.25*log10(condition_number)
```

Validation selection score:

```text
cost + 0.25*log10(condition_number)
     + 4*validation_NRMSE
     + 2*validation_noisy_NRMSE
```

The coefficients are declared benchmark weights, not universal physical constants.

## Declared engineering gates

A design is marked deployment-pass in this benchmark only if:

```text
condition_number <= 1000
noiseless NRMSE <= 0.50
1%-noise NRMSE <= 1.00
```

These are engineering benchmark gates, not theorems. They were declared before the final head-to-head run and were not relaxed after seeing the test result.

## Comparison rule

The result JSON reports both a common scalar objective and Pareto dominance on final test data.

ObservableFlow Pareto-dominates PySensors only if it is no worse in all three of:

1. declared total acquisition cost;
2. noiseless full-reference NRMSE;
3. noisy full-reference NRMSE;

and is strictly better in at least one.

The reverse rule defines PySensors dominance. If neither condition holds, the result is a trade-off rather than a winner.

Condition number is reported separately and is enforced by the deployment gate, but it is not one of the three coordinates in this particular Pareto rule. This distinction is important because PySensors is much better conditioned in the verified test.

## Claim boundary

This benchmark does **not** establish general market superiority. One cavity trajectory does not establish superiority across turbulence regimes, geometries, Reynolds numbers, sensor modalities, hardware, industrial constraints, other sparse-sensor algorithms, or commercial products.

The positive benchmark-specific result justifies the next evidentiary step: a preregistered multi-case OpenFOAM suite with multiple flow regimes, multiple seeds/noise levels, and additional baselines. Deployment claims require the declared accuracy gate to pass on unseen cases rather than merely outperforming another method that also fails it.
