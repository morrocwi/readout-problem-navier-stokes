#!/usr/bin/env python3
"""Componentwise exact-preconditioned radius certificate for EPSC-18 at N=1.

The preceding exact-preconditioner checker constructs the actual characteristic-zero
49x49 Jacobian J0 and its exact rational inverse A=J0^{-1}.  Its first quantitative
bound still feeds A with deliberately coarse scalar derivative majorants.

This checker keeps the same exact A but removes another large source of slack.  It
constructs the full finite coefficient tensor of the integer-scaled N=1 quadratic
Galerkin map and propagates componentwise nonnegative Taylor/first-/second-derivative
majorants on a declared rational box around the small-integer center.

For state coordinate m, the propagated quantities bound

    a[n,m] >= |X_n,m|,
    b[n,m] >= sum_l |d X_n,m / d x_l|,
    c[n,m] >= sum_l,r |d^2 X_n,m / d x_l d x_r|.

The shell-energy output recurrence then gives one Hessian-row l1 majorant H_j for
each selected observation.  Therefore

    ||A (J(x)-J0)||_infinity
      <= r * max_i sum_j |A_ij| H_j.

Choosing r=1/(2S) with S equal to that exact weighted maximum gives q<=1/2.  The
box half-width is 1/1000 and the checker fails closed unless the derived radius lies
inside that box.

This is still a finite N=1 local certificate, not a practical sensor tolerance, not
a global inverse, not an arbitrary-N result, and not a continuum/Clay statement.
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
import check_volume7_eps18_n1_exact_preconditioner as exact
import check_volume7_eps18_n1_explicit_radius as coarse
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910
BOX_MARGIN = Fraction(1, 1000)
RMAX = 23


def digit_count(n: int) -> int:
    return len(str(abs(int(n)))) if n else 1


def scaled_bilinear_tensor(cube: base.CubeGalerkinModP) -> list[list[list[int]]]:
    """Return exact integer coefficients T[m][j][k] of C*B(e_j,e_k)."""
    d = cube.d
    pairs = d * d
    A = np.zeros((pairs, d), dtype=object)
    B = np.zeros((pairs, d), dtype=object)
    idx = 0
    for j in range(d):
        for k in range(d):
            A[idx, j] = 1
            B[idx, k] = 1
            idx += 1
    values = exact._scaled_bilinear(cube, A, B)
    T = [[[0 for _ in range(d)] for _ in range(d)] for _ in range(d)]
    for j in range(d):
        for k in range(d):
            row = values[j * d + k]
            for m in range(d):
                T[m][j][k] = int(row[m])
    return T


def sparse_absolute_tensor(T: list[list[list[int]]]) -> list[list[tuple[int, int, int]]]:
    out: list[list[tuple[int, int, int]]] = []
    for Tm in T:
        entries = []
        for j, row in enumerate(Tm):
            for k, value in enumerate(row):
                a = abs(int(value))
                if a:
                    entries.append((j, k, a))
        out.append(entries)
    return out


def babs(sparse_T, u, v):
    out = [Fraction(0) for _ in sparse_T]
    for m, entries in enumerate(sparse_T):
        acc = Fraction(0)
        for j, k, coeff in entries:
            acc += coeff * u[j] * v[k]
        out[m] = acc
    return out


def componentwise_majorants(cube, sparse_T, center_abs, margin: Fraction):
    """Propagate componentwise exact rational state/Jacobian/Hessian majorants."""
    d = cube.d
    a = [[Fraction(center_abs[m]) + margin for m in range(d)]]
    b = [[Fraction(1) for _ in range(d)]]
    c = [[Fraction(0) for _ in range(d)]]
    y2: list[list[Fraction]] = []

    abs_lc = [
        3 * sum(int(v) * int(v) for v in k)
        for k in cube.reps
        for _ in range(4)
    ]
    W = [[int(cube.weights[s, m]) for m in range(d)] for s in range(len(cube.shells))]

    for n in range(RMAX + 1):
        y2n = [Fraction(0) for _ in cube.shells]
        for i in range(n + 1):
            j = n - i
            choose = math.comb(n, i)
            for shell in range(len(cube.shells)):
                acc = Fraction(0)
                for m in range(d):
                    w = W[shell][m]
                    if w:
                        acc += w * (
                            c[i][m] * a[j][m]
                            + 2 * b[i][m] * b[j][m]
                            + a[i][m] * c[j][m]
                        )
                y2n[shell] += choose * acc
        y2.append(y2n)

        if n == RMAX:
            break

        an = [Fraction(abs_lc[m]) * a[n][m] for m in range(d)]
        bn = [Fraction(abs_lc[m]) * b[n][m] for m in range(d)]
        cn = [Fraction(abs_lc[m]) * c[n][m] for m in range(d)]

        for i in range(n + 1):
            j = n - i
            choose = math.comb(n, i)
            aa = babs(sparse_T, a[i], a[j])
            ba = babs(sparse_T, b[i], a[j])
            ab = babs(sparse_T, a[i], b[j])
            ca = babs(sparse_T, c[i], a[j])
            bb = babs(sparse_T, b[i], b[j])
            ac = babs(sparse_T, a[i], c[j])
            for m in range(d):
                an[m] += choose * aa[m]
                bn[m] += choose * (ba[m] + ab[m])
                cn[m] += choose * (ca[m] + 2 * bb[m] + ac[m])

        a.append(an)
        b.append(bn)
        c.append(cn)

    return y2


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared small-integer N=1 center did not reproduce")

    x0 = small.small_state(CENTER_SEED, cube.d)
    selected = [int(i) for i in center["selected_observation_rows"]]
    gauge = [int(i) for i in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    shell_count = len(cube.shells)

    blocks = exact.exact_scaled_shell_blocks(cube, x0)
    J0 = [
        [int(blocks[r // shell_count][r % shell_count, j]) for j in free]
        for r in selected
    ]
    A, det_j0 = exact.exact_inverse(J0)
    if det_j0 == 0:
        raise ArithmeticError("exact selected Jacobian unexpectedly singular")

    T = scaled_bilinear_tensor(cube)
    sparse_T = sparse_absolute_tensor(T)
    bilinear_inf = max(
        sum(coeff for _, _, coeff in entries)
        for entries in sparse_T
    )
    nonzero_coefficients = sum(len(entries) for entries in sparse_T)

    center_abs = [abs(int(v)) for v in x0]
    y2 = componentwise_majorants(cube, sparse_T, center_abs, BOX_MARGIN)
    H = [y2[r // shell_count][r % shell_count] for r in selected]

    slopes = [
        sum((abs(A[i][j]) * H[j] for j in range(49)), Fraction(0))
        for i in range(49)
    ]
    slope = max(slopes)
    radius = Fraction(1, 2) / slope
    radius_digit, radius_bracket = exact.reciprocal_power10_bracket(radius)
    box_contained = radius <= BOX_MARGIN

    # Baseline exact-preconditioner radius from the older scalar M=4 majorants.
    op = coarse.finite_operator_bounds(cube)
    scalar = coarse.derivative_majorants(M=4, op=op)
    scalar_H = [Fraction(scalar["output_second"][r // shell_count]) for r in selected]
    scalar_slope = max(
        sum((abs(A[i][j]) * scalar_H[j] for j in range(49)), Fraction(0))
        for i in range(49)
    )
    scalar_radius = Fraction(1, 2) / scalar_slope
    scalar_digit, scalar_bracket = exact.reciprocal_power10_bracket(scalar_radius)

    improved = radius > scalar_radius
    gain_lower_bracket = scalar_digit - radius_digit
    quantitative_ok = (
        bilinear_inf == 36000
        and nonzero_coefficients > 0
        and slope > 0
        and box_contained
        and improved
    )

    claims = [
        {
            "id": "V7-EPSC18-N1-EXACT-BILINEAR-TENSOR",
            "name": "exact finite coefficient tensor for the integer-scaled N=1 Galerkin bilinear map",
            "tier": "finite_diagnostic",
            "status": "PASS" if bilinear_inf == 36000 and nonzero_coefficients > 0 else "FAIL",
            "evidence": (
                f"52x52x52 finite tensor; nonzero coefficients={nonzero_coefficients}; "
                f"exact induced infinity bilinear row-sum bound={bilinear_inf}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-COMPONENTWISE-HESSIAN-ENCLOSURE",
            "name": "componentwise rational Hessian-row enclosure on the N=1 local box",
            "tier": "finite_diagnostic",
            "status": "PASS" if quantitative_ok else "FAIL",
            "evidence": (
                "nonnegative coefficientwise Taylor/first-/second-derivative recurrence; "
                f"box half-width=1/1000; derived radius is contained in box={box_contained}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-COMPONENTWISE-PRECONDITIONED-RADIUS",
            "name": "componentwise exact-preconditioned positive radius for the full N=1 local inverse",
            "tier": "Dr",
            "status": "DERIVED" if quantitative_ok else "OPEN",
            "evidence": (
                f"A=J0^-1 exact and componentwise H_j give {radius_bracket}; q<=1/2; "
                f"scalar exact-preconditioner baseline was {scalar_bracket}"
                if quantitative_ok else
                "componentwise enclosure prerequisites did not all certify"
            ),
        },
        {
            "id": "V7-EPSC18-N1-COMPONENTWISE-IMPROVEMENT",
            "name": "componentwise finite majorants materially tighten the exact-preconditioned N=1 radius",
            "tier": "finite_diagnostic",
            "status": "PASS" if quantitative_ok else "FAIL",
            "evidence": (
                f"power-of-ten lower-bracket index improves from {scalar_digit} to {radius_digit}; "
                f"gain={gain_lower_bracket} decimal orders"
            ),
        },
        {
            "id": "V7-EPSC18-N1-PRACTICAL-LOCAL-INTERVAL",
            "name": "practically informative branch-stable measurement radius after componentwise tightening",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the rigorous finite radius is now between 10^-28 and 10^-27, a major tightening but still "
                "far below a practical measurement tolerance; exact local interval/Jacobian structure and "
                "measurement-noise branch containment remain open"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "slice_dimension": 49,
        "center_seed": CENTER_SEED,
        "box_half_width": "1/1000",
        "scaled_bilinear_tensor_nonzero_coefficients": nonzero_coefficients,
        "scaled_bilinear_infinity_bound": bilinear_inf,
        "scalar_exact_preconditioner_radius_bracket": scalar_bracket,
        "componentwise_radius_bracket": radius_bracket,
        "componentwise_radius_numerator_digits": digit_count(radius.numerator),
        "componentwise_radius_denominator_digits": digit_count(radius.denominator),
        "decimal_order_gain_vs_scalar_exact_preconditioner": gain_lower_bracket,
        "box_containment_certified": box_contained,
        "q_bound_at_chosen_radius": "1/2",
        "finite_first_scope": (
            "fixed N=1 finite symmetry slice; exact integer coefficient tensor, exact rational inverse, "
            "and exact rational nonnegative majorants only"
        ),
    }

    print("EPSC-18 N=1 componentwise exact-preconditioned radius certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
