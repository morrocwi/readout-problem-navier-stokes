#!/usr/bin/env python3
"""Exact finite validated-tube certificate for the N=1 Galerkin ODE.

Purpose
-------
Close one *checker-side* substep of NS-FUB-A1C without claiming a global
constructor.  For the existing deterministic small-integer N=1 center x0, this
script reconstructs the exact quadratic Galerkin vector field

    F(x) = (D x + T(x,x)) / C,      C = 600,

where D is the integer-scaled viscous diagonal and T is the already-audited
integer tensor for C times the bilinear Galerkin map.

For a rational box X = x0 + [-r,r]^d it computes exact rational bounds M_i with

    |F_i(x)| <= M_i   for every x in X,

and an exact infinity-norm Lipschitz bound L for F on X.  It then chooses a
positive rational step h satisfying the stronger fail-closed margins

    h * max_i M_i <= r/2,
    h * L           <= 1/2.

Consequently the Picard integral operator maps C([0,h], X) into itself and is a
contraction.  By the standard Banach fixed-point theorem, the finite ODE has a
unique trajectory on [0,h] that remains in X.  Its endpoint is enclosed by

    x_i(h) in [x0_i - h M_i, x0_i + h M_i].

The checker then converts that endpoint box to full Fourier-coefficient
rectangles and feeds it into the exact NS-FUB-A1V H^3 lower-bound verifier.

Scope
-----
This is a fixed-N=1 finite certificate calibration.  It does NOT construct a
tube for arbitrary initial data/cutoff, does NOT prove the finite tube reaches a
singularity witness, and does NOT prove Navier--Stokes global regularity.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Tuple

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as component
import check_volume7_eps18_n1_explicit_radius as coarse
import check_volume7_eps18_n1_small_witness as small
import check_ns_fub_a1_h3_certificate as h3

C = coarse.C
NU = coarse.NU
CENTER_SEED = 20260910
TUBE_RADIUS = Fraction(1, 1000)
H3_THRESHOLD = Fraction(1)

Interval = Tuple[Fraction, Fraction]


def interval_scale(a: int | Fraction, iv: Interval) -> Interval:
    lo, hi = iv
    a = Fraction(a)
    if a >= 0:
        return a * lo, a * hi
    return a * hi, a * lo


def interval_add(a: Interval, b: Interval) -> Interval:
    return a[0] + b[0], a[1] + b[1]


def linear_interval(coeffs: Iterable[int], ivs: Iterable[Interval]) -> Interval:
    out = (Fraction(0), Fraction(0))
    for a, iv in zip(coeffs, ivs):
        out = interval_add(out, interval_scale(a, iv))
    return out


def exact_vector_field_bounds(cube: base.CubeGalerkinModP, x0, radius: Fraction):
    """Return exact |F_i| bounds and an infinity-norm Lipschitz bound on x0±r."""
    T = component.scaled_bilinear_tensor(cube)
    sparse_T = component.sparse_absolute_tensor(T)
    d = cube.d

    R = [Fraction(abs(int(x0[j]))) + radius for j in range(d)]
    # C*L = -3 |k|^2 on each of the four coordinates of a representative mode.
    scaled_linear = [
        -3 * sum(int(v) * int(v) for v in k)
        for k in cube.reps
        for _ in range(4)
    ]
    assert len(scaled_linear) == d

    scaled_F_abs = []
    scaled_lipschitz_rows = []
    for i, entries in enumerate(sparse_T):
        f_abs = Fraction(abs(scaled_linear[i])) * R[i]
        lip = Fraction(abs(scaled_linear[i]))
        for j, k, coeff in entries:
            coeff = Fraction(coeff)
            f_abs += coeff * R[j] * R[k]
            # Row-sum Jacobian bound:
            # sum_l |dF_i/dx_l| <= |D_i| + sum_jk |T_ijk|(R_j+R_k), scaled by C.
            lip += coeff * (R[j] + R[k])
        scaled_F_abs.append(f_abs)
        scaled_lipschitz_rows.append(lip)

    M = [v / C for v in scaled_F_abs]
    L_rows = [v / C for v in scaled_lipschitz_rows]
    return T, M, max(L_rows), max(M), max(scaled_lipschitz_rows)


def endpoint_box(x0, h: Fraction, M: list[Fraction]) -> list[Interval]:
    return [
        (Fraction(int(x0[i])) - h * M[i], Fraction(int(x0[i])) + h * M[i])
        for i in range(len(M))
    ]


def full_fourier_mode_records(cube: base.CubeGalerkinModP, x_box: list[Interval]):
    """Convert basis-coordinate intervals to full ±k Fourier velocity rectangles."""
    records = []
    zero = (Fraction(0), Fraction(0))
    for mi, k in enumerate(cube.modes):
        ri, conj = cube.full_to_rep[mi]
        e1, e2, _, _ = cube.bases[ri]
        ar = x_box[4 * ri]
        ai = x_box[4 * ri + 1]
        br = x_box[4 * ri + 2]
        bi = x_box[4 * ri + 3]

        re_vec = []
        im_vec = []
        for axis in range(3):
            re_iv = linear_interval((int(e1[axis]), int(e2[axis])), (ar, br))
            im_iv = linear_interval((int(e1[axis]), int(e2[axis])), (ai, bi))
            if conj:
                im_iv = interval_scale(-1, im_iv)
            re_vec.append(re_iv)
            im_vec.append(im_iv)
        assert len(re_vec) == 3 and len(im_vec) == 3
        records.append((tuple(int(v) for v in k), tuple(re_vec), tuple(im_vec)))

    # N=1 nonzero Fourier cube has 26 modes; the zero mode is absent.
    assert len(records) == len(cube.modes)
    assert all(k != (0, 0, 0) for k, _, _ in records)
    return records


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared deterministic N=1 center did not reproduce")
    x0 = small.small_state(CENTER_SEED, cube.d)

    T, M, L, Mmax, scaled_Lmax = exact_vector_field_bounds(cube, x0, TUBE_RADIUS)
    if Mmax <= 0 or L <= 0:
        raise ArithmeticError("unexpected zero vector-field/Lipschitz bound")

    # Use half of each admissible limit, producing explicit strict slack.
    h_self = TUBE_RADIUS / (2 * Mmax)
    h_contract = Fraction(1, 2) / L
    h = min(h_self, h_contract)

    self_ratio = h * Mmax / TUBE_RADIUS
    contraction = h * L
    tube_pass = h > 0 and self_ratio <= Fraction(1, 2) and contraction <= Fraction(1, 2)
    if not tube_pass:
        raise AssertionError("validated tube gate failed")

    end_box = endpoint_box(x0, h, M)
    if any(lo > hi for lo, hi in end_box):
        raise AssertionError("invalid endpoint interval")
    # The endpoint enclosure must sit strictly inside the declared tube box.
    for i, (lo, hi) in enumerate(end_box):
        c = Fraction(int(x0[i]))
        if lo < c - TUBE_RADIUS or hi > c + TUBE_RADIUS:
            raise AssertionError("endpoint enclosure escaped tube")

    records = full_fourier_mode_records(cube, end_box)
    h3_status, h3_margin = h3.verdict(records, H3_THRESHOLD)
    h3_lower = h3.h3_squared_lower(records)
    if h3_status != "PASS":
        raise AssertionError(
            f"calibration endpoint did not retain the fixed H3>{H3_THRESHOLD} witness: "
            f"lower={h3_lower}"
        )

    sparse = component.sparse_absolute_tensor(T)
    tensor_nonzero = sum(len(row) for row in sparse)
    tensor_inf = max(sum(coeff for _, _, coeff in row) for row in sparse)
    if tensor_nonzero != 2096 or tensor_inf != 36000:
        raise AssertionError(
            f"exact N=1 tensor drift: nonzero={tensor_nonzero}, inf={tensor_inf}"
        )

    summary = {
        "cutoff": 1,
        "dimension": cube.d,
        "center_seed": CENTER_SEED,
        "C": C,
        "nu": frac_text(NU),
        "tube_radius": frac_text(TUBE_RADIUS),
        "exact_tensor_nonzero_coefficients": tensor_nonzero,
        "exact_tensor_infinity_row_sum": tensor_inf,
        "max_abs_vector_field_bound": frac_text(Mmax),
        "lipschitz_infinity_bound": frac_text(L),
        "scaled_lipschitz_row_max": frac_text(Fraction(scaled_Lmax)),
        "chosen_h": frac_text(h),
        "self_map_ratio_hM_over_r": frac_text(self_ratio),
        "contraction_q": frac_text(contraction),
        "tube_certificate": "PASS",
        "endpoint_H3_threshold": frac_text(H3_THRESHOLD),
        "endpoint_H3_squared_lower": frac_text(h3_lower),
        "endpoint_H3_margin": frac_text(h3_margin),
        "endpoint_H3_certificate": h3_status,
        "scope": (
            "fixed N=1 exact finite Galerkin calibration; checker-side trajectory enclosure only; "
            "no arbitrary-N/data constructor and no Clay conclusion"
        ),
    }
    print("NS-FUB-A1C N=1 validated finite ODE tube certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("NS-FUB-A1C N1 VALIDATED TUBE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
