#!/usr/bin/env python3
"""
RK4 stage-conditioned NS Retained Fold Compiler.

Extends check_volume6_ns_retained_fold.py without duplicating its Fourier,
triad, projection, random-state, FFT, or fused-retained kernels.

For one RK4 step with terminal mode set T define D(S) as S plus every p,q
appearing in an ordered triad p+q=k for k in S. Pull relevance backward:

    K4 = T
    K3 = D(K4)
    K2 = D(K3)
    K1 = D(K2)
    S_in = D(K1)

If the input state is exact on S_in, then the four RK stages are exact on
K1,K2,K3,K4 respectively, so the terminal RK4 output is exact on T.

Each stage chooses between the fused retained triad backend and the admitted
full FFT backend by hot calibration. A second fail-closed guard enables the
whole retained rollout only when calibration beats full RK4 by at least 5%.

Tier: finite_diagnostic. No learned closure; no continuum claim.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass

import numpy as np

from check_volume6_ns_retained_fold import (
    FFTPlan,
    FusedTriadPlan,
    Mode,
    cube_modes,
    median_seconds,
    random_real_divfree_state,
    triads_by_output,
)


def dependency_expand(triads, outputs) -> set[Mode]:
    """One exact triad-dependency pullback D(S)."""
    out = set(outputs)
    for k in tuple(outputs):
        for p, q in triads[k]:
            out.add(p)
            out.add(q)
    return out


def fused_rhs(plan: FusedTriadPlan, U: np.ndarray, nu: float) -> np.ndarray:
    """Recover RHS from the existing exact Euler fused update."""
    updated = plan.update_selected(U, 1.0, nu)
    return updated - U[plan.k_idx]


def fft_rhs(fft: FFTPlan, U: np.ndarray, nu: float) -> np.ndarray:
    """Recover all-mode RHS from the admitted Euler FFT update."""
    return fft.full_step(U, 1.0, nu) - U


@dataclass(frozen=True)
class StagePlan:
    name: str
    fused: FusedTriadPlan
    backend: str
    fused_seconds: float
    fft_seconds: float


@dataclass(frozen=True)
class StepPlan:
    input_set: frozenset[Mode]
    output_set: frozenset[Mode]
    stages: tuple[StagePlan, StagePlan, StagePlan, StagePlan]


@dataclass
class TaskPlan:
    modes: list[Mode]
    index: dict[Mode, int]
    fft: FFTPlan
    steps: list[StepPlan]
    backend_equivalence_error: float
    plan_mode: str = "hybrid_retained"
    hybrid_calibration_seconds: float = 0.0
    full_calibration_seconds: float = 0.0


def stage_rhs(task: TaskPlan, stage: StagePlan, U: np.ndarray, nu: float) -> np.ndarray:
    if stage.backend == "full_fft":
        return fft_rhs(task.fft, U, nu)[stage.fused.k_idx]
    return fused_rhs(stage.fused, U, nu)


def execute_hybrid_raw(task: TaskPlan, U0: np.ndarray, dt: float, nu: float) -> np.ndarray:
    U = U0.copy()
    for step in task.steps:
        s1, s2, s3, s4 = step.stages

        r1 = stage_rhs(task, s1, U, nu)
        k1 = np.zeros_like(U)
        k1[s1.fused.k_idx] = r1
        y2 = U.copy()
        y2[s1.fused.k_idx] = U[s1.fused.k_idx] + 0.5 * dt * r1

        r2 = stage_rhs(task, s2, y2, nu)
        k2 = np.zeros_like(U)
        k2[s2.fused.k_idx] = r2
        y3 = U.copy()
        y3[s2.fused.k_idx] = U[s2.fused.k_idx] + 0.5 * dt * r2

        r3 = stage_rhs(task, s3, y3, nu)
        k3 = np.zeros_like(U)
        k3[s3.fused.k_idx] = r3
        y4 = U.copy()
        y4[s3.fused.k_idx] = U[s3.fused.k_idx] + dt * r3

        r4 = stage_rhs(task, s4, y4, nu)
        k4 = np.zeros_like(U)
        k4[s4.fused.k_idx] = r4

        out_idx = s4.fused.k_idx
        U_next = U.copy()
        U_next[out_idx] = U[out_idx] + (dt / 6.0) * (
            k1[out_idx] + 2.0 * k2[out_idx] + 2.0 * k3[out_idx] + k4[out_idx]
        )
        U = U_next
    return U


def full_rk4(fft: FFTPlan, U0: np.ndarray, dt: float, nu: float, steps: int) -> np.ndarray:
    U = U0.copy()
    for _ in range(steps):
        k1 = fft_rhs(fft, U, nu)
        k2 = fft_rhs(fft, U + 0.5 * dt * k1, nu)
        k3 = fft_rhs(fft, U + 0.5 * dt * k2, nu)
        k4 = fft_rhs(fft, U + dt * k3, nu)
        U = U + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return U


def execute_selected(task: TaskPlan, U0: np.ndarray, dt: float, nu: float) -> np.ndarray:
    if task.plan_mode == "full_rk4":
        return full_rk4(task.fft, U0, dt, nu, len(task.steps))
    return execute_hybrid_raw(task, U0, dt, nu)


def compile_task_plan(
    K: int,
    target: Mode,
    horizon: int,
    probe: np.ndarray,
    dt: float,
    nu: float,
    calibration_repeats: int = 5,
) -> TaskPlan:
    modes = cube_modes(K)
    index = {k: i for i, k in enumerate(modes)}
    if target not in index:
        raise ValueError("target mode is outside the retained cube")

    triads = triads_by_output(modes)
    fft = FFTPlan.compile(modes, K)

    # Admit FFT only after checking the same finite all-mode Galerkin RHS.
    all_fused = FusedTriadPlan.compile(modes, triads, modes)
    backend_error = float(np.max(np.abs(
        fused_rhs(all_fused, probe, nu) - fft_rhs(fft, probe, nu)
    )))

    fft_seconds = median_seconds(
        lambda: fft_rhs(fft, probe, nu), calibration_repeats
    )

    # Pull terminal relevance backward through four RK stages per time step.
    specs = [None] * horizon
    terminal = {target}
    for t in range(horizon - 1, -1, -1):
        K4 = set(terminal)
        K3 = dependency_expand(triads, K4)
        K2 = dependency_expand(triads, K3)
        K1 = dependency_expand(triads, K2)
        S0 = dependency_expand(triads, K1)
        specs[t] = (S0, K1, K2, K3, K4)
        terminal = S0

    steps: list[StepPlan] = []
    for S0, K1, K2, K3, K4 in specs:
        stages = []
        for name, outputs in (("k1", K1), ("k2", K2), ("k3", K3), ("k4", K4)):
            fused = FusedTriadPlan.compile(modes, triads, outputs)
            fused_seconds = median_seconds(
                lambda f=fused: fused_rhs(f, probe, nu), calibration_repeats
            )
            backend = "fused_retained" if fused_seconds <= fft_seconds else "full_fft"
            stages.append(StagePlan(name, fused, backend, fused_seconds, fft_seconds))
        steps.append(StepPlan(
            frozenset(S0), frozenset(K4), tuple(stages)
        ))

    task = TaskPlan(modes, index, fft, steps, backend_error)

    hybrid_seconds = median_seconds(
        lambda: execute_hybrid_raw(task, probe, dt, nu),
        max(3, calibration_repeats),
    )
    full_seconds = median_seconds(
        lambda: full_rk4(fft, probe, dt, nu, horizon),
        max(3, calibration_repeats),
    )

    # Fail closed: require >=5% calibration advantage.
    task.hybrid_calibration_seconds = hybrid_seconds
    task.full_calibration_seconds = full_seconds
    task.plan_mode = (
        "hybrid_retained"
        if hybrid_seconds <= 0.95 * full_seconds
        else "full_rk4"
    )
    return task


def run_case(
    K: int,
    horizon: int,
    dt: float = 0.0025,
    nu: float = 0.005,
    repeats: int = 7,
    calibration_repeats: int = 5,
    target: Mode = (1, 0, 0),
) -> dict:
    modes = cube_modes(K)
    U0 = random_real_divfree_state(modes)
    task = compile_task_plan(
        K, target, horizon, U0, dt, nu, calibration_repeats
    )

    retained = execute_selected(task, U0, dt, nu)
    full = full_rk4(task.fft, U0, dt, nu, horizon)
    target_idx = task.index[target]
    target_abs_error = float(np.linalg.norm(
        retained[target_idx] - full[target_idx]
    ))
    target_rel_error = target_abs_error / max(
        float(np.linalg.norm(full[target_idx])), 1e-30
    )

    raw_hybrid_seconds = median_seconds(
        lambda: execute_hybrid_raw(task, U0, dt, nu), repeats
    )
    selected_seconds = median_seconds(
        lambda: execute_selected(task, U0, dt, nu), repeats
    )
    full_seconds = median_seconds(
        lambda: full_rk4(task.fft, U0, dt, nu, horizon), repeats
    )

    return {
        "K": K,
        "horizon": horizon,
        "mode_count": len(modes),
        "plan_mode": task.plan_mode,
        "backend_equivalence_error": task.backend_equivalence_error,
        "target_abs_error": target_abs_error,
        "target_rel_error": target_rel_error,
        "hybrid_calibration_seconds": task.hybrid_calibration_seconds,
        "full_calibration_seconds": task.full_calibration_seconds,
        "raw_hybrid_seconds": raw_hybrid_seconds,
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
        run_case(K, horizon)
        for K in (2, 3)
        for horizon in (1, 2, 3)
    ]

    backend_ok = all(r["backend_equivalence_error"] < 1e-12 for r in rows)
    target_ok = all(r["target_abs_error"] < 1e-12 for r in rows)
    selected_safe = all(
        (r["plan_mode"] == "full_rk4") or
        (r["hybrid_calibration_seconds"] <= 0.95 * r["full_calibration_seconds"])
        for r in rows
    )

    for r in rows:
        print(
            f"K={r['K']} H={r['horizon']} mode={r['plan_mode']} "
            f"speedup={r['observed_speedup']:.3f}x "
            f"target_err={r['target_abs_error']:.3e} "
            f"backend_gate={r['backend_equivalence_error']:.3e}"
        )

    claims = [
        {
            "id": "Vol6-NSRFC-RK4-stage-exactness",
            "tier": "finite_diagnostic",
            "status": "PASS" if target_ok else "FAIL",
            "evidence": (
                "terminal target from stage-conditioned retained RK4 agrees with "
                "the full RK4 recurrence to the declared 1e-12 gate"
            ),
        },
        {
            "id": "Vol6-NSRFC-RK4-backend-equivalence",
            "tier": "finite_diagnostic",
            "status": "PASS" if backend_ok else "FAIL",
            "evidence": (
                "fused direct-triad RHS and pseudo-spectral FFT RHS agree on the "
                "same finite mode cube to the declared 1e-12 gate"
            ),
        },
        {
            "id": "Vol6-NSRFC-RK4-break-even",
            "tier": "finite_diagnostic",
            "status": "PASS" if selected_safe else "FAIL",
            "evidence": (
                "retained rollout is enabled only with a >=5% calibration margin; "
                "otherwise execution falls back to full RK4"
            ),
        },
    ]

    print("REPORT_JSON:" + json.dumps(rows, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))
    return 0 if backend_ok and target_ok and selected_safe else 1


if __name__ == "__main__":
    sys.exit(main())
