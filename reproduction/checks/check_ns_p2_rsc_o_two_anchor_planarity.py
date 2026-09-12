#!/usr/bin/env python3
"""Exact symbolic audit for PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01.

The proof is local linear algebra.  On the orthogonality branch a_i·q=0,
projected cross silence is equivalent to b·p_i=0.  With b·q=0 and b!=0,
q,p1,p2 cannot span R^3.

The adapted-coordinate check below verifies the determinant factor and the two
logical branches exactly; no floating arithmetic is used.
"""

import sympy as sp

# Adapt coordinates so W=span(a1,a2) is the xy-plane and q is its normal.
# Take a1=e1 and a2=(c,s,0) with s != 0 (independence).
c, s, Q = sp.symbols('c s Q', nonzero=True, real=True)
y1, z1, u, z2 = sp.symbols('y1 z1 u z2', real=True)
bx, by = sp.symbols('bx by', real=True)


def V(*xs):
    return sp.Matrix(xs)


a1 = V(1, 0, 0)
a2 = V(c, s, 0)
q = V(0, 0, Q)

# Parameterize anchors from a_i · p_i = 0.
p1 = V(0, y1, z1)
p2 = V(s*u, -c*u, z2)

# Recruited polarization b lies in q^perp.
b = V(bx, by, 0)

assert sp.simplify(a1.dot(p1)) == 0
assert sp.simplify(a2.dot(p2)) == 0
assert sp.simplify(a1.dot(q)) == 0
assert sp.simplify(a2.dot(q)) == 0
assert sp.simplify(b.dot(q)) == 0

# On the O branch, exact cross silence is b·p_i = 0.
e1 = sp.factor(b.dot(p1))
e2 = sp.factor(b.dot(p2))
assert e1 == by*y1
assert e2 == u*(s*bx - c*by)

# Wavevector planarity determinant.
det = sp.factor(sp.Matrix.hstack(p1, p2, q).det())
assert det == -Q*s*u*y1

# Exact case split for nonzero b:
#   by != 0 => e1=0 forces y1=0 => det=0.
#   by == 0 => bx != 0; e2=0 and s!=0 force u=0 => det=0.
# The checker verifies the algebraic factors used in both branches.
assert sp.factor(det.subs(y1, 0)) == 0
assert sp.factor(det.subs(u, 0)) == 0

# Non-vacuity rational fixtures for each branch.
# Branch A: by != 0 -> y1=0.
vals_A = {c: sp.Rational(1,2), s: 1, Q: 2, y1: 0, z1: 3,
          u: 5, z2: 7, bx: sp.Rational(1,2), by: 1}
# Choose bx so e2=0: s*bx-c*by = 1/2 - 1/2 = 0.
assert sp.simplify(e1.subs(vals_A)) == 0
assert sp.simplify(e2.subs(vals_A)) == 0
assert sp.simplify(det.subs(vals_A)) == 0

# Branch B: by=0, bx!=0 -> u=0.
vals_B = {c: 2, s: 3, Q: 5, y1: 7, z1: 11,
          u: 0, z2: 13, bx: 1, by: 0}
assert sp.simplify(e1.subs(vals_B)) == 0
assert sp.simplify(e2.subs(vals_B)) == 0
assert sp.simplify(det.subs(vals_B)) == 0

# q direction lock is explicit in adapted coordinates: q || a1 x a2.
normal = sp.simplify(a1.cross(a2))
assert normal == V(0, 0, s)
assert sp.simplify(q.cross(normal)) == sp.zeros(3, 1)

print('NS P2 RSC-O two-anchor planarity audit: PASS')
print('O-silence equations:', e1, ',', e2)
print('det[p1,p2,q] =', det)
print('nonzero b case split forces det=0 exactly')
print('q is direction-locked to a1 x a2')
