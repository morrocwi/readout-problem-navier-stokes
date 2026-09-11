#!/usr/bin/env python3
"""Exact coherence-defect identity for the analytic NS triad.

For the repository's reduced triad variables
  x' = 2 c_a r - 2 nu s_a x
  y' = 2 c_b r - 2 nu s_b y
  z' = 2 c_c r - 2 nu s_c z
  r' = c_a y z + c_b x z + c_c x y - nu(s_a+s_b+s_c) r,
with (c_a,c_b,c_c)=(3/10,-4/5,1/2) and (s_a,s_b,s_c)=(1,2,5),
define the phase-coherence defect

  D = x y z - r^2.

Exact algebra gives

  D' = -2 nu(s_a+s_b+s_c) D = -16 nu D.

Thus D=0 is invariant: an isolated triad can remain perfectly phase locked.  This
refutes the precise shortcut 'individual triad dynamics or viscosity necessarily
creates a positive decoherence margin'.  Any strict margin must come from overlap
constraints/network frustration or another additional mechanism.
"""
import sympy as sp

x,y,z,r,nu = sp.symbols('x y z r nu')
ca,cb,cc = sp.Rational(3,10),sp.Rational(-4,5),sp.Rational(1,2)
sa,sb,sc = 1,2,5

xp=2*ca*r-2*nu*sa*x
yp=2*cb*r-2*nu*sb*y
zp=2*cc*r-2*nu*sc*z
rp=ca*y*z+cb*x*z+cc*x*y-nu*(sa+sb+sc)*r
D=x*y*z-r**2
Dp=sp.expand(xp*y*z+x*yp*z+x*y*zp-2*r*rp)
expected=-2*nu*(sa+sb+sc)*D

assert sp.simplify(Dp-expected)==0
assert sp.simplify(expected + 16*nu*D)==0

print('NS P2 exact isolated-triad coherence defect')
print('D = xyz-r^2')
print("D' =", sp.factor(Dp))
print('D=0 invariant: PASS')
print('individual-triad automatic decoherence candidate: REFUTED')
print('NS-P2 TRIAD COHERENCE DEFECT PASS')
