#!/usr/bin/env python3
"""Floating target-selection probe for a practical direct N=1 sample schedule.

NON-CERTIFYING by design. This integrates the finite 52-real-dimensional N=1
Fourier--Galerkin ODE together with the 49 slice tangent directions in binary64 and
searches finite sample spacings h for a well-conditioned direct 49-sample shell-energy
map. It does not reconstruct high-order Taylor derivatives from data.

The output is only a target selector for a later exact/interval certificate. No PASS
from this file is a theorem.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as comp
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910
C = 600.0
NU = 1.0 / 200.0
MAX_NODE = 23


def build_float_operators(cube):
    Tint = comp.scaled_bilinear_tensor(cube)
    T = np.asarray(Tint, dtype=np.float64) / C
    L = np.repeat(
        np.asarray([-NU * sum(float(v) * float(v) for v in k) for k in cube.reps]),
        4,
    )
    W = np.asarray(cube.weights, dtype=np.float64)
    return T, L, W


def rhs_factory(T, L, d, free):
    nf = len(free)

    def rhs(_t, y):
        x = y[:d]
        G = y[d:].reshape(d, nf)
        Bxx = np.einsum("mjk,j,k->m", T, x, x, optimize=True)
        BGx = np.einsum("mjk,ja,k->ma", T, G, x, optimize=True)
        BxG = np.einsum("mjk,j,ka->ma", T, x, G, optimize=True)
        dx = L * x + Bxx
        dG = L[:, None] * G + BGx + BxG
        return np.concatenate([dx, dG.reshape(-1)])

    return rhs


def sample_jacobian(sol, W, h, d, free):
    nf = len(free)
    rows = []
    for shell in (0, 1):
        for node in range(24):
            y = sol.sol(node * h)
            x = y[:d]
            G = y[d:].reshape(d, nf)
            rows.append(2.0 * ((W[shell] * x) @ G))
    y0 = sol.sol(0.0)
    x0 = y0[:d]
    G0 = y0[d:].reshape(d, nf)
    rows.append(2.0 * ((W[2] * x0) @ G0))
    return np.asarray(rows, dtype=np.float64)


def shell_values(sol, W, h, d):
    vals = []
    for shell in (0, 1):
        for node in range(24):
            x = sol.sol(node * h)[:d]
            vals.append(float(np.sum(W[shell] * x * x)))
    x0 = sol.sol(0.0)[:d]
    vals.append(float(np.sum(W[2] * x0 * x0)))
    return np.asarray(vals)


def candidate_grid():
    a = np.logspace(-4, -1, 25)
    b = np.linspace(0.11, 0.50, 40)
    c = np.asarray([
        1/24, 1/22, 1/20, 1/19, 1/18, 9/160, 1/17, 1/16, 1/15, 1/14,
    ], dtype=float)
    return np.unique(np.concatenate([a, b, c]))


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared N=1 small-integer center did not reproduce")
    x0 = small.small_state(CENTER_SEED, cube.d).astype(np.float64)
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    if len(free) != 49:
        raise RuntimeError("expected 49-dimensional slice")

    T, L, W = build_float_operators(cube)
    G0 = np.zeros((cube.d, len(free)), dtype=np.float64)
    for a, j in enumerate(free):
        G0[j, a] = 1.0
    y0 = np.concatenate([x0, G0.reshape(-1)])

    hs = candidate_grid()
    tmax = MAX_NODE * float(np.max(hs))
    sol = solve_ivp(
        rhs_factory(T, L, cube.d, free),
        (0.0, tmax),
        y0,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        dense_output=True,
        max_step=0.02,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    records = []
    for h in hs:
        J = sample_jacobian(sol, W, float(h), cube.d, free)
        s = np.linalg.svd(J, compute_uv=False)
        rank = int(np.linalg.matrix_rank(J, tol=max(J.shape) * np.finfo(float).eps * s[0]))
        vals = shell_values(sol, W, float(h), cube.d)
        abs_scale = float(max(1.0, np.max(np.abs(vals))))
        row_scale = np.maximum(np.abs(vals), 1.0)
        Jrel = J / row_scale[:, None]
        srel = np.linalg.svd(Jrel, compute_uv=False)
        rank_rel = int(np.linalg.matrix_rank(Jrel, tol=max(Jrel.shape) * np.finfo(float).eps * srel[0]))
        if rank == 49 and rank_rel == 49 and s[-1] > 0 and srel[-1] > 0:
            try:
                A = np.linalg.inv(J)
                Arel = np.linalg.inv(Jrel)
                ainv = float(np.linalg.norm(A, ord=np.inf))
                arel = float(np.linalg.norm(Arel, ord=np.inf))
            except np.linalg.LinAlgError:
                ainv = math.inf
                arel = math.inf
            cond2 = float(s[0] / s[-1])
            cond2rel = float(srel[0] / srel[-1])
            sigma_min = float(s[-1])
            sigma_min_rel = float(srel[-1])
        else:
            ainv = arel = math.inf
            cond2 = cond2rel = math.inf
            sigma_min = sigma_min_rel = 0.0
        records.append({
            "h": float(h),
            "T": float(MAX_NODE * h),
            "rank": rank,
            "sigma_min": sigma_min,
            "cond2": cond2,
            "inverse_inf": ainv,
            "sample_abs_scale": abs_scale,
            "rho_proxy_for_1e-6_relative_energy_noise_using_global_abs_scale": ainv * 1e-6 * abs_scale if math.isfinite(ainv) else math.inf,
            "sigma_min_relative_chart": sigma_min_rel,
            "cond2_relative_chart": cond2rel,
            "inverse_inf_relative_chart": arel,
            "rho_proxy_for_1e-6_rowwise_relative_sensor_radius": arel * 1e-6 if math.isfinite(arel) else math.inf,
        })

    finite = [r for r in records if math.isfinite(r["inverse_inf"])]
    if not finite:
        raise RuntimeError("no finite full-rank sample Jacobian in the declared grid")
    best = min(finite, key=lambda r: r["inverse_inf"])
    best_rel = min(finite, key=lambda r: r["inverse_inf_relative_chart"])
    shortlist = sorted(finite, key=lambda r: r["inverse_inf_relative_chart"])[:15]

    summary = {
        "scope": "NON-CERTIFYING floating target selection only",
        "cutoff": 1,
        "state_dimension": 52,
        "slice_dimension": 49,
        "sample_count": 49,
        "searched_h_min": float(np.min(hs)),
        "searched_h_max": float(np.max(hs)),
        "best_absolute_chart_inverse_inf": best,
        "best_rowwise_relative_chart_inverse_inf": best_rel,
        "shortlist_by_relative_inverse_inf": shortlist,
        "relative_measurement_model": "each row divided by max(|center shell energy|,1); sigma then approximates a uniform rowwise relative sensor radius",
        "physical_interpretation": "if t*=t U/L, then Delta t_phys=h L/U and total window=23 h L/U; no seconds are claimed until L,U are declared",
        "claim_boundary": "diagnostic only; candidate must be recertified with validated finite flow/tangent intervals and an exact or outward-rounded preconditioner",
    }
    print("EPSC-19 N=1 practical direct-sample schedule probe (NON-CERTIFYING)")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({
        "claims": [{
            "id": "V7-EPSC19-N1-PRACTICAL-SCHEDULE-PROBE",
            "name": "floating target selection for a finite-time direct sample schedule",
            "tier": "finite_diagnostic",
            "status": "PASS",
            "evidence": f"best absolute h={best['h']:.12g}; best relative h={best_rel['h']:.12g}, relative Ainf={best_rel['inverse_inf_relative_chart']:.6g}; NON-CERTIFYING",
        }],
        "summary": summary,
    }, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
