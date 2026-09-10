from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Sequence
import math
import numpy as np


@dataclass(frozen=True)
class Sensor:
    name: str
    cost: float = 1.0
    noise_std: float = 1.0


@dataclass(frozen=True)
class AnalysisResult:
    selected: tuple[int, ...]
    depth: int
    rank: int
    target_rank: int
    sigma_min: float
    sigma_max: float
    condition_number: float
    sensor_cost: float
    depth_cost: float
    total_cost: float
    feasible: bool

    def to_dict(self) -> dict:
        return asdict(self)


def state_transition_products(transitions: np.ndarray, depth: int) -> list[np.ndarray]:
    """Return Phi_k = d x_k / d x_0 for k=0..depth."""
    A = np.asarray(transitions, dtype=float)
    if A.ndim != 3 or A.shape[1] != A.shape[2]:
        raise ValueError("transitions must have shape (T, n, n)")
    if depth < 0 or depth > A.shape[0]:
        raise ValueError("depth must satisfy 0 <= depth <= number of transitions")
    n = A.shape[1]
    out = [np.eye(n)]
    phi = np.eye(n)
    for k in range(depth):
        phi = A[k] @ phi
        out.append(phi.copy())
    return out


def observability_matrix(
    transitions: np.ndarray,
    measurement_jacobians: np.ndarray,
    selected: Sequence[int],
    depth: int,
    noise_std: Sequence[float] | None = None,
) -> np.ndarray:
    """Build a noise-whitened finite-horizon local observability matrix.

    measurement_jacobians has shape (m, T+1, n). Each candidate sensor is
    scalar. H[i,k] is dh_i/dx at trajectory time k. Returned rows are
    H[i,k] Phi_k, optionally divided by the sensor noise standard deviation.
    """
    H = np.asarray(measurement_jacobians, dtype=float)
    if H.ndim != 3:
        raise ValueError("measurement_jacobians must have shape (m, T+1, n)")
    m, steps, n = H.shape
    A = np.asarray(transitions, dtype=float)
    if A.shape != (steps - 1, n, n):
        raise ValueError("transitions shape must be (T, n, n) matching H=(m,T+1,n)")
    selected = tuple(int(i) for i in selected)
    if not selected:
        return np.empty((0, n), dtype=float)
    if min(selected) < 0 or max(selected) >= m:
        raise IndexError("selected sensor index out of range")
    if depth >= steps:
        raise ValueError("depth exceeds available measurement horizon")
    sigmas = np.ones(m, dtype=float) if noise_std is None else np.asarray(noise_std, dtype=float)
    if sigmas.shape != (m,) or np.any(sigmas <= 0):
        raise ValueError("noise_std must be positive with shape (m,)")
    phis = state_transition_products(A, depth)
    rows = []
    for k in range(depth + 1):
        phi = phis[k]
        for i in selected:
            rows.append((H[i, k] @ phi) / sigmas[i])
    return np.vstack(rows)


def svd_metrics(O: np.ndarray, rtol: float = 1e-10) -> tuple[int, float, float, float]:
    O = np.asarray(O, dtype=float)
    if O.ndim != 2:
        raise ValueError("O must be a matrix")
    if O.size == 0 or O.shape[0] == 0:
        return 0, 0.0, 0.0, math.inf
    s = np.linalg.svd(O, compute_uv=False)
    if len(s) == 0 or s[0] == 0:
        return 0, 0.0, 0.0, math.inf
    threshold = rtol * s[0]
    rank = int(np.count_nonzero(s > threshold))
    sigma_max = float(s[0])
    sigma_min = float(s[rank - 1]) if rank else 0.0
    cond = float(sigma_max / sigma_min) if sigma_min > 0 else math.inf
    return rank, sigma_min, sigma_max, cond


def analyze_design(
    transitions: np.ndarray,
    measurement_jacobians: np.ndarray,
    sensors: Sequence[Sensor],
    selected: Sequence[int],
    depth: int,
    *,
    target_rank: int | None = None,
    depth_unit_cost: float = 0.0,
    min_sigma: float = 0.0,
    rtol: float = 1e-10,
) -> AnalysisResult:
    n = np.asarray(measurement_jacobians).shape[-1]
    target = n if target_rank is None else int(target_rank)
    selected = tuple(sorted(set(int(i) for i in selected)))
    if len(sensors) != np.asarray(measurement_jacobians).shape[0]:
        raise ValueError("sensors length must match candidate measurement count")
    O = observability_matrix(
        transitions,
        measurement_jacobians,
        selected,
        depth,
        noise_std=[s.noise_std for s in sensors],
    )
    rank, sigma_min, sigma_max, cond = svd_metrics(O, rtol=rtol)
    sensor_cost = float(sum(sensors[i].cost for i in selected))
    depth_cost = float(depth_unit_cost * depth)
    total_cost = sensor_cost + depth_cost
    feasible = rank >= target and sigma_min >= min_sigma
    return AnalysisResult(
        selected=selected,
        depth=depth,
        rank=rank,
        target_rank=target,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        condition_number=cond,
        sensor_cost=sensor_cost,
        depth_cost=depth_cost,
        total_cost=total_cost,
        feasible=feasible,
    )
