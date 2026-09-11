#!/usr/bin/env python3
"""Exact finite verifier for an NS-FUB-A1V H^3 exceedance certificate.

This checker proves only the finite arithmetic statement

    certified interval enclosure -> lower_bound(||v_N||_{H^3}^2) > B^2.

It does NOT prove that the supplied intervals enclose the actual Galerkin
trajectory. That enclosure is a separate validated-dynamics adapter obligation.

All arithmetic is fractions.Fraction; no floating-point arithmetic is used in
PASS/HOLD decisions.
"""

from fractions import Fraction
from typing import Iterable, Tuple

Interval = Tuple[Fraction, Fraction]
ModeRecord = Tuple[Tuple[int, int, int], Tuple[Interval, Interval, Interval], Tuple[Interval, Interval, Interval]]


def q(x: str | int) -> Fraction:
    return Fraction(x)


def validate_interval(iv: Interval) -> None:
    lo, hi = iv
    if lo > hi:
        raise ValueError(f"invalid interval [{lo}, {hi}]")


def min_square(iv: Interval) -> Fraction:
    """Exact minimum of x^2 over a closed rational interval."""
    validate_interval(iv)
    lo, hi = iv
    if lo <= 0 <= hi:
        return Fraction(0)
    return min(lo * lo, hi * hi)


def complex_rect_abs2_lower(re_iv: Interval, im_iv: Interval) -> Fraction:
    """Exact lower bound for |z|^2 over a rectangular complex interval."""
    return min_square(re_iv) + min_square(im_iv)


def h3_weight(k: Tuple[int, int, int]) -> int:
    k1, k2, k3 = k
    return (1 + k1 * k1 + k2 * k2 + k3 * k3) ** 3


def h3_squared_lower(records: Iterable[ModeRecord]) -> Fraction:
    """Lower bound for sum_k (1+|k|^2)^3 sum_j |u_j(k)|^2."""
    total = Fraction(0)
    for k, re_vec, im_vec in records:
        if len(re_vec) != 3 or len(im_vec) != 3:
            raise ValueError("each velocity mode must have exactly 3 components")
        w = h3_weight(k)
        for j in range(3):
            total += w * complex_rect_abs2_lower(re_vec[j], im_vec[j])
    return total


def verdict(records: Iterable[ModeRecord], threshold: Fraction) -> tuple[str, Fraction]:
    if threshold < 0:
        raise ValueError("threshold must be nonnegative")
    lower = h3_squared_lower(records)
    margin = lower - threshold * threshold
    return ("PASS" if margin > 0 else "HOLD", margin)


def fixture_pass() -> None:
    # One coefficient exactly equal to 1 at k=(1,0,0).
    # H^3 squared lower bound = (1+1)^3 * 1 = 8 > 2^2 = 4.
    z = (q(0), q(0))
    one = (q(1), q(1))
    records = [((1, 0, 0), (one, z, z), (z, z, z))]
    status, margin = verdict(records, q(2))
    assert status == "PASS"
    assert margin == q(4)


def fixture_hold_threshold() -> None:
    z = (q(0), q(0))
    one = (q(1), q(1))
    records = [((1, 0, 0), (one, z, z), (z, z, z))]
    status, margin = verdict(records, q(3))
    assert status == "HOLD"
    assert margin == q(-1)


def fixture_interval_crossing_zero() -> None:
    # A wide interval crossing zero contributes no certified positive lower bound.
    z = (q(0), q(0))
    wide = (q(-5), q(7))
    records = [((2, 0, 0), (wide, z, z), (z, z, z))]
    status, margin = verdict(records, q(1))
    assert h3_squared_lower(records) == 0
    assert status == "HOLD"
    assert margin == q(-1)


def fixture_exact_rational_margin() -> None:
    # k=0 has weight 1. Re coefficient in [3/2, 5/3] gives lower square 9/4.
    z = (q(0), q(0))
    re = (q("3/2"), q("5/3"))
    records = [((0, 0, 0), (re, z, z), (z, z, z))]
    status, margin = verdict(records, q("7/5"))
    assert status == "PASS"
    assert margin == q("9/4") - q("49/25")
    assert margin == q("29/100")


def main() -> None:
    fixture_pass()
    fixture_hold_threshold()
    fixture_interval_crossing_zero()
    fixture_exact_rational_margin()
    print("NS-FUB-A1V H3 CERTIFICATE CHECKER PASS")
    print("finite arithmetic only; state-enclosure adapter remains OPEN")


if __name__ == "__main__":
    main()
