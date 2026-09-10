#!/usr/bin/env python3
"""Row-aware rigorous positive-radius certificate for EPSC-18 at N=1.

The previous conservative checker proves a strictly positive local inverse radius on
an explicit 49-dimensional symmetry slice by combining:

  * a nonzero integer-scaled 49x49 Jacobian determinant;
  * a uniform row majorant Jmax;
  * a uniform Hessian majorant Hmax;
  * Cramer + Hadamard.

That proof is rigorous but wastes the large variation between Taylor orders by
replacing every row with the largest row.  This checker keeps the same finite proof
architecture while retaining one certified row majorant per selected observation.

Let R_j bound the l1 norm (hence also the l2 norm) of selected Jacobian row j at the
small-integer center, and let H_j bound the corresponding Jacobian-row variation per
unit infinity-radius on the enclosing ||x||_infinity<=4 box.  Since the row-scaled
center Jacobian J0 is an invertible integer matrix, |det J0|>=1.  Hadamard applied to
each cofactor gives

    |(J0^{-1})_{i j}| <= C_j := product_{k != j} R_k.

Therefore for every x in the radius-r infinity ball around the center,

    ||J0^{-1}(J(x)-J0)||_infinity
        <= r * sum_j C_j H_j.

Choosing

    r = 1 / (2 * sum_j C_j H_j)

certifies q<=1/2 and hence a quantitative local inverse on the same branch/slice.
This remains deliberately conservative: it is not an entrywise interval/Krawczyk
preconditioner and is not advertised as a practical sensor tolerance.

All arithmetic in the reported radius construction is finite integer arithmetic.
No completed infinite Fourier object appears.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Python 3.11 protects accidental conversion of enormous integers to decimal strings.
# The integers here are intentional finite certificate objects, so raise that reporting
# guard explicitly without changing any mathematical arithmetic.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_explicit_radius as coarse
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910


def digit_count(n: int) -> int:
    return len(str(abs(int(n)))) if n else 1


def reciprocal_power10_bracket(den: int) -> str:
    d = digit_count(den)
    return f"10^(-{d}) < r <= 10^(-{d-1})"


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    center_ok = bool(center["pass"] and center["max_abs_coordinate"] <= 3)
    selected = list(center["selected_observation_rows"])
    shell_count = len(cube.shells)

    op = coarse.finite_operator_bounds(cube)
    at_center = coarse.derivative_majorants(M=3, op=op)
    on_box = coarse.derivative_majorants(M=4, op=op)

    # Each global observation row is (Taylor order, shell slot).  The scalar
    # majorants are valid for every shell at that order, so they remain valid after
    # deleting the three gauge-fixed state columns.
    orders = [int(row // shell_count) for row in selected]
    row_bounds = [int(at_center["output_first"][n]) for n in orders]
    hessian_row_bounds = [int(on_box["output_second"][n]) for n in orders]

    row_bounds_positive = len(row_bounds) == 49 and all(r > 0 for r in row_bounds)
    hessian_bounds_nonnegative = len(hessian_row_bounds) == 49 and all(h >= 0 for h in hessian_row_bounds)

    # Product form is exact integer arithmetic.  C_j is a Hadamard upper bound for
    # every cofactor that deletes observation row j.  Because the integer-scaled
    # determinant is nonzero, |det| >= 1 and the same C_j bounds the corresponding
    # column of J0^{-1} entrywise.
    row_product = math.prod(row_bounds) if row_bounds_positive else 0
    cofactor_bounds = [row_product // r for r in row_bounds] if row_product else []
    inverse_inf_bound = sum(cofactor_bounds)

    # Row-aware preconditioned Jacobian variation:
    # max_i sum_l |sum_j A_ij DeltaJ_jl|
    # <= sum_j C_j ||DeltaJ_j,*||_1
    # <= r sum_j C_j H_j.
    q_slope = sum(c * h for c, h in zip(cofactor_bounds, hessian_row_bounds))
    radius_den = 2 * q_slope if q_slope > 0 else 0

    # Recompute the earlier max-row denominator for an apples-to-apples comparison.
    jmax = max(at_center["output_first"])
    hmax = max(on_box["output_second"])
    old_inverse_bound = 49 * pow(jmax, 48)
    old_radius_den = 2 * old_inverse_bound * hmax

    improved = radius_den > 0 and radius_den < old_radius_den
    improvement_digits = digit_count(old_radius_den) - digit_count(radius_den) if improved else 0
    q_half_certified = center_ok and row_bounds_positive and hessian_bounds_nonnegative and radius_den > 0

    claims = [
        {
            "id": "V7-EPSC18-N1-ROWWISE-COFACTOR-BOUND",
            "name": "row-aware Hadamard cofactor bound for the full N=1 symmetry-slice inverse",
            "tier": "Dr",
            "status": "DERIVED" if q_half_certified else "OPEN",
            "evidence": (
                f"49 selected rows; product-row cofactor construction exact=True; "
                f"inverse infinity bound has {digit_count(inverse_inf_bound)} decimal digits"
                if q_half_certified else
                "small-center or finite row-majorant preconditions were not certified"
            ),
        },
        {
            "id": "V7-EPSC18-N1-ROWWISE-POSITIVE-RADIUS",
            "name": "strictly positive row-aware quantitative radius for the full N=1 local inverse",
            "tier": "Dr",
            "status": "DERIVED" if q_half_certified else "OPEN",
            "evidence": (
                f"choose r=1/D with D having {digit_count(radius_den)} decimal digits; "
                f"{reciprocal_power10_bracket(radius_den)}; q<=1/2"
                if q_half_certified else
                "row-aware q slope was not certified positive"
            ),
        },
        {
            "id": "V7-EPSC18-N1-ROWWISE-IMPROVEMENT",
            "name": "row-aware finite proof materially improves the previous uniform-row radius bound",
            "tier": "finite_diagnostic",
            "status": "PASS" if improved else "FAIL",
            "evidence": (
                f"old denominator digits={digit_count(old_radius_den)}; "
                f"row-aware denominator digits={digit_count(radius_den)}; "
                f"gain={improvement_digits} decimal orders in the power-of-ten bracket"
            ),
        },
        {
            "id": "V7-EPSC18-N1-PRACTICAL-PRECONDITIONED-RADIUS",
            "name": "practically informative entrywise preconditioned interval radius for N=1",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the row-aware theorem removes more than four thousand orders of avoidable uniform-row slack, "
                "but the remaining radius is still far too small for a practical measurement tolerance; "
                "an actual entrywise Jacobian enclosure with an effective rational preconditioner remains required"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "state_dimension": 52,
        "slice_dimension": 49,
        "center_seed": CENTER_SEED,
        "selected_rows": 49,
        "selected_taylor_orders": orders,
        "row_product_digits": digit_count(row_product),
        "inverse_inf_bound_digits": digit_count(inverse_inf_bound),
        "q_slope_digits": digit_count(q_slope),
        "old_radius_denominator_digits": digit_count(old_radius_den),
        "rowwise_radius_denominator_digits": digit_count(radius_den),
        "decimal_order_gain": improvement_digits,
        "rowwise_radius_power10_bracket": reciprocal_power10_bracket(radius_den) if radius_den else None,
        "q_bound_at_chosen_radius": "1/2",
        "finite_first_scope": (
            "fixed 49-dimensional symmetry slice; integer row/cofactor/Hessian majorants only; "
            "no completed N=infinity state"
        ),
    }

    print("EPSC-18 N=1 row-aware local-inverse radius certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
