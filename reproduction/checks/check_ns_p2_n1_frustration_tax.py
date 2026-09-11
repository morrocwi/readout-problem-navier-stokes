#!/usr/bin/env python3
"""Exact four-term frustration-tax theorem from the N=1 H3 conflict cycle.

The verified sign-frustration classifier exposes the following four monomials in
the integer-scaled nonlinear H3 production polynomial:

  -11400 a b c + 10800 a b d - 11400 a c e - 10800 a d e
= 600 a (-19bc + 18bd - 19ce - 18de).

Because the product of the four signed terms is always non-positive and is strictly
negative when abcde != 0, not all four terms can have the same nonzero sign.
Consequently, if S is the sum of absolute term magnitudes and m their minimum,

  |Q_cycle| <= S - 2m.

This is an exact quantitative local cancellation tax.  It gives no uniform relative
deficit without a separate lower bound on m/S; that missing lower bound is the next
dynamical/network-level obligation.
"""
from fractions import Fraction
import itertools

COEFFS = (-11400, 10800, -11400, -10800)


def terms(a,b,c,d,e):
    return (
        COEFFS[0]*a*b*c,
        COEFFS[1]*a*b*d,
        COEFFS[2]*a*c*e,
        COEFFS[3]*a*d*e,
    )


def verify_integer_box(radius=3):
    tested = 0
    strict_when_nonzero = 0
    vals = range(-radius, radius+1)
    for a,b,c,d,e in itertools.product(vals, repeat=5):
        if a == b == c == d == e == 0:
            continue
        ts = terms(a,b,c,d,e)
        S = sum(abs(t) for t in ts)
        m = min(abs(t) for t in ts)
        q = abs(sum(ts))
        if q > S - 2*m:
            raise AssertionError((a,b,c,d,e,ts,q,S,m))
        tested += 1
        if all(v != 0 for v in (a,b,c,d,e)):
            # Product of term signs is negative, so at least one cancellation occurs.
            prod = 1
            for t in ts:
                prod *= 1 if t > 0 else -1
            if prod != -1:
                raise AssertionError('signed four-term product must be negative')
            if m <= 0 or q > S-2*m:
                raise AssertionError('strict nonzero frustration tax failed')
            strict_when_nonzero += 1
    return tested, strict_when_nonzero


def symbolic_coefficient_checks():
    # Remove common 600*a and verify the 2x2 bilinear matrix structure.
    # [b,e] M [c,d]^T with M=[[-19,18],[-19,-18]].
    M = ((-19,18),(-19,-18))
    # Columns are orthogonal; this exposes the Hadamard-like sign cycle.
    col_dot = M[0][0]*M[0][1] + M[1][0]*M[1][1]
    col0_sq = M[0][0]**2 + M[1][0]**2
    col1_sq = M[0][1]**2 + M[1][1]**2
    assert col_dot == 0
    assert col0_sq == 2*19**2
    assert col1_sq == 2*18**2
    return M, col_dot, col0_sq, col1_sq


def main():
    M, dot, c0, c1 = symbolic_coefficient_checks()
    tested, strict = verify_integer_box(3)
    print('NS P2 N=1 exact frustration-tax theorem')
    print('cycle matrix:', M)
    print('column dot:', dot, 'column squares:', c0, c1)
    print('integer tuples tested:', tested)
    print('all-amplitudes inequality: |Q_cycle| <= S_cycle - 2 m_cycle')
    print('strict nonzero tuples checked:', strict)
    print('uniform relative deficit requires separate control of m_cycle/S_cycle')
    print('NS-P2 N1 FRUSTRATION TAX PASS')


if __name__ == '__main__':
    main()
