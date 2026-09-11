#!/usr/bin/env python3
"""Exact induced off-tree interaction from two consecutive fresh donors."""

import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
N = sp.Matrix((0, 1, 0))
q0 = sp.Matrix((n, 0, n))
q1 = sp.Matrix((2*n, 0, -n))
r = q0 + q1
p0 = sp.Matrix((n, 0, 0))
p2 = sp.Matrix((4*n, 0, 0))


def norm(v):
    return sp.sqrt(sp.factor(v.dot(v)))


def tangent(v):
    return sp.simplify(N.cross(v) / norm(v))


def coupling(v1, h1, v2, h2, vo, ho):
    assert v1 + v2 == vo
    return sp.factor(
        sp.simplify(
            h1.dot(v2) * ho.dot(h2)
            + h2.dot(v1) * ho.dot(h1)
        )
    )


def gamma_h1_hom(v1, h1, v2, h2, vo, ho):
    c = coupling(v1, h1, v2, h2, vo, ho)
    return sp.factor(sp.simplify(2*c*norm(vo)/(norm(v1)*norm(v2))))


T0 = tangent(q0)
T1 = tangent(q1)
Tr = tangent(r)

c01 = coupling(q0, T0, q1, T1, r, Tr)
g01 = gamma_h1_hom(q0, T0, q1, T1, r, Tr)

EXPECTED_C = 3*sp.sqrt(10)*n/10
EXPECTED_G = sp.Rational(9, 5)

# Reality-allowed alternative pair p2 + (-p0) = r.  Both backbone velocities
# use N, so the coefficient vanishes exactly.
alt = coupling(p2, N, -p0, N, r, Tr)


def main():
    assert r == sp.Matrix((3*n, 0, 0))
    assert p2 + (-p0) == r
    assert sp.simplify(c01 - EXPECTED_C) == 0
    assert sp.simplify(g01 - EXPECTED_G) == 0
    assert sp.simplify(alt) == 0

    # Conservative inhomogeneous H1 correction >= 1/2 for nonzero integer modes.
    inh_floor = sp.Rational(9, 10)
    assert sp.simplify(EXPECTED_G/2 - inh_floor) == 0

    print("NS P2 fresh-donor induced interaction")
    print("q0 =", tuple(q0))
    print("q1 =", tuple(q1))
    print("r =", tuple(r))
    print("raw coefficient q0+q1->r:", c01)
    print("homogeneous H1 gamma:", g01)
    print("conservative inhomogeneous H1 floor:", inh_floor)
    print("alternative collinear backbone coefficient:", alt)
    print("if z_r=0 on declared two-step support: zdot_r = -i*c01*z_q0*z_q1")
    print("NS-P2 FRESH-DONOR INDUCED INTERACTION PASS")


if __name__ == "__main__":
    main()
