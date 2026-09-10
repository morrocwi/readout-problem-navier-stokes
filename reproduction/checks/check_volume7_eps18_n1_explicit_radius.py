#!/usr/bin/env python3
"""Rigorous but deliberately conservative positive-radius certificate for EPSC-18 at N=1.

The preceding checkers certify an explicit full-rank 49-dimensional shell-energy
observation chart at a small-integer N=1 state.  This checker adds a quantitative,
finite-native neighborhood using only integer/rational inequalities.

It does NOT construct a sharp numerical inverse.  Instead it:
  1. uses the nonzero good-prime minor to know that the row-scaled real Jacobian J0
     is an invertible integer matrix;
  2. bounds ||J0^{-1}||_infinity by Cramer + Hadamard, using |det J0|>=1;
  3. derives a finite global Hessian majorant for the selected Taylor-energy map on
     ||x||_infinity<=4 from the quadratic Galerkin recurrence;
  4. chooses an explicit positive radius r with ||J0^{-1}(J(x)-J0)||<=1/2.

The resulting radius is expected to be extremely small.  Its value is a mathematical
existence/conditioning certificate, not a practical sensor tolerance.  The practical
large-box interval/Krawczyk problem remains open.

No completed infinite Fourier object is used anywhere in this checker.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_small_witness as small

P = base.P
CENTER_SEED = 20260910
RMAX = 23
C = 600  # clears nu=1/200 and every N=1 coordinate-extraction denominator used below
NU = Fraction(1, 200)


def ceil_fraction(x: Fraction) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def finite_operator_bounds(cube: base.CubeGalerkinModP) -> dict:
    # If every real coordinate coefficient is bounded by X, each real/imaginary
    # physical vector component is bounded by alpha*X after reconstruction.
    alpha = 0
    extraction = Fraction(0)
    for e1, e2, n1, n2 in cube.bases:
        e1 = [int(v) for v in e1]
        e2 = [int(v) for v in e2]
        alpha = max(
            alpha,
            max(abs(e1[j]) + abs(e2[j]) for j in range(3)),
        )
        extraction = max(
            extraction,
            Fraction(sum(abs(v) for v in e1), int(n1)),
            Fraction(sum(abs(v) for v in e2), int(n2)),
        )

    triad_max = max(len(t) for t in cube.triads)
    q_l1_max = max(sum(abs(v) for v in k) for k in cube.modes)

    # Complex product bound: each output real/imag component of (U_p.q) U_q
    # is <= 2 * (q_l1*alpha*X) * (alpha*Y).  Sum over ordered triads and
    # extract a coordinate by dotting with e1/e2.  Leray projection does not
    # worsen this extraction because e1,e2 are exactly perpendicular to k.
    B_bound = Fraction(2 * triad_max * q_l1_max * alpha * alpha, 1) * extraction
    Btilde_bound = ceil_fraction(C * B_bound)

    # C*L is integer diagonal because C*nu=3.  max |k|^2 at N=1 is 3.
    Lc_bound = int(C * NU * max(sum(v * v for v in k) for k in cube.reps))

    # Q_batch shell row sums bound the quadratic shell-energy bilinear map.
    q_rows = []
    for row in cube.weights:
        q_rows.append(sum(int(v) for v in row))
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
    }


def derivative_majorants(*, M: int, op: dict) -> dict:
    """Majorize scaled Taylor state, first derivative, second derivative and output jets.

    X_n = C^n n! x_n, where x(t)=sum x_n t^n.  With Btilde=C B,

      X_{n+1}=C L X_n + sum_i binom(n,i) Btilde(X_i,X_{n-i}).

    The scalar recurrences below are induced-infinity-norm majorants.
    """
    lc = op["Lc_bound"]
    bt = op["Btilde_bound"]
    qq = op["Q_bound"]

    a = [int(M)]       # ||X_n||
    b = [1]            # ||D X_n||
    c = [0]            # ||D^2 X_n||
    y1 = []             # ||D Y_n||
    y2 = []             # ||D^2 Y_n||

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
    digits = len(str(den))
    # 10^(digits-1) <= den < 10^digits, so 10^-digits < 1/den <= 10^-(digits-1).
    return {
        "denominator_digits": digits,
        "lower_power10_exponent": -digits,
        "upper_power10_exponent": -(digits - 1),
        "statement": f"10^(-{digits}) < r <= 10^(-{digits-1})",
    }


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    center_ok = bool(center["pass"] and center["max_abs_coordinate"] <= 3)

    # Row scaling by C^n n! is invertible modulo p for n<=23 because p does not
    # divide C or any factorial factor.  Hence the already nonzero selected minor
    # remains nonzero after integer row scaling.
    scaling_good_mod_p = math.gcd(P, C) == 1 and all(math.gcd(P, n) == 1 for n in range(1, RMAX + 1))
    integer_scaled_minor_nonzero = center_ok and center["minor_det_mod_p"] != 0 and scaling_good_mod_p

    op = finite_operator_bounds(cube)
    at_center = derivative_majorants(M=3, op=op)
    on_box = derivative_majorants(M=4, op=op)

    # For the selected 49x49 integer-scaled center Jacobian, every row 1-norm is
    # bounded by Jrow.  A 48x48 cofactor is bounded by Jrow^48 by Hadamard.
    # Since det is a nonzero integer, |det|>=1. Thus each inverse entry is at most
    # Jrow^48 and ||J0^-1||_infinity <= 49 Jrow^48.
    Jrow = max(at_center["output_first"])
    Hrow = max(on_box["output_second"])
    A_bound = 49 * pow(Jrow, 48)

    # On the radius-r infinity ball around a max-norm-3 center, r<=1 keeps the
    # entire box in ||x||<=4. Mean value gives ||J(x)-J0||<=Hrow*r.
    # Choose r=1/(2*A_bound*Hrow), so q<=1/2 exactly.
    radius_den = 2 * A_bound * Hrow
    radius_positive = radius_den > 0
    q_num, q_den = 1, 2
    inverse_factor_bound = 2 * A_bound
    bracket = decimal_bracket_for_reciprocal(radius_den)

    quantitative_ok = integer_scaled_minor_nonzero and radius_positive

    claims = [
        {
            "id": "V7-EPSC18-N1-FINITE-OPERATOR-MAJORANTS",
            "name": "finite N=1 quadratic Galerkin and shell-energy operator majorants",
            "tier": "finite_diagnostic",
            "status": "PASS" if op["Btilde_bound"] > 0 and op["Q_bound"] > 0 and op["Lc_bound"] == 9 else "FAIL",
            "evidence": (
                f"C={C}; CL bound={op['Lc_bound']}; C*B bound<={op['Btilde_bound']}; "
                f"Q bound={op['Q_bound']}; max center coordinate=3"
            ),
        },
        {
            "id": "V7-EPSC18-N1-EXPLICIT-POSITIVE-RADIUS",
            "name": "explicit positive quantitative local inverse radius for the full N=1 symmetry slice",
            "tier": "Dr",
            "status": "DERIVED" if quantitative_ok else "OPEN",
            "evidence": (
                f"integer-scaled minor nonzero={integer_scaled_minor_nonzero}; choose r=1/D with D having "
                f"{bracket['denominator_digits']} decimal digits; {bracket['statement']}; q<=1/2; "
                f"inverse Lipschitz factor <=2*A_bound (A_bound has {len(str(A_bound))} digits)"
                if quantitative_ok else "preconditions for the conservative finite-box estimate were not certified"
            ),
        },
        {
            "id": "V7-EPSC18-N1-PRACTICAL-INTERVAL-RADIUS",
            "name": "practically informative interval/Krawczyk radius for the N=1 energy-jet inverse",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the explicit positive radius uses Cramer/Hadamard plus global operator majorants and is intentionally extremely conservative; "
                "entrywise interval Jacobians and a numerically effective preconditioner are still needed"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "finite_state_dimension": 52,
        "slice_dimension": 49,
        "center_seed": CENTER_SEED,
        "center_max_abs_coordinate": center["max_abs_coordinate"],
        "center_minor_det_mod_p": center["minor_det_mod_p"],
        "row_scaling_C": C,
        "operator_bounds": op,
        "Jrow_majorant_digits": len(str(Jrow)),
        "Hrow_majorant_digits": len(str(Hrow)),
        "A_bound_digits": len(str(A_bound)),
        "radius_denominator_digits": bracket["denominator_digits"],
        "radius_power10_bracket": bracket["statement"],
        "q_bound": f"{q_num}/{q_den}",
        "finite_first_scope": "all bounds are on a fixed 49-dimensional finite symmetry slice; no N=infinity object appears",
    }
    print("EPSC-18 full N=1 conservative explicit-radius certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
