#!/usr/bin/env python3
"""Exact checker for rank-2 plane-switch capacity / two-lineage plane lock.

This is pure retained-space linear algebra used after the existing rank-2
self-closure proposal.  It does not assert physical dissipation.

If a zero-defect/no-exit rank-2 recompression keeps future-relevant retained
polarization vectors c_i active, all c_i must lie in one next plane W'. Hence
three retained vectors can be absorbed only if det[c1,c2,c3]=0. Two independent
retained vectors uniquely determine W'=span(c1,c2); every further retained
novelty must satisfy det[c1,c2,c]=0 or be routed through a registered
cancellation/terminal/exit/defect channel.
"""

import sympy as sp

x1,y1,z1,x2,y2,z2,x3,y3,z3 = sp.symbols(
    'x1 y1 z1 x2 y2 z2 x3 y3 z3', real=True)

c1 = sp.Matrix([x1,y1,z1])
c2 = sp.Matrix([x2,y2,z2])
c3 = sp.Matrix([x3,y3,z3])

D = sp.factor(sp.Matrix.hstack(c1,c2,c3).det())
triple = sp.factor(c1.dot(c2.cross(c3)))
assert sp.simplify(D-triple) == 0

n = sp.simplify(c1.cross(c2))
assert sp.simplify(n.dot(c1)) == 0
assert sp.simplify(n.dot(c2)) == 0
assert sp.simplify(n.dot(c3)-D) == 0

a = sp.Matrix([1,0,1])
b = sp.Matrix([0,1,1])
c_in = a+b
c_out = sp.Matrix([0,0,1])

assert a.cross(b) != sp.zeros(3,1)
assert sp.Matrix.hstack(a,b,c_in).det() == 0
assert sp.Matrix.hstack(a,b,c_out).det() != 0

a0 = sp.Matrix([1,2,0])
b0 = sp.Matrix([0,1,3])
n0 = a0.cross(b0)
assert n0.dot(a0) == 0 and n0.dot(b0) == 0
u,v,w = sp.symbols('u v w', real=True)
M = sp.Matrix([[a0[0],a0[1],a0[2]], [b0[0],b0[1],b0[2]]])
assert M.rank() == 2
assert len(M.nullspace()) == 1
assert M.nullspace()[0].cross(n0) == sp.zeros(3,1)

print('NS P2 plane-switch capacity: PASS')
print('three retained novelties fit one rank-2 plane iff det[c1,c2,c3]=0')
print('two independent retained lineages uniquely lock the next rank-2 plane')
