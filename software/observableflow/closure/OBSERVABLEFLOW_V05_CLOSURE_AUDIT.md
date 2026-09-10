# ObservableFlow v0.5 — Adversarial Closure Audit

**Status:** PASS WITH SCOPE LIMITATIONS  
**Closure date:** 2026-09-10  
**Evidence lane:** `[SimulatedData] Simulation=Yes`  
**Frozen benchmark execution commit:** `0355cb94b10f5698378298b9a03512009265ce97`  
**Frozen result blob:** `11cb7e7e01fe5436832c436a7311a268fb1623bb`  
**Workflow run:** `34487277000`

This audit is intentionally narrower than a software-security audit or a general scientific peer review. It asks whether the v0.5 OpenFOAM-vs-PySensors result is internally coherent enough to freeze as a benchmark-specific research result without silently upgrading it into a market-superiority or deployment claim.

## 1. Audit question

The frozen question is:

> On one pinned OpenFOAM-13 cavity trajectory, using the same train-standardized 196 scalar measurement channels and the same rank-8 training POD basis, can ObservableFlow's stability-aware sensor x temporal-depth design beat a pinned PySensors SSPOR/QR static sparse-sensor baseline on the declared acquisition-cost, noiseless reconstruction-error, and 1%-noise reconstruction-error axes of an untouched final test segment?

The audit does **not** ask whether ObservableFlow is generally better than PySensors, whether the temporal-cost coefficient is economically correct, or whether the system is production ready.

## 2. Data leakage audit — PASS

The comparison code performs a chronological 60/20/20 split. Training statistics (`mu`, `sd`), the POD basis, the reduced trajectory, affine dynamics/measurement fits, and sensor-ranking models are derived from the training portion. ObservableFlow candidate design and PySensors reconstruction method are selected on validation. Final metrics are then computed on the final test segment.

The PySensors test helper recomputes predictions for candidate sensor counts from the already training-fitted model, but the final test candidate is selected by exact identity with the validation-selected method and selected sensor indices. No test metric is used to choose that identity. This is computationally broader than necessary but does not create a selection leak in the current code path.

**Finding:** no blocking train/validation/test leakage was identified in the frozen v0.5 lane.

## 3. Representation fairness audit — PASS

Both methods receive the same standardized 196 scalar channels. The standardization parameters are training-only. Both methods use the same rank-8 POD basis learned on training data. PySensors is instantiated with its native `SSPOR`, `QR`, and `Custom` basis interface; the external dependency is pinned to commit `65400cd12e2f2b79e8a24d16852dd1371c14aa4e`.

ObservableFlow uses its finite-horizon observation system; PySensors is evaluated as a static sparse-sensor baseline at temporal depth zero. This asymmetry is the object of the experiment rather than an accidental mismatch: the benchmark explicitly asks whether temporal history can substitute for spatial sensors.

**Finding:** representation and candidate-channel inputs are matched closely enough for the declared benchmark question.

## 4. Objective and gate audit — PASS, BENCHMARK-SPECIFIC

The frozen selection objective is:

```text
cost + 0.25*log10(kappa)
     + 4*validation_NRMSE
     + 2*validation_noisy_NRMSE
```

The deployment gates are:

```text
condition number <= 1000
noiseless NRMSE <= 0.50
1%-noise NRMSE <= 1.00
```

These numbers are declared engineering benchmark choices, not physical constants or theorems. The final test result is not allowed to relax them. Both methods fail the noiseless-NRMSE gate, and the frozen result preserves that failure.

**Finding:** no post-hoc threshold relaxation was found. The cost and gate values must remain labelled as benchmark assumptions.

## 5. Winner-rule audit — PASS

The final Pareto rule compares only three declared axes:

1. total acquisition cost under the benchmark cost model;
2. full-reference noiseless NRMSE;
3. full-reference 1%-noise NRMSE.

ObservableFlow is marked as dominating only if it is no worse on all three and strictly better on at least one. The workflow explicitly validates the artifact **without forcing a winner** and asserts that the general `market_superiority_claim` remains false.

Frozen test values:

| Quantity | ObservableFlow v0.5 | PySensors SSPOR/QR |
|---|---:|---:|
| Spatial channels | 3 | 8 |
| Temporal depth | 4 | 0 |
| Declared total cost | 4.0 | 8.0 |
| Rank | 8/8 | 8/8 |
| Condition number | 106.3039898 | 8.8488199 |
| Noiseless full-reference NRMSE | 0.6072567 | 0.7676302 |
| 1%-noise full-reference NRMSE | 0.6075815 | 0.7675811 |
| Deployment pass | No | No |

Under the declared three-axis Pareto rule, ObservableFlow dominates on this test. PySensors has substantially better conditioning, which is retained in the result and must not be hidden when discussing engineering robustness.

## 6. Reproducibility/provenance audit — PASS

The real-solver workflow pins:

- OpenFOAM Foundation v13 cavity source commit: `18870c24d21c6b982e2cdec27b2f59738cca5f90`;
- PySensors commit: `65400cd12e2f2b79e8a24d16852dd1371c14aa4e`;
- OpenFOAM runtime digest: `sha256:a891bb2da102378efc956fb00ff05fc1c686edf38e8343fb87f3603e081ca524`;
- benchmark execution commit: `0355cb94b10f5698378298b9a03512009265ce97`.

GitHub Actions run `34487277000` completed successfully through solver execution, benchmark execution, artifact validation, upload, and result commit. The uploaded artifact digest is `sha256:70eb6dceb36c55b2fb65ac6c1c8edc1e705a1c2a9476c627dab50c73483d9022`. The Actions artifact is temporary, but the result JSON is permanently committed to the repository at the frozen blob SHA recorded in the manifest.

## 7. Blocking defects found

**None identified for the narrow frozen benchmark claim.**

This means only that the current code/result pair supports the benchmark-specific statement recorded in the final manifest. It is not a declaration that the implementation is free of all numerical, software, modelling, or external-validity defects.

## 8. Residual risks that prevent stronger claims

### Single trajectory / single geometry

The evidence is one transient cavity trajectory. There is no demonstrated generalization across Reynolds numbers, geometries, forcing regimes, turbulence, sensor modalities, or physical hardware.

### Benchmark cost model is not an economic model

The scalar channel cost `1.0` and temporal depth cost `0.25` are declared experimental weights. The observed 50% reduction is therefore a **declared benchmark-cost reduction**, not a demonstrated 50% industrial CAPEX/OPEX saving.

### Static-vs-temporal conditioning is not a universal robustness comparison

ObservableFlow's reported condition number is for a finite-horizon observation system; PySensors' is for the selected static POD-basis rows. Both are meaningful internally, but they are not evidence that one package is universally more numerically robust. In this frozen result, PySensors has the smaller condition number.

### Deployment gate fails

ObservableFlow's final noiseless NRMSE is about `0.6073`, above the frozen `0.50` gate. The benchmark therefore cannot support a deployment-ready claim even though ObservableFlow wins the declared Pareto comparison.

### Dense probe surrogate is not the native CFD field

The 7x7 p,U grid is a dense sampled reference surrogate, not the entire native CFD mesh. “Full-reference” in this benchmark means full reference **within that sampled surrogate**.

## 9. Allowed wording after closure

Safe concise wording:

> In one frozen OpenFOAM-13 cavity benchmark with matched training representation and an untouched final test segment, ObservableFlow v0.5 used 3 spatial channels plus temporal depth 4 and Pareto-dominated a pinned PySensors SSPOR/QR static baseline on the benchmark's declared acquisition-cost, noiseless-NRMSE, and 1%-noise-NRMSE axes. Both methods nevertheless failed the predeclared noiseless NRMSE deployment gate, so the result is benchmark-specific evidence, not a market-superiority or deployment claim.

## 10. Forbidden wording after closure

Do not state or imply:

- “ObservableFlow is better than PySensors” without the single-benchmark qualifier;
- “ObservableFlow is better than the market”;
- “ObservableFlow cuts real sensor cost by 50%”;
- “ObservableFlow is deployment ready”;
- “3 sensors are sufficient for Navier-Stokes flows in general”;
- “the benchmark validates turbulent/industrial operation”;
- “the software solves the Navier-Stokes Millennium problem.”

## Closure verdict

`PASS WITH SCOPE LIMITATIONS`.

The v0.5 evidence lane is suitable to freeze. Further model tuning, different objective weights, new cost models, broader baselines, additional flows, or attempts to cross the deployment gate must be versioned as **v0.6 or later** and must not overwrite the frozen v0.5 result.
