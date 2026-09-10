# ObservableFlow Future Work — v0.6 and Beyond

Status: active roadmap after the frozen v0.5.0 evidence lane  
Date: 2026-09-10  
Data status for future numerical lanes: `[SimulatedData] Simulation=Yes` unless measured physical data are explicitly used.

## Boundary

ObservableFlow v0.5.0 is closed. Its benchmark objective, gates, split, upstream pins, final test metrics, and claim boundary are immutable evidence. This document is deliberately separate from `closure/` so that future development cannot be mistaken for retrospective tuning of v0.5.

Any change to the design objective, cost model, candidate sensors, temporal depth, reduced-model class, benchmark suite, reconstruction method, noise model, or deployment gate belongs to a new version.

## v0.6 — preregistered multi-case validation

The next evidentiary step is a new benchmark suite designed before final test evaluation.

Minimum suite:

1. at least three independent CFD cases rather than one cavity trajectory;
2. variation in geometry and operating regime;
3. at least one genuinely unsteady wake or stronger transient case;
4. retained external sparse-sensing baselines, including PySensors where compatible;
5. a fixed train/validation/test policy declared before final scoring;
6. clean and noisy reconstruction metrics reported for every case, including failures;
7. condition number and singular-spectrum diagnostics reported alongside error;
8. a predeclared aggregation rule across cases rather than choosing the best case after evaluation.

Primary v0.6 question:

> Does the spatial-sensor / temporal-readout trade remain useful across independently specified flow cases, or was the v0.5 advantage specific to one cavity benchmark?

A positive v0.6 result must require cross-case evidence. A single additional winning case is not sufficient for a general claim.

## v0.6 cost model hardening

The v0.5 declared cost was intentionally simple. v0.6 should separate at least:

- spatial hardware/channel cost;
- sampling and acquisition cost;
- temporal latency cost;
- storage/history cost;
- computation/reconstruction cost;
- synchronization or multiplexing cost where relevant.

A general cost interface should take the form

\[
C_{\mathrm{deploy}}(S,R)
= C_{\mathrm{sensor}}(S)
+ C_{\mathrm{latency}}(R)
+ C_{\mathrm{storage}}(S,R)
+ C_{\mathrm{compute}}(S,R),
\]

with every term declared before benchmark selection. This is a future design equation, not a v0.5 result.

## v0.7 — robustness and model mismatch

After multi-case replication, test robustness to conditions that the current fitted affine reduced model does not capture well:

- reduced-order model mismatch;
- nonlinear or locally linear observers;
- nonstationary measurement noise;
- missing channels and sensor dropout;
- asynchronous or delayed measurements;
- temporal jitter;
- perturbations outside the training operating range;
- uncertainty in the transition model and measurement map.

The key question is whether temporal depth still buys spatial-channel reduction when the dynamics used by the observer are imperfect.

## v0.8 — estimator and uncertainty layer

The current v0.5 reconstruction is a finite-window inverse problem. A later version should compare against state-estimation methods that update uncertainty sequentially, for example Kalman-family or nonlinear Bayesian observers when assumptions permit.

Required outputs should include uncertainty calibration, failure detection, and a fail-closed rule when observability or conditioning becomes inadequate.

No claim of stable noisy observability should be made until this lane is tested directly.

## Physical-data lane

The strongest engineering step is measured physical data. Candidate experiments include a benchtop flow system, PIV-derived reference field with sparse physical probes, or an instrumented duct/wake setup.

The physical-data lane must distinguish:

- real sensor count from derived CFD channels;
- physical latency from algorithmic temporal depth;
- calibration error from model error;
- sensor noise from numerical noise;
- true reference uncertainty from reconstruction error.

Only after this lane should the project discuss hardware savings as empirical evidence rather than a benchmark interpretation.

## Closed-loop control lane

Reconstruction quality does not imply control performance. Closed-loop work therefore remains separate.

A future control study should compare sensor/readout designs under the same controller or jointly optimize sensing and control while preserving a held-out evaluation protocol. Report stability, control effort, constraint violations, and failure recovery in addition to state reconstruction error.

## Theory lane

The finite-dimensional engineering package should remain distinct from continuum Navier--Stokes claims. High-value theoretical work includes:

- conditions under which temporal readout can replace simultaneous spatial channels in finite-dimensional reduced systems;
- lower bounds connecting state dimension, sensor count, temporal depth, and rank;
- conditioning/noise amplification bounds beyond rank alone;
- observability under time-varying local Jacobians;
- identifiability of the sensor-depth cost frontier;
- links between the engineering observation matrix and the exact finite Fourier--Galerkin readout results elsewhere in this repository.

These are open research directions unless separately proved or exactly certified.

## Evidence discipline for all future versions

Every new benchmark version should preserve the v0.5 discipline:

1. freeze objective, gates, cost model, data split, and upstream versions before final test evaluation;
2. fit preprocessing, POD/reduced model, and sensor ranking on training data only;
3. use validation for design/model selection;
4. touch the final test set only after selection is frozen;
5. commit machine-readable results and provenance;
6. keep negative results and failed gates visible;
7. distinguish simulation, exact finite computation, and measured physical data;
8. never overwrite a closed evidence lane.

## Immediate next implementation target

The next code-bearing milestone is **ObservableFlow v0.6 preregistration**, not another v0.5 cavity tuning pass. It should define the multi-case suite, cross-case scoring rule, physical/latency-aware cost interface, baselines, noise protocol, and success/failure criteria before running final held-out comparisons.
