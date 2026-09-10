from __future__ import annotations

from itertools import combinations
from typing import Sequence
import math
import numpy as np

from .core import Sensor, AnalysisResult, analyze_design


def _dominates(a: AnalysisResult, b: AnalysisResult) -> bool:
    weak = (
        a.total_cost <= b.total_cost
        and a.depth <= b.depth
        and a.sigma_min >= b.sigma_min
    )
    strict = (
        a.total_cost < b.total_cost
        or a.depth < b.depth
        or a.sigma_min > b.sigma_min
    )
    return weak and strict


def pareto_optimize(
    transitions: np.ndarray,
    measurement_jacobians: np.ndarray,
    sensors: Sequence[Sensor],
    *,
    target_rank: int,
    max_depth: int,
    max_sensors: int | None = None,
    depth_unit_cost: float = 0.0,
    min_sigma: float = 0.0,
    max_combinations: int = 200_000,
    rtol: float = 1e-10,
) -> list[AnalysisResult]:
    """Exhaustive Pareto search for small/medium finite candidate sets."""
    m = len(sensors)
    max_sensors = m if max_sensors is None else min(int(max_sensors), m)
    count = sum(math.comb(m, k) for k in range(1, max_sensors + 1)) * (max_depth + 1)
    if count > max_combinations:
        raise ValueError(
            f"design space has {count} sensor/depth combinations; "
            f"raise max_combinations or use greedy_optimize"
        )
    feasible: list[AnalysisResult] = []
    for k in range(1, max_sensors + 1):
        for subset in combinations(range(m), k):
            for depth in range(max_depth + 1):
                r = analyze_design(
                    transitions,
                    measurement_jacobians,
                    sensors,
                    subset,
                    depth,
                    target_rank=target_rank,
                    depth_unit_cost=depth_unit_cost,
                    min_sigma=min_sigma,
                    rtol=rtol,
                )
                if r.feasible:
                    feasible.append(r)
    frontier: list[AnalysisResult] = []
    for r in feasible:
        if not any(_dominates(other, r) for other in feasible if other is not r):
            frontier.append(r)
    return sorted(frontier, key=lambda x: (x.total_cost, x.depth, -x.sigma_min, len(x.selected)))


def greedy_optimize(
    transitions: np.ndarray,
    measurement_jacobians: np.ndarray,
    sensors: Sequence[Sensor],
    *,
    target_rank: int,
    max_depth: int,
    max_sensors: int | None = None,
    depth_unit_cost: float = 0.0,
    min_sigma: float = 0.0,
    rtol: float = 1e-10,
) -> AnalysisResult | None:
    """Scalable heuristic: greedy sensor additions at every temporal depth."""
    m = len(sensors)
    limit = m if max_sensors is None else min(int(max_sensors), m)
    best: AnalysisResult | None = None
    for depth in range(max_depth + 1):
        selected: list[int] = []
        current = analyze_design(
            transitions, measurement_jacobians, sensors, selected, depth,
            target_rank=target_rank, depth_unit_cost=depth_unit_cost,
            min_sigma=min_sigma, rtol=rtol,
        )
        for _ in range(limit):
            candidates = []
            for i in range(m):
                if i in selected:
                    continue
                trial = analyze_design(
                    transitions, measurement_jacobians, sensors, selected + [i], depth,
                    target_rank=target_rank, depth_unit_cost=depth_unit_cost,
                    min_sigma=min_sigma, rtol=rtol,
                )
                rank_gain = trial.rank - current.rank
                sigma_gain = trial.sigma_min - current.sigma_min
                effective_cost = max(sensors[i].cost, 1e-12)
                candidates.append((rank_gain, sigma_gain / effective_cost, -effective_cost, i, trial))
            if not candidates:
                break
            candidates.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
            _, _, _, i, current = candidates[0]
            selected.append(i)
            if current.feasible:
                if best is None or (current.total_cost, current.condition_number) < (best.total_cost, best.condition_number):
                    best = current
                break
    return best
