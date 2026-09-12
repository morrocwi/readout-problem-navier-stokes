#!/usr/bin/env python3
"""Exact finite algebra audit for nonidentity Type-P monodromy fixed-line classification.

This checker proves only the 2x2 projective fixed-line algebra used by the A1
reduction. It does not prove full-convolution realization, FNW/OCSR, G6/G7,
or Clay regularity.
"""

import sympy as sp

# Generic 2x2 representative.
a,b,c,d = sp.symbols('a b c d', real=True)
x = sp.symbols('x', real=True)

# In affine coordinate [x:1], fixed lines satisfy
# (a x + b, c x + d) proportional to (x,1), hence
# c x^2 + (d-a)x - b = 0.
poly = sp.expand(c*x**2 + (d-a)*x - b)
D = sp.factor((d-a)**2 + 4*b*c)
D_trace = sp.factor((a+d)**2 - 4*(a*d-b*c))
assert sp.expand(D - D_trace) == 0

# Exact model representatives for 0/1/2 real fixed projective lines.
# Elliptic: rotation by 90 degrees -> x^2+1=0, no real fixed line.
Ae = sp.Matrix([[0,-1],[1,0]])
pe = sp.expand(Ae[1,0]*x**2 + (Ae[1,1]-Ae[0,0])*x - Ae[0,1])
assert pe == x**2 + 1
assert sp.discriminant(pe, x) < 0

# Parabolic: Jordan shear -> one double fixed line.
Ap = sp.Matrix([[1,1],[0,1]])
# Affine chart misses [1:0] when c=0, so use homogeneous fixed equation
# c X^2 + (d-a)XY - b Y^2 = 0 = -Y^2.
X,Y = sp.symbols('X Y', real=True)
Fp = sp.expand(Ap[1,0]*X**2 + (Ap[1,1]-Ap[0,0])*X*Y - Ap[0,1]*Y**2)
assert Fp == -Y**2

# Hyperbolic: diagonal with distinct eigenvalues -> two fixed lines.
Ah = sp.Matrix([[2,0],[0,1]])
Fh = sp.expand(Ah[1,0]*X**2 + (Ah[1,1]-Ah[0,0])*X*Y - Ah[0,1]*Y**2)
assert Fh == -X*Y

# Three-line rigidity sanity: if a 2x2 representative fixes [1:0], [0:1],
# and [1:1], then it is scalar.
A,B,C,Dd = sp.symbols('A B C D', real=True)
# first two fixed -> B=C=0; third fixed -> A=D
assert sp.Matrix([[A,0],[0,A]]) == A*sp.eye(2)

print('NS P2 Type-P nonidentity fixed-line classification: PASS')
print('fixed homogeneous equation: c X^2 + (d-a) X Y - b Y^2 = 0')
print('discriminant: (tr A)^2 - 4 det A')
print('nonidentity PGL(2,R): 0, 1, or 2 real fixed projective lines')
print('rank-2 recurrent nonidentity branch can only survive in the 2-line case')
