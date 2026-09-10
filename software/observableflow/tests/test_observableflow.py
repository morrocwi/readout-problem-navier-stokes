import numpy as np
from observableflow import Sensor, analyze_design, pareto_optimize
from observableflow.ns_bounds import summary


def test_ns_bounds_match_anchor_cases():
    k1 = summary(1)
    assert k1["real_state_dimension"] == 52
    assert k1["shell_count"] == 3
    assert k1["scalar_min_depth"] == 48
    assert k1["shell_min_depth"] == 23

    k2 = summary(2)
    assert k2["real_state_dimension"] == 248
    assert k2["shell_count"] == 9
    assert k2["scalar_min_depth"] == 244

    k3 = summary(3)
    assert k3["real_state_dimension"] == 684
    assert k3["shell_count"] == 18
    assert k3["scalar_min_depth"] == 680
    assert k3["shell_min_depth"] == 39


def test_time_history_can_replace_simultaneous_channels():
    A = np.array([[[1.0, 0.0], [0.0, 2.0]]])
    H = np.array([[[1.0, 1.0], [1.0, 1.0]]])
    sensors = [Sensor("sum", cost=1.0, noise_std=1.0)]
    r0 = analyze_design(A, H, sensors, [0], 0, target_rank=2)
    r1 = analyze_design(A, H, sensors, [0], 1, target_rank=2)
    assert r0.rank == 1 and not r0.feasible
    assert r1.rank == 2 and r1.feasible


def test_pareto_optimizer_trades_sensor_cost_for_depth():
    A = np.array([[[1.0, 0.0], [0.0, 2.0]]])
    H = np.array([
        [[1.0, 1.0], [1.0, 1.0]],
        [[1.0, 0.0], [1.0, 0.0]],
        [[0.0, 1.0], [0.0, 1.0]],
    ])
    sensors = [Sensor("dynamic", 1.0), Sensor("x1", 1.0), Sensor("x2", 1.0)]
    frontier = pareto_optimize(A, H, sensors, target_rank=2, max_depth=1, max_sensors=2, depth_unit_cost=0.5)
    assert any(r.selected == (0,) and r.depth == 1 for r in frontier)
    assert any(r.selected == (1, 2) and r.depth == 0 for r in frontier)
