#!/usr/bin/env python3
"""Exact checker: Type-P (projective polarization/lineage) loop transport is shell-confined,
and explicit equal-shell loop monodromies (identity and two-fixed-line) are reproduced.

Reuses Standalone Sections 114.1-114.2: each zero-cross interaction k1 -> k2 defines the
partial projective transport

    T_e([a]) = [b],   b in k2^perp,   B_{k1,k2}(a,b) = 0,
    B_{p,q}(a,b) = P_{p+q}[ (a.q) b + (b.p) a ],

which is single-valued exactly when the kernel of b |-> B_{k1,k2}(a,b) on k2^perp is a line.

By the general anchor-cross nullity theorem (PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01,
p=k1, q=k2, anchor a in k1^perp) that kernel is nontrivial iff a.k2 = 0 or |k1| = |k2|.
Hence:

  * on an unequal-shell edge the transport is undefined for every class except the single
    class [k1 x k2], which is sent to [k1 x k2];
  * on an equal-shell edge the transport is defined on the whole fiber and is a projective
    map P(k1^perp) -> P(k2^perp), represented by an exact 2x2 rational matrix.

The loop monodromy M in PGL(2,Q) of a closed equal-shell integer cycle is then computed and
its real fixed projective lines counted (ALL when M ~ I; the three-line rigidity dichotomy of
PROP-P3-PROJECTIVE-THREE-LINE-RIGIDITY-01 applied to concrete loops).

All fixtures are explicit and deterministic; no random sampling.
"""

import sympy as sp


def proj(v, k):
    return v - (v.dot(k) / k.dot(k)) * k


def B(p, q, a, b):
    return proj((a.dot(q)) * b + (b.dot(p)) * a, p + q)


def perp_basis(k):
    """Exact rational basis (u, v) of k^perp."""
    k = sp.Matrix(k)
    e = sp.Matrix([1, 0, 0]) if (k[0] == 0 and k[1] == 0) else sp.Matrix([0, 0, 1])
    u = k.cross(e)
    v = k.cross(u)
    return [u, v]


def cross_matrix(k1, k2, a):
    """Exact 2x2 matrix of b |-> B_{k1,k2}(a,b) from perp_basis(k2) to perp_basis(k1+k2)."""
    k1 = sp.Matrix(k1)
    k2 = sp.Matrix(k2)
    U2 = perp_basis(k2)
    Uk = perp_basis(k1 + k2)
    cols = []
    for b in U2:
        w = B(k1, k2, a, b)
        # coordinates of w in the (orthogonal) basis Uk of (k1+k2)^perp
        cols.append(sp.Matrix([w.dot(Uk[0]) / Uk[0].dot(Uk[0]), w.dot(Uk[1]) / Uk[1].dot(Uk[1])]))
    return sp.Matrix.hstack(*cols)


def zero_cross_kernel(k1, k2, a):
    """Kernel of b |-> B_{k1,k2}(a,b) on k2^perp as a list of basis vectors (exact)."""
    k1 = sp.Matrix(k1)
    k2 = sp.Matrix(k2)
    U2 = perp_basis(k2)
    s, t = sp.symbols('s t')
    b = s * U2[0] + t * U2[1]
    eqs = [sp.expand(c) for c in B(k1, k2, a, b)]
    lin = sp.linsolve(eqs, [s, t])
    if lin == sp.EmptySet:
        return []
    (sv, tv), = lin
    free = sorted(sv.free_symbols | tv.free_symbols, key=str)
    return [sv.coeff(f) * U2[0] + tv.coeff(f) * U2[1] for f in free]


def T_matrix(k1, k2):
    """Exact 2x2 matrix of T_e in perp bases, or None if not single-valued on the whole fiber."""
    U1 = perp_basis(k1)
    U2 = perp_basis(k2)
    s, t = sp.symbols('s t')
    cols = []
    for a in U1:
        b = s * U2[0] + t * U2[1]
        eqs = [sp.expand(c) for c in B(sp.Matrix(k1), sp.Matrix(k2), a, b)]
        lin = sp.linsolve(eqs, [s, t])
        if lin == sp.EmptySet:
            return None
        (sv, tv), = lin
        free = sv.free_symbols | tv.free_symbols
        if len(free) != 1:
            return None
        f = free.pop()
        cols.append(sp.Matrix([sv.coeff(f), tv.coeff(f)]))
    return sp.Matrix.hstack(*cols)


def fixed_lines(M):
    """'ALL' if M ~ I in PGL(2), else the number of distinct real fixed lines in P^1."""
    if M[0, 1] == 0 and M[1, 0] == 0 and M[0, 0] == M[1, 1]:
        return 'ALL'
    x = sp.symbols('x')
    poly = sp.expand(M[1, 0] + M[1, 1] * x - x * (M[0, 0] + M[0, 1] * x))
    roots = [r for r in sp.roots(sp.Poly(poly, x), multiple=True) if r.is_real]
    return len(set(roots)) + (1 if M[0, 1] == 0 else 0)


def loop_transport(cycle):
    M = sp.eye(2)
    for i in range(len(cycle)):
        T = T_matrix(cycle[i], cycle[(i + 1) % len(cycle)])
        assert T is not None, f'edge {cycle[i]}->{cycle[(i + 1) % len(cycle)]} not single-valued'
        M = T * M
    return M


def parallel(u, v):
    return sp.Matrix(u).cross(sp.Matrix(v)) == sp.zeros(3, 1)


# ---------------------------------------------------------------------------
# 1. Shell confinement: on unequal-shell edges the zero-cross transport is undefined
#    off the single class [k1 x k2]; that class is sent to [k1 x k2].
# ---------------------------------------------------------------------------
alpha, beta = sp.symbols('alpha beta', real=True)
unequal_edges = [
    ([1, 0, 0], [0, 2, 0]),      # |k1|^2=1, |k2|^2=4
    ([1, 1, 0], [0, 1, 2]),      # |k1|^2=2, |k2|^2=5
    ([2, -1, 1], [1, 2, 2]),     # |k1|^2=6, |k2|^2=9
]
for k1, k2 in unequal_edges:
    K1, K2 = sp.Matrix(k1), sp.Matrix(k2)
    assert K1.dot(K1) != K2.dot(K2)
    U1 = perp_basis(k1)
    a = alpha * U1[0] + beta * U1[1]          # generic class in P(k1^perp)
    det = sp.factor(cross_matrix(k1, k2, a).det())
    lam = sp.expand(a.dot(K2))
    ratio = sp.simplify(det / lam**2)
    # det vanishes exactly on the locus a.k2 = 0 (double), with a nonzero constant cofactor
    assert ratio.free_symbols == set() and ratio != 0, (k1, k2, det)
    # explicit generic classes: kernel trivial, transport undefined
    for a0 in (U1[0], U1[1], U1[0] + U1[1]):
        if a0.dot(K2) != 0:
            assert zero_cross_kernel(k1, k2, a0) == [], (k1, k2, a0)
    # the exceptional class [k1 x k2] has a one-dimensional kernel spanned by k1 x k2
    n = K1.cross(K2)
    ker = zero_cross_kernel(k1, k2, n)
    assert len(ker) == 1 and parallel(ker[0], n), (k1, k2, ker)
    assert T_matrix(k1, k2) is None
print('shell confinement: 3 unequal-shell edges, transport undefined off [k1 x k2]  PASS')

# Equal-shell control: transport defined on the whole fiber (kernel is a line for every basis class).
equal_edges = [([1, 0, 0], [0, 1, 0]), ([1, 2, 0], [0, 1, 2]), ([2, -2, 1], [2, -2, -1])]
for k1, k2 in equal_edges:
    K1, K2 = sp.Matrix(k1), sp.Matrix(k2)
    assert K1.dot(K1) == K2.dot(K2)
    U1 = perp_basis(k1)
    a = alpha * U1[0] + beta * U1[1]
    assert sp.expand(cross_matrix(k1, k2, a).det()) == 0
    assert T_matrix(k1, k2) is not None
print('equal-shell control: 3 edges, transport single-valued on the whole fiber  PASS')

# ---------------------------------------------------------------------------
# 2. Identity-monodromy loop fixtures (branch B witnesses; not counterexamples to anything).
# ---------------------------------------------------------------------------
identity_loops = {
    'shell-9 rectangle': [[2, -2, 1], [2, -2, -1], [-2, -2, 1], [-2, -2, -1]],
    'shell-5 planar 3-cycle (z=0)': [[-1, -2, 0], [-2, 1, 0], [2, 1, 0]],
}
for name, cyc in identity_loops.items():
    shells = {sum(x * x for x in k) for k in cyc}
    assert len(shells) == 1
    M = loop_transport(cyc)
    assert M == sp.eye(2), (name, M)
    assert fixed_lines(M) == 'ALL'
    print(f'identity monodromy: {name} {cyc}  M = I  PASS')
assert all(k[2] == 0 for k in identity_loops['shell-5 planar 3-cycle (z=0)'])

# ---------------------------------------------------------------------------
# 3. Nonidentity monodromy with exactly two real fixed lines (three-line rigidity, branch A).
# ---------------------------------------------------------------------------
two_line_loops = {
    'shell-5 3-cycle': ([[1, 0, 2], [-2, 1, 0], [-1, 2, 0]], sp.Matrix([[1, 1], [sp.Rational(5, 2), -2]])),
    'shell-6 3-cycle': ([[1, 2, -1], [-2, 1, 1], [-1, -1, 2]], sp.Matrix([[7, -3], [-1, 4]])),
}
for name, (cyc, M_expected) in two_line_loops.items():
    assert len({sum(x * x for x in k) for k in cyc}) == 1
    M = loop_transport(cyc)
    assert M == M_expected, (name, M)
    assert not (M[0, 1] == 0 and M[1, 0] == 0 and M[0, 0] == M[1, 1])
    assert fixed_lines(M) == 2, (name, fixed_lines(M))
    print(f'nonidentity monodromy: {name} {cyc}  M = {M.tolist()}  two real fixed lines  PASS')

# Zero-real-fixed-line control (elliptic type), also from the equal-shell sample.
cyc0 = [[1, 0, -2], [-2, 1, 0], [0, -1, 2]]
M0 = loop_transport(cyc0)
assert M0 == sp.Matrix([[1, 1], [-sp.Rational(5, 2), 2]])
assert fixed_lines(M0) == 0
print(f'nonidentity monodromy: shell-5 3-cycle {cyc0}  M = {M0.tolist()}  zero real fixed lines  PASS')

print('NS P2 Type-P loop transport shell confinement + identity/two-line loop fixtures: PASS')
