# ObservableFlow v0.5: Trading Spatial Sensors for Temporal Readout in Reduced-Order Flow Reconstruction

**Yaoharee Lahtee**  
Open Civil Science Initiative, Bangkok, Thailand  
Version 0.5 closure note — September 2026

`[SimulatedData] Simulation=Yes`

## Abstract

Sensor placement is usually posed as a spatial selection problem: given a reduced representation of a physical system, choose a small set of measurements that preserves enough information for reconstruction or estimation. ObservableFlow v0.5 studies a different but related design degree of freedom: a system may trade **spatial measurement channels** for **temporal readout depth**. Instead of asking only which sensors should be installed, the design variable is a pair `(S,R)`, where `S` is a selected set of measurement channels and `R` is the finite temporal depth used by the observer.

The v0.5 implementation combines a finite-horizon observability matrix, rank and singular-value diagnostics, a stability-aware greedy search, an OpenFOAM adapter, reduced-order modelling, held-out reconstruction, and an external PySensors baseline. The final frozen experiment uses one pinned OpenFOAM Foundation v13 cavity trajectory, 196 standardized scalar channels derived from a 7x7 p,U probe grid, and a common rank-8 POD basis learned on training data. Data are split chronologically into 60% training, 20% validation, and 20% untouched test. ObservableFlow selects three spatial channels at temporal depth four, while the validation-selected PySensors SSPOR/QR baseline uses eight static channels. Under the benchmark's declared cost model, the ObservableFlow design has cost 4.0 versus 8.0 and lower final full-reference NRMSE in both the noiseless and 1%-noise tests. ObservableFlow therefore Pareto-dominates the pinned static baseline on the three declared final-test axes. However, its noiseless NRMSE is about 0.607, above the predeclared deployment gate of 0.50. The correct result is therefore **benchmark-specific superiority on the declared comparison axes without deployment readiness or general market superiority**.

## 1. Problem

Suppose a reduced dynamical state is represented by

\[
x_{t+1}=A x_t+a,
\]

and candidate measurement channels satisfy

\[
y_t=Cx_t+c.
\]

A conventional sparse-sensor formulation chooses a subset of rows of `C`. ObservableFlow additionally allows the observer to retain a finite measurement history. For a selected sensor set `S` and temporal depth `R`, the finite-horizon observation map stacks the selected measurements across time:

\[
\mathcal O_{S,R}
=
\begin{bmatrix}
C_S\\
C_SA\\
C_SA^2\\
\vdots\\
C_SA^R
\end{bmatrix}.
\]

The structural requirement is

\[
\operatorname{rank}(\mathcal O_{S,R})\ge r_{\rm target}.
\]

Rank is necessary but not sufficient. The v0.4 benchmark demonstrated the failure mode directly: a one-channel temporal design reached the requested rank but was catastrophically ill-conditioned and reconstructed poorly. v0.5 therefore adds an explicit stability layer and does not stop at the first full-rank design.

The structural score used during search is

\[
C_{\rm sensor}(S)
+C_{\rm depth}(R)
+0.25\log_{10}\kappa(\mathcal O_{S,R}),
\]

with a declared hard condition-number ceiling. Candidate designs that survive the structural search are evaluated on validation reconstruction. Final design selection uses

\[
C
+0.25\log_{10}\kappa
+4E_{\rm val}
+2E_{\rm val,noise}.
\]

These coefficients are benchmark choices, not universal physical constants.

## 2. Implementation architecture

ObservableFlow v0.5 is implemented as a Python package inside the Navier--Stokes readout repository. Its relevant layers are:

1. **Core observability analysis.** Construction of finite-horizon measurement systems, numerical rank, singular values, condition number, and declared sensor/depth cost.
2. **Stability-aware search.** A deterministic greedy path is grown at every temporal depth. Before full rank, rank gain dominates the local choice; after full rank, the search continues so additional channels may improve conditioning. Every full-rank point is retained for application-level validation.
3. **OpenFOAM adapter.** The package reads standard `postProcessing` outputs for scalar and vector probes, including restarted time segments, and converts them into measurement channels and time series.
4. **Reduced-order bridge.** Training snapshots are standardized using training statistics, projected to a POD basis, and fitted with affine reduced dynamics and measurement maps.
5. **Engineering validation.** Candidate designs are evaluated on held-out data in both noiseless and noisy settings.
6. **External baseline.** The comparison uses the real `dynamicslab/pysensors` project pinned to a specific commit, with `SSPOR`, native `QR`, and the exact same rank-8 training POD basis supplied through PySensors' `Custom` basis interface.

The design intentionally separates structural selection from held-out validation. Test error is not part of the structural optimizer.

## 3. Frozen benchmark protocol

The final v0.5 evidence lane uses:

- OpenFOAM Foundation v13 cavity tutorial at commit `18870c24d21c6b982e2cdec27b2f59738cca5f90`;
- pinned runtime image digest `sha256:a891bb2da102378efc956fb00ff05fc1c686edf38e8343fb87f3603e081ca524`;
- PySensors at commit `65400cd12e2f2b79e8a24d16852dd1371c14aa4e`;
- 401 transient samples;
- 196 scalar channels from p and U on a dense 7x7 probe surrogate;
- rank-8 POD, carrying about 0.9998809 of the training energy under the benchmark's standardized representation;
- chronological split: 240 train, 80 validation, 81 final test samples;
- Gaussian measurement noise with standard deviation 0.01 in training-standardized units;
- at most eight spatial channels and temporal depth at most twelve.

Training is the only segment used to determine standardization, POD, reduced dynamics, measurement fits, and sensor rankings. Validation chooses the final ObservableFlow design and the final PySensors reconstruction method. The test segment is untouched until the final comparison.

The declared deployment gates are:

\[
\kappa\le1000,
\qquad
E_{\rm clean}\le0.50,
\qquad
E_{\rm noise}\le1.00.
\]

No gate is relaxed after observing final test performance.

## 4. Final result

The frozen test result is:

| Quantity | ObservableFlow v0.5 | PySensors SSPOR/QR |
|---|---:|---:|
| Spatial channels | **3** | 8 |
| Temporal depth | 4 | 0 |
| Effective time samples per estimate | 5 | 1 |
| Reduced target rank | 8 | 8 |
| Achieved rank | 8 | 8 |
| Condition number | 106.304 | **8.849** |
| Declared total cost | **4.0** | 8.0 |
| Full-reference noiseless NRMSE | **0.6073** | 0.7676 |
| Full-reference 1%-noise NRMSE | **0.6076** | 0.7676 |
| Deployment pass | No | No |

The selected ObservableFlow channels are two pressure channels and one y-velocity component:

- `p[p7]` at `(0.0125, 0.025, 0.005)`;
- `p[p27]` at `(0.0875, 0.05, 0.005)`;
- `U[p42].y` at `(0.0125, 0.0875, 0.005)`.

Under the declared cost model, the final design reduces the benchmark cost from 8.0 to 4.0, a 50% reduction. It uses 62.5% fewer spatial channels. Relative to the selected PySensors baseline, noiseless NRMSE is lower by about 20.89% and noisy NRMSE by about 20.84%.

The comparison rule is deliberately simple. ObservableFlow Pareto-dominates the baseline only if it is no worse in all three final-test quantities

\[
(C,E_{\rm clean},E_{\rm noise})
\]

and strictly better in at least one. On this frozen benchmark, ObservableFlow is strictly better in all three and is therefore marked as the benchmark-specific Pareto winner.

This does not mean it is better on every engineering property. PySensors has much better static conditioning in the selected result: about 8.85 versus 106.3. The ObservableFlow condition number remains below the declared ceiling but is not evidence of universal numerical superiority.

## 5. Why the negative deployment result matters

The strongest engineering conclusion is not merely that one method won a table. It is that the development sequence separated three distinct claims that are often conflated:

\[
\text{full rank}
\not\Rightarrow
\text{stable inversion}
\not\Rightarrow
\text{held-out reconstruction quality}
\not\Rightarrow
\text{deployment readiness}.
\]

v0.4 exposed the first failure: a rank-complete single-channel design could be unusably ill-conditioned. v0.5 repaired the optimization logic by continuing beyond first rank saturation and by selecting among stable candidates using validation data. The resulting design is dramatically more stable and performs better than the matched static baseline on the frozen test axes.

Yet the final noiseless NRMSE remains above 0.50. Rather than tuning the same benchmark until it crosses the gate, v0.5 is frozen with the failure intact. This protects the distinction between method development and retrospective benchmark fitting.

## 6. What is and is not established

### Established for this frozen benchmark

- A real OpenFOAM solver lane can feed ObservableFlow end to end.
- Spatial sensor count and temporal depth can be optimized jointly in a reduced-order flow reconstruction workflow.
- Stability-aware continuation beyond first full rank avoids at least the catastrophic rank-only design found in the preceding version.
- With the declared cost model, matched representation, frozen split, and pinned PySensors SSPOR/QR baseline, ObservableFlow v0.5 Pareto-dominates on final cost, clean NRMSE, and noisy NRMSE.
- Both methods fail the predeclared clean-error deployment gate.

### Not established

- General superiority to PySensors or other sparse-sensing methods.
- Superiority to commercial digital-twin, observer, or sensor-placement products.
- Industrial sensor savings, CAPEX reduction, or OPEX reduction.
- Performance across geometries, Reynolds numbers, turbulent regimes, forcing conditions, or sensor technologies.
- Reconstruction of the entire native CFD mesh; the dense 7x7 p,U probe set is the benchmark's reference surrogate.
- Stable differentiation or observability guarantees under arbitrary noise.
- Closed-loop control performance.
- Any result concerning continuum Navier--Stokes existence or smoothness.

## 7. Reproducibility

The frozen execution is GitHub Actions run `34487277000`. Its benchmark artifact is named `observableflow-v05-head2head` and has digest

`sha256:70eb6dceb36c55b2fb65ac6c1c8edc1e705a1c2a9476c627dab50c73483d9022`.

The committed final result is

`software/observableflow/benchmarks/openfoam13_cavity/results/head_to_head_v05.json`

with Git blob SHA

`11cb7e7e01fe5436832c436a7311a268fb1623bb`.

The workflow pins both upstream code and the OpenFOAM runtime digest. The temporary Actions artifact may expire, so the committed JSON and the final manifest are the permanent canonical records of the numerical result.

## 8. Closure and next evidentiary step

ObservableFlow v0.5 is closed as a **benchmark-specific research prototype**. The appropriate next experiment is not to continue tuning the frozen cavity lane. It is a new version with independent cases and regimes.

A future v0.6 should pre-register a multi-case suite before final evaluation. At minimum it should vary geometry and flow regime, retain external baselines, use physically motivated sensor and latency costs, and report both reconstruction error and conditioning. A stronger suite should include a genuinely unsteady wake or turbulent case and, eventually, measured physical data.

Until that evidence exists, the correct concise statement is:

> ObservableFlow v0.5 demonstrates, on one frozen OpenFOAM-13 cavity benchmark, that a stability-aware sensor x temporal-depth design can use fewer spatial channels and achieve lower reconstruction error than a pinned PySensors SSPOR/QR static baseline under the benchmark's declared cost model. Both methods fail the frozen deployment-error gate, so the result is evidence for the design principle, not evidence of general market superiority or production readiness.
