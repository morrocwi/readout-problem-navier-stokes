#!/usr/bin/env python3
"""Exact antipodal cancellation ladder for the NS P2 OCSR/cancellation branch.

The family reuses one antipodal reality-coupled mode pair ±p and a strip of
q_j modes. Interior exact cancellations force equal source coefficients, so
any finite productive strip has nonzero boundary descendants; a bi-infinite
strip escapes to unbounded wavevector magnitude.
"""

import sympy as sp

K, P, c, z, J = sp.symbols("K P c z J", nonzero=True, real=True)


def proj(v, k):
    return sp.simplify(v - (v.dot(k) / k.dot(k)) * k)


def B(p, q, a, b):
    k = p + q
    return sp.simplify(proj((a.dot(q)) * b + (b.dot(p)) * a, k))


p = sp.Matrix([0, P, 0])
pm = -p
a = sp.Matrix([0, 0, 1])

qJ = sp.Matrix([K, (2 * J + 1) * P, 0])
bJ = sp.Matrix([-(2 * J + 1) * P * c / K, c, z])

assert sp.simplify(qJ.dot(bJ)) == 0

up = B(p, qJ, a, bJ)
down = B(pm, qJ, a, bJ)
assert sp.simplify(up - sp.Matrix([0, 0, P * c])) == sp.zeros(3, 1)
assert sp.simplify(down + sp.Matrix([0, 0, P * c])) == sp.zeros(3, 1)

s_up = p + qJ
s_down = pm + qJ
assert sp.simplify(s_up - sp.Matrix([K, (2 * J + 2) * P, 0])) == sp.zeros(3, 1)
assert sp.simplify(s_down - sp.Matrix([K, 2 * J * P, 0])) == sp.zeros(3, 1)

# Interior target s_j receives +P c_{j-1} from p+q_{j-1} and -P c_j
# from -p+q_j. Exact cancellation therefore forces c_j=c_{j-1}.
c_prev, c_now = sp.symbols("c_prev c_now", real=True)
interior = sp.Matrix([0, 0, P * (c_prev - c_now)])
assert sp.solve([sp.expand(interior[2])], [c_now], dict=True) == [{c_now: c_prev}]

# On a finite strip j=m..n with productive constant c != 0, the two edge
# targets have single-source descendants ±P c e3 and cannot vanish without
# recruiting additional q modes outside the strip.
edge_low = sp.Matrix([0, 0, -P * c])
edge_high = sp.Matrix([0, 0, P * c])
assert edge_low != sp.zeros(3, 1)
assert edge_high != sp.zeros(3, 1)

# q_j scale is unbounded for |j| -> infinity when P != 0.
qnorm2 = sp.expand(qJ.dot(qJ))
assert sp.simplify(qnorm2 - (K**2 + (2 * J + 1)**2 * P**2)) == 0

print("NS P2 antipodal cancellation ladder: PASS")
print("B(p,q_j)=+P c_j e3; B(-p,q_j)=-P c_j e3")
print("interior cancellation => c_j=c_{j-1}")
print("finite productive strip => two nonzero boundary descendants")
print("bi-infinite productive strip => |q_j| unbounded, hence scale escape")
