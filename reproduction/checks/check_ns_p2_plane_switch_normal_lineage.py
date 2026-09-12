#!/usr/bin/env python3
"""Exact checker for normal/lineage reconstruction in a genuine plane switch.

For a basis-replacement chain W_j=span(c_j,c_{j+1}), define normals
n_j=c_j x c_{j+1}.  Then

  n_j x n_{j+1} = det[c_j,c_{j+1},c_{j+2}] c_{j+1}.

Hence on a genuine switch (nonzero determinant), the shared retained lineage
[c_{j+1}] is projectively determined by adjacent plane normals.
"""

import sympy as sp

a1,a2,a3,b1,b2,b3,c1,c2,c3 = sp.symbols(
    'a1 a2 a3 b1 b2 b3 c1 c2 c3', real=True)

a = sp.Matrix([a1,a2,a3])
b = sp.Matrix([b1,b2,b3])
c = sp.Matrix([c1,c2,c3])

n0 = a.cross(b)
n1 = b.cross(c)
Delta = sp.factor(sp.Matrix.hstack(a,b,c).det())
identity = sp.simplify(n0.cross(n1) - Delta*b)
assert identity == sp.zeros(3,1)

# Exact rational genuine-switch control.
a0 = sp.Matrix([1,0,0])
b0 = sp.Matrix([0,1,0])
c0 = sp.Matrix([0,0,1])
N0 = a0.cross(b0)
N1 = b0.cross(c0)
D0 = sp.Matrix.hstack(a0,b0,c0).det()
assert D0 == 1
assert N0.cross(N1) == b0

# Degenerate/no-switch control: c in span(a,b) gives Delta=0 and adjacent
# normals are parallel, so shared lineage cannot be reconstructed by the cross.
cdeg = a0+b0
N1d = b0.cross(cdeg)
assert sp.Matrix.hstack(a0,b0,cdeg).det() == 0
assert N0.cross(N1d) == sp.zeros(3,1)

print('NS P2 plane-switch normal-lineage reconstruction: PASS')
print('n_j x n_{j+1} = det[c_j,c_{j+1},c_{j+2}] c_{j+1}')
print('genuine switch => shared lineage determined projectively by adjacent normals')
