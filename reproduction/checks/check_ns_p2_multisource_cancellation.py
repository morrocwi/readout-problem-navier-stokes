#!/usr/bin/env python3
"""Exact fixtures for multi-source cancellation, equal-shell direction lock, and W3 generation-1 closure.

All arithmetic is exact (sympy over Q, Q(sqrt3), Q(i)); no floats enter any PASS decision.
"""

import itertools

import sympy as sp

R3 = sp.sqrt(3)


def proj(v, k):
    return v - (v.dot(k) / k.dot(k)) * k


def B(p, q, a, b):
    """Symmetric NSE triad interaction into k=p+q with a perp p, b perp q."""
    k = p + q
    return proj((a.dot(q)) * b + (b.dot(p)) * a, k)


def V(*xs):
    return sp.Matrix([sp.nsimplify(x) for x in xs])


def rank_of_image(p, q):
    """Rank of the bilinear map (a,b) -> B_{p,q}(a,b) over transverse bases at p and q."""
    def basis(m):
        cands = [V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]
        out = []
        for c in cands:
            w = c - (c.dot(m) / m.dot(m)) * m
            if w != sp.zeros(3, 1) and sp.Matrix.hstack(*(out + [w])).rank() == len(out) + 1:
                out.append(w)
            if len(out) == 2:
                break
        return out
    cols = [B(p, q, u, v) for u in basis(p) for v in basis(q)]
    return sp.Matrix.hstack(*cols).rank()


# ---------------------------------------------------------------------------
# 1. Section 14 / Section 113: equal source shells lock the interaction direction.
# ---------------------------------------------------------------------------
t, L = sp.symbols("t L", positive=True)
al, be, ga, de = sp.symbols("alpha beta gamma delta", real=True)
C, S = sp.cos(t), sp.sin(t)
p113 = sp.Matrix([L * C, L * S, 0])
r113 = sp.Matrix([L * C, -L * S, 0])
n = V(0, 0, 1)
t_p = sp.Matrix([-S, C, 0])
t_r = sp.Matrix([S, C, 0])
a113 = al * n + be * t_p
c113 = ga * n + de * t_r
B113 = B(p113, r113, a113, c113)
target113 = 2 * L * S * C * (al * de - be * ga) * n
assert sp.simplify(B113 - target113) == sp.zeros(3, 1)          # (113.1) exact, factor 1

# Exact rational instances: rank 1 iff |p| = |q| (given p not parallel q, k != 0).
assert rank_of_image(V(3, 4, 0), V(3, -4, 0)) == 1                # |p|=|q|=5, |k|=6
assert rank_of_image(V(3, 4, 0), V(0, 4, 3)) == 1                 # |p|=|q|=5, |k|^2=82 (3D)
assert rank_of_image(V(1, 0, 0), V(0, 2, 0)) == 2                 # |p|=1, |q|=2
assert rank_of_image(V(3, 4, 0), V(2, -4, 0)) == 2                # |p|=|k|=5, |q|^2=20
assert rank_of_image(V(1, 0, 0), V(0, 1, 1)) == 2                 # |p|=1, |q|^2=2, |k|^2=3

# ---------------------------------------------------------------------------
# 2. Witness W3: three equal-shell triads at k=(0,0,1) cancel exactly; N=2 cannot.
# ---------------------------------------------------------------------------
k3 = V(0, 0, 1)
thetas = [0, 2 * sp.pi / 3, 4 * sp.pi / 3]


def e_th(th):
    return sp.Matrix([-sp.sin(th), sp.cos(th), 0])


def p_th(th):
    return sp.Matrix([R3 / 2 * sp.cos(th), R3 / 2 * sp.sin(th), sp.Rational(1, 2)])


W3 = []
for th in thetas:
    p, e = p_th(th), e_th(th)
    q = k3 - p
    a, b = e, -(q.cross(e))
    assert sp.simplify(p.dot(p)) == 1 and sp.simplify(q.dot(q)) == 1
    assert sp.simplify(a.dot(p)) == 0 and sp.simplify(b.dot(q)) == 0
    g = sp.simplify(B(p, q, a, b))
    assert sp.simplify(g - (R3 / 2) * e) == sp.zeros(3, 1)
    W3.append((p, q, a, b, g, e))
assert sp.simplify(sum((w[4] for w in W3), sp.zeros(3, 1))) == sp.zeros(3, 1)
assert sp.Matrix.hstack(*[w[0] for w in W3]).rank() == 3          # genuinely 3D sources

# Direction lock symbolic in theta and free amplitudes (real and complex).
th = sp.symbols("theta", real=True)
A1, A2, B1, B2 = sp.symbols("A1 A2 B1 B2")
p, e = p_th(th), e_th(th)
q = k3 - p
a = A1 * e + A2 * p.cross(e)
b = B1 * e + B2 * q.cross(e)
g = B(p, q, a, b)
assert sp.simplify(g.cross(e)) == sp.zeros(3, 1) and sp.simplify(g[2]) == 0
Cexpr = sp.simplify(g.dot(e) / (R3 / 2))
assert sp.expand(Cexpr - (A2 * B1 - A1 * B2)) == 0 or sp.expand(Cexpr + (A2 * B1 - A1 * B2)) == 0

# N=2: two distinct equal-shell triads have independent locked directions.
e0, e1 = e_th(0), e_th(2 * sp.pi / 3)
assert sp.Matrix.hstack(e0, e1).rank() == 2

# Reality constraint is vacuous on W3 (no antipodal sources).
srcs = [w[0] for w in W3] + [w[1] for w in W3]
assert all(sp.simplify(u + v) != sp.zeros(3, 1) for u, v in itertools.combinations(srcs, 2))

# ---------------------------------------------------------------------------
# 3. Witness W1: two-shell N=2 exact cancellation at k=(1,0,0).
# ---------------------------------------------------------------------------
k1 = V(1, 0, 0)
W1 = [(V(1, 1, 0), V(0, -1, 0), V(-1, 1, -1), V(1, 0, 1)),
      (V(1, 0, 1), V(0, 0, -1), V(-1, 1, 1), V(2, 3, 0))]
gs1 = []
for p, q, a, b in W1:
    assert p + q == k1 and a.dot(p) == 0 and b.dot(q) == 0
    assert p.dot(p) != q.dot(q)                                    # not equal-shell
    raw = (a.dot(q)) * b + (b.dot(p)) * a
    assert raw != sp.zeros(3, 1)                                   # productive before projection
    gs1.append(B(p, q, a, b))
assert gs1[0] == V(0, 1, -2) and gs1[1] == V(0, -1, 2)
assert gs1[0] + gs1[1] == sp.zeros(3, 1)
assert sp.Matrix.hstack(*[x for pq in W1 for x in pq[:2]]).rank() == 3
assert sp.Matrix.hstack(*[x for pq in W1 for x in pq[2:]]).rank() == 3
srcs1 = [x for pq in W1 for x in pq[:2]]
assert all(u + v != sp.zeros(3, 1) for u, v in itertools.combinations(srcs1, 2))

# ---------------------------------------------------------------------------
# 4. Witness W2: rank-2 genericity at k=(1,1,1), N=3 real and complex.
# ---------------------------------------------------------------------------
k2 = V(1, 1, 1)
W2 = [(V(1, 0, 0), V(0, 66, -22), V(1, -1, 1)),
      (V(0, 1, 0), V(1, 0, 2), V(-2, 1, 2)),
      (V(0, 0, 1), V(3, 1, 0), V(-2, 2, 1))]
gs2 = []
for p, a, b in W2:
    q = k2 - p
    assert a.dot(p) == 0 and b.dot(q) == 0
    gs2.append(B(p, q, a, b))
assert sum(gs2, sp.zeros(3, 1)) == sp.zeros(3, 1)
assert sp.Matrix.hstack(*gs2).rank() == 2
assert all(g != sp.zeros(3, 1) for g in gs2)
# each single-source map a -> g (b fixed) is onto the 2D plane k-perp
for p, _, b in W2:
    q = k2 - p
    cols = []
    for c in [V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]:
        u = c - (c.dot(p) / p.dot(p)) * p
        if u != sp.zeros(3, 1):
            cols.append(B(p, q, u, b))
    assert sp.Matrix.hstack(*cols).rank() == 2
# complex-phase instance
I = sp.I
W2c = [(V(1, 0, 0), sp.Matrix([0, 69 + 10 * I, -24 - 3 * I]), V(1, -1, 1)),
       (V(0, 1, 0), sp.Matrix([1 + 2 * I, 0, 3 - I]), V(-2, 1, 2)),
       (V(0, 0, 1), sp.Matrix([I, 2, 0]), V(-2, 2, 1))]
tot = sp.zeros(3, 1)
for p, a, b in W2c:
    q = k2 - p
    assert sp.expand(a.dot(p)) == 0 and b.dot(q) == 0
    tot += B(p, q, a, b)
assert sp.expand(tot) == sp.zeros(3, 1)

# ---------------------------------------------------------------------------
# 5. W3 generation 1 through k: suppressing both outward descendants kills the parent.
# ---------------------------------------------------------------------------
c1, c2, lam, mu = sp.symbols("c1 c2 lambda mu")
c = sp.Matrix([c1, c2, 0])
for th_i in thetas:
    p, e = p_th(th_i), e_th(th_i)
    q = k3 - p
    s1, s2 = p + k3, q + k3
    assert sp.simplify(s1.dot(s1)) == 3 and sp.simplify(s2.dot(s2)) == 3
    a = A1 * e + A2 * p.cross(e)
    b = B1 * e + B2 * q.cross(e)
    D1 = sp.simplify(B(p, k3, a, c))
    D2 = sp.simplify(B(q, k3, b, c))
    assert sp.simplify(D1.cross(e)) == sp.zeros(3, 1) and sp.simplify(D2.cross(e)) == sp.zeros(3, 1)
    d1, d2 = sp.expand(D1.dot(e)), sp.expand(D2.dot(e))
    M1 = sp.Matrix([[d1.coeff(A1).coeff(c1), d1.coeff(A1).coeff(c2)],
                    [d1.coeff(A2).coeff(c1), d1.coeff(A2).coeff(c2)]])
    M2 = sp.Matrix([[d2.coeff(B1).coeff(c1), d2.coeff(B1).coeff(c2)],
                    [d2.coeff(B2).coeff(c1), d2.coeff(B2).coeff(c2)]])
    assert sp.simplify(M2 + M1) == sp.zeros(2, 2)
    assert sp.simplify(M1.det()) == sp.Rational(3, 4)
    w = M1 * sp.Matrix([c1, c2])
    subs = {A1: lam * w[1], A2: -lam * w[0], B1: mu * w[1], B2: -mu * w[0]}
    assert sp.simplify(d1.subs(subs)) == 0 and sp.simplify(d2.subs(subs)) == 0
    Cpar = (A2 * B1 - A1 * B2).subs(subs)
    assert sp.simplify(Cpar) == 0

# Six descendant targets are pairwise distinct (no multi-source structure through k).
desc = []
for th_i in thetas:
    p = p_th(th_i)
    desc += [sp.simplify(p + k3), sp.simplify((k3 - p) + k3)]
assert all(sp.simplify(u - v) != sp.zeros(3, 1) for u, v in itertools.combinations(desc, 2))

# ---------------------------------------------------------------------------
# 6. W3 full-convolution depth 1 with dead k-mode: not lossless.
# ---------------------------------------------------------------------------
modes = []
for p, q, a, b, _, _ in W3:
    modes += [(p, a), (-p, a), (q, b), (-q, b)]
assert len(modes) == 12
targets = {}
for (m1, u1), (m2, u2) in itertools.combinations(modes, 2):
    tvec = sp.simplify(m1 + m2)
    if tvec == sp.zeros(3, 1):
        continue
    f = sp.simplify(B(m1, m2, u1, u2))
    key = tuple(tvec)
    targets.setdefault(key, []).append((m1, m2, u1, u2, f))
assert sum(len(v) for v in targets.values()) == 60
assert len(targets) == 44
hist, nonzero, single = {}, 0, 0
for key, lst in targets.items():
    tvec = sp.Matrix(key)
    n2 = sp.simplify(tvec.dot(tvec))
    hist[n2] = hist.get(n2, 0) + 1
    F = sp.simplify(sum((x[4] for x in lst), sp.zeros(3, 1)))
    if n2 == 1:
        assert F == sp.zeros(3, 1)                                  # +-k exactly cancelled
    if n2 == sp.Rational(9, 4):
        for m1, m2, u1, u2, f in lst:                               # projection zeros
            raw = (u1.dot(m2)) * u2 + (u2.dot(m1)) * u1
            assert sp.simplify(raw.cross(tvec)) == sp.zeros(3, 1) and sp.simplify(raw) != sp.zeros(3, 1)
            assert f == sp.zeros(3, 1)
    if F != sp.zeros(3, 1):
        nonzero += 1
        if len(lst) == 1:
            single += 1
assert hist == {1: 2, sp.Rational(3, 4): 6, sp.Rational(7, 4): 12, sp.Rational(9, 4): 6, 3: 6, sp.Rational(13, 4): 12}
assert nonzero == 36 and single == 30

print("NS P2 multi-source cancellation / equal-shell lock / W3 generation-1 fixtures")
print("(113.1) exact: B_{p,r} = 2 L S C (alpha delta - beta gamma) n; rank 1 iff |p|=|q|")
print("W3: three equal-shell triads cancel exactly at k; N=2 equal-shell cannot; sources rank 3")
print("W1: two-shell N=2 exact cancellation g1=(0,1,-2), g2=(0,-1,2)")
print("W2: k=(1,1,1) system rank 2, real and complex exact cancellations")
print("W3 gen-1: both outward descendants null => parent determinant 0; six distinct targets")
print("W3 depth-1 full convolution: 44 targets, +-k cancelled, 36 nonzero, 30 single-source")
print("NS-P2 MULTISOURCE CANCELLATION PASS")
