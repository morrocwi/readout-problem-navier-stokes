#!/usr/bin/env python3
"""Exact finite interface for the P2 H^3 dissipative-margin reduction.

The checker verifies one declared finite cutoff/time-cell inequality
    P_plus <= theta * D_minus + C * (1 + X_plus)
using Fraction-only arithmetic.

It does NOT prove that the enclosures are sound, that cells cover all times, or that
the same theta,C work uniformly over all cutoffs. Those are exactly the OPEN
NS-P2-H3-MARGIN-UNIFORM obligations.
"""
from fractions import Fraction
import json


def verify_margin(P_plus: Fraction, D_minus: Fraction, X_plus: Fraction,
                  theta: Fraction, C: Fraction) -> bool:
    if not (Fraction(0) <= theta < Fraction(1)):
        return False
    if D_minus < 0 or X_plus < 0 or C < 0:
        return False
    return P_plus <= theta * D_minus + C * (1 + X_plus)


def gronwall_series_upper(X0: Fraction, C: Fraction, T: Fraction, m: int = 8) -> Fraction:
    """A finite rational upper calibration for (1+X0)e^(2CT).

    Uses e^x <= 1/(1-x) only when 0<=x<1, so it is a deliberately local
    calibration, not the analytic proof of Gronwall used in the manuscript.
    """
    if X0 < 0 or C < 0 or T < 0:
        raise ValueError("nonnegative data required")
    x = 2 * C * T / m
    if not (Fraction(0) <= x < 1):
        raise ValueError("choose more subdivisions so 2CT/m < 1")
    one_step = Fraction(1, 1) / (1 - x)
    return (1 + X0) * (one_step ** m)


def main() -> int:
    # Positive cell.
    good = dict(
        P_plus=Fraction(23, 10),
        D_minus=Fraction(4, 1),
        X_plus=Fraction(3, 2),
        theta=Fraction(1, 2),
        C=Fraction(3, 25),
    )
    # RHS = 2 + (3/25)*(5/2) = 23/10 exactly.
    if not verify_margin(**good):
        raise AssertionError("exact boundary margin cell should PASS")

    bad = dict(good)
    bad["P_plus"] = Fraction(231, 100)
    if verify_margin(**bad):
        raise AssertionError("insufficient dissipative margin must HOLD")

    bad_theta = dict(good)
    bad_theta["theta"] = Fraction(1)
    if verify_margin(**bad_theta):
        raise AssertionError("theta>=1 must HOLD")

    # Rational calibration of the resulting finite-time bound only.
    X0 = Fraction(2)
    C = Fraction(1, 10)
    T = Fraction(1)
    upper = gronwall_series_upper(X0, C, T, m=4)
    if upper <= 1 + X0:
        raise AssertionError("positive C,T should enlarge the Gronwall envelope")

    result = {
        "cell_pass": True,
        "cell_hold": True,
        "theta_guard": True,
        "positive_cell_rhs": str(good["theta"] * good["D_minus"] + good["C"] * (1 + good["X_plus"])),
        "positive_cell_P_upper": str(good["P_plus"]),
        "gronwall_rational_calibration": str(upper),
        "all_time_coverage": "NOT_PROVED_BY_THIS_CHECKER",
        "uniform_in_N_constants": "NOT_PROVED_BY_THIS_CHECKER",
        "enclosure_soundness": "NOT_PROVED_BY_THIS_CHECKER",
        "scope": "exact finite margin arithmetic only; NS-P2-H3-MARGIN-UNIFORM remains OPEN",
    }
    print("NS P2 H3 dissipative-margin exact interface")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS P2 H3 MARGIN INTERFACE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
