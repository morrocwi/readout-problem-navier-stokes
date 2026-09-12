#!/usr/bin/env python3
"""Exact checker for projective three-line monodromy rigidity.

This checker concerns projective polarization-line transport on P^1.  It does
NOT identify this projective holonomy with the repository's separate complex
phase-incidence holonomy.

Claim: a projective linear map of a two-dimensional real fiber that fixes three
distinct projective lines is the identity in PGL(2,R).
"""

import sympy as sp

# After conjugating two distinct fixed lines to [1:0] and [0:1], any linear
# representative preserving both lines is diagonal.  A third distinct line can
# be written [1:t] with t != 0.  Fixing it projectively forces equal diagonal
# entries.
a, d, t, lam = sp.symbols('a d t lam', nonzero=True, real=True)
M = sp.diag(a, d)
v = sp.Matrix([1, t])

# M v = lambda v gives a=lambda and d*t=lambda*t. Since t!=0, d=lambda=a.
sol = sp.solve([sp.Eq(a, lam), sp.Eq(d*t, lam*t)], [lam, d], dict=True)
assert sol == [{d: a, lam: a}]

# Rational non-vacuity / falsifier controls.
M_nonid = sp.diag(2, 1)
e1 = sp.Matrix([1, 0])
e2 = sp.Matrix([0, 1])
e3 = sp.Matrix([1, 1])

# Nonidentity diagonal map fixes exactly the two coordinate projective lines,
# but not the third test line.
def collinear(u, v):
    return sp.simplify(u[0]*v[1] - u[1]*v[0]) == 0

assert collinear(M_nonid*e1, e1)
assert collinear(M_nonid*e2, e2)
assert not collinear(M_nonid*e3, e3)

M_scalar = 3*sp.eye(2)
for v0 in [e1, e2, e3, sp.Matrix([2, -5])]:
    assert collinear(M_scalar*v0, v0)

print('NS P2 projective three-line rigidity: PASS')
print('three distinct fixed projective lineage classes => scalar GL2 representative => identity in PGL2')
print('complex phase-incidence holonomy remains a separate typed object')
