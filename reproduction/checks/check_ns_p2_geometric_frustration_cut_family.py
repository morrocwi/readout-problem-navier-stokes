#!/usr/bin/env python3
"""Exact symbolic geometric frustration-or-cut family for the P2 NSE attack.

For positive integers a,b,c take

  p=(0,0,a), q=(b,-b,c), k=(b,-b,a+c), p+q=k,

and fix p in its e1 polarization.  Let q and k each use e1/e2, producing
the 2x2 channel rectangle

  A: q/e1 -> k/e1
  B: q/e2 -> k/e1
  C: q/e1 -> k/e2
  D: q/e2 -> k/e2.

The exact Fourier-Leray coefficients are derived in the repository's standard
unnormalised divergence-free basis.  Their product has sign exactly
sign(a^2-b^2-c^2).  Since the phase-incidence rows obey A-B-C+D=0, a negative
coefficient-sign product is equivalent to a pi target holonomy for the four
outward-saturation equations.

Thus:
  a^2 < b^2+c^2  -> exact phase frustration;
  a^2 = b^2+c^2  -> channel A is exactly zero (cut);
  a^2 > b^2+c^2  -> this rectangle is phase-compatible.

The checker also verifies the homogeneous-H3 dimensionless normalized channel
formulas.  On the phase-compatible branch, if c/a >= 1/2, elementary bounds in
the accompanying theorem note give

  |Gamma_i^inh| <= 6144*sqrt(2)*(b/a)/a^2.

If additionally a+c >= (2-eta)a with 0<=eta<=1/2, then
b/a <= sqrt(2 eta), hence

  |Gamma_i^inh| <= 12288*sqrt(eta)/a^2.

The inequality proof is analytic in the paper note; this script is the exact
symbolic identity/sign-factor checker and arithmetic audit for its constants.
"""
import sympy as sp


a, b, c = sp.symbols("a b c", positive=True, integer=True)
x, y = sp.symbols("x y", positive=True, real=True)


def basis(k):
    kv = sp.Matrix(k)
    for axis in (
        sp.Matrix((1, 0, 0)),
        sp.Matrix((0, 1, 0)),
        sp.Matrix((0, 0, 1)),
    ):
        e1 = kv.cross(axis)
        if any(sp.simplify(v) != 0 for v in e1):
            e2 = kv.cross(e1)
            return e1, e2, sp.factor(e1.dot(e1)), sp.factor(e2.dot(e2))
    raise AssertionError("zero wavevector not allowed")


def slot_vector(k, slot):
    e1, e2, _, _ = basis(k)
    return e1 if slot == "e1" else e2


def coupling(p, pslot, q, qslot, k, kslot):
    pv, qv, kv = sp.Matrix(p), sp.Matrix(q), sp.Matrix(k)
    assert all(sp.simplify((pv + qv - kv)[i]) == 0 for i in range(3))
    hp = slot_vector(p, pslot)
    hq = slot_vector(q, qslot)
    hk = slot_vector(k, kslot)
    return sp.factor(
        sp.simplify(
            (hp.dot(qv) * hk.dot(hq) + hq.dot(pv) * hk.dot(hp))
            / hk.dot(hk)
        )
    )


def h3_hom_weight(k, slot):
    e1, e2, n1, n2 = basis(k)
    physical = n1 if slot == "e1" else n2
    k2 = sp.factor(sp.Matrix(k).dot(sp.Matrix(k)))
    return sp.factor(physical * k2**3)


p = (0, 0, a)
q = (b, -b, c)
k = (b, -b, a + c)

A = coupling(p, "e1", q, "e1", k, "e1")
B = coupling(p, "e1", q, "e2", k, "e1")
C = coupling(p, "e1", q, "e1", k, "e2")
D = coupling(p, "e1", q, "e2", k, "e2")

D1 = a**2 + 2*a*c + b**2 + c**2
D2 = a**2 + 2*a*c + 2*b**2 + c**2
P = (
    a**2*b**2 + a**2*c**2 + 4*a*b**2*c + 2*a*c**3
    + 2*b**4 + 3*b**2*c**2 + c**4
)
EXPECTED = (
    a*b*(a**2-b**2-c**2)/D1,
    a**2*b*(a*c+b**2+c**2)/D1,
    -2*a**2*b**3/(D1*D2),
    -a*b*P/(D1*D2),
)

ROWS = (
    (1, 1, 0, -1, 0),
    (1, 0, 1, -1, 0),
    (1, 1, 0, 0, -1),
    (1, 0, 1, 0, -1),
)
RELATION = (1, -1, -1, 1)


def normalized_homogeneous(cc, qslot, kslot):
    wp = h3_hom_weight(p, "e1")
    wq = h3_hom_weight(q, qslot)
    wk = h3_hom_weight(k, kslot)
    return sp.factor(2*cc*sp.sqrt(wk)/sp.sqrt(wp*wq))


def main():
    got = (A, B, C, D)
    for g, e in zip(got, EXPECTED):
        assert sp.simplify(g-e) == 0, (g, e)

    product = sp.factor(A*B*C*D)
    expected_product = sp.factor(
        2*a**6*b**6*(a**2-b**2-c**2)*(a*c+b**2+c**2)*P
        /(D1**4*D2**2)
    )
    assert sp.simplify(product-expected_product) == 0

    # B>0, C<0, D<0 for positive a,b,c; therefore the product sign is
    # exactly sign(a^2-b^2-c^2).  A vanishes exactly on the geometric cut.
    assert sp.ask(sp.Q.positive(B))
    assert sp.ask(sp.Q.negative(C))
    assert sp.ask(sp.Q.negative(D))
    assert sp.simplify(A.subs(a**2, b**2+c**2)) == 0

    combined_row = tuple(
        sum(RELATION[i]*ROWS[i][j] for i in range(4))
        for j in range(5)
    )
    assert combined_row == (0, 0, 0, 0, 0)

    # Dimensionless homogeneous-H3 normalized coefficients: substitute
    # b=a*x, c=a*y and multiply by a^2.
    hom = (
        normalized_homogeneous(A, "e1", "e1"),
        normalized_homogeneous(B, "e2", "e1"),
        normalized_homogeneous(C, "e1", "e2"),
        normalized_homogeneous(D, "e2", "e2"),
    )
    dimensionless = tuple(sp.factor(g.subs({b:a*x, c:a*y})*a**2) for g in hom)

    r = x**2+y**2
    u = 2*x**2+y**2
    v = x**2+y**2+2*y+1
    w = 2*x**2+y**2+2*y+1
    pxy = 2*x**4+3*x**2*y**2+4*x**2*y+x**2+y**4+2*y**3+y**2
    expected_dim = (
        2*x*(1-r)*w**sp.Rational(3,2)/(sp.sqrt(r)*u**sp.Rational(3,2)*sp.sqrt(v)),
        2*x*(r+y)*w**sp.Rational(3,2)/(sp.sqrt(r)*u**2*sp.sqrt(v)),
        -4*x**3*w/(sp.sqrt(r)*u**sp.Rational(3,2)*sp.sqrt(v)),
        -2*x*w*pxy/(sp.sqrt(r)*u**2*sp.sqrt(v)),
    )
    for g, e in zip(dimensionless, expected_dim):
        assert sp.simplify(g-e) == 0, (g, e)

    # Arithmetic audit of the conservative analytic envelope used in the note
    # on y>=1/2 and x^2+y^2<=1.  The note proves:
    # r>=1/4, u>=1/4, v>=9/4, w<=4, x^2<=3/4, pxy<=14.
    component_bounds = (
        sp.Rational(512,3),
        sp.Rational(2048,3),
        sp.Integer(128),
        sp.Rational(7168,3),
    )
    assert all(bound <= 3072 for bound in component_bounds)
    inh_factor = 2*sp.sqrt(2)  # (1+|k|^2)^(3/2)/|k|^3 <= 2sqrt2
    envelope = sp.simplify(3072*inh_factor)
    assert envelope == 6144*sp.sqrt(2)
    near_dyadic = sp.simplify(envelope*sp.sqrt(2))
    assert near_dyadic == 12288

    print("NS P2 geometric frustration-or-cut family")
    print("coefficients:", [sp.factor(v) for v in got])
    print("coefficient product:", product)
    print("sign product = sign(a^2-b^2-c^2)")
    print("phase incidence relation: A - B - C + D = 0")
    print("a^2 < b^2+c^2 -> pi holonomy; equality -> exact channel cut")
    print("phase-compatible branch a^2 >= b^2+c^2: b/a <= sqrt(1-(c/a)^2)")
    print("if c/a>=1/2: |Gamma_i^inh| <= 6144*sqrt(2)*(b/a)/a^2")
    print("if a+c >= (2-eta)a, eta<=1/2: |Gamma_i^inh| <= 12288*sqrt(eta)/a^2")
    print("scope: one 3-parameter Fourier-Leray family; global boundary coverage remains OPEN")
    print("NS-P2 GEOMETRIC FRUSTRATION-CUT FAMILY PASS")


if __name__ == "__main__":
    main()
