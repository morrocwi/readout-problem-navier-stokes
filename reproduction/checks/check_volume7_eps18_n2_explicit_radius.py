#!/usr/bin/env python3
"""Conservative positive-radius EPSC-18 certificate for the explicit N=2 shell chart.

This checker upgrades the fixed-N=2 structural local-inverse result into a fully
quantitative, finite-native statement.  It deliberately uses coarse integer/rational
majorants rather than attempting a 245x245 exact rational inverse.

The already-certified small-integer center has coordinates bounded by 3 and an
explicit 245-dimensional translation slice.  Its selected 245 shell-energy Taylor
rows through R=30 have a nonzero good-prime minor over F_251.  We choose a row scale
C that clears every N=2 basis-extraction denominator and nu=1/200.  After the
C^n n! Taylor-row scaling the characteristic-zero chart Jacobian J0 is therefore an
integer matrix.  Its good-prime determinant is nonzero, so det(J0) is a nonzero
integer and |det J0|>=1.

A Cramer/Hadamard inverse bound and a finite Hessian majorant on ||x||_inf<=4 then
give a positive explicit radius r for which

    q_2 = ||J0^{-1}(J(x)-J0)||_inf <= 1/2 < 1.

The radius is intentionally extremely small.  Its purpose is to certify that the
observability -> square chart -> quantitative inverse bridge has crossed N=2 without
assuming a completed infinite object.  This is not yet a practical sensor tolerance,
noise-stable branch-capture theorem, arbitrary-N result, DNS claim, continuum
regularity theorem, or Clay solution.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction

import check_k2_energy_observability as k2
import check_volume7_eps18_n2_small_witness as small

# This checker intentionally constructs finite integers with tens of thousands of
# decimal digits.  Python 3.11's defensive int<->str conversion cap is appropriate
# for untrusted text, but here every integer is produced deterministically inside the
# finite recurrence.  Disable that display-only cap so exact digit counts/evidence can
# be emitted without changing the mathematical computation.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

P = k2.P
RMAX = 30
NU_DEN = 200
SLICE_DIM = k2.d - 3
CENTER_SEED = 20260910


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def row_scale() -> int:
    c = NU_DEN
    for _, _, n1, n2 in k2.bases:
        c = lcm(c, int(n1))
        c = lcm(c, int(n2))
    return c


def ceil_fraction(x: Fraction) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def finite_operator_bounds(C: int) -> dict:
    alpha = 0
    extraction = Fraction(0)
    for e1, e2, n1, n2 in k2.bases:
        e1 = [int(v) for v in e1]
        e2 = [int(v) for v in e2]
        alpha = max(alpha, max(abs(e1[j]) + abs(e2[j]) for j in range(3)))
        extraction = max(
            extraction,
            Fraction(sum(abs(v) for v in e1), int(n1)),
            Fraction(sum(abs(v) for v in e2), int(n2)),
        )

    triad_max = max(int(k2.starts[i + 1] - k2.starts[i]) for i in range(len(k2.reps)))
    q_l1_max = max(sum(abs(int(v)) for v in mode) for mode in k2.modes)

    # Reconstructing one velocity component from two transverse amplitudes costs
    # at most alpha.  The convective bilinear form has one q dot-product and one
    # velocity component, and the coordinate extraction costs at most extraction.
    # The factor 2 safely covers real/imaginary product accumulation.
    B_bound = Fraction(2 * triad_max * q_l1_max * alpha * alpha, 1) * extraction
    Btilde_bound = ceil_fraction(C * B_bound)

    max_k2 = max(sum(int(v) * int(v) for v in mode) for mode in k2.reps)
    if C % NU_DEN:
        raise RuntimeError("row scale does not clear viscosity denominator")
    Lc_bound = (C // NU_DEN) * max_k2

    q_rows = [sum(int(v) for v in row) for row in k2.weights]
    Q_bound = max(q_rows)

    return {
        "alpha": int(alpha),
        "extraction_num": extraction.numerator,
        "extraction_den": extraction.denominator,
        "triad_max": int(triad_max),
        "q_l1_max": int(q_l1_max),
        "B_bound_num": B_bound.numerator,
        "B_bound_den": B_bound.denominator,
        "Btilde_bound": int(Btilde_bound),
        "Lc_bound": int(Lc_bound),
        "Q_bound": int(Q_bound),
        "max_k_squared": int(max_k2),
    }


def derivative_majorants(*, M: int, op: dict) -> dict:
    """Majorize scaled Taylor state, first/second derivatives, and shell outputs.

    With X_n=C^n n! x_n and Btilde=C B,

      X_{n+1}=C L X_n + sum_i binom(n,i) Btilde(X_i,X_{n-i}).

    b_n majorizes one first variation for unit infinity-norm input and c_n a
    mixed second variation.  Consequently output_second[n] bounds the Hessian
    bilinear operator norm of each shell-energy Taylor row at order n.
    """
    lc = op["Lc_bound"]
    bt = op["Btilde_bound"]
    qq = op["Q_bound"]

    a = [int(M)]
    b = [1]
    c = [0]
    y1 = []
    y2 = []

    for n in range(RMAX + 1):
        d1 = 0
        d2 = 0
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            d1 += w * (b[i] * a[j] + a[i] * b[j])
            d2 += w * (c[i] * a[j] + 2 * b[i] * b[j] + a[i] * c[j])
        y1.append(qq * d1)
        y2.append(qq * d2)

        if n == RMAX:
            break

        an = lc * a[n]
        bn = lc * b[n]
        cn = lc * c[n]
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            an += bt * w * a[i] * a[j]
            bn += bt * w * (b[i] * a[j] + a[i] * b[j])
            cn += bt * w * (c[i] * a[j] + 2 * b[i] * b[j] + a[i] * c[j])
        a.append(an)
        b.append(bn)
        c.append(cn)

    return {
        "state": a,
        "first": b,
        "second": c,
        "output_first": y1,
        "output_second": y2,
    }


def decimal_bracket_for_reciprocal(den: int) -> dict:
    if den <= 0:
        raise ValueError("positive denominator required")
    digits = len(str(den))
    return {
        "denominator_digits": digits,
        "statement": f"10^(-{digits}) < r <= 10^(-{digits-1})",
    }


def main() -> int:
    assert k2.N == 2 and k2.d == 248 and SLICE_DIM == 245 and P == 251 and P > RMAX

    winner = small.evaluate_candidate(CENTER_SEED)
    center_ok = bool(winner["pass"] and winner["max_abs_coordinate"] <= 3)
    selected = [int(v) for v in winner.get("selected_observation_rows", [])]
    selected_orders = [r // len(k2.shells) for r in selected]

    C = row_scale()
    clears_basis = all(C % int(n1) == 0 and C % int(n2) == 0 for _, _, n1, n2 in k2.bases)
    row_scaling_good_mod_p = (
        math.gcd(P, C) == 1
        and all(math.gcd(P, n) == 1 for n in range(1, RMAX + 1))
    )
    integer_scaled_minor_nonzero = bool(
        center_ok
        and len(selected) == SLICE_DIM
        and winner["selected_minor_det_mod_p"] != 0
        and clears_basis
        and C % NU_DEN == 0
        and row_scaling_good_mod_p
    )

    op = finite_operator_bounds(C)
    at_center = derivative_majorants(M=3, op=op)
    on_box = derivative_majorants(M=4, op=op)

    # Only selected orders are needed; using their maximum row bounds is still
    # conservative.  Jrow bounds every selected Jacobian-row l1 norm at x_*.
    Jrow = max(at_center["output_first"][n] for n in selected_orders)
    Hrow = max(on_box["output_second"][n] for n in selected_orders)

    # Every (244 x 244) cofactor is at most Jrow^244 by Hadamard, because row
    # l2 <= row l1 <= Jrow.  Since |det J0|>=1, each inverse row has l1 norm
    # at most 245*Jrow^244.
    A_bound = SLICE_DIM * pow(Jrow, SLICE_DIM - 1)
    radius_den = 2 * A_bound * Hrow
    bracket = decimal_bracket_for_reciprocal(radius_den)

    radius_lt_one = radius_den > 1
    quantitative_ok = bool(
        integer_scaled_minor_nonzero
        and Jrow > 0
        and Hrow > 0
        and A_bound > 0
        and radius_lt_one
    )

    claims = [
        {
            "id": "V7-EPSC18-N2-FINITE-OPERATOR-MAJORANTS",
            "name": "finite N=2 scaled Galerkin and shell-output derivative majorants",
            "tier": "finite_diagnostic",
            "status": "PASS" if (C == 14400 and clears_basis and op["Lc_bound"] == 864 and op["Btilde_bound"] > 0 and op["Q_bound"] > 0) else "FAIL",
            "evidence": (
                f"C={C}; CL bound={op['Lc_bound']}; C*B bound<={op['Btilde_bound']}; "
                f"Q bound={op['Q_bound']}; triad_max={op['triad_max']}; center max|x_j|={winner['max_abs_coordinate']}"
            ),
        },
        {
            "id": "V7-EPSC18-N2-INTEGER-SCALED-NONZERO-MINOR",
            "name": "selected N=2 small-center shell chart has a nonzero integer-scaled characteristic-zero determinant",
            "tier": "Dr",
            "status": "DERIVED" if integer_scaled_minor_nonzero else "OPEN",
            "evidence": (
                f"good-prime selected minor det mod {P}={winner['selected_minor_det_mod_p']}; "
                f"C={C} clears viscosity/basis denominators and C^n n! is invertible mod {P} through n={RMAX}; "
                "therefore the corresponding row-scaled characteristic-zero determinant is a nonzero integer"
                if integer_scaled_minor_nonzero else
                "integer-scaled determinant prerequisites were not all certified"
            ),
        },
        {
            "id": "V7-EPSC18-N2-EXPLICIT-POSITIVE-RADIUS",
            "name": "explicit positive quantitative local inverse radius for the fixed N=2 shell chart",
            "tier": "Dr",
            "status": "DERIVED" if quantitative_ok else "OPEN",
            "evidence": (
                f"A_bound=245*Jrow^244 with {len(str(A_bound))} decimal digits; Hrow has {len(str(Hrow))} digits; "
                f"choose r=1/(2*A_bound*Hrow), whose denominator has {bracket['denominator_digits']} digits; "
                f"{bracket['statement']}; then q_2<=1/2 on ||x-x_*||_inf<=r"
                if quantitative_ok else
                "preconditions for the conservative finite-box inverse estimate were not certified"
            ),
        },
        {
            "id": "V7-EPSC18-N2-PRACTICAL-INTERVAL-RADIUS",
            "name": "practically informative entrywise/preconditioned N=2 inverse radius and measurement tolerance",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the Cramer/Hadamard certificate proves a strictly positive branch-wide radius but is intentionally very loose; "
                "an exact or validated numerical preconditioner plus centered entrywise Jacobian propagation is still needed for a useful rho_2"
            ),
        },
    ]

    summary = {
        "cutoff": 2,
        "finite_state_dimension": k2.d,
        "slice_dimension": SLICE_DIM,
        "shell_count": len(k2.shells),
        "center_seed": CENTER_SEED,
        "center_max_abs_coordinate": winner["max_abs_coordinate"],
        "center_minor_det_mod_p": winner["selected_minor_det_mod_p"],
        "selected_row_count": len(selected),
        "max_selected_order": max(selected_orders) if selected_orders else None,
        "row_scaling_C": C,
        "operator_bounds": op,
        "Jrow_majorant_digits": len(str(Jrow)),
        "Hrow_majorant_digits": len(str(Hrow)),
        "A_bound_digits": len(str(A_bound)),
        "radius_denominator_digits": bracket["denominator_digits"],
        "radius_power10_bracket": bracket["statement"],
        "q_bound": "1/2",
        "finite_first_scope": "fixed 245-dimensional N=2 translation slice only; no completed N=infinity object",
    }

    print("EPSC-18 N=2 conservative explicit-radius certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")), flush=True)
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
