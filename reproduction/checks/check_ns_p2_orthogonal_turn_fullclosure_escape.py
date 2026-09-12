#!/usr/bin/env python3
"""Exact symbolic audit for the orthogonal-turn full-closure escape geometry.

This upgrades Standalone vNext Section 11 from scratch algebra to an exact
symbolic checker for the wavevector geometry only.

Claim boundary:
- if a nonplanar zero-dispersion shared-mode patch remains zero-dispersion
  after adjoining the cross geometry q x r to both parent plane normals,
  then the first-generation survivor is the mutually orthogonal triple;
- for that survivor, the next full-convolution descendants s=p+q and t=p+r
  have a shared plane normal with strictly positive projective dispersion
  relative to each parent plane, provided all three scale parameters are
  nonzero.

The checker does not prove the corresponding NSE scalar channels are nonzero;
that remains routed through the existing coupling/cancellation/degeneracy
ledger.
"""

import sympy as sp

P, a, b, c, d, Q, R = sp.symbols('P a b c d Q R', nonzero=True, real=True)


def V(*xs):
    return sp.Matrix(xs)

# First zero-dispersion orthogonal turn.
p = V(P, 0, 0)
q = V(a, b, 0)
r = V(c, 0, d)

n1 = sp.simplify(p.cross(q))  # parent plane 1 normal
n2 = sp.simplify(p.cross(r))  # parent plane 2 normal
n3 = sp.simplify(q.cross(r))  # cross geometry normal

assert sp.simplify(n1.dot(n2)) == 0
assert sp.simplify(n1 - V(0, 0, P*b)) == sp.zeros(3, 1)
assert sp.simplify(n2 - V(0, -P*d, 0)) == sp.zeros(3, 1)
assert sp.simplify(n3 - V(b*d, -a*d, -b*c)) == sp.zeros(3, 1)

# Because b,d != 0, n3 cannot be parallel to n1 or n2: its x-coordinate bd
# is nonzero. Hence zero projective dispersion relative to n1 and n2 forces
# orthogonality to both. Those two orthogonality conditions are exactly c=0
# and a=0 respectively.
assert sp.factor(n3.dot(n1)) == -P*b**2*c
assert sp.factor(n3.dot(n2)) == P*a*d**2

# Exact survivor after imposing a=c=0.
p0 = V(P, 0, 0)
q0 = V(0, Q, 0)
r0 = V(0, 0, R)

s = p0 + q0
t = p0 + r0
nst = sp.simplify(s.cross(t))
assert sp.simplify(nst - V(Q*R, -P*R, -P*Q)) == sp.zeros(3, 1)

npq = p0.cross(q0)
npr = p0.cross(r0)
D = sp.expand(nst.dot(nst))
assert sp.expand(D - (Q**2*R**2 + P**2*R**2 + P**2*Q**2)) == 0

# Squared cosines with the two parent normals.
c2_pq = sp.factor((nst.dot(npq))**2 / (D * npq.dot(npq)))
c2_pr = sp.factor((nst.dot(npr))**2 / (D * npr.dot(npr)))
assert sp.simplify(c2_pq - P**2*Q**2 / D) == 0
assert sp.simplify(c2_pr - P**2*R**2 / D) == 0

# Algebraic positivity certificates: c^2 > 0 and 1-c^2 > 0 for nonzero
# P,Q,R because the omitted parts are sums of positive squares.
one_minus_pq = sp.factor(1 - c2_pq)
one_minus_pr = sp.factor(1 - c2_pr)
assert sp.simplify(one_minus_pq - (Q**2*R**2 + P**2*R**2)/D) == 0
assert sp.simplify(one_minus_pr - (Q**2*R**2 + P**2*Q**2)/D) == 0

mu_pq = sp.factor(4*c2_pq*(1-c2_pq))
mu_pr = sp.factor(4*c2_pr*(1-c2_pr))

print('NS P2 orthogonal-turn full-closure geometry audit: PASS')
print('first-generation zero-dispersion survivor requires a=c=0')
print('next normal = (Q R, -P R, -P Q)')
print('mu_pq =', mu_pq)
print('mu_pr =', mu_pr)
print('for nonzero P,Q,R both dispersions are strictly positive')
