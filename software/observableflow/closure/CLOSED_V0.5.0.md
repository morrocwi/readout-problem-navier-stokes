# ObservableFlow v0.5.0 — CLOSED

**Closure date:** 2026-09-10  
**Status:** CLOSED  
**Evidence type:** benchmark-specific research prototype  
**Data label:** `[SimulatedData] Simulation=Yes`

ObservableFlow v0.5 is frozen at the evidence state recorded in `OBSERVABLEFLOW_V05_FINAL_MANIFEST.json`.

The final benchmark-specific result is positive on the declared comparison axes but negative on deployment readiness:

- ObservableFlow: 3 spatial channels, temporal depth 4, declared cost 4.0, clean NRMSE 0.6073, 1%-noise NRMSE 0.6076;
- pinned PySensors SSPOR/QR: 8 static channels, declared cost 8.0, clean NRMSE 0.7676, 1%-noise NRMSE 0.7676;
- ObservableFlow Pareto-dominates on the frozen cost/clean-error/noisy-error axes;
- both methods fail the predeclared clean NRMSE <= 0.50 deployment gate;
- no general market-superiority or deployment-ready claim is permitted.

## Freeze rule

Do not modify the v0.5 objective weights, deployment gates, split, upstream pins, test result, or winner rule in place. Any new tuning, additional benchmark, alternative cost model, expanded baseline set, or attempt to improve the deployment result belongs to **ObservableFlow v0.6 or later**.

## Canonical closure files

- `OBSERVABLEFLOW_V05_FINAL_MANIFEST.json` — machine-readable evidence/provenance;
- `OBSERVABLEFLOW_V05_CLOSURE_AUDIT.md` — adversarial scope and leakage audit;
- `OBSERVABLEFLOW_V05_TECHNICAL_NOTE.md` — final technical narrative;
- `CLOSED_V0.5.0.md` — this freeze marker;
- `../benchmarks/openfoam13_cavity/results/head_to_head_v05.json` — frozen numerical result.

## Release wording

Recommended release title:

`ObservableFlow v0.5.0 — frozen OpenFOAM/PySensors benchmark`

Recommended tag:

`observableflow-v0.5.0`

Recommended release summary:

> ObservableFlow v0.5.0 freezes the first matched external head-to-head benchmark of the sensor x temporal-depth design principle. On one pinned OpenFOAM-13 cavity trajectory, using the same training-standardized channels and the same rank-8 training POD basis, ObservableFlow selected 3 spatial channels with temporal depth 4 and Pareto-dominated a pinned PySensors SSPOR/QR static baseline on the declared acquisition-cost, noiseless-NRMSE, and 1%-noise-NRMSE axes of an untouched final test segment. Both methods nevertheless failed the predeclared clean-NRMSE deployment gate. The release therefore records benchmark-specific evidence only; it does not claim deployment readiness or general market superiority.

The GitHub connector used for this closure does not expose release/tag creation. The repository files and closure pointer can therefore be finalized in-chat, while creation of the GitHub Release/tag remains an external repository action unless a release-capable connector is later available.
