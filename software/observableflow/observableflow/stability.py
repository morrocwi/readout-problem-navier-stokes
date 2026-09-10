from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Sequence
import math

import numpy as np

from .core import AnalysisResult, Sensor, analyze_design


@dataclass(frozen=True)
class StabilityCandidate:
    """One full-rank design on a greedy sensor/depth search path."""

    design: AnalysisResult
    score: float
    passes_condition: bool

    def to_dict(self) -> dict:
        out = asdict(self)
        out["design"] = self.design.to_dict()
        return out


def stability_objective(
    design: AnalysisResult,
    *,
    condition_weight: float = 0.25,
) -> float:
    """Cost plus a scale-invariant conditioning penalty.

    This objective deliberately excludes validation/test error. Validation-aware
    selection belongs in a benchmark or application layer so that held-out data
    cannot silently leak into the structural optimizer.
    """
    if condition_weight < 0:
        raise ValueError("condition_weight must be non-negative")
    cond = float(design.condition_number)
    if not math.isfinite(cond):
        return math.inf
    return float(design.total_cost + condition_weight * math.log10(max(cond, 1.0)))


def _trial_key(
    trial: AnalysisResult,
    current: AnalysisResult,
    *,
    target_rank: int,
    sensor_cost: float,
) -> tuple[float, ...]:
    """Lexicographic utility used only to grow one deterministic greedy path."""
    cost = max(float(sensor_cost), 1e-12)
    rank_gain = float(trial.rank - current.rank)
    cond = float(trial.condition_number)
    log_cond = math.log10(max(cond, 1.0)) if math.isfinite(cond) else math.inf
    sigma_per_cost = float(trial.sigma_min / cost)

    if current.rank < target_rank:
        # Reach the requested information dimension first.  Among equal rank
        # gains, prefer a better-conditioned and stronger singular spectrum.
        return (rank_gain, -log_cond, sigma_per_cost, -cost)

    # Once full rank has been reached, keep exploring extra sensors rather than
    # stopping at the first rank-feasible design.  This is the key difference
    # from the original rank-first greedy lane.
    return (-log_cond, sigma_per_cost, -cost, rank_gain)


def stability_greedy_candidates(
    transitions: np.ndarray,
    measurement_jacobians: np.ndarray,
    sensors: Sequence[Sensor],
    *,
    target_rank: int,
    max_depth: int,
    max_sensors: int | None = None,
    depth_unit_cost: float = 0.0,
    min_sigma: float = 0.0,
    max_condition_number: float | None = None,
    condition_weight: float = 0.25,
    rtol: float = 1e-10,
) -> list[StabilityCandidate]:
    """Return full-rank candidates while continuing past first rank saturation.

    The routine grows one deterministic greedy sensor path for each temporal
    depth.  Rank gain is prioritized until ``target_rank`` is reached; after
    that, additional sensors are chosen to improve conditioning.  Every
    full-rank point on every depth path is retained and scored.

    ``max_condition_number`` is a declared engineering gate, not a theorem.
    The returned list contains both passing and failing designs so negative
    results remain inspectable.
    """
    if target_rank < 1:
        raise ValueError("target_rank must be positive")
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    if depth_unit_cost < 0:
        raise ValueError("depth_unit_cost must be non-negative")
    if min_sigma < 0:
        raise ValueError("min_sigma must be non-negative")
    if max_condition_number is not None and max_condition_number < 1:
        raise ValueError("max_condition_number must be >= 1 when supplied")

    m = len(sensors)
    limit = m if max_sensors is None else min(int(max_sensors), m)
    if limit < 1:
        return []

    out: list[StabilityCandidate] = []
    for depth in range(max_depth + 1):
        selected: list[int] = []
        current = analyze_design(
            transitions,
            measurement_jacobians,
            sensors,
            selected,
            depth,
            target_rank=target_rank,
            depth_unit_cost=depth_unit_cost,
            min_sigma=min_sigma,
            rtol=rtol,
        )

        for _ in range(limit):
            trials: list[tuple[tuple[float, ...], int, AnalysisResult]] = []
            for i in range(m):
                if i in selected:
                    continue
                trial = analyze_design(
                    transitions,
                    measurement_jacobians,
                    sensors,
                    selected + [i],
                    depth,
                    target_rank=target_rank,
                    depth_unit_cost=depth_unit_cost,
                    min_sigma=min_sigma,
                    rtol=rtol,
                )
                trials.append(
                    (
                        _trial_key(
                            trial,
                            current,
                            target_rank=target_rank,
                            sensor_cost=sensors[i].cost,
                        ),
                        i,
                        trial,
                    )
                )
            if not trials:
                break

            trials.sort(key=lambda item: (item[0], -item[1]), reverse=True)
            _, chosen, current = trials[0]
            selected.append(chosen)

            if current.rank >= target_rank and current.sigma_min >= min_sigma:
                passes = (
                    max_condition_number is None
                    or current.condition_number <= max_condition_number
                )
                out.append(
                    StabilityCandidate(
                        design=current,
                        score=stability_objective(
                            current, condition_weight=condition_weight
                        ),
                        passes_condition=bool(passes),
                    )
                )

    return sorted(
        out,
        key=lambda c: (
            not c.passes_condition,
            c.score,
            c.design.condition_number,
            c.design.total_cost,
            c.design.depth,
            len(c.design.selected),
        ),
    )


def stability_greedy_optimize(
    transitions: np.ndarray,
    measurement_jacobians: np.ndarray,
    sensors: Sequence[Sensor],
    *,
    target_rank: int,
    max_depth: int,
    max_sensors: int | None = None,
    depth_unit_cost: float = 0.0,
    min_sigma: float = 0.0,
    max_condition_number: float | None = None,
    condition_weight: float = 0.25,
    rtol: float = 1e-10,
) -> AnalysisResult | None:
    """Return the best condition-gated candidate from the stability search."""
    candidates = stability_greedy_candidates(
        transitions,
        measurement_jacobians,
        sensors,
        target_rank=target_rank,
        max_depth=max_depth,
        max_sensors=max_sensors,
        depth_unit_cost=depth_unit_cost,
        min_sigma=min_sigma,
        max_condition_number=max_condition_number,
        condition_weight=condition_weight,
        rtol=rtol,
    )
    for candidate in candidates:
        if candidate.passes_condition:
            return candidate.design
    return None
