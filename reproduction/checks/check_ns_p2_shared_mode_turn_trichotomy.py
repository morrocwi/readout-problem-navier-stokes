#!/usr/bin/env python3
"""Exact integer fixtures for shared-mode plane-turn classification."""

import sympy as sp


def turn_invariant(p, q1, q2):
    p = sp.Matrix(p); q1 = sp.Matrix(q1); q2 = sp.Matrix(q2)
    n1 = p.cross(q1); n2 = p.cross(q2)
    assert n1.dot(n1) != 0 and n2.dot(n2) != 0
    c2 = sp.factor((n1.dot(n2))**2 / (n1.dot(n1)*n2.dot(n2)))
    mu = sp.factor(4*c2*(1-c2))
    return n1, n2, c2, mu

# Same-plane fixture.
n1, n2, c2_same, mu_same = turn_invariant(
    (1,0,0), (0,0,1), (1,0,1)
)
assert c2_same == 1
assert mu_same == 0
assert n1.cross(n2) == sp.zeros(3,1)

# Orthogonal-turn fixture.
o1, o2, c2_orth, mu_orth = turn_invariant(
    (2,0,1), (-1,0,0), (2,4,1)
)
assert sp.simplify(o1.dot(o2)) == 0
assert c2_orth == 0
assert mu_orth == 0
assert o1.cross(o2) != sp.zeros(3,1)

# Positive-dispersion fixture: normals have acute angle pi/4.
d1, d2, c2_disp, mu_disp = turn_invariant(
    (1,0,0), (0,0,1), (0,1,1)
)
assert c2_disp == sp.Rational(1,2)
assert mu_disp == 1

# Algebraic zero-set audit for mu=4 c2(1-c2).
x = sp.symbols("x", real=True)
poly = sp.factor(4*x*(1-x))
assert sp.solve(sp.Eq(poly,0),x) == [0,1]

print("NS P2 shared-mode plane-turn trichotomy")
print("same-plane: c^2 =", c2_same, "mu =", mu_same, "normals =", tuple(n1), tuple(n2))
print("orthogonal-turn: c^2 =", c2_orth, "mu =", mu_orth, "normals =", tuple(o1), tuple(o2))
print("positive-dispersion: c^2 =", c2_disp, "mu =", mu_disp, "normals =", tuple(d1), tuple(d2))
print("zero dispersion iff projective normal lines are parallel or orthogonal")
print("NS-P2 SHARED-MODE TURN TRICHOTOMY PASS")
