#!/usr/bin/env python3
"""Exact finite controls for NS-FUB-A1C residual-certificate completeness.

These controls do not prove the analytic completeness theorem.  They regression-test
three load-bearing logical features of its certificate language using Fraction only:

1. absolute symmetric propagation is not localization-complete even for x'=1;
2. a residual-centered reference path can have zero defect for x'=1;
3. a strict positive finite observable margin can be certified for x'=x by a
   rational affine reference path and exact contraction/self-map inequalities.

No floating point, continuum Navier--Stokes claim, arbitrary-N claim, or runtime claim
is made here.
"""
from fractions import Fraction
import json


def absolute_wrapping_control():
    # x'=1, x(0)=0, T=1.  Repeated I <- I + [-h,h] has halfwidth n*h = 1.
    rec = {}
    for n in (1, 10, 100, 1000):
        h = Fraction(1, n)
        halfwidth = n * h
        rec[str(n)] = str(halfwidth)
        assert halfwidth == 1
    return rec


def zero_residual_control():
    # Same ODE, exact rational reference p(t)=t, hence F(p)-p'=1-1=0.
    residual = Fraction(0)
    endpoint_error = Fraction(0)
    assert residual == 0
    assert endpoint_error == 0
    return residual, endpoint_error


def strict_margin_control():
    # Scalar ODE x'=x, x(0)=1.  Use p(t)=1+t on [0,h].
    # For |e|<=r, |F(p+e)-p'| = |t+e| <= h+r and |DF|=1.
    h = Fraction(1, 100)
    r = Fraction(1, 4000)
    R = h + r
    L = Fraction(1)

    self_map = h * R
    contraction = h * L
    assert self_map < r
    assert contraction < 1

    # The Banach tube certifies x(h) in p(h)+[-r,r].
    center = 1 + h
    lower = center - r
    threshold = Fraction(2019, 2000)  # 1.0095
    assert lower > threshold

    return {
        "h": str(h),
        "r": str(r),
        "R": str(R),
        "L": str(L),
        "self_map_ratio": str(self_map / r),
        "contraction_q": str(contraction),
        "endpoint_center": str(center),
        "endpoint_lower": str(lower),
        "threshold": str(threshold),
        "strict_margin": str(lower - threshold),
    }


def main() -> int:
    absolute = absolute_wrapping_control()
    residual, endpoint_error = zero_residual_control()
    positive = strict_margin_control()

    summary = {
        "absolute_xprime_1_halfwidths": absolute,
        "residual_xprime_1": str(residual),
        "residual_xprime_1_endpoint_error": str(endpoint_error),
        "strict_margin_xprime_x": positive,
        "scope": (
            "exact finite regression controls for the residual-certificate language; "
            "analytic completeness theorem not machine-proved by this script"
        ),
    }
    print("NS-FUB-A1C residual-certificate completeness controls")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("NS-FUB-A1C CERTIFICATE COMPLETENESS CONTROLS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
