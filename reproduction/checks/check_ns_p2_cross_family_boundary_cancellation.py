#!/usr/bin/env python3
"""Exact symbolic audit for cross-family cancellation at an antipodal-strip boundary.

Reuses the existing symmetric projected NSE interaction.  All PASS decisions are
exact SymPy identities; no floating arithmetic is used.

Claim proved only for the declared anchor geometry:
    p = (0,P,0), a = e3,
    s = (K,L,0),
with an external cancelling triad r+t=s.

If the external pair is genuinely 3D (r_z != 0), then a nonzero parent source
parallel to e3 cannot have both anchor-cross interactions B_{p,r}(a,u) and
B_{p,t}(a,v) vanish.  Hence full convolution creates at least one off-plane
cross descendant.  If r_z = 0, the recruited triad is planar.
"""

import sympy as sp

P, K, L, x, y, z = sp.symbols("P K L x y z", real=True)


def V(*xs):
    return sp.Matrix(xs)


def proj(w, k):
    return sp.simplify(w - (w.dot(k) / k.dot(k)) * k)


def B(p, q, a, b):
    k = p + q
    return sp.simplify(proj((a.dot(q)) * b + (b.dot(p)) * a, k))


# Anchor / boundary geometry.
p = V(0, P, 0)
a = V(0, 0, 1)
s = V(K, L, 0)
r = V(x, y, z)
t = sp.simplify(s - r)

# ---------------------------------------------------------------------------
# 1. Exact transverse-map determinant for u -> B_{p,r}(a,u), z != 0.
# ---------------------------------------------------------------------------
# Bases of r^perp and (p+r)^perp whose first two coordinates are the identity.
# They are valid on the branch z != 0.
u1 = V(1, 0, -x / z)
u2 = V(0, 1, -y / z)
assert sp.simplify(r.dot(u1)) == 0
assert sp.simplify(r.dot(u2)) == 0

Br1 = B(p, r, a, u1)
Br2 = B(p, r, a, u2)
Mr = sp.Matrix([
    [sp.simplify(Br1[0]), sp.simplify(Br2[0])],
    [sp.simplify(Br1[1]), sp.simplify(Br2[1])],
])

det_r = sp.factor(Mr.det())
expected_r = sp.factor(z**2 * (r.dot(r) - p.dot(p)) / (p + r).dot(p + r))
assert sp.simplify(det_r - expected_r) == 0

# Same identity for t=s-r.  Since t_z=-z, the square is again z^2.
tx, ty, tz = t
v1 = V(1, 0, -tx / tz)
v2 = V(0, 1, -ty / tz)
assert sp.simplify(t.dot(v1)) == 0
assert sp.simplify(t.dot(v2)) == 0

Bt1 = B(p, t, a, v1)
Bt2 = B(p, t, a, v2)
Mt = sp.Matrix([
    [sp.simplify(Bt1[0]), sp.simplify(Bt2[0])],
    [sp.simplify(Bt1[1]), sp.simplify(Bt2[1])],
])

det_t = sp.factor(Mt.det())
expected_t = sp.factor(z**2 * (t.dot(t) - p.dot(p)) / (p + t).dot(p + t))
assert sp.simplify(det_t - expected_t) == 0

# Therefore, on z != 0, an anchor-cross map can have a nonzero kernel only
# on the equal-shell locus |r|=|p| (respectively |t|=|p|).

# ---------------------------------------------------------------------------
# 2. Equal-shell escape is incompatible with an e3-directed parent source
#    on a genuinely 3D pair.
# ---------------------------------------------------------------------------
# If both anchor-cross interactions vanished for nonzero source polarizations,
# the determinant identities force |r|=|t|=|p|.  Existing equal-shell
# direction lock then makes B_{r,t} parallel to r x t.  But for s=r+t in the
# xy-plane, the horizontal part of r x t has exact squared norm
# z^2 (K^2 + L^2), so it cannot be parallel to e3 when z != 0 and s != 0.
rt_cross = sp.simplify(r.cross(t))
assert sp.simplify(rt_cross - V(-L * z, K * z, -K * y + L * x)) == sp.zeros(3, 1)
xy_cross_sq = sp.factor(rt_cross[0] ** 2 + rt_cross[1] ** 2)
assert sp.simplify(xy_cross_sq - z**2 * (K**2 + L**2)) == 0

# ---------------------------------------------------------------------------
# 3. Off-plane novelty: on z != 0, the two anchor-cross targets have z
#    coordinates +z and -z, so any nonzero cross interaction lands outside
#    the original planar strip.
# ---------------------------------------------------------------------------
assert sp.simplify((p + r)[2] - z) == 0
assert sp.simplify((p + t)[2] + z) == 0

# ---------------------------------------------------------------------------
# 4. Exact rational non-vacuity control.
# ---------------------------------------------------------------------------
# Boundary target s=(1,2,0), genuinely 3D external pair r+t=s, and exact
# polarizations with B_{r,t}=-e3.  Both anchor-cross descendants are nonzero.
p0 = V(0, 1, 0)
a0 = V(0, 0, 1)
r0 = V(1, 0, 1)
t0 = V(0, 2, -1)
u0 = V(0, 1, 0)
v0 = V(sp.Rational(-1, 3), sp.Rational(-1, 4), sp.Rational(-1, 2))

assert r0 + t0 == V(1, 2, 0)
assert r0.dot(u0) == 0
assert t0.dot(v0) == 0
assert B(r0, t0, u0, v0) == V(0, 0, -1)
assert B(p0, r0, a0, u0) != sp.zeros(3, 1)
assert B(p0, t0, a0, v0) != sp.zeros(3, 1)
assert (p0 + r0)[2] != 0 and (p0 + t0)[2] != 0

print("NS P2 cross-family boundary cancellation audit: PASS")
print("det_r = z^2 (|r|^2-|p|^2)/|p+r|^2")
print("det_t = z^2 (|t|^2-|p|^2)/|p+t|^2")
print("equal-shell + e3 parent direction + z!=0 is impossible by direction lock")
print("therefore a genuinely 3D external canceller forces off-plane cross novelty")
