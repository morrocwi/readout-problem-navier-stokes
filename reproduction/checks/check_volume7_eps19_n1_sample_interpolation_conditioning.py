#!/usr/bin/env python3
"""Exact finite conditioning diagnostic for the N=1 EPSC-19 sample interface.

The fixed-N=1 shell-energy inverse currently uses the row-scaled Taylor chart

    z_n = (600^n n!) a_n,

for the two primary shell channels through n=23. The finite-time sample-chart result
shows that 24 samples per primary shell at nodes 0,...,23 times a common spacing h
are structurally locally invertible for sufficiently small nonzero h.

This checker asks a different question: what happens if those finite samples are first
interpolated back to the *scaled Taylor chart* and only then passed to the existing
inverse?

For one shell channel,

    y = V D_h a,
    z = S a,

where V[j,n]=j^n, D_h=diag(h^n), and S=diag(600^n n!). Therefore

    z = S D_h^{-1} V^{-1} y,

and the exact induced infinity-norm noise amplification is

    kappa_inf(h)
      = max_n 600^n n! |h|^{-n} sum_j |(V^{-1})[n,j]|.

The Vandermonde inverse is constructed exactly over Q by Lagrange interpolation.
No floating inversion is used. This is a finite algebra certificate about the
sample->scaled-Taylor reconstruction route only. It does not certify the conditioning
of the direct 49-sample map S_h(x), an analytic-flow remainder, branch capture,
physical sensor noise, arbitrary N, continuum regularity, or the Clay problem.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction

RMAX = 23
C = 600
NODES = tuple(range(RMAX + 1))
SPACINGS = (
    Fraction(1, 1),
    Fraction(1, 10),
    Fraction(1, 100),
    Fraction(1, 600),
)
EXPECTED_FLOOR_LOG10 = {
    Fraction(1, 1): 70,
    Fraction(1, 10): 93,
    Fraction(1, 100): 116,
    Fraction(1, 600): 134,
}


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def vandermonde_inverse_rows(nodes: tuple[int, ...]) -> list[list[Fraction]]:
    xs = [Fraction(x) for x in nodes]
    if len(set(xs)) != len(xs):
        raise ValueError("sample nodes must be distinct")
    rows = [[Fraction(0) for _ in xs] for _ in xs]
    for j, xj in enumerate(xs):
        coeff = [Fraction(1)]
        denom = Fraction(1)
        for k, xk in enumerate(xs):
            if k == j:
                continue
            coeff = poly_mul(coeff, [-xk, Fraction(1)])
            denom *= xj - xk
        for n, c in enumerate(coeff):
            rows[n][j] = c / denom
    return rows


def floor_log10_fraction(x: Fraction) -> int:
    """Return exact floor(log10(x)) for positive rational x without floating logs."""
    if x <= 0:
        raise ValueError("positive rational required")
    n = x.numerator
    d = x.denominator
    e = len(str(n)) - len(str(d))
    if e >= 0:
        if n < d * (10 ** e):
            e -= 1
    else:
        if n * (10 ** (-e)) < d:
            e -= 1
    if not (Fraction(10) ** e <= x < Fraction(10) ** (e + 1)):
        raise ArithmeticError("power-of-ten bracket failed")
    return e


def amplification(rows: list[list[Fraction]], h: Fraction) -> dict:
    if h == 0:
        raise ValueError("nonzero spacing required")
    row_l1 = [sum((abs(c) for c in row), Fraction(0)) for row in rows]
    h_abs = abs(h)
    factors = [
        Fraction((C ** n) * math.factorial(n), 1) * row_l1[n] / (h_abs ** n)
        for n in range(RMAX + 1)
    ]
    kappa = max(factors)
    dominant = max(range(len(factors)), key=lambda n: factors[n])
    power = floor_log10_fraction(kappa)
    return {
        "spacing": h,
        "dominant_order": dominant,
        "kappa": kappa,
        "floor_log10_kappa": power,
        "power10_bracket": f"10^{power} <= kappa < 10^{power + 1}",
        "highest_order_row_l1": row_l1[-1],
    }


def main() -> int:
    rows = vandermonde_inverse_rows(NODES)

    # Exact inverse cross-check V*V^{-1}=I over Q.
    inverse_ok = True
    for i, t in enumerate(NODES):
        for n in range(RMAX + 1):
            value = sum((Fraction(t) ** k) * rows[k][n] for k in range(RMAX + 1))
            inverse_ok = inverse_ok and value == (1 if i == n else 0)

    results = [amplification(rows, h) for h in SPACINGS]
    exponents_ok = all(
        r["floor_log10_kappa"] == EXPECTED_FLOOR_LOG10[r["spacing"]]
        for r in results
    )
    dominant_ok = all(r["dominant_order"] == RMAX for r in results)
    monotone_ok = all(results[i + 1]["kappa"] > results[i]["kappa"] for i in range(len(results) - 1))
    algebra_ok = bool(inverse_ok and exponents_ok and dominant_ok and monotone_ok)

    claims = [
        {
            "id": "V7-EPSC19-N1-SAMPLE-TO-SCALED-JET-NORM",
            "name": "exact induced infinity norm for the N=1 sample-to-scaled-Taylor interpolation operator",
            "tier": "Dr",
            "status": "DERIVED" if algebra_ok else "OPEN",
            "evidence": (
                "exact rational Lagrange inversion of the 24x24 power Vandermonde; "
                "kappa_inf(h)=max_n 600^n n! |h|^-n sum_j |V^-1[n,j]|"
                if algebra_ok else
                "exact interpolation cross-check or declared scale brackets failed"
            ),
        },
        {
            "id": "V7-EPSC19-N1-TAYLOR-INTERMEDIATE-ILL-CONDITIONING",
            "name": "small-spacing reconstruction of the existing scaled Taylor chart strongly amplifies sample-space error",
            "tier": "finite_diagnostic",
            "status": "PASS" if algebra_ok else "FAIL",
            "evidence": "; ".join(
                f"h={r['spacing']}: {r['power10_bracket']}, dominant n={r['dominant_order']}"
                for r in results
            ),
        },
        {
            "id": "V7-EPSC19-N1-DIRECT-SAMPLE-MAP-CONDITIONING",
            "name": "branch-wide conditioning and inverse radius for the direct 49-sample map",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "this checker diagnoses the sample->scaled-Taylor intermediate map only; "
                "the direct finite sample map may condition differently and still needs an explicit spacing, "
                "validated flow/tangent enclosure, preconditioner, q_h<1, noise propagation and branch capture"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "primary_shell_channels": 2,
        "samples_per_primary_shell": 24,
        "nodes": list(NODES),
        "scaled_taylor_rows": "s_n=600^n n!",
        "exact_vandermonde_inverse": inverse_ok,
        "results": [
            {
                "spacing": f"{r['spacing'].numerator}/{r['spacing'].denominator}",
                "dominant_order": r["dominant_order"],
                "floor_log10_kappa": r["floor_log10_kappa"],
                "power10_bracket": r["power10_bracket"],
                "highest_order_inverse_row_l1": f"{r['highest_order_row_l1'].numerator}/{r['highest_order_row_l1'].denominator}",
            }
            for r in results
        ],
        "finite_first_scope": "fixed N=1 finite interpolation algebra; no continuum premise",
        "interpretation": (
            "structural invertibility as h->0 does not imply that recovering the high-order scaled Taylor chart "
            "from samples is a useful measurement interface; direct sample-map inversion should be certified instead"
        ),
    }

    print("EPSC-19 N=1 exact sample interpolation conditioning")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")))
    return 0 if algebra_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
