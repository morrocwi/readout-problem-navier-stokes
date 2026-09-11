#!/usr/bin/env python3
"""NON-CERTIFYING search for robust overdetermined N=1 energy-sample schedules.

A practical instrument is not restricted to exactly 49 scalar observations.  This probe
samples all three shell energies at n uniformly spaced times, forms the M x 49 direct
sample Jacobian (M=3n), normalizes each measurement by its center magnitude to model a
uniform relative sensor-error budget, and constructs a floating left inverse with
``numpy.linalg.pinv``.  It searches total windows of O(1) turnover times.

The result is target selection only.  Any candidate must later be recertified with an
outward-rounded/interval center Jacobian, branch-wide q<1 bound, and a declared sensor
model.  No result here is a theorem.
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


def build_float_operators(cube):
    T = np.asarray(comp.scaled_bilinear_tensor(cube), dtype=np.float64) / C
    L = np.repeat(
        np.asarray([-NU * sum(float(v) * float(v) for v in k) for k in cube.reps]), 4
    )
    W = np.asarray(cube.weights, dtype=np.float64)
    return T, L, W


def rhs_factory(T, L, d, nf):
    def rhs(_t, y):
        x = y[:d]
        G = y[d:].reshape(d, nf)
        dx = L * x + np.einsum("mjk,j,k->m", T, x, x, optimize=True)
        dG = (
            L[:, None] * G
            + np.einsum("mjk,ja,k->ma", T, G, x, optimize=True)
            + np.einsum("mjk,j,ka->ma", T, x, G, optimize=True)
        )
        return np.concatenate([dx, dG.reshape(-1)])
    return rhs


def map_and_jacobian(sol, W, times, d, nf):
    vals, rows = [], []
    for t in times:
        y = sol.sol(float(t))
        x = y[:d]
        G = y[d:].reshape(d, nf)
        for shell in range(3):
            vals.append(float(np.sum(W[shell] * x * x)))
            rows.append(2.0 * ((W[shell] * x) @ G))
    return np.asarray(vals), np.asarray(rows)


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared N=1 center did not reproduce")
    x0 = small.small_state(CENTER_SEED, cube.d).astype(np.float64)
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    nf = len(free)
    if nf != 49:
        raise RuntimeError("expected 49-dimensional slice")

    T, L, W = build_float_operators(cube)
    G0 = np.zeros((cube.d, nf), dtype=float)
    for a, j in enumerate(free):
        G0[j, a] = 1.0
    y0 = np.concatenate([x0, G0.reshape(-1)])

    windows = np.linspace(0.4, 3.0, 27)
    counts = (17, 21, 25, 33, 41, 49, 65)
    sol = solve_ivp(
        rhs_factory(T, L, cube.d, nf),
        (0.0, float(np.max(windows))),
        y0,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        dense_output=True,
        max_step=0.01,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    records = []
    for window in windows:
        for n in counts:
            times = np.linspace(0.0, float(window), n)
            vals, J = map_and_jacobian(sol, W, times, cube.d, nf)
            scale = np.maximum(np.abs(vals), 1.0)
            Jrel = J / scale[:, None]
            s = np.linalg.svd(Jrel, compute_uv=False)
            tol = max(Jrel.shape) * np.finfo(float).eps * s[0]
            rank = int(np.sum(s > tol))
            if rank != nf:
                continue
            A = np.linalg.pinv(Jrel, rcond=1e-13)
            identity_defect = float(np.linalg.norm(A @ Jrel - np.eye(nf), ord=np.inf))
            Ainf = float(np.linalg.norm(A, ord=np.inf))
            sigma_min = float(s[-1])
            cond2 = float(s[0] / s[-1])
            records.append({
                "window": float(window),
                "samples_per_shell": int(n),
                "measurement_count": int(3*n),
                "cadence": float(window/(n-1)),
                "rank": rank,
                "sigma_min_relative_chart": sigma_min,
                "cond2_relative_chart": cond2,
                "left_inverse_inf_relative_chart": Ainf,
                "identity_defect": identity_defect,
                "rho_proxy_for_1e-6_relative_sensor_radius": Ainf * 1e-6,
            })

    if not records:
        raise RuntimeError("no full-rank overdetermined candidate")
    records.sort(key=lambda r: r["left_inverse_inf_relative_chart"])
    best = records[0]
    shortlist = records[:20]
    summary = {
        "scope": "NON-CERTIFYING floating target selection only",
        "measurement_model": "all three shell energies; each row divided by max(|center shell energy|,1), so sigma is an approximate relative-error radius",
        "best": best,
        "shortlist": shortlist,
        "physical_interpretation": "for advective scaling t*=tU/L: cadence_phys=cadence*L/U and window_phys=window*L/U",
        "next_gate": "validated center-flow/tangent enclosure + outward left inverse + branch-wide q<1 + explicit sensor/model error budget",
    }
    print("EPSC-19 N=1 overdetermined practical schedule probe (NON-CERTIFYING)")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({
        "claims": [{
            "id": "V7-EPSC19-N1-OVERDETERMINED-SCHEDULE-PROBE",
            "name": "floating relative-noise search for an overdetermined direct sample schedule",
            "tier": "finite_diagnostic",
            "status": "PASS",
            "evidence": f"best window={best['window']:.6g}, n={best['samples_per_shell']}, cadence={best['cadence']:.6g}, Ainf={best['left_inverse_inf_relative_chart']:.6g}; NON-CERTIFYING",
        }],
        "summary": summary,
    }, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
