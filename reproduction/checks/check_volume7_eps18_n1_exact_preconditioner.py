#!/usr/bin/env python3
"""Exact characteristic-zero preconditioner certificate for EPSC-18 at N=1.

This checker replaces determinant-only inverse majorants by the actual inverse of the
selected 49x49 characteristic-zero Jacobian at the already-certified small-integer
center.  Everything remains finite:

  * the N=1 Fourier-Galerkin state has 52 real coordinates;
  * a fixed three-coordinate translation gauge leaves a 49-dimensional slice;
  * 49 selected shell-energy Taylor observations define the local chart;
  * the Taylor/Jacobian recurrence is reconstructed with integer arithmetic after the
    exact row scaling C^n n!, C=600;
  * the resulting 49x49 integer matrix is inverted by exact Fraction Gauss-Jordan;
  * the same certified row Hessian majorants as the preceding conservative checker
    bound Jacobian variation on ||x||_infinity <= 4.

If A=J0^{-1}, then at the center A J0=I exactly.  For a radius-r infinity ball,

    ||A(J(x)-J0)||_infinity
      <= r * max_i sum_j |A_ij| H_j.

Thus r=1/(2 S), S=max_i sum_j |A_ij| H_j, certifies q<=1/2.  This is a
strictly positive finite local-inverse radius.  It is still not advertised as a
practical sensor/noise tolerance, does not solve branch capture, does not extend to
arbitrary N, and has no continuum-regularity or Clay implication.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_explicit_radius as coarse
import check_volume7_eps18_n1_small_witness as small

P = base.P
C = coarse.C
CENTER_SEED = 20260910
RMAX = 23


def digit_count(n: int) -> int:
    return len(str(abs(int(n)))) if n else 1


def reciprocal_power10_bracket(q: Fraction) -> tuple[int, str]:
    """Return d with 10^-d < q <= 10^-(d-1), using exact rationals."""
    if q <= 0:
        raise ValueError("q must be positive")
    d = 1
    while Fraction(1, 10**d) >= q:
        d += 1
    return d, f"10^(-{d}) < r <= 10^(-{d-1})"


def _reconstruct_integer_batch(cube: base.CubeGalerkinModP, X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=object)
    if X.ndim == 1:
        X = X[None, :]
    out = np.empty((X.shape[0], len(cube.modes), 3, 2), dtype=object)
    out.fill(0)
    for mi, (ri, conj) in enumerate(cube.full_to_rep):
        ar = X[:, 4 * ri]
        ai = X[:, 4 * ri + 1]
        br = X[:, 4 * ri + 2]
        bi = X[:, 4 * ri + 3]
        if conj:
            ai = -ai
            bi = -bi
        e1, e2, _, _ = cube.bases[ri]
        for axis in range(3):
            out[:, mi, axis, 0] = ar * int(e1[axis]) + br * int(e2[axis])
            out[:, mi, axis, 1] = ai * int(e1[axis]) + bi * int(e2[axis])
    return out


def _scaled_bilinear(cube: base.CubeGalerkinModP, A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Return C times the exact rational Galerkin bilinear map as integers.

    Coordinate extraction against e1/e2 annihilates the Leray-parallel component,
    because both basis vectors are perpendicular to k.  The only remaining extraction
    denominators are the basis norms n1,n2, all divisors of C=600 for N=1.
    """
    A = np.asarray(A, dtype=object)
    B = np.asarray(B, dtype=object)
    a_was_1d = A.ndim == 1
    b_was_1d = B.ndim == 1
    if a_was_1d:
        A = A[None, :]
    if b_was_1d:
        B = B[None, :]
    if A.shape[0] != B.shape[0]:
        if A.shape[0] == 1:
            A = np.broadcast_to(A, (B.shape[0], cube.d))
        elif B.shape[0] == 1:
            B = np.broadcast_to(B, (A.shape[0], cube.d))
        else:
            raise ValueError("incompatible batch sizes")

    UA = _reconstruct_integer_batch(cube, A)
    UB = _reconstruct_integer_batch(cube, B)
    out = np.empty((A.shape[0], cube.d), dtype=object)
    out.fill(0)

    for ri, k in enumerate(cube.reps):
        ki = cube.mode_index[k]
        vre = np.empty((A.shape[0], 3), dtype=object)
        vim = np.empty((A.shape[0], 3), dtype=object)
        vre.fill(0)
        vim.fill(0)

        for pi, qi in cube.triads[ki]:
            qv = cube.modes[qi]
            sr = (
                UA[:, pi, 0, 0] * int(qv[0])
                + UA[:, pi, 1, 0] * int(qv[1])
                + UA[:, pi, 2, 0] * int(qv[2])
            )
            si = (
                UA[:, pi, 0, 1] * int(qv[0])
                + UA[:, pi, 1, 1] * int(qv[1])
                + UA[:, pi, 2, 1] * int(qv[2])
            )
            for axis in range(3):
                br = UB[:, qi, axis, 0]
                bi = UB[:, qi, axis, 1]
                vre[:, axis] += sr * br - si * bi
                vim[:, axis] += sr * bi + si * br

        qr = vim
        qi_im = -vre
        e1, e2, n1, n2 = cube.bases[ri]
        n1 = int(n1)
        n2 = int(n2)
        if C % n1 or C % n2:
            raise RuntimeError("declared row scale does not clear N=1 extraction denominators")
        c1 = C // n1
        c2 = C // n2

        dot1r = sum(qr[:, axis] * int(e1[axis]) for axis in range(3))
        dot1i = sum(qi_im[:, axis] * int(e1[axis]) for axis in range(3))
        dot2r = sum(qr[:, axis] * int(e2[axis]) for axis in range(3))
        dot2i = sum(qi_im[:, axis] * int(e2[axis]) for axis in range(3))
        out[:, 4 * ri] = c1 * dot1r
        out[:, 4 * ri + 1] = c1 * dot1i
        out[:, 4 * ri + 2] = c2 * dot2r
        out[:, 4 * ri + 3] = c2 * dot2i

    if a_was_1d and b_was_1d:
        return out[0]
    return out


def _q_batch_integer(cube: base.CubeGalerkinModP, A: np.ndarray, b: np.ndarray) -> np.ndarray:
    A = np.asarray(A, dtype=object)
    if A.ndim == 1:
        A = A[None, :]
    b = np.asarray(b, dtype=object)
    W = np.asarray(cube.weights, dtype=object)
    return (A * b[None, :]) @ W.T


def exact_scaled_shell_blocks(cube: base.CubeGalerkinModP, x0_signed: np.ndarray) -> list[np.ndarray]:
    """Return integer blocks C^n n! D(I_n)(x0), n=0..RMAX."""
    x0 = np.asarray(x0_signed, dtype=object)
    X = [x0]
    DX = [np.eye(cube.d, dtype=object)]
    blocks: list[np.ndarray] = []

    # C*L is integer because C=600 and nu=1/200.
    lc_diag = np.repeat(
        np.asarray(
            [-3 * sum(int(v) * int(v) for v in k) for k in cube.reps],
            dtype=object,
        ),
        4,
    )

    for n in range(RMAX + 1):
        dy = np.empty((cube.d, len(cube.shells)), dtype=object)
        dy.fill(0)
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            dy += w * (
                _q_batch_integer(cube, DX[i], X[j])
                + _q_batch_integer(cube, DX[j], X[i])
            )
        blocks.append(dy.T.copy())

        if n == RMAX:
            break

        rhs = X[n] * lc_diag
        drhs = DX[n] * lc_diag[None, :]
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            rhs += w * _scaled_bilinear(cube, X[i], X[j])
            drhs += w * (
                _scaled_bilinear(cube, DX[i], X[j])
                + _scaled_bilinear(cube, X[i], DX[j])
            )
        X.append(rhs)
        DX.append(drhs)

    return blocks


def exact_inverse(A: list[list[int]]) -> tuple[list[list[Fraction]], int]:
    """Exact Fraction Gauss-Jordan inverse plus determinant."""
    n = len(A)
    if n == 0 or any(len(row) != n for row in A):
        raise ValueError("square nonempty matrix required")
    M = [
        [Fraction(int(A[i][j])) for j in range(n)]
        + [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]
    det = Fraction(1)
    sign = 1

    for col in range(n):
        pivot = next((r for r in range(col, n) if M[r][col]), None)
        if pivot is None:
            raise ArithmeticError("selected exact Jacobian is singular")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            sign = -sign
        pv = M[col][col]
        det *= pv
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r == col:
                continue
            coeff = M[r][col]
            if coeff:
                M[r] = [M[r][j] - coeff * M[col][j] for j in range(2 * n)]

    det *= sign
    if det.denominator != 1:
        raise ArithmeticError("integer matrix determinant did not reduce to an integer")
    return [row[n:] for row in M], int(det.numerator)


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"] or center["max_abs_coordinate"] > 3:
        raise RuntimeError("the declared small-integer full-rank center was not reproduced")

    x0_signed = small.small_state(CENTER_SEED, cube.d)
    selected = [int(i) for i in center["selected_observation_rows"]]
    gauge = [int(i) for i in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    shell_count = len(cube.shells)

    exact_blocks = exact_scaled_shell_blocks(cube, x0_signed)
    modular_blocks = small.formal_shell_blocks_from_state(cube, x0_signed)

    # Cross-check every selected full Jacobian row against the already-reproduced
    # modular construction after the exact C^n n! row scaling.
    row_crosscheck = True
    row_scale_product_mod_p = 1
    for global_row in selected:
        order = global_row // shell_count
        shell_slot = global_row % shell_count
        scale = (pow(C, order, P) * math.factorial(order)) % P
        row_scale_product_mod_p = row_scale_product_mod_p * scale % P
        exact_row = exact_blocks[order][shell_slot]
        modular_row = modular_blocks[order][shell_slot]
        for j in range(cube.d):
            if int(exact_row[j]) % P != (int(modular_row[j]) * scale) % P:
                row_crosscheck = False
                break
        if not row_crosscheck:
            break

    J0 = [
        [int(exact_blocks[r // shell_count][r % shell_count, j]) for j in free]
        for r in selected
    ]
    Jinv, det_j0 = exact_inverse(J0)

    expected_det_mod_p = int(center["minor_det_mod_p"]) * row_scale_product_mod_p % P
    determinant_crosscheck = det_j0 % P == expected_det_mod_p

    a_row_sums = [sum((abs(x) for x in row), Fraction(0)) for row in Jinv]
    a_inf = max(a_row_sums)
    a_inf_bracket_ok = Fraction(128, 100) < a_inf < Fraction(129, 100)

    op = coarse.finite_operator_bounds(cube)
    on_box = coarse.derivative_majorants(M=4, op=op)
    orders = [int(r // shell_count) for r in selected]
    H = [int(on_box["output_second"][n]) for n in orders]

    weighted_row_slopes = [
        sum((abs(Jinv[i][j]) * H[j] for j in range(49)), Fraction(0))
        for i in range(49)
    ]
    q_slope = max(weighted_row_slopes)
    radius = Fraction(1, 2) / q_slope
    radius_digit, radius_bracket = reciprocal_power10_bracket(radius)

    # Previous rigorous row-aware radius was bracketed by 10^-3878 and 10^-3877.
    decimal_order_gain_lower = 3877 - radius_digit
    quantitative_ok = (
        row_crosscheck
        and determinant_crosscheck
        and det_j0 != 0
        and q_slope > 0
        and a_inf_bracket_ok
        and radius > 0
    )

    claims = [
        {
            "id": "V7-EPSC18-N1-EXACT-CHAR0-JACOBIAN",
            "name": "exact characteristic-zero integer-scaled 49x49 N=1 observability Jacobian",
            "tier": "finite_diagnostic",
            "status": "PASS" if row_crosscheck and determinant_crosscheck and det_j0 != 0 else "FAIL",
            "evidence": (
                f"all 49 selected rows agree with the good-prime construction after C^n n! scaling; "
                f"|det J0| has {digit_count(det_j0)} decimal digits; det mod {P}={det_j0 % P}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-EXACT-INVERSE-NORM",
            "name": "exact rational inverse norm for the selected full N=1 symmetry-slice Jacobian",
            "tier": "finite_diagnostic",
            "status": "PASS" if quantitative_ok else "FAIL",
            "evidence": (
                f"exact Fraction Gauss-Jordan gives 1.28 < ||J0^-1||_inf < 1.29; "
                f"max-row rational numerator digits={digit_count(a_inf.numerator)}, "
                f"denominator digits={digit_count(a_inf.denominator)}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-EXACT-PRECONDITIONED-RADIUS",
            "name": "strictly positive exact-preconditioned quantitative radius for full N=1",
            "tier": "Dr",
            "status": "DERIVED" if quantitative_ok else "OPEN",
            "evidence": (
                f"A=J0^-1 exactly; choose r=1/(2*max_i sum_j |A_ij|H_j); "
                f"{radius_bracket}; q<=1/2; at least {decimal_order_gain_lower} decimal orders "
                "larger than the previous 10^-3878 lower-bracket scale"
                if quantitative_ok else
                "exact preconditioner or finite Hessian prerequisites did not certify"
            ),
        },
        {
            "id": "V7-EPSC18-N1-MEASUREMENT-SCALE-RADIUS",
            "name": "measurement-scale robust radius for the full N=1 energy-jet inverse",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the exact center inverse removes essentially all determinant-bound slack, but the rigorous "
                "global row-Hessian enclosure still gives a radius between 10^-59 and 10^-58; "
                "entrywise/local interval Jacobian bounds plus branch/noise containment remain required"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "state_dimension": cube.d,
        "slice_dimension": len(free),
        "center_seed": CENTER_SEED,
        "gauge_coordinates": gauge,
        "selected_rows": len(selected),
        "row_scaling": "C^n n!, C=600",
        "characteristic_zero_row_crosscheck": row_crosscheck,
        "determinant_mod_p_crosscheck": determinant_crosscheck,
        "determinant_decimal_digits": digit_count(det_j0),
        "determinant_mod_p": det_j0 % P,
        "inverse_inf_exact_numerator_digits": digit_count(a_inf.numerator),
        "inverse_inf_exact_denominator_digits": digit_count(a_inf.denominator),
        "inverse_inf_exact_bracket": "1.28 < ||J0^-1||_inf < 1.29",
        "radius_exact_numerator_digits": digit_count(radius.numerator),
        "radius_exact_denominator_digits": digit_count(radius.denominator),
        "radius_power10_bracket": radius_bracket,
        "q_bound_at_chosen_radius": "1/2",
        "minimum_decimal_order_gain_vs_rowwise_lower_bracket": decimal_order_gain_lower,
        "finite_first_scope": (
            "fixed N=1 49-dimensional symmetry slice, exact integers/Fractions and certified finite derivative majorants only"
        ),
    }

    print("EPSC-18 N=1 exact characteristic-zero preconditioner certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
