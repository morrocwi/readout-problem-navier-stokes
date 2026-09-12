#!/usr/bin/env python3
"""Exact antipodal-source cancellation/outward-descendant family for NS P2."""

import sympy as sp

K, P, x, z, w = sp.symbols("K P x z w", nonzero=True, real=True)


def proj(v, k):
    return sp.simplify(v - (v.dot(k) / k.dot(k)) * k)


def B(p, q, a, b):
    k = p + q
    return sp.simplify(proj((a.dot(q)) * b + (b.dot(p)) * a, k))


k = sp.Matrix([K, 0, 0])
p = sp.Matrix([0, P, 0])
pm = -p
q = k - p
qp = k + p

a = sp.Matrix([0, 0, 1])
b = sp.Matrix([P * x, K * x, z])
d = sp.Matrix([-P * x, K * x, w])

assert sp.simplify(p.dot(a)) == 0
assert sp.simplify(pm.dot(a)) == 0
assert sp.simplify(q.dot(b)) == 0
assert sp.simplify(qp.dot(d)) == 0

g1 = B(p, q, a, b)
g2 = B(pm, qp, a, d)
assert sp.simplify(g1 - sp.Matrix([0, 0, K * P * x])) == sp.zeros(3, 1)
assert sp.simplify(g2 + sp.Matrix([0, 0, K * P * x])) == sp.zeros(3, 1)
assert sp.simplify(g1 + g2) == sp.zeros(3, 1)

splus = p + qp
sminus = pm + q
hplus = B(p, qp, a, d)
hminus = B(pm, q, a, b)

assert sp.simplify(splus - sp.Matrix([K, 2 * P, 0])) == sp.zeros(3, 1)
assert sp.simplify(sminus - sp.Matrix([K, -2 * P, 0])) == sp.zeros(3, 1)
assert sp.simplify(hplus - sp.Matrix([0, 0, K * P * x])) == sp.zeros(3, 1)
assert sp.simplify(hminus + sp.Matrix([0, 0, K * P * x])) == sp.zeros(3, 1)

s2 = sp.expand(splus.dot(splus))
q2 = sp.expand(q.dot(q))
p2 = sp.expand(p.dot(p))
k2 = sp.expand(k.dot(k))
assert sp.simplify(s2 - q2 - 3 * P**2) == 0
assert sp.simplify(s2 - p2 - (K**2 + 3 * P**2)) == 0
assert sp.simplify(s2 - k2 - 4 * P**2) == 0

print("NS P2 antipodal cancellation/outward family: PASS")
print("parent: +KP x e3 and -KP x e3 cancel exactly at k")
print("cross descendants: +KP x e3 at (K,2P,0), -KP x e3 at (K,-2P,0)")
print("productive x != 0 => both outward descendants nonzero")
