#!/usr/bin/env python3
"""Exact finite algebra checks for the planar Fourier-support branch.

The analytic regularity step uses the classical 2D NSE theorem; this checker
verifies only the lattice/convolution geometry and the fresh-donor/mirror
fixtures used by the branch reduction.
"""

import sympy as sp

# Generic symbolic dot-linearity audit: if m.p=m.q=0 then m.(p+q)=0.
m1, m2, m3 = sp.symbols("m1 m2 m3")
p1, p2, p3 = sp.symbols("p1 p2 p3")
q1, q2, q3 = sp.symbols("q1 q2 q3")
m = sp.Matrix((m1,m2,m3))
p = sp.Matrix((p1,p2,p3))
q = sp.Matrix((q1,q2,q3))
assert sp.expand(m.dot(p+q) - m.dot(p) - m.dot(q)) == 0

# Concrete primitive plane for the fresh-donor/mirror family: ky=0, normal e_y.
n = sp.symbols("n", positive=True, integer=True)
normal = sp.Matrix((0,1,0))
modes = [
    sp.Matrix((n,0,0)),
    sp.Matrix((n,0,n)),
    sp.Matrix((2*n,0,n)),
    sp.Matrix((2*n,0,-n)),
    sp.Matrix((4*n,0,0)),
    sp.Matrix((n,0,-n)),
    sp.Matrix((3*n,0,0)),
]
for v in modes:
    assert sp.simplify(normal.dot(v)) == 0

# Closure on all pair sums in the fixture.
for a in modes:
    for b in modes:
        assert sp.simplify(normal.dot(a+b)) == 0

# First two fresh-donor steps and mirror cancellation target stay in the plane.
p0 = sp.Matrix((n,0,0))
q0 = sp.Matrix((n,0,n))
p1 = p0+q0
q1 = sp.Matrix((2*n,0,-n))
p2 = p1+q1
qt0 = sp.Matrix((n,0,-n))
qt1 = sp.Matrix((2*n,0,n))
r = q0+q1
assert p1 == sp.Matrix((2*n,0,n))
assert p2 == sp.Matrix((4*n,0,0))
assert qt0+qt1 == r == sp.Matrix((3*n,0,0))
for v in (p0,q0,p1,q1,p2,qt0,qt1,r):
    assert normal.dot(v) == 0

print("NS P2 planar escape branch geometry")
print("symbolic plane closure m.(p+q)=m.p+m.q: PASS")
print("fresh-donor/mirror fixture plane: ky=0")
print("all tested convolution sums stay in ky=0")
print("analytic next step: plane-supported NSE = 2D3C; classical 2D regularity invoked separately")
print("NS-P2 PLANAR FOURIER SUPPORT CHECK PASS")
