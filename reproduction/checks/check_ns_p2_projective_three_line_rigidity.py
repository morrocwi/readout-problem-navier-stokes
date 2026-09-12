#!/usr/bin/env python3
"""Exact checker for projective three-line monodromy rigidity.

This checker concerns projective polarization-line transport on P^1. It does
NOT identify this projective holonomy with the repository's separate complex
phase-incidence holonomy.
"""
import sympy as sp

a, d, t, lam = sp.symbols('a d t lam', nonzero=True, real=True)
M = sp.diag(a, d)
v = sp.Matrix([1, t])
sol = sp.solve([sp.Eq(a, lam), sp.Eq(d*t, lam*t)], [lam, d], dict=True)
assert sol == [{d: a, lam: a}]


def collinear(u, v):
    return sp.simplify(u[0]*v[1] - u[1]*v[0]) == 0

M_nonid = sp.diag(2, 1)
e1 = sp.Matrix([1, 0])
e2 = sp.Matrix([0, 1])
e3 = sp.Matrix([1, 1])
assert collinear(M_nonid*e1, e1)
assert collinear(M_nonid*e2, e2)
assert not collinear(M_nonid*e3, e3)

M_scalar = 3*sp.eye(2)
for v0 in [e1, e2, e3, sp.Matrix([2, -5])]:
    assert collinear(M_scalar*v0, v0)

print('NS P2 projective three-line rigidity: PASS')
print('three distinct fixed projective lineage classes => identity in PGL2')
print('complex phase-incidence holonomy remains a separate typed object')
