#!/usr/bin/env python3
"""Physical plane-average Navier-Stokes retained RK4 benchmark.

The exact periodic plane-average reader normal to x keeps only terminal modes
A_x = {(a,0,0): 1 <= |a| <= K}.  Its Fourier support is sparse, but one exact
NS triad dependency pullback saturates the whole retained cube:

    D(A_x) = K_M.

Therefore an exact RK4 step can remove work only from its terminal k4 stage;
k1,k2,k3 require all modes.  Earlier time steps in a multi-step horizon are
fully relevant.  This checker verifies that structural fact, terminal task
exactness, backend equivalence, and reports finite timing without promoting it
to a universal speed theorem.
"""
from __future__ import annotations

import json
import sys

import numpy as np

from check_volume6_ns_retained_fold import (
    FusedTriadPlan,
    Mode,
    cube_modes,
    median_seconds,
    random_real_divfree_state,
    triads_by_output,
)
from check_volume6_ns_retained_fold_rk4 import (
    FFTPlan,
    StagePlan,
    StepPlan,
    TaskPlan,
    dependency_expand,
    execute_hybrid_raw,
    execute_selected,
    fft_rhs,
    full_rk4,
    fused_rhs,
)


def plane_modes(K: int, axis: int = 0) -> list[Mode]:
    modes = cube_modes(K)
    return [
        k for k in modes
        if all(k[j] == 0 for j in range(3) if j != axis)
    ]


def plane_value(
    U: np.ndarray,
    targets: list[Mode],
    index: dict[Mode, int],
    axis: int,
    coordinate: float,
) -> np.ndarray:
    out = np.zeros(3, dtype=complex)
    for k in targets:
        out += U[index[k]] * np.exp(1j * k[axis] * coordinate)
    return out


def compile_terminal_plan(
    K: int,
    targets: list[Mode],
    horizon: int,
    probe: np.ndarray,
    dt: float,
    nu: float,
    calibration_repeats: int = 5,
) -> tuple[TaskPlan, dict]:
    modes = cube_modes(K)
    index = {k: i for i, k in enumerate(modes)}
    triads = triads_by_output(modes)
    fft = FFTPlan.compile(modes, K)

    all_fused = FusedTriadPlan.compile(modes, triads, modes)
    backend_error = float(np.max(np.abs(
        fused_rhs(all_fused, probe, nu) - fft_rhs(fft, probe, nu)
    )))
    fft_seconds = median_seconds(
        lambda: fft_rhs(fft, probe, nu), calibration_repeats
    )

    specs = [None] * horizon
    terminal = set(targets)
    for t in range(horizon - 1, -1, -1):
        K4 = set(terminal)
        K3 = dependency_expand(triads, K4)
        K2 = dependency_expand(triads, K3)
        K1 = dependency_expand(triads, K2)
        S0 = dependency_expand(triads, K1)
        specs[t] = (S0, K1, K2, K3, K4)
        terminal = S0

    steps = []
    for S0, K1, K2, K3, K4 in specs:
        stages = []
        for name, outputs in (("k1", K1), ("k2", K2), ("k3", K3), ("k4", K4)):
            fused = FusedTriadPlan.compile(modes, triads, outputs)
            fused_seconds = median_seconds(
                lambda f=fused: fused_rhs(f, probe, nu), calibration_repeats
            )
            backend = "fused_retained" if fused_seconds <= fft_seconds else "full_fft"
            stages.append(StagePlan(name, fused, backend, fused_seconds, fft_seconds))
        steps.append(StepPlan(frozenset(S0), frozenset(K4), tuple(stages)))

    task = TaskPlan(modes, index, fft, steps, backend_error)
    hybrid_seconds = median_seconds(
        lambda: execute_hybrid_raw(task, probe, dt, nu),
        max(3, calibration_repeats),
    )
    full_seconds = median_seconds(
        lambda: full_rk4(fft, probe, dt, nu, horizon),
        max(3, calibration_repeats),
    )
    task.hybrid_calibration_seconds = hybrid_seconds
    task.full_calibration_seconds = full_seconds
    task.plan_mode = (
        "hybrid_retained"
        if hybrid_seconds <= 0.95 * full_seconds
        else "full_rk4"
    )
    return task, triads


def run_case(
    K: int,
    horizon: int,
    axis: int = 0,
    coordinate: float = 0.7,
    dt: float = 0.0025,
    nu: float = 0.005,
    repeats: int = 7,
    calibration_repeats: int = 5,
) -> dict:
    modes = cube_modes(K)
    mode_set = set(modes)
    targets = plane_modes(K, axis)
    U0 = random_real_divfree_state(modes)
    task, triads = compile_terminal_plan(
        K, targets, horizon, U0, dt, nu, calibration_repeats
    )

    one_pullback = dependency_expand(triads, set(targets))
    saturation = one_pullback == mode_set

    retained = execute_selected(task, U0, dt, nu)
    full = full_rk4(task.fft, U0, dt, nu, horizon)
    q_ret = plane_value(retained, targets, task.index, axis, coordinate)
    q_full = plane_value(full, targets, task.index, axis, coordinate)
    target_error = float(np.linalg.norm(q_ret - q_full))

    raw_seconds = median_seconds(
        lambda: execute_hybrid_raw(task, U0, dt, nu), repeats
    )
    selected_seconds = median_seconds(
        lambda: execute_selected(task, U0, dt, nu), repeats
    )
    full_seconds = median_seconds(
        lambda: full_rk4(task.fft, U0, dt, nu, horizon), repeats
    )

    full_triads = sum(len(triads[k]) for k in modes)
    axis_triads = sum(len(triads[k]) for k in targets)
    full_work = 4 * horizon * full_triads
    retained_work = sum(
        stage.fused.triad_count
        for step in task.steps
        for stage in step.stages
    )
    predicted_retained_work = (4 * horizon - 1) * full_triads + axis_triads
    structural_ratio = full_work / retained_work
    predicted_ratio = full_work / predicted_retained_work

    return {
        "K": K,
        "horizon": horizon,
        "mode_count": len(modes),
        "terminal_mode_count": len(targets),
        "readout_density": len(targets) / len(modes),
        "one_pullback_saturates_full_cube": saturation,
        "backend_equivalence_error": task.backend_equivalence_error,
        "target_abs_error": target_error,
        "imaginary_residual": float(np.max(np.abs(q_ret.imag))),
        "longitudinal_residual": float(abs(q_ret[axis])),
        "full_triad_work": full_work,
        "retained_triad_work": retained_work,
        "predicted_retained_triad_work": predicted_retained_work,
        "structural_work_reduction": structural_ratio,
        "predicted_structural_work_reduction": predicted_ratio,
        "plan_mode": task.plan_mode,
        "raw_hybrid_seconds": raw_seconds,
        "selected_seconds": selected_seconds,
        "full_seconds": full_seconds,
        "observed_speedup": full_seconds / selected_seconds,
        "steps": [
            {
                "input_modes": len(step.input_set),
                "output_modes": len(step.output_set),
                "stages": [
                    {
                        "stage": stage.name,
                        "output_modes": len(stage.fused.outputs),
                        "triads": stage.fused.triad_count,
                        "backend": stage.backend,
                    }
                    for stage in step.stages
                ],
            }
            for step in task.steps
        ],
    }


def main() -> int:
    rows = [
        run_case(K, H)
        for K in (2, 3)
        for H in (1, 2, 3)
    ]

    saturation_ok = all(r["one_pullback_saturates_full_cube"] for r in rows)
    backend_ok = all(r["backend_equivalence_error"] < 1e-12 for r in rows)
    target_ok = all(r["target_abs_error"] < 1e-12 for r in rows)
    real_ok = all(r["imaginary_residual"] < 1e-12 for r in rows)
    div_ok = all(r["longitudinal_residual"] < 1e-12 for r in rows)
    work_formula_ok = all(
        r["retained_triad_work"] == r["predicted_retained_triad_work"]
        for r in rows
    )

    for r in rows:
        print(
            f"K={r['K']} H={r['horizon']} density={r['readout_density']:.6f} "
            f"structural={r['structural_work_reduction']:.3f}x "
            f"mode={r['plan_mode']} speed={r['observed_speedup']:.3f}x "
            f"err={r['target_abs_error']:.3e}"
        )

    claims = [
        {
            "id": "Vol6-NSPlane-sparse-terminal-support",
            "tier": "finite_diagnostic",
            "status": "PASS" if saturation_ok else "FAIL",
            "evidence": (
                "the plane-average reader uses only axis modes, while one exact "
                "triad dependency pullback saturates the full tested Fourier cube"
            ),
        },
        {
            "id": "Vol6-NSPlane-task-exactness",
            "tier": "finite_diagnostic",
            "status": "PASS" if target_ok and backend_ok else "FAIL",
            "evidence": (
                "retained plane-average RK4 readout agrees with full finite RK4 "
                "to 1e-12 and the fused/FFT RHS backends pass the same gate"
            ),
        },
        {
            "id": "Vol6-NSPlane-real-divfree-readout",
            "tier": "finite_diagnostic",
            "status": "PASS" if real_ok and div_ok else "FAIL",
            "evidence": (
                "plane readout is real to floating tolerance and its component "
                "along the plane normal vanishes to floating tolerance"
            ),
        },
        {
            "id": "Vol6-NSPlane-structural-work-law",
            "tier": "finite_diagnostic",
            "status": "PASS" if work_formula_ok else "FAIL",
            "evidence": (
                "with D(A)=K_M, retained triad work equals "
                "(4H-1) C_full + C_axis for every tested case"
            ),
        },
    ]

    ok = saturation_ok and backend_ok and target_ok and real_ok and div_ok and work_formula_ok
    print("REPORT_JSON:" + json.dumps(rows, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
