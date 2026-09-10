#!/usr/bin/env python3
"""Exact explicit quotient-chart witness for the N=2 shell-energy reader.

The companion N=2 shell checker proves rank 245 at R=30 using a 245-column
random tangent projection.  This checker removes that last structural shortcut.
It fixes three concrete translation-gauge coordinates, propagates the 245
coordinate tangent directions spanning the resulting affine slice, and selects
an explicit 245-row shell-energy Taylor chart whose determinant is nonzero
modulo p=251.

At the deterministic finite-field center, the gauge coordinates are the
imaginary first-basis amplitudes of the three axial representative modes
(1,0,0), (0,1,0), (0,0,1).  The translation differential on these coordinates
is diagonal with entries equal to the corresponding real first-basis
amplitudes, which are nonzero at the declared center.  Hence the coordinate
slice is transverse to the three-dimensional translation orbit.

Because p=251 is larger than R=30 and all declared basis, viscosity, Taylor and
factorial denominators are invertible modulo p, a nonzero selected 245x245
minor proves the corresponding characteristic-zero rational minor at the
integer lift of this center is nonzero.  This establishes fixed-N=2 local
inverse existence on an explicit finite symmetry slice.  It does not supply a
quantitative radius q_2<1, branch/noise stability, arbitrary-N induction,
continuum regularity, DNS adequacy, or a Clay result.
"""
from __future__ import annotations

import json
import time
import numpy as np

import check_k2_energy_observability as k2

P = k2.P
RMAX = 30
SEED_STATE = k2.SEED_STATE
BATCH = k2.d - 3


@k2.njit(parallel=True, cache=True)
def shell_block(n, Vcoef, xcoef, weights, P):
    batch = Vcoef.shape[1]
    ns = weights.shape[0]
    out = np.empty((ns, batch), dtype=np.uint16)
    for bb in k2.prange(batch):
        for s in range(ns):
            acc = np.int64(0)
            for i in range(n + 1):
                j = n - i
                for c in range(Vcoef.shape[2]):
                    acc += (
                        2
                        * np.int64(weights[s, c])
                        * np.int64(Vcoef[i, bb, c])
                        * np.int64(xcoef[j, c])
                    )
            out[s, bb] = acc % P
    return out


def axial_gauge_coordinates():
    coords = []
    for mode in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        ri = k2.rep_index[mode]
        coords.append(4 * ri + 1)  # imaginary coordinate of first transverse basis amplitude
    return coords


def translation_gauge_matrix(x0, gauge):
    """Differential of the three gauge coordinates along translation generators."""
    G = np.zeros((3, 3), dtype=np.int64)
    axial = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for row, (mode, coord) in enumerate(zip(axial, gauge)):
        ri = k2.rep_index[mode]
        ar = int(x0[4 * ri]) % P
        # d(ai)/d a_j = k_j * ar for exp(i k.a) action.
        for j in range(3):
            G[row, j] = (int(mode[j]) * ar) % P
    return G


def det_mod(A, p=P):
    A = np.asarray(A, dtype=np.int64).copy() % p
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError("square matrix required")
    det = 1
    sign = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if int(A[r, col]) % p), None)
        if pivot is None:
            return 0
        if pivot != col:
            A[[col, pivot]] = A[[pivot, col]]
            sign = -sign
        pv = int(A[col, col]) % p
        det = det * pv % p
        inv = pow(pv, -1, p)
        A[col] = A[col] * inv % p
        for r in range(col + 1, n):
            c = int(A[r, col]) % p
            if c:
                A[r] = (A[r] - c * A[col]) % p
    if sign < 0:
        det = (-det) % p
    return int(det)


def select_independent_rows(A, target, p=P):
    """Greedy exact row-basis selection with row indices over F_p."""
    A = np.asarray(A, dtype=np.int64) % p
    pivots = []  # list of (pivot_col, normalized row, original_index)
    selected = []
    for idx in range(A.shape[0]):
        row = A[idx].copy()
        for col, prow, _ in pivots:
            c = int(row[col]) % p
            if c:
                row = (row - c * prow) % p
        nz = np.flatnonzero(row % p)
        if nz.size == 0:
            continue
        col = int(nz[0])
        row = row * pow(int(row[col]), -1, p) % p
        # Keep earlier pivots reduced in the new pivot column so future reduction
        # remains deterministic and the selected rows form a certified basis.
        new_pivots = []
        for pcol, prow, pidx in pivots:
            c = int(prow[col]) % p
            if c:
                prow = (prow - c * row) % p
            new_pivots.append((pcol, prow, pidx))
        pivots = new_pivots + [(col, row, idx)]
        pivots.sort(key=lambda t: t[0])
        selected.append(idx)
        if len(selected) == target:
            break
    return selected


def main() -> int:
    ns = len(k2.shells)
    ceiling = k2.d - 3
    assert k2.N == 2 and k2.d == 248 and BATCH == 245 and ns == 9
    assert P == 251 and P > RMAX

    rng = np.random.default_rng(SEED_STATE)
    x0 = rng.integers(1, P, size=k2.d, dtype=np.uint16)

    gauge = axial_gauge_coordinates()
    free = [j for j in range(k2.d) if j not in gauge]
    assert len(free) == BATCH and len(set(gauge)) == 3
    G = translation_gauge_matrix(x0, gauge)
    gauge_det = det_mod(G)
    gauge_ok = gauge_det != 0
    if not gauge_ok:
        raise RuntimeError("declared axial coordinate gauge is not transverse at the center")

    print(
        f"N=2 explicit quotient shell chart: d={k2.d} slice={BATCH} shells={ns} "
        f"Rmax={RMAX} prime={P} gauge={gauge} gauge_det={gauge_det}",
        flush=True,
    )

    # State Taylor coefficients at the declared center.
    xcoef = np.zeros((RMAX + 1, k2.d), dtype=np.uint16)
    Ux = np.zeros((RMAX + 1, k2.nm, 3, 2), dtype=np.uint16)
    xcoef[0] = x0
    k2.recon_one(xcoef[0], Ux[0], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    _ = k2.state_rhs(
        0, xcoef, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
        k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
    )
    t0 = time.time()
    for n in range(RMAX):
        rhs = k2.state_rhs(
            n, xcoef, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
            k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
        )
        xcoef[n + 1] = (rhs.astype(np.int64) * pow(n + 1, -1, P) % P).astype(np.uint16)
        k2.recon_one(xcoef[n + 1], Ux[n + 1], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    state_sec = time.time() - t0

    # Tangent basis of the explicit coordinate slice, not a random projection.
    Vcoef = np.zeros((RMAX + 1, BATCH, k2.d), dtype=np.uint16)
    UV = np.zeros((RMAX + 1, BATCH, k2.nm, 3, 2), dtype=np.uint16)
    for col, coord in enumerate(free):
        Vcoef[0, col, coord] = 1
    k2.recon_batch(Vcoef[0], UV[0], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    _ = k2.tangent_rhs(
        0, Vcoef, UV, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
        k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
    )

    weights = k2.weights.astype(np.uint16)
    blocks = [shell_block(0, Vcoef, xcoef, weights, P)]
    t1 = time.time()
    for n in range(RMAX):
        rhs = k2.tangent_rhs(
            n, Vcoef, UV, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
            k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
        )
        Vcoef[n + 1] = (rhs.astype(np.int64) * pow(n + 1, -1, P) % P).astype(np.uint16)
        k2.recon_batch(Vcoef[n + 1], UV[n + 1], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
        blocks.append(shell_block(n + 1, Vcoef, xcoef, weights, P))

    Aall = np.vstack(blocks).astype(np.int64) % P
    rank_all = k2.rank_mod(Aall)
    selected = select_independent_rows(Aall, ceiling)
    square_ok = len(selected) == ceiling
    det_square = det_mod(Aall[selected, :]) if square_ok else 0
    chart_ok = rank_all == ceiling and square_ok and det_square != 0

    selected_orders = [int(r // ns) for r in selected]
    selected_shell_slots = [int(r % ns) for r in selected]
    max_selected_order = max(selected_orders) if selected_orders else None
    order_counts = {str(r): selected_orders.count(r) for r in sorted(set(selected_orders))}

    claims = [
        {
            "id": "V7-EPSC32-N2-EXPLICIT-TRANSLATION-SLICE",
            "name": "explicit three-coordinate N=2 translation gauge is transverse at the declared finite center",
            "tier": "finite_diagnostic",
            "status": "PASS" if gauge_ok else "FAIL",
            "evidence": f"gauge coordinates={gauge}; exact F_251 translation-gauge determinant={gauge_det} != 0",
        },
        {
            "id": "V7-EPSC32-N2-EXPLICIT-SLICE-RANK",
            "name": "N=2 shell jet reaches rank 245 on an explicit 245-dimensional coordinate slice",
            "tier": "finite_diagnostic",
            "status": "PASS" if rank_all == ceiling else "FAIL",
            "evidence": f"exact F_251 shell-jet Jacobian on coordinate slice has rank={rank_all}; target={ceiling}; R<=30",
        },
        {
            "id": "V7-EPSC32-N2-SQUARE-SHELL-CHART",
            "name": "explicit 245-observation N=2 shell-energy chart has a nonzero maximal minor",
            "tier": "finite_diagnostic",
            "status": "PASS" if chart_ok else "FAIL",
            "evidence": f"greedy exact row basis selected {len(selected)} rows; determinant mod 251={det_square}; max selected order={max_selected_order}",
        },
        {
            "id": "V7-EPSC32-N2-LOCAL-INVERSE-EXISTENCE",
            "name": "fixed finite N=2 shell chart has local characteristic-zero inverse on the explicit translation slice",
            "tier": "Dr",
            "status": "DERIVED" if chart_ok else "OPEN",
            "evidence": (
                "nonzero good-prime reduction of the explicit 245x245 Taylor-chart minor, with p>30 and all declared denominators invertible, proves the corresponding rational minor is nonzero at the integer lift; finite-dimensional inverse-function theorem applies locally on the transverse slice"
                if chart_ok else
                "explicit square-chart prerequisites did not all certify"
            ),
        },
        {
            "id": "V7-EPSC32-N2-QUANTITATIVE-Q2",
            "name": "positive branch-wide quantitative N=2 inverse certificate q_2<1 and rho_2",
            "tier": "Open",
            "status": "OPEN",
            "evidence": "local inverse existence does not yet supply a characteristic-zero preconditioner, interval Jacobian enclosure, branch capture, or measurement radius at N=2",
        },
    ]

    summary = {
        "N": 2,
        "state_dimension": k2.d,
        "slice_dimension": BATCH,
        "shell_count": ns,
        "max_taylor_order": RMAX,
        "gauge_coordinates": gauge,
        "gauge_det_mod_p": gauge_det,
        "slice_rank_mod_p": rank_all,
        "selected_row_count": len(selected),
        "selected_minor_det_mod_p": det_square,
        "max_selected_order": max_selected_order,
        "selected_order_counts": order_counts,
        "selected_shell_slots_sha_like_checksum": int(sum((i + 1) * s for i, s in enumerate(selected_shell_slots)) % P),
        "state_series_sec": state_sec,
        "tangent_and_chart_sec": time.time() - t1,
        "prime": P,
        "finite_first_scope": "fixed N=2 finite polynomial system and explicit finite coordinate slice; no completed-infinity premise",
    }
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")), flush=True)
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
