#!/usr/bin/env python3
"""Exact all-n dyadic complex phase-holonomy witness.

For every positive integer n take the genuine high-high -> high Fourier triad

  p=(0,0,n), q=(n,-n,n), k=(n,-n,2n),  p+q=k,

so max-coordinate scale(p)=scale(q)=n and scale(k)=2n.

Using the same unnormalised real divergence-free basis convention as the other
P2 symbolic checkers, the four scalar polarization channels

  A: p/e1 + q/e1 -> k/e1
  B: p/e1 + q/e2 -> k/e1
  C: p/e1 + q/e1 -> k/e2
  D: p/e1 + q/e2 -> k/e2

have exact Fourier-Leray coefficients

  c_A = -n^2/5
  c_B = +3 n^3/5
  c_C = -n/15
  c_D = -7 n^2/15.

Thus their saturation targets in quarter-turn units pi/2 are (-1,+1,-1,-1).
The phase-incidence rows obey A-B-C+D=0, but the same target combination is
-2 quarter turns = -pi, so the four outward-saturation equations are exactly
UNSAT for every integer n>=1.

This is an all-n phase-holonomy motif whose every channel crosses the dyadic
boundary n -> 2n.  It is still a single wavevector-triad polarization network,
not a coverage theorem for all boundary-crossing NSE interactions.
"""
import sympy as sp

n = sp.symbols("n", positive=True, integer=True)


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
            return e1, e2, sp.expand(e1.dot(e1)), sp.expand(e2.dot(e2))
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
            (
                hp.dot(qv) * hk.dot(hq)
                + hq.dot(pv) * hk.dot(hp)
            )
            / hk.dot(hk)
        )
    )


def h3_weight(k, slot):
    e1, e2, n1, n2 = basis(k)
    physical = n1 if slot == "e1" else n2
    k2 = sp.expand(sp.Matrix(k).dot(sp.Matrix(k)))
    return sp.factor(physical * (1 + k2) ** 3)


p = (0, 0, n)
q = (n, -n, n)
k = (n, -n, 2 * n)

CHANNELS = (
    ("A", p, "e1", q, "e1", k, "e1"),
    ("B", p, "e1", q, "e2", k, "e1"),
    ("C", p, "e1", q, "e1", k, "e2"),
    ("D", p, "e1", q, "e2", k, "e2"),
)

EXPECTED = (
    -n**2 / 5,
    3 * n**3 / 5,
    -n / 15,
    -7 * n**2 / 15,
)

# Phase vertices (p/e1, q/e1, q/e2, k/e1, k/e2)
ROWS = (
    (1, 1, 0, -1, 0),  # A
    (1, 0, 1, -1, 0),  # B
    (1, 1, 0, 0, -1),  # C
    (1, 0, 1, 0, -1),  # D
)
TARGETS = (-1, +1, -1, -1)
RELATION = (+1, -1, -1, +1)


def main():
    got = tuple(
        coupling(pv, ps, qv, qs, kv, ks)
        for _, pv, ps, qv, qs, kv, ks in CHANNELS
    )
    for g, e in zip(got, EXPECTED):
        assert sp.simplify(g - e) == 0, (g, e)

    assert sp.ask(sp.Q.negative(got[0]))
    assert sp.ask(sp.Q.positive(got[1]))
    assert sp.ask(sp.Q.negative(got[2]))
    assert sp.ask(sp.Q.negative(got[3]))

    # Exact dyadic geometry.
    assert max(abs(v) for v in p) == n
    assert max(abs(v) for v in q) == n
    assert max(abs(v) for v in k) == 2 * n

    combined_row = tuple(
        sum(RELATION[i] * ROWS[i][j] for i in range(4))
        for j in range(5)
    )
    assert combined_row == (0, 0, 0, 0, 0)

    target_holonomy = sum(RELATION[i] * TARGETS[i] for i in range(4))
    assert target_holonomy == -2
    assert target_holonomy % 4 != 0

    # Exact H3-normalized output-production coefficient magnitudes.
    wp = h3_weight(p, "e1")
    wq1 = h3_weight(q, "e1")
    wq2 = h3_weight(q, "e2")
    wk1 = h3_weight(k, "e1")
    wk2 = h3_weight(k, "e2")

    abs_c = (-got[0], got[1], -got[2], -got[3])
    gammas = (
        sp.factor(2 * abs_c[0] * sp.sqrt(wk1) / sp.sqrt(wp * wq1)),
        sp.factor(2 * abs_c[1] * sp.sqrt(wk1) / sp.sqrt(wp * wq2)),
        sp.factor(2 * abs_c[2] * sp.sqrt(wk2) / sp.sqrt(wp * wq1)),
        sp.factor(2 * abs_c[3] * sp.sqrt(wk2) / sp.sqrt(wp * wq2)),
    )

    common = sp.factor(
        n * (6 * n**2 + 1) ** sp.Rational(3, 2)
        / ((n**2 + 1) ** sp.Rational(3, 2) * (3 * n**2 + 1) ** sp.Rational(3, 2))
    )
    expected_gamma = (
        sp.sqrt(10) * common / 5,
        sp.sqrt(30) * common / 5,
        2 * sp.sqrt(15) * common / 15,
        14 * sp.sqrt(5) * common / 15,
    )
    for g, e in zip(gammas, expected_gamma):
        assert sp.simplify(g - e) == 0, (g, e)

    tax = sp.simplify(1 - sp.sqrt(2) / 2)
    assert sp.ask(sp.Q.positive(tax))

    print("NS P2 all-n dyadic complex phase holonomy")
    print("wavevectors:", p, q, k)
    print("coefficients:", [sp.factor(v) for v in got])
    print("all four channels cross max-coordinate scale n -> 2n")
    print("incidence relation: A - B - C + D = 0")
    print("target holonomy:", target_holonomy, "quarter turns = -pi")
    print("result: simultaneous outward saturation is UNSAT for every integer n>=1")
    print("phase consequence: max channel error >= pi/4")
    print("local tax constant: 1 - 1/sqrt(2)")
    print("H3-normalized coefficient magnitudes:", gammas)
    print("all share an explicit common factor asymptotic to const/n^2")
    print("scope: one dyadic polarization-channel motif; full boundary coverage remains OPEN")
    print("NS-P2 DYADIC COMPLEX HOLONOMY ALL-N PASS")


if __name__ == "__main__":
    main()
