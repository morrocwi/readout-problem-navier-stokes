#!/usr/bin/env python3
"""Exact common-denominator entrywise interval certificate for EPSC-18 at N=1.

The earlier componentwise certificate bounds second derivatives on one comparatively
large box and then linearizes that bound all the way down to the accepted radius.  The
floating interval probe showed that much less wrapping is possible if the *centered
state and tangent recurrences themselves* are enclosed componentwise.

This checker turns that idea into an exact finite proof at the conservative target

    ||x-x_*||_infinity <= 10^-17

on the already-certified 49-dimensional translation slice.

There is no floating interval arithmetic here.  Perturbation radii are represented by
nonnegative Python integers over powers of D=10^17.  Because the scaled N=1 recurrence
has integer coefficients after the C^n n! row scaling (C=600), every enclosure step is
an exact integer inequality.  At Taylor order n we use the common denominators

    state-radius     D^(n+1),
    tangent-radius   D^n,
    Jacobian-radius  D^(n+1).

The exact rational preconditioner A=J0^{-1} from the characteristic-zero checker is
then applied to the row-wise entry radii with Fraction arithmetic.  If the resulting
induced infinity defect q is below one, the standard finite interval inverse criterion
is certified on this box.  We demand the stronger q<=1/2 gate.

Scope: fixed finite N=1 local symmetry slice only.  This is a state-space local inverse
box, not yet a sensor/noise tolerance or branch-capture theorem; it has no continuum
regularity, singularity, DNS-adequacy, or Clay implication.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(200_000)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as component
import check_volume7_eps18_n1_exact_preconditioner as exact
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910
RMAX = 23
D = 10**17
TARGET_RADIUS = Fraction(1, D)


def _zeros_vec(d: int):
    return np.zeros(d, dtype=object)


def _zeros_mat(d: int, f: int):
    return np.zeros((d, f), dtype=object)


def center_state_and_tangent(cube, x0, free):
    """Exact integer scaled center state/tangent coefficients through order RMAX."""
    d, f = cube.d, len(free)
    X = [np.asarray(x0, dtype=object)]
    G0 = _zeros_mat(d, f)
    for c, j in enumerate(free):
        G0[j, c] = 1
    G = [G0]
    lc = np.repeat(
        np.asarray([-3 * sum(int(v) * int(v) for v in k) for k in cube.reps], dtype=object),
        4,
    )

    def b_left(M, v):
        # columns of M are first bilinear arguments
        vals = exact._scaled_bilinear(cube, M.T, np.asarray(v, dtype=object))
        return np.asarray(vals, dtype=object).T

    def b_right(v, M):
        vals = exact._scaled_bilinear(cube, np.asarray(v, dtype=object), M.T)
        return np.asarray(vals, dtype=object).T

    for n in range(RMAX):
        xn = X[n] * lc
        gn = G[n] * lc[:, None]
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            xn += w * exact._scaled_bilinear(cube, X[i], X[j])
            gn += w * (b_left(G[i], X[j]) + b_right(X[i], G[j]))
        X.append(xn)
        G.append(gn)
    return X, G


def sparse_abs_tensor(cube):
    T = component.scaled_bilinear_tensor(cube)
    return component.sparse_absolute_tensor(T)


def babs_vec(sparse_T, u, v):
    out = _zeros_vec(len(sparse_T))
    for m, entries in enumerate(sparse_T):
        acc = 0
        for a, b, coeff in entries:
            acc += coeff * int(u[a]) * int(v[b])
        out[m] = acc
    return out


def babs_left(sparse_T, M, v):
    """Absolute bilinear majorant B_abs(M[:,c],v), all columns c."""
    d, f = M.shape
    out = _zeros_mat(d, f)
    for m, entries in enumerate(sparse_T):
        row = out[m]
        for a, b, coeff in entries:
            vb = int(v[b])
            if vb:
                row += (coeff * vb) * M[a]
    return out


def babs_right(sparse_T, u, M):
    """Absolute bilinear majorant B_abs(u,M[:,c]), all columns c."""
    d, f = M.shape
    out = _zeros_mat(d, f)
    for m, entries in enumerate(sparse_T):
        row = out[m]
        for a, b, coeff in entries:
            ua = int(u[a])
            if ua:
                row += (coeff * ua) * M[b]
    return out


def q_jacobian_radius(cube, Gabs, RG, Xabs, RX, i, j, target_power):
    """Integer numerator for radius of Q(G_i,X_j) at denominator D^target_power."""
    # RG_i denominator D^i; RX_j denominator D^(j+1).
    shell_count = len(cube.shells)
    f = RG[i].shape[1]
    out = np.zeros((shell_count, f), dtype=object)
    W = np.asarray(cube.weights, dtype=object)
    mul_rg_x = D ** (target_power - i)
    mul_g_rx = D ** (target_power - (j + 1))
    # Product perturbation has denominator D^(i+j+1)=D^target_power.
    for s in range(shell_count):
        for m in range(cube.d):
            w = int(W[s, m])
            if not w:
                continue
            out[s] += w * (
                RG[i][m] * int(Xabs[j][m]) * mul_rg_x
                + Gabs[i][m] * int(RX[j][m]) * mul_g_rx
                + RG[i][m] * int(RX[j][m])
            )
    return out


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared small-integer N=1 center did not reproduce")

    x0 = small.small_state(CENTER_SEED, cube.d)
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    selected = [int(v) for v in center["selected_observation_rows"]]
    f = len(free)
    shells = len(cube.shells)
    if f != 49 or shells != 3:
        raise RuntimeError("checker is scoped to the declared 49-dimensional N=1 slice")

    # Exact center chart and preconditioner.
    blocks = exact.exact_scaled_shell_blocks(cube, x0)
    J0 = [
        [int(blocks[r // shells][r % shells, j]) for j in free]
        for r in selected
    ]
    A, det_j0 = exact.exact_inverse(J0)
    if det_j0 == 0:
        raise ArithmeticError("exact center Jacobian unexpectedly singular")

    X, G = center_state_and_tangent(cube, x0, free)
    Xabs = [np.abs(np.asarray(v, dtype=object)) for v in X]
    Gabs = [np.abs(np.asarray(M, dtype=object)) for M in G]
    sparse_T = sparse_abs_tensor(cube)

    # Perturbation-radius numerators. RX[n]/D^(n+1), RG[n]/D^n.
    RX = [_zeros_vec(cube.d)]
    for j in free:
        RX[0][j] = 1
    RG = [_zeros_mat(cube.d, f)]  # G_0 is constant, so its variation radius is zero.

    abs_lc = np.repeat(
        np.asarray([3 * sum(int(v) * int(v) for v in k) for k in cube.reps], dtype=object),
        4,
    )
    jrad_blocks = []

    for n in range(RMAX + 1):
        target_power = n + 1
        jr = np.zeros((shells, f), dtype=object)
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            jr += w * q_jacobian_radius(cube, Gabs, RG, Xabs, RX, i, j, target_power)
            jr += w * q_jacobian_radius(cube, Gabs, RG, Xabs, RX, j, i, target_power)
        jrad_blocks.append(jr)

        if n == RMAX:
            break

        # Next state radius numerator at denominator D^(n+2).
        rxn = abs_lc * RX[n] * D
        # Next tangent radius numerator at denominator D^(n+1).
        rgn = abs_lc[:, None] * RG[n] * D

        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)

            # State: B(X_i+dX_i, X_j+dX_j)-B(X_i,X_j).
            rxn += w * (
                babs_vec(sparse_T, Xabs[i], RX[j]) * (D ** (i + 1))
                + babs_vec(sparse_T, RX[i], Xabs[j]) * (D ** (j + 1))
                + babs_vec(sparse_T, RX[i], RX[j])
            )

            # Tangent: B(G_i+dG_i, X_j+dX_j)-B(G_i,X_j).
            rgn += w * (
                babs_left(sparse_T, Gabs[i], RX[j]) * (D ** i)
                + babs_left(sparse_T, RG[i], Xabs[j]) * (D ** (j + 1))
                + babs_left(sparse_T, RG[i], RX[j])
            )
            # Tangent: B(X_i+dX_i, G_j+dG_j)-B(X_i,G_j).
            rgn += w * (
                babs_right(sparse_T, Xabs[i], RG[j]) * (D ** (i + 1))
                + babs_right(sparse_T, RX[i], Gabs[j]) * (D ** j)
                + babs_right(sparse_T, RX[i], RG[j])
            )

        RX.append(rxn)
        RG.append(rgn)

    # Exact induced-infinity defect bound. Each selected observation row r of order n
    # has entry radii jrad/D^(n+1). Summing state columns first is exact for the
    # nonnegative interval-radius matrix used in |A|*Jrad.
    row_radius_l1 = []
    row_denominators = []
    for r in selected:
        order = r // shells
        slot = r % shells
        row_radius_l1.append(sum(int(v) for v in jrad_blocks[order][slot]))
        row_denominators.append(D ** (order + 1))

    q_rows = []
    for i in range(f):
        qi = Fraction(0)
        for j in range(f):
            qi += abs(A[i][j]) * Fraction(row_radius_l1[j], row_denominators[j])
        q_rows.append(qi)
    q = max(q_rows)

    q_lt_one = q < 1
    q_le_half = q <= Fraction(1, 2)
    probe_consistent = Fraction(1, 100) < q < Fraction(1, 5)  # expected ~8.6e-2 at 1e-17
    rigorous_gain_orders = 11  # from prior 10^-28 lower bracket to certified 10^-17 box

    claims = [
        {
            "id": "V7-EPSC18-N1-EXACT-ENTRYWISE-INTERVAL",
            "name": "exact centered componentwise Jacobian interval enclosure on the N=1 10^-17 box",
            "tier": "finite_diagnostic",
            "status": "PASS" if q_le_half else "FAIL",
            "evidence": (
                f"integer common-denominator propagation D=10^17 through Taylor order {RMAX}; "
                f"exact preconditioned infinity defect q={float(q):.12e} <= 1/2={q_le_half}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-EXACT-ENTRYWISE-RADIUS",
            "name": "certified exact-entrywise local inverse box of radius 10^-17 for full N=1",
            "tier": "Dr",
            "status": "DERIVED" if q_le_half else "OPEN",
            "evidence": (
                "A=J0^-1 is exact rational; centered state/tangent interval propagation is exact integer arithmetic; "
                f"q<=1/2 on ||x-x_*||_inf<=10^-17; at least {rigorous_gain_orders} decimal orders above the prior 10^-28 lower bracket"
                if q_le_half else
                "the exact entrywise defect did not pass the q<=1/2 gate at radius 10^-17"
            ),
        },
        {
            "id": "V7-EPSC18-N1-ENTRYWISE-PROBE-CROSSCHECK",
            "name": "exact 10^-17 enclosure is consistent with the preceding floating scale probe",
            "tier": "finite_diagnostic",
            "status": "PASS" if probe_consistent else "FAIL",
            "evidence": f"exact q={float(q):.12e}; expected probe-guided interval (0.01,0.2) contains q={probe_consistent}",
        },
        {
            "id": "V7-EPSC18-N1-MEASUREMENT-READY-AFTER-EXACT-INTERVAL",
            "name": "measurement-ready branch/noise-stable inverse after exact entrywise enclosure",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "a rigorous state-space q<1 box is now available if the exact gate passes, but conversion of measured "
                "energy-jet uncertainty into guaranteed image/branch capture and a physically meaningful sensor tolerance remains separate"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "slice_dimension": f,
        "center_seed": CENTER_SEED,
        "target_radius": "1e-17",
        "common_denominator_base": D,
        "max_taylor_order": RMAX,
        "exact_q_float_display": float(q),
        "exact_q_numerator_digits": len(str(q.numerator)),
        "exact_q_denominator_digits": len(str(q.denominator)),
        "q_lt_one": q_lt_one,
        "q_le_half": q_le_half,
        "gain_vs_componentwise_lower_bracket_orders": rigorous_gain_orders,
        "arithmetic": "integer common-denominator radii + exact Fraction preconditioner",
        "finite_first_scope": "fixed N=1 49-dimensional translation slice; no continuum or floating interval promotion",
    }
    print("EPSC-18 N=1 exact centered entrywise interval certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
