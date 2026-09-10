#!/usr/bin/env python3
"""Non-certifying floating probe for the next EPSC-18 entrywise interval stage.

This script is deliberately a DIAGNOSTIC, not a proof.  It keeps the exact finite N=1
center Jacobian and its exact rational inverse from the certified checker, but propagates
symmetric center-radius enclosures in numpy long-double arithmetic to estimate where a
future directed-rounding/exact-rational interval implementation is worth targeting.

The probe preserves substantially more structure than the previous scalar Hessian bounds:
state and tangent radii are componentwise, the exact center recurrence is retained, and
the final 49x49 Jacobian radius is preconditioned entrywise by |J0^{-1}|.

No q<1 value from this file is promoted to a rigorous certificate.  The only purpose is
to locate a promising box scale for the subsequent exact interval checker.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as component
import check_volume7_eps18_n1_exact_preconditioner as exact
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910
RMAX = 23
RADII = [10.0 ** (-k) for k in (2, 4, 6, 8, 10, 12, 16, 20, 24, 28)]
LD = np.longdouble


def center_state_tangent(cube, x0):
    x0 = np.asarray(x0, dtype=object)
    X = [x0]
    DX = [np.eye(cube.d, dtype=object)]
    lc = np.repeat(np.asarray([-3 * sum(int(v) * int(v) for v in k) for k in cube.reps], dtype=object), 4)
    for n in range(RMAX):
        rhs = X[n] * lc
        drhs = DX[n] * lc[None, :]
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            rhs += w * exact._scaled_bilinear(cube, X[i], X[j])
            drhs += w * (exact._scaled_bilinear(cube, DX[i], X[j]) + exact._scaled_bilinear(cube, X[i], DX[j]))
        X.append(rhs)
        DX.append(drhs)
    return X, DX


def tensor_abs_float(cube):
    T = component.scaled_bilinear_tensor(cube)
    return np.abs(np.asarray(T, dtype=LD))


def left_matrix(Tabs, v):
    # M(v)[m,a] = sum_b |T[m,a,b]| v[b]
    return np.tensordot(Tabs, v, axes=([2], [0]))


def right_matrix(Tabs, u):
    # N(u)[m,b] = sum_a |T[m,a,b]| u[a]
    return np.tensordot(Tabs, u, axes=([1], [0]))


def babs_vec(Tabs, u, v):
    return left_matrix(Tabs, v) @ u


def propagate_q(cube, Tabs, Xc, Gc, Aabs, selected, free, radius):
    d = cube.d
    shells = len(cube.shells)
    rx = [np.zeros(d, dtype=LD)]
    rx[0][free] = LD(radius)
    rg = [np.zeros((d, len(free)), dtype=LD)]
    W = np.asarray(cube.weights, dtype=LD)
    lcabs = np.repeat(np.asarray([3 * sum(int(v) * int(v) for v in k) for k in cube.reps], dtype=LD), 4)

    Xabs = [np.abs(np.asarray(x, dtype=LD)) for x in Xc]
    Gfree = [np.asarray(g[:, free], dtype=LD) for g in Gc]
    Gabs = [np.abs(g) for g in Gfree]
    jrad_blocks = []

    for n in range(RMAX + 1):
        jr = np.zeros((shells, len(free)), dtype=LD)
        for i in range(n + 1):
            j = n - i
            w = LD(math.comb(n, i))
            # Q(G_i, X_j): exact diagonal shell quadratic readout.
            jr += w * ((rg[i] * Xabs[j][:, None] + (Gabs[i] + rg[i]) * rx[j][:, None]).T @ W.T).T
            jr += w * ((rg[j] * Xabs[i][:, None] + (Gabs[j] + rg[j]) * rx[i][:, None]).T @ W.T).T
        jrad_blocks.append(jr)
        if n == RMAX:
            break

        rxn = lcabs * rx[n]
        rgn = lcabs[:, None] * rg[n]
        for i in range(n + 1):
            j = n - i
            w = LD(math.comb(n, i))

            # Radius of B(X_i, X_j) around the exact center.
            rxn += w * (
                babs_vec(Tabs, Xabs[i], rx[j])
                + babs_vec(Tabs, rx[i], Xabs[j] + rx[j])
            )

            # Radius of B(G_i, X_j).
            M_rxj = left_matrix(Tabs, rx[j])
            M_xj_plus = left_matrix(Tabs, Xabs[j] + rx[j])
            rgn += w * (M_rxj @ Gabs[i] + M_xj_plus @ rg[i])

            # Radius of B(X_i, G_j).
            N_rxi = right_matrix(Tabs, rx[i])
            N_xi_plus = right_matrix(Tabs, Xabs[i] + rx[i])
            rgn += w * (N_rxi @ Gabs[j] + N_xi_plus @ rg[j])

        rx.append(rxn)
        rg.append(rgn)

    Jrad = np.vstack(jrad_blocks)[selected, :]
    defect_radius = Aabs @ Jrad
    q = np.max(np.sum(defect_radius, axis=1))
    return float(q)


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("small-integer N=1 center did not reproduce")
    x0 = small.small_state(CENTER_SEED, cube.d)
    selected = [int(v) for v in center["selected_observation_rows"]]
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    shells = len(cube.shells)

    blocks = exact.exact_scaled_shell_blocks(cube, x0)
    J0 = [[int(blocks[r // shells][r % shells, j]) for j in free] for r in selected]
    A, det = exact.exact_inverse(J0)
    if det == 0:
        raise ArithmeticError("exact center Jacobian unexpectedly singular")
    Aabs = np.asarray([[LD(abs(x.numerator)) / LD(x.denominator) for x in row] for row in A], dtype=LD)

    Xc, Gc = center_state_tangent(cube, x0)
    Tabs = tensor_abs_float(cube)

    results = []
    first_below_one = None
    for radius in RADII:
        q = propagate_q(cube, Tabs, Xc, Gc, Aabs, selected, free, radius)
        finite = math.isfinite(q)
        rec = {"radius": radius, "q_probe": q, "finite": finite, "q_below_one_probe": bool(finite and q < 1.0)}
        results.append(rec)
        if rec["q_below_one_probe"] and first_below_one is None:
            first_below_one = radius

    claims = [
        {
            "id": "V7-EPSC18-N1-ENTRYWISE-INTERVAL-SCALE-PROBE",
            "name": "floating componentwise/entrywise probe for the next exact N=1 interval box",
            "tier": "finite_diagnostic",
            "status": "PASS" if all(r["finite"] for r in results) else "FAIL",
            "evidence": f"long-double structured radius propagation completed at {len(results)} declared box radii; first q<1 probe radius={first_below_one}",
        },
        {
            "id": "V7-EPSC18-N1-ENTRYWISE-INTERVAL-CERTIFICATE",
            "name": "directed-rounding or exact-rational entrywise q<1 interval certificate at the probed scale",
            "tier": "Open",
            "status": "OPEN",
            "evidence": "this file intentionally uses nondirected floating arithmetic only to select the next exact target; no q value here is a proof",
        },
    ]
    print("EPSC-18 N=1 structured entrywise interval scale probe")
    print(json.dumps({"results": results, "first_q_below_one_probe_radius": first_below_one}, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
