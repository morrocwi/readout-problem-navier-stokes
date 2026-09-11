#!/usr/bin/env python3
"""Exact reflected donor pair with opposite target coefficient."""

import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
N = sp.Matrix((0, 1, 0))
q0 = sp.Matrix((n, 0, n))
q1 = sp.Matrix((2*n, 0, -n))
t0 = sp.Matrix((n, 0, -n))
t1 = sp.Matrix((2*n, 0, n))
r = sp.Matrix((3*n, 0, 0))


def norm(v):
    return sp.sqrt(sp.factor(v.dot(v)))


def tang(v):
    return sp.simplify(N.cross(v)/norm(v))


def coupling(p, hp, q, hq, k, hk):
    assert p + q == k
    return sp.factor(sp.simplify(hp.dot(q)*hk.dot(hq) + hq.dot(p)*hk.dot(hp)))


def alpha(p, q, k):
    c = coupling(p, tang(p), q, tang(q), k, tang(k))
    return sp.factor(c*sp.sqrt(1+norm(k)**2)/(sp.sqrt(1+norm(p)**2)*sp.sqrt(1+norm(q)**2)))

c_orig = coupling(q0, tang(q0), q1, tang(q1), r, tang(r))
c_mirr = coupling(t0, tang(t0), t1, tang(t1), r, tang(r))
a_orig = alpha(q0, q1, r)
a_mirr = alpha(t0, t1, r)


def main():
    expected = 3*sp.sqrt(10)*n/10
    assert q0 + q1 == r
    assert t0 + t1 == r
    assert sp.simplify(c_orig-expected) == 0
    assert sp.simplify(c_mirr+expected) == 0
    assert sp.simplify(c_orig+c_mirr) == 0
    assert sp.simplify(a_orig+a_mirr) == 0

    # Equal product amplitudes give exact cancellation in the target equation.
    Z = sp.symbols("Z", complex=True)
    target_sum = sp.simplify(-sp.I*a_orig*Z - sp.I*a_mirr*Z)
    assert target_sum == 0

    # All modes lie in the same Fourier plane ky=0.
    for v in (q0, q1, t0, t1, r):
        assert v[1] == 0

    print("NS P2 fresh-donor mirror cancellation")
    print("original coefficient:", c_orig)
    print("mirror coefficient:", c_mirr)
    print("normalized alpha original:", a_orig)
    print("normalized alpha mirror:", a_mirr)
    print("equal pair products cancel target forcing exactly")
    print("all wavevectors satisfy ky=0")
    print("scope: one target cancellation; full support invariance not asserted here")
    print("NS-P2 FRESH-DONOR MIRROR CANCELLATION PASS")


if __name__ == "__main__":
    main()
