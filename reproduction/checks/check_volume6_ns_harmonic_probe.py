#!/usr/bin/env python3
"""Exact real harmonic-probe NS retained RK4 benchmark.

Physical reader:
    Q(T) = < u(x,T) cos(k0.x + phase) >_x
which reads exactly the conjugate Fourier pair +/-k0.

For corner probes k0=(K,K,K), the exact triad cone grows more slowly than for
axis plane averages.  This checker also evaluates a segmented fused-triad
accumulator based on np.add.reduceat.  Triads are compiled contiguously by
output mode, so segmented reduction is algebraically the same sum as np.add.at.

Timing is finite_diagnostic only; exactness claims are relative to the same
fixed finite Fourier-Galerkin RK4 recurrence.
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
    project_vectors,
    random_real_divfree_state,
    triads_by_output,
)
from check_volume6_ns_retained_fold_rk4 import (
    FFTPlan,
    dependency_expand,
    fft_rhs,
    full_rk4,
    fused_rhs,
)


def segmented_fused_rhs(plan: FusedTriadPlan, U: np.ndarray, nu: float) -> np.ndarray:
    """Same ordered-triad sum as fused_rhs, using contiguous segment reduction."""
    up = U[plan.p_idx]
    uq = U[plan.q_idx]
    qdot = np.einsum("ij,ij->i", plan.qvec, up)
    contributions = 1j * qdot[:, None] * uq
    nout = len(plan.outputs)

    conv = np.zeros((nout, 3), dtype=complex)
    if len(plan.out_slot):
        counts = np.bincount(plan.out_slot, minlength=nout)
        starts_all = np.cumsum(np.r_[0, counts[:-1]])
        nonempty = np.flatnonzero(counts)
        starts = starts_all[nonempty]
        conv[nonempty] = np.add.reduceat(contributions, starts, axis=0)

    conv = project_vectors(conv, plan.kvec)
    return -conv - nu * plan.k2[:, None] * U[plan.k_idx]


def fast_fused_rhs(plan: FusedTriadPlan, U: np.ndarray, nu: float) -> np.ndarray:
    # np.add.at remains cheaper for very small terminal batches.
    if plan.triad_count < 256:
        return fused_rhs(plan, U, nu)
    return segmented_fused_rhs(plan, U, nu)


def harmonic_value(U, index, k0: Mode, phase: float) -> np.ndarray:
    km = tuple(-x for x in k0)
    return 0.5 * (
        U[index[km]] * np.exp(1j * phase)
        + U[index[k0]] * np.exp(-1j * phase)
    )


def compile_plan(K, horizon, Uprobe, dt, nu, calibration_repeats=5):
    modes = cube_modes(K)
    index = {k: i for i, k in enumerate(modes)}
    triads = triads_by_output(modes)
    fft = FFTPlan.compile(modes, K)
    k0 = (K, K, K)
    targets = {k0, (-K, -K, -K)}

    allf = FusedTriadPlan.compile(modes, triads, modes)
    kernel_equiv = float(np.max(np.abs(
        fast_fused_rhs(allf, Uprobe, nu) - fused_rhs(allf, Uprobe, nu)
    )))
    backend_equiv = float(np.max(np.abs(
        fast_fused_rhs(allf, Uprobe, nu) - fft_rhs(fft, Uprobe, nu)
    )))
    fft_seconds = median_seconds(lambda: fft_rhs(fft, Uprobe, nu), calibration_repeats)

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
            fp = FusedTriadPlan.compile(modes, triads, outputs)
            fsec = median_seconds(
                lambda f=fp: fast_fused_rhs(f, Uprobe, nu), calibration_repeats
            )
            backend = "fused_segmented" if fsec <= fft_seconds else "full_fft"
            stages.append((name, fp, backend, fsec, fft_seconds))
        steps.append((S0, K4, stages))

    return {
        "modes": modes,
        "index": index,
        "triads": triads,
        "fft": fft,
        "k0": k0,
        "targets": targets,
        "steps": steps,
        "kernel_equivalence_error": kernel_equiv,
        "backend_equivalence_error": backend_equiv,
    }


def execute(plan, U0, dt, nu):
    U = U0.copy()
    for _, _, stages in plan["steps"]:
        stage_derivs = []
        stage_state = U
        factors = (0.5, 0.5, 1.0)
        for si, (_, fp, backend, _, _) in enumerate(stages):
            if backend == "full_fft":
                selected = fft_rhs(plan["fft"], stage_state, nu)[fp.k_idx]
            else:
                selected = fast_fused_rhs(fp, stage_state, nu)
            deriv = np.zeros_like(U)
            deriv[fp.k_idx] = selected
            stage_derivs.append(deriv)
            if si < 3:
                next_fp = stages[si + 1][1]
                stage_state = U.copy()
                stage_state[fp.k_idx] = U[fp.k_idx] + factors[si] * dt * selected

        k1, k2, k3, k4 = stage_derivs
        out_idx = stages[3][1].k_idx
        U_next = U.copy()
        U_next[out_idx] = U[out_idx] + (dt / 6.0) * (
            k1[out_idx] + 2 * k2[out_idx] + 2 * k3[out_idx] + k4[out_idx]
        )
        U = U_next
    return U


def run_case(K, horizon, dt=0.0025, nu=0.005, phase=0.3, repeats=7):
    modes = cube_modes(K)
    U0 = random_real_divfree_state(modes)
    plan = compile_plan(K, horizon, U0, dt, nu)

    retained = execute(plan, U0, dt, nu)
    full = full_rk4(plan["fft"], U0, dt, nu, horizon)
    qr = harmonic_value(retained, plan["index"], plan["k0"], phase)
    qf = harmonic_value(full, plan["index"], plan["k0"], phase)
    err = float(np.linalg.norm(qr - qf))

    retained_seconds = median_seconds(lambda: execute(plan, U0, dt, nu), repeats)
    full_seconds = median_seconds(
        lambda: full_rk4(plan["fft"], U0, dt, nu, horizon), repeats
    )

    C = sum(len(plan["triads"][k]) for k in modes)
    full_work = 4 * horizon * C
    retained_work = sum(
        stage[1].triad_count
        for step in plan["steps"]
        for stage in step[2]
    )

    return {
        "K": K,
        "horizon": horizon,
        "wavevector": list(plan["k0"]),
        "mode_count": len(modes),
        "terminal_mode_count": 2,
        "readout_density": 2 / len(modes),
        "kernel_equivalence_error": plan["kernel_equivalence_error"],
        "backend_equivalence_error": plan["backend_equivalence_error"],
        "target_abs_error": err,
        "imaginary_residual": float(np.max(np.abs(qr.imag))),
        "structural_work_reduction": full_work / retained_work,
        "retained_seconds": retained_seconds,
        "full_seconds": full_seconds,
        "observed_speedup": full_seconds / retained_seconds,
        "terminal_step_cone": {
            "input_modes": len(plan["steps"][-1][0]),
            "k1_modes": len(plan["steps"][-1][2][0][1].outputs),
            "k2_modes": len(plan["steps"][-1][2][1][1].outputs),
            "k3_modes": len(plan["steps"][-1][2][2][1].outputs),
            "k4_modes": len(plan["steps"][-1][2][3][1].outputs),
        },
        "backends": [
            [stage[2] for stage in step[2]]
            for step in plan["steps"]
        ],
    }


def main():
    rows = [run_case(K, H) for K in (2, 3) for H in (1, 2, 3)]
    kernel_ok = all(r["kernel_equivalence_error"] < 1e-12 for r in rows)
    backend_ok = all(r["backend_equivalence_error"] < 1e-12 for r in rows)
    target_ok = all(r["target_abs_error"] < 1e-12 for r in rows)
    real_ok = all(r["imaginary_residual"] < 1e-12 for r in rows)

    for r in rows:
        c = r["terminal_step_cone"]
        print(
            f"K={r['K']} H={r['horizon']} cone="
            f"{c['k1_modes']}/{c['k2_modes']}/{c['k3_modes']}/{c['k4_modes']} "
            f"structural={r['structural_work_reduction']:.3f}x "
            f"speed={r['observed_speedup']:.3f}x err={r['target_abs_error']:.3e}"
        )

    claims = [
        {"id": "Vol6-NSHarmonic-segmented-kernel", "tier": "finite_diagnostic",
         "status": "PASS" if kernel_ok else "FAIL",
         "evidence": "segmented reduceat fused kernel agrees with the original fused triad sum to 1e-12"},
        {"id": "Vol6-NSHarmonic-backend-equivalence", "tier": "finite_diagnostic",
         "status": "PASS" if backend_ok else "FAIL",
         "evidence": "optimized fused and pseudo-spectral FFT RHS agree on the same finite cube to 1e-12"},
        {"id": "Vol6-NSHarmonic-task-exactness", "tier": "finite_diagnostic",
         "status": "PASS" if target_ok and real_ok else "FAIL",
         "evidence": "real harmonic retained RK4 readout agrees with full finite RK4 and is real to 1e-12"},
    ]
    ok = kernel_ok and backend_ok and target_ok and real_ok
    print("REPORT_JSON:" + json.dumps(rows, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
