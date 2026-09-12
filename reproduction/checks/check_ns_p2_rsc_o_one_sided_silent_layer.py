#!/usr/bin/env python3
"""Exact symbolic audit for PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01.

Scope (exact, local):
  Under one-sided O_+ persistence every recruit (q_j, b_j) satisfies q_j in a_+^perp
  and [b_j] = [a_+] (ALT-1 of NS_P2_RSC_O_ALTERNATION_TRANSFER.md, PR #63).  Hence for
  all i, j:  b_i . q_j = b_j . q_i = 0, and therefore

        B_{q_i,q_j}(b_i,b_j) = P_{q_i+q_j}[ (b_i . q_j) b_j + (b_j . q_i) b_i ] = 0.

  The recruit layer has no recruit-recruit quadratic productivity: it is a 2D3C-like
  passive layer with respect to internal recruit-recruit interactions.  This is NOT a
  full 2D3C branch: interactions with the O_- anchor / core may stay active.

This checker certifies only that algebra.  It proves nothing about global RSC-O,
RSC-E / RSC-C, OCSR, Witness Soundness, G6/G7 or Clay Navier-Stokes regularity.

Bilinear form: B(p,q,a,b) = P_{p+q}[(a.q) b + (b.p) a], the same operator as
check_ns_p2_multisource_cancellation.py and check_ns_p2_m3_suppression_labels.py.
All arithmetic is exact (sympy); no floats in any decision.
"""

import sympy as sp


def V(*xs):
    return sp.Matrix([sp.nsimplify(x) for x in xs])


def proj(v, k):
    return v - (v.dot(k) / k.dot(k)) * k


def B(p, q, a, b):
    return proj((a.dot(q)) * b + (b.dot(p)) * a, p + q)


def is_zero(v):
    return all(sp.expand(sp.simplify(x)) == 0 for x in v)


# ---------------------------------------------------------------------------
# 1. Symbolic proof: generic anchor polarization n = a_+, two recruits q, r in n^perp
#    parametrised by a basis of n^perp, recruited polarizations b = s n, d = t n.
# ---------------------------------------------------------------------------
n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)
x1, x2, y1, y2, s, t = sp.symbols('x1 x2 y1 y2 s t', real=True)

n = sp.Matrix([n1, n2, n3])
# Two vectors spanning n^perp for generic n (both exactly orthogonal to n).
v1 = sp.Matrix([n2, -n1, 0])
v2 = sp.Matrix([n1 * n3, n2 * n3, -(n1**2 + n2**2)])
assert sp.expand(n.dot(v1)) == 0
assert sp.expand(n.dot(v2)) == 0
assert sp.expand(v1.dot(v2)) == 0            # v1, v2 orthogonal: a genuine basis of n^perp when n2 != 0 or n1 != 0

q = x1 * v1 + x2 * v2                          # recruit wavevectors in a_+^perp
r = y1 * v1 + y2 * v2
b = s * n                                      # recruited polarizations on the line [a_+]  (ALT-1)
d = t * n

assert sp.expand(n.dot(q)) == 0
assert sp.expand(n.dot(r)) == 0
assert sp.expand(b.dot(q)) == 0                # transversality of the recruits
assert sp.expand(d.dot(r)) == 0

# The two scalar coefficients of the unprojected source vanish identically.
assert sp.expand(b.dot(r)) == 0
assert sp.expand(d.dot(q)) == 0

# The projected recruit-recruit interaction is identically zero, componentwise, before
# projection and after it (the projection is well defined whenever q + r != 0).
raw = sp.expand((b.dot(r)) * d + (d.dot(q)) * b)
assert is_zero(raw)
k = q + r
B_sym = ((b.dot(r)) * d + (d.dot(q)) * b) - ((((b.dot(r)) * d + (d.dot(q)) * b).dot(k)) / k.dot(k)) * k
assert is_zero(B_sym)

# Symmetry: the same holds with the roles of (q,b) and (r,d) exchanged (B is symmetric).
assert is_zero(sp.expand((d.dot(q)) * b + (b.dot(r)) * d))

# ---------------------------------------------------------------------------
# 2. Two explicit rational fixtures.
# ---------------------------------------------------------------------------
fixtures = [
    # (a_+, q, r, b, d)
    (V(0, 0, 1), V(1, 2, 0), V(-3, 1, 0), V(0, 0, 2), V(0, 0, -5)),
    (V(1, 2, 2), V(2, -1, 0), V(0, 1, -1), V(sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(2, 3)),
     V(-2, -4, -4)),
]
for ap, qq, rr, bb, dd in fixtures:
    assert ap.dot(qq) == 0 and ap.dot(rr) == 0          # recruits in a_+^perp
    assert bb.dot(qq) == 0 and dd.dot(rr) == 0          # transversal
    assert bb.cross(ap) == sp.zeros(3, 1) and dd.cross(ap) == sp.zeros(3, 1)   # [b]=[d]=[a_+]
    assert (qq + rr) != sp.zeros(3, 1)
    assert bb.dot(rr) == 0 and dd.dot(qq) == 0
    g = sp.simplify(B(qq, rr, bb, dd))
    assert g == sp.zeros(3, 1), g
    g_swap = sp.simplify(B(rr, qq, dd, bb))
    assert g_swap == sp.zeros(3, 1), g_swap

# ---------------------------------------------------------------------------
# 3. Non-vacuity control: one recruit polarization NOT parallel to a_+ gives a nonzero
#    recruit-recruit interaction on the same wavevectors.
# ---------------------------------------------------------------------------
ap, qq, rr, bb, _ = fixtures[0]
d_ctrl = V(1, 3, 0)                                     # in r^perp (r = (-3,1,0)) but off the line [a_+]
assert d_ctrl.dot(rr) == 0
assert d_ctrl.cross(ap) != sp.zeros(3, 1)
g_ctrl = sp.simplify(B(qq, rr, bb, d_ctrl))
assert g_ctrl != sp.zeros(3, 1), g_ctrl
assert sp.simplify(g_ctrl.dot(g_ctrl)) > 0

# Second control on the symbolic family: a generic d = t n + w with w in r^perp cap n^perp
# (w != 0) makes d . q generically nonzero, so the source is generically nonzero.
w1 = sp.symbols('w1', real=True)
w = w1 * n.cross(r)                                     # in n^perp and r^perp
assert sp.expand(w.dot(r)) == 0 and sp.expand(w.dot(n)) == 0
d_gen = t * n + w
coef = sp.expand(d_gen.dot(q))                          # = w1 * (n x r) . q, generically nonzero
assert coef != 0
assert sp.expand(coef.subs({x1: 1, x2: 0, y1: 0, y2: 1, w1: 1, n1: 1, n2: 2, n3: 3})) != 0

print('NS P2 RSC-O one-sided silent layer audit: PASS')
print('one-sided O_+ persistence + ALT-1: b_i.q_j = b_j.q_i = 0 for all recruits i, j')
print('recruit-recruit interaction B_{q_i,q_j}(b_i,b_j) == 0 identically (symbolic + 2 rational fixtures)')
print('control: a recruit polarization off the line [a_+] makes the interaction nonzero')
print('2D3C-like passive layer w.r.t. internal recruit-recruit interactions only; layer/core interface NOT silenced')
print('global RSC-O / RSC-E / RSC-C / OCSR / WS / G6/G7 / Clay remain OPEN')
