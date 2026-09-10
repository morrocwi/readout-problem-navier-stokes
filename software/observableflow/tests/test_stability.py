import numpy as np

from observableflow import Sensor
from observableflow.stability import (
    stability_greedy_candidates,
    stability_greedy_optimize,
    stability_objective,
)


def test_stability_search_keeps_rank_only_false_positive_but_does_not_select_it():
    # One dynamic scalar sensor becomes full rank with one-step history, but the
    # two rows are almost parallel. Two simultaneous channels are stable.
    A = np.array([[[1.0, 0.0], [0.0, 1.000001]]])
    H = np.array(
        [
            [[1.0, 1.0], [1.0, 1.0]],
            [[1.0, 0.0], [1.0, 0.0]],
            [[0.0, 1.0], [0.0, 1.0]],
        ]
    )
    sensors = [Sensor("dynamic"), Sensor("x1"), Sensor("x2")]

    candidates = stability_greedy_candidates(
        A,
        H,
        sensors,
        target_rank=2,
        max_depth=1,
        max_sensors=2,
        depth_unit_cost=0.5,
        max_condition_number=1000.0,
    )

    bad = [
        c for c in candidates
        if c.design.selected == (0,) and c.design.depth == 1
    ]
    assert bad
    assert bad[0].design.rank == 2
    assert bad[0].design.condition_number > 1e6
    assert not bad[0].passes_condition

    best = stability_greedy_optimize(
        A,
        H,
        sensors,
        target_rank=2,
        max_depth=1,
        max_sensors=2,
        depth_unit_cost=0.5,
        max_condition_number=1000.0,
    )
    assert best is not None
    assert best.rank == 2
    assert best.condition_number <= 1000.0
    assert not (best.selected == (0,) and best.depth == 1)


def test_stability_objective_penalizes_bad_conditioning():
    A = np.array([[[1.0, 0.0], [0.0, 1.000001]]])
    H = np.array(
        [
            [[1.0, 1.0], [1.0, 1.0]],
            [[1.0, 0.0], [1.0, 0.0]],
            [[0.0, 1.0], [0.0, 1.0]],
        ]
    )
    sensors = [Sensor("dynamic"), Sensor("x1"), Sensor("x2")]
    candidates = stability_greedy_candidates(
        A,
        H,
        sensors,
        target_rank=2,
        max_depth=1,
        max_sensors=2,
        depth_unit_cost=0.0,
    )
    bad = next(c.design for c in candidates if c.design.selected == (0,) and c.design.depth == 1)
    stable = min(
        (c.design for c in candidates if c.design.condition_number < 10),
        key=lambda d: d.total_cost,
    )
    assert stability_objective(bad, condition_weight=1.0) > stability_objective(stable, condition_weight=1.0)
