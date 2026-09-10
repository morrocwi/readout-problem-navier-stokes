from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Sequence
import json
import numpy as np

from .core import AnalysisResult
from .openfoam import ProbeDataset, PODReduction, load_probes, pod_reduce_snapshots, fit_lti_probe_model, _align_times


@dataclass(frozen=True)
class ReconstructionMetrics:
    windows: int
    rmse: float
    nrmse: float
    median_l2_error: float
    p95_l2_error: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ProbeReferenceBenchmarkResult:
    n_times: int
    n_train: int
    n_test: int
    reference_channels: int
    candidate_channels: int
    pod_rank: int
    pod_train_energy_fraction: float
    train_state_one_step_rmse: float
    train_measurement_rmse: float
    temporal_design: dict | None
    static_design: dict | None
    holdout_noiseless: dict | None
    holdout_noisy: dict | None
    noise_fraction_of_train_std: float
    candidate_object: str
    reference_object: str
    candidate_fields: tuple[str, ...]
    reference_fields: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def _subset_probe_dataset(ds: ProbeDataset, idx: np.ndarray) -> ProbeDataset:
    return ProbeDataset(
        ds.times[idx], ds.values[idx], ds.channel_names, ds.channel_locations,
        ds.fields, ds.source_files,
    )


def _fit_affine(X: np.ndarray, Y: np.ndarray, ridge: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    Z = np.column_stack([X, np.ones(len(X))])
    if ridge <= 0:
        beta = np.linalg.lstsq(Z, Y, rcond=None)[0]
    else:
        reg = np.eye(Z.shape[1]) * float(ridge)
        reg[-1, -1] = 0.0
        beta = np.linalg.solve(Z.T @ Z + reg, Z.T @ Y)
    return beta[:-1], beta[-1]


def _affine_observation_system(
    A: np.ndarray,
    C: np.ndarray,
    state_offset: np.ndarray,
    measurement_offset: np.ndarray,
    selected: Sequence[int],
    depth: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return y_stack = O x0 + q for selected channels over k=0..depth."""
    A = np.asarray(A, dtype=float)
    C = np.asarray(C, dtype=float)
    a = np.asarray(state_offset, dtype=float)
    c = np.asarray(measurement_offset, dtype=float)
    sel = np.asarray(tuple(selected), dtype=int)
    n = A.shape[0]
    phi = np.eye(n)
    b = np.zeros(n)
    rows: list[np.ndarray] = []
    offsets: list[np.ndarray] = []
    for _ in range(depth + 1):
        rows.append(C[sel] @ phi)
        offsets.append(C[sel] @ b + c[sel])
        b = A @ b + a
        phi = A @ phi
    return np.vstack(rows), np.concatenate(offsets)


def reconstruct_holdout_states(
    states: np.ndarray,
    measurements: np.ndarray,
    *,
    A: np.ndarray,
    C: np.ndarray,
    state_offset: np.ndarray,
    measurement_offset: np.ndarray,
    design: AnalysisResult,
    noise_std: Sequence[float] | None = None,
    rng: np.random.Generator | None = None,
) -> ReconstructionMetrics:
    """Reconstruct each hold-out window's initial reduced state from actual outputs."""
    X = np.asarray(states, dtype=float)
    Y = np.asarray(measurements, dtype=float)
    depth = int(design.depth)
    if len(X) != len(Y):
        raise ValueError("states and measurements must have equal time length")
    if len(X) <= depth:
        raise ValueError("holdout series is shorter than design temporal depth")
    selected = tuple(design.selected)
    O, q = _affine_observation_system(A, C, state_offset, measurement_offset, selected, depth)
    pinv = np.linalg.pinv(O)
    sigmas = None if noise_std is None else np.asarray(noise_std, dtype=float)[list(selected)]
    errors: list[np.ndarray] = []
    rng = np.random.default_rng(0) if rng is None else rng
    for t in range(len(X) - depth):
        blocks = []
        for k in range(depth + 1):
            y = Y[t + k, list(selected)].copy()
            if sigmas is not None:
                y += rng.normal(0.0, sigmas, size=len(selected))
            blocks.append(y)
        y_stack = np.concatenate(blocks)
        x_hat = pinv @ (y_stack - q)
        errors.append(x_hat - X[t])
    E = np.asarray(errors)
    l2 = np.linalg.norm(E, axis=1)
    rmse = float(np.sqrt(np.mean(E * E)))
    scale = float(np.sqrt(np.mean(X[:len(E)] * X[:len(E)])))
    nrmse = rmse / scale if scale > 0 else float("inf")
    return ReconstructionMetrics(
        windows=len(E), rmse=rmse, nrmse=nrmse,
        median_l2_error=float(np.median(l2)),
        p95_l2_error=float(np.quantile(l2, 0.95)),
    )


def benchmark_probe_reference_case(
    case_dir: str | Path,
    *,
    candidate_object: str,
    reference_object: str,
    candidate_fields: Sequence[str],
    reference_fields: Sequence[str],
    pod_rank: int,
    train_fraction: float = 0.7,
    max_depth: int = 12,
    max_sensors: int | None = None,
    depth_unit_cost: float = 0.25,
    noise_fraction: float = 0.01,
    costs: Sequence[float] | None = None,
    ridge: float = 1e-10,
    min_sigma: float = 0.0,
    seed: int = 20260910,
) -> ProbeReferenceBenchmarkResult:
    """Train on dense-reference probes and evaluate sparse-sensor reconstruction on hold-out CFD data.

    The dense reference grid is a sampled surrogate for the CFD state, not the native full mesh.
    POD is fit on the training interval only. Sensor/depth selection uses the training ROM only;
    hold-out reconstruction uses untouched later OpenFOAM measurements.
    """
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must satisfy 0.5 <= train_fraction < 1")
    if noise_fraction < 0:
        raise ValueError("noise_fraction must be non-negative")

    cand = load_probes(case_dir, object_name=candidate_object, fields=candidate_fields)
    ref = load_probes(case_dir, object_name=reference_object, fields=reference_fields)
    ic, ir = _align_times(cand.times, ref.times)
    cand = _subset_probe_dataset(cand, ic)
    ref = _subset_probe_dataset(ref, ir)
    n = len(cand.times)
    split = int(np.floor(n * train_fraction))
    split = min(max(split, pod_rank + 2, 4), n - 2)
    if split <= pod_rank or n - split < 2:
        raise ValueError("not enough aligned samples for requested POD rank and holdout")

    pod = pod_reduce_snapshots(ref.values[:split], rank=pod_rank)
    X_all = (ref.values - pod.mean) @ pod.basis
    X_train, X_test = X_all[:split], X_all[split:]
    Y_train, Y_test = cand.values[:split], cand.values[split:]

    train_std = np.std(Y_train, axis=0, ddof=1)
    floor = max(float(np.max(np.abs(Y_train))) * 1e-12, 1e-12)
    sensor_noise = np.maximum(train_std * noise_fraction, floor)
    train_cand = ProbeDataset(
        cand.times[:split], Y_train, cand.channel_names, cand.channel_locations,
        cand.fields, cand.source_files,
    )
    model = fit_lti_probe_model(
        X_train, train_cand, costs=costs, noise_std=sensor_noise, ridge=ridge
    )

    Bd, state_offset = _fit_affine(X_train[:-1], X_train[1:], ridge)
    Bm, measurement_offset = _fit_affine(X_train, Y_train, ridge)
    A = Bd.T
    C = Bm.T

    temporal = model.optimize(
        target_rank=pod_rank, max_depth=max_depth, max_sensors=max_sensors,
        depth_unit_cost=depth_unit_cost, min_sigma=min_sigma, method="greedy"
    )
    static = model.optimize(
        target_rank=pod_rank, max_depth=0, max_sensors=max_sensors,
        depth_unit_cost=depth_unit_cost, min_sigma=min_sigma, method="greedy"
    )

    noiseless = None
    noisy = None
    if isinstance(temporal, AnalysisResult) and temporal.feasible and len(X_test) > temporal.depth:
        noiseless = reconstruct_holdout_states(
            X_test, Y_test, A=A, C=C,
            state_offset=state_offset, measurement_offset=measurement_offset,
            design=temporal,
        )
        noisy = reconstruct_holdout_states(
            X_test, Y_test, A=A, C=C,
            state_offset=state_offset, measurement_offset=measurement_offset,
            design=temporal, noise_std=sensor_noise,
            rng=np.random.default_rng(seed),
        )

    return ProbeReferenceBenchmarkResult(
        n_times=n, n_train=split, n_test=n-split,
        reference_channels=ref.n_channels, candidate_channels=cand.n_channels,
        pod_rank=pod_rank,
        pod_train_energy_fraction=float(np.sum(pod.explained_energy_ratio)),
        train_state_one_step_rmse=model.state_rmse,
        train_measurement_rmse=model.measurement_rmse,
        temporal_design=None if temporal is None else temporal.to_dict(),
        static_design=None if static is None else static.to_dict(),
        holdout_noiseless=None if noiseless is None else noiseless.to_dict(),
        holdout_noisy=None if noisy is None else noisy.to_dict(),
        noise_fraction_of_train_std=float(noise_fraction),
        candidate_object=candidate_object, reference_object=reference_object,
        candidate_fields=tuple(candidate_fields), reference_fields=tuple(reference_fields),
    )
