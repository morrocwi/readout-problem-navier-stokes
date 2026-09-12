#!/usr/bin/env python3
"""Exact symbolic checker for the general anchor-cross nullity locus.

For nonzero p,q,k=p+q in R^3, nonzero anchor polarization a with a.p=0,
define L_{p,q,a}: q^perp -> k^perp by
    L(b) = B_{p,q}(a,b)
for the existing symmetric projected NSE interaction B.

The exact kernel locus is
    ker L != {0}  <=>  (a.q = 0) OR (|q| = |p|),
away from the excluded k=0 case.

This checker verifies the adapted-coordinate determinant factorization and the
explicit equal-shell kernel vector. No floating arithmetic is used.
"""

import sympy as sp

P,A,C,x,y,z = sp.symbols("P A C x y z", real=True)


def V(*xs):
    return sp.Matrix(xs)


def proj(w,k):
    return sp.simplify(w - (w.dot(k)/k.dot(k))*k)


def B(p,q,a,b):
    k = p+q
    return sp.simplify(proj((a.dot(q))*b + (b.dot(p))*a, k))

# Adapted coordinates: p along e1; a lies in p^perp but is otherwise generic.
p = V(P,0,0)
a = V(0,A,C)
q = V(x,y,z)
k = p+q
lam = sp.expand(a.dot(q))

# q^perp chart, valid on z != 0; first two target coordinates provide a
# transverse chart whenever k_z=z != 0.
b1 = V(1,0,-x/z)
b2 = V(0,1,-y/z)
assert sp.simplify(q.dot(b1)) == 0
assert sp.simplify(q.dot(b2)) == 0

L1 = B(p,q,a,b1)
L2 = B(p,q,a,b2)
M = sp.Matrix([[sp.simplify(L1[0]), sp.simplify(L2[0])],
               [sp.simplify(L1[1]), sp.simplify(L2[1])]])

detL = sp.factor(sp.together(M.det()))
expected = sp.factor(lam**2 * (q.dot(q)-p.dot(p)) / k.dot(k))
assert sp.simplify(detL-expected) == 0

# Explicit kernel vector on the equal-shell branch lambda != 0:
# b_* = k - (k.p/lambda) a.
bstar = sp.simplify(k - (k.dot(p)/lam)*a)
assert sp.factor(sp.together(q.dot(bstar))) == sp.factor(q.dot(q)-p.dot(p))

beta = sp.simplify(bstar.dot(p))
raw = sp.simplify(lam*bstar + beta*a)
assert sp.simplify(raw - lam*k) == sp.zeros(3,1)
# The projected interaction is therefore zero identically; on |q|=|p|,
# bstar is also transverse to q and is an admissible kernel vector.
assert sp.simplify(B(p,q,a,bstar)) == sp.zeros(3,1)

# Orthogonality branch lambda=0: any nonzero b in p^perp cap q^perp is killed.
borth = sp.simplify(p.cross(q))
assert sp.simplify(q.dot(borth)) == 0
assert sp.simplify(p.dot(borth)) == 0
raw_orth = sp.expand((a.dot(q))*borth + (borth.dot(p))*a)
# borth = p x q is orthogonal to p identically, so raw_orth = (a.q) * borth exactly;
# on the orthogonality branch a.q = lam = 0 it vanishes.  (Substituting the sum A*y + C*z -> 0
# is not a reliable sympy pattern substitution; eliminate z through lam = 0 instead.)
assert sp.simplify(raw_orth - lam*borth) == sp.zeros(3,1)
raw_orth_lam0 = sp.simplify(raw_orth.subs(z, sp.solve(sp.Eq(lam, 0), z)[0]))
assert raw_orth_lam0 == sp.zeros(3,1)

# Exact rational controls for all three branches.
p0=V(2,0,0); a0=V(0,0,1)
# Generic invertible branch: a.q !=0 and |q| != |p|.
q0=V(1,1,1)
assert a0.dot(q0)!=0 and q0.dot(q0)!=p0.dot(p0)
# Equal-shell kernel branch.
qe=V(0,0,2)
be=V(1,0,0)
assert qe.dot(qe)==p0.dot(p0) and a0.dot(qe)!=0 and qe.dot(be)==0
assert B(p0,qe,a0,be)==sp.zeros(3,1)
# Polarization-orthogonality branch.
qo=V(1,1,0); bo=p0.cross(qo)
assert a0.dot(qo)==0 and bo!=sp.zeros(3,1) and qo.dot(bo)==0
assert B(p0,qo,a0,bo)==sp.zeros(3,1)

print("NS P2 general anchor-cross nullity: PASS")
print("det L ~ (a.q)^2 (|q|^2-|p|^2) / |p+q|^2")
print("kernel iff polarization-orthogonality or equal-shell, for k!=0")
