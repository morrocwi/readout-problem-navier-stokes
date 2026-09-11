#!/usr/bin/env python3
"""Exact rational controls for NS-P2-HH-GEOM-LIFT.

This script verifies the arithmetic of the finite-prefix + geometric-tail lifting
formula for the H^3 dyadic weight 64^j. It does NOT prove that Navier--Stokes
High--High defects obey the supplied envelope; that is the OPEN NS-P2-HH-UNIFORM
obligation.
"""
from fractions import Fraction
import json

WEIGHT_BASE = 64


def prefix_constant(coeffs):
    total = Fraction(0)
    for j, c in coeffs:
        if j < 0 or c < 0:
            raise ValueError("prefix shells and coefficients must be nonnegative")
        total += Fraction(WEIGHT_BASE**j) * c
    return total


def geometric_tail_constant(A: Fraction, q: Fraction, J: int):
    if A < 0 or q < 0 or J < 0:
        raise ValueError("need A,q,J nonnegative")
    r = Fraction(WEIGHT_BASE) * q
    if not r < 1:
        return None
    return A * (r ** (J + 1)) / (1 - r)


def main() -> int:
    # Positive exact calibration: r = 64 q = 1/2.
    q = Fraction(1, 128)
    A = Fraction(2)
    J = 3
    prefix = [
        (0, Fraction(1, 100)),
        (1, Fraction(1, 12800)),
        (2, Fraction(1, 819200)),
        (3, Fraction(1, 104857600)),
    ]
    prefix_c = prefix_constant(prefix)
    tail_c = geometric_tail_constant(A, q, J)
    if tail_c is None:
        raise AssertionError("q=1/128 must satisfy 64q<1")

    r = Fraction(WEIGHT_BASE) * q
    expected_tail = A * (r ** (J + 1)) / (1 - r)
    if tail_c != expected_tail:
        raise AssertionError("geometric tail formula mismatch")

    # Direct finite partial sums must remain below the infinite-tail formula.
    partial = Fraction(0)
    for j in range(J + 1, J + 25):
        partial += Fraction(WEIGHT_BASE**j) * A * (q ** j)
    if not partial < tail_c:
        raise AssertionError("finite geometric partial sum must lie below exact infinite tail")

    total_c = prefix_c + tail_c
    if total_c <= 0:
        raise AssertionError("combined adapter coefficient must be positive in calibration")

    # Sharp certificate-template guard: q=1/64 is not summable under H^3 weights.
    critical = geometric_tail_constant(Fraction(1), Fraction(1, 64), J)
    if critical is not None:
        raise AssertionError("critical 64q=1 must HOLD")

    supercritical = geometric_tail_constant(Fraction(1), Fraction(1, 32), J)
    if supercritical is not None:
        raise AssertionError("supercritical 64q>1 must HOLD")

    result = {
        "weight_base": WEIGHT_BASE,
        "q": str(q),
        "64q": str(r),
        "J": J,
        "A": str(A),
        "prefix_constant": str(prefix_c),
        "tail_constant": str(tail_c),
        "combined_C_R": str(total_c),
        "critical_q_1_over_64": "HOLD",
        "supercritical_q_1_over_32": "HOLD",
        "uniform_defect_envelope": "NOT_PROVED_BY_THIS_CHECKER",
        "scope": "exact arithmetic for P2 lifting theorem only; NS-P2-HH-UNIFORM remains OPEN",
    }
    print("NS P2 geometric tail lift exact controls")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS P2 GEOMETRIC TAIL LIFT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
