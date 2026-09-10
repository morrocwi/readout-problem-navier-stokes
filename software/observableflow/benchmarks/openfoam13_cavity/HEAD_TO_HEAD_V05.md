# ObservableFlow v0.5 vs PySensors — head-to-head protocol

`[SimulatedData] Simulation=Yes`

This lane asks a narrower question than market superiority:

> On the same OpenFOAM-13 cavity trajectory, the same standardized measurement channels, and the same POD basis, can a stability-aware **sensor x temporal-depth** design outperform a mature static sparse-sensor baseline on held-out reconstruction cost and error?

A positive result is benchmark-specific. A negative result is retained unchanged.

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

These are engineering benchmark gates, not theorems. They are declared before the final head-to-head run and must not be relaxed after seeing the test result.

## Comparison rule

The result JSON reports both a common scalar objective and Pareto dominance on final test data.

ObservableFlow Pareto-dominates PySensors only if it is no worse in all three of:

1. declared total acquisition cost;
2. noiseless full-reference NRMSE;
3. noisy full-reference NRMSE;

and is strictly better in at least one.

The reverse rule defines PySensors dominance. If neither condition holds, the result is a trade-off rather than a winner.

## Claim boundary

Even if ObservableFlow wins this benchmark, the repository must **not** claim general market superiority. One cavity trajectory does not establish superiority across turbulence regimes, geometries, Reynolds numbers, sensor modalities, hardware, industrial constraints, or competing commercial products.

The next evidentiary step after a positive result is a multi-case benchmark suite. After a negative result, the correct next step is to diagnose the failure without changing the declared test gate retroactively.
