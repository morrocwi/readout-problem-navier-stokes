#!/usr/bin/env python3
"""Exact symbolic audit for PROP-P3-RSC-O-ALTERNATION-TRANSFER-01.

This checker certifies only the local algebra used by the proposal:
1) a nonparallel O-suppressed recruit copies the anchor polarization line;
2) for two genuine alternating single-O recruits on distinct fixed lines,
   exact nullity of their mutual cross interaction forces equal shell.

It does not prove global RSC-O, OCSR, Witness Soundness, G6/G7 or Clay.
"""

import sympy as sp


def V(*xs):
    return sp.Matrix(xs)

# ---------------------------------------------------------------------------
# 1. Single-O polarization-line copy in an adapted chart.
# ---------------------------------------------------------------------------
# Put the anchor polarization on e3.  Since a.p=a.q=0, both p and q lie in
# the xy-plane.  If p x q != 0 then their common orthogonal complement is e3.
P1, P2, Q1, Q2 = sp.symbols('P1 P2 Q1 Q2', real=True)
a = V(0, 0, 1)
p = V(P1, P2, 0)
q = V(Q1, Q2, 0)
D = sp.expand(P1*Q2 - P2*Q1)
assert sp.simplify(p.cross(q) - V(0, 0, D)) == sp.zeros(3, 1)
assert a.dot(p) == 0
assert a.dot(q) == 0

# On the O branch a.q=0, the projected interaction is (b.p) a because a is
# also perpendicular to k=p+q.  Exact suppression therefore imposes b.p=0;
# together with b.q=0 and D!=0 this places b on span(e3)=span(a).
# The checker records the exact common-normal direction.

# ---------------------------------------------------------------------------
# 2. Alternating genuine single-O pair.
# ---------------------------------------------------------------------------
# Choose a_+=e1 and a_-=(c,s,0), with s != 0 so the two projective lines are
# distinct.  Parameterize q perpendicular to a_+ but not a_-, and r
# perpendicular to a_- but not a_+.
c, s, R, Rz, Qy, Qz = sp.symbols(
    'c s R Rz Qy Qz', nonzero=True, real=True
)
ap = V(1, 0, 0)
am = V(c, s, 0)
q = V(0, Qy, Qz)
r = V(s*R, -c*R, Rz)

assert ap.dot(q) == 0
assert sp.expand(am.dot(r)) == 0
assert sp.expand(am.dot(q)) == Qy*s       # genuine: nonzero
assert sp.expand(ap.dot(r)) == R*s         # genuine: nonzero

# By the single-O copy lemma, the recruited polarizations are projectively
# ap and am.  Build the unprojected symmetric interaction source.
alpha = sp.expand(ap.dot(r))
beta = sp.expand(am.dot(q))
raw = sp.simplify(alpha*am + beta*ap)
k = sp.simplify(q + r)

assert sp.simplify(raw - V(s*(Qy + R*c), R*s**2, 0)) == sp.zeros(3, 1)

# The projected interaction vanishes iff raw is parallel to k, equivalently
# raw x k = 0.  Exact factorization:
cross = sp.simplify(raw.cross(k))
expected_cross = V(
    R*s**2*(Qz + Rz),
    -s*(Qy + R*c)*(Qz + Rz),
    s*(Qy**2 - R**2*(c**2 + s**2)),
)
assert sp.simplify(cross - expected_cross) == sp.zeros(3, 1)

# Since R,s are declared nonzero, cross=0 forces Qz+Rz=0 from component 1,
# and Qy^2=R^2(c^2+s^2) from component 3.  Those two identities are exactly
# |q|^2=|r|^2.
norm_diff = sp.expand(q.dot(q) - r.dot(r))
assert sp.expand(norm_diff - (
    Qy**2 + Qz**2 - R**2*(c**2+s**2) - Rz**2
)) == 0

# Substitute the two consequences of cross=0 and verify equal shell exactly.
forced_norm_diff = sp.expand(norm_diff.subs({Rz: -Qz, Qy**2: R**2*(c**2+s**2)}))
assert forced_norm_diff == 0

# Non-vacuity control: choose an unequal-shell genuine alternating pair and
# verify the cross interaction is nonzero.
control = {
    c: sp.Rational(1, 2),
    s: sp.Rational(3, 2),
    R: 1,
    Rz: 1,
    Qy: 2,
    Qz: 1,
}
control_cross = sp.simplify(cross.subs(control))
control_norm_diff = sp.simplify(norm_diff.subs(control))
assert control_norm_diff != 0
assert control_cross != sp.zeros(3, 1)

print('NS P2 RSC-O single-O alternation transfer audit: PASS')
print('single-O nonparallel suppression copies the anchor projective line')
print('genuine opposite-line alternation: cross-null => equal shell')
print('global RSC-O / RSC-E / RSC-C / OCSR / WS / G6/G7 / Clay remain OPEN')
