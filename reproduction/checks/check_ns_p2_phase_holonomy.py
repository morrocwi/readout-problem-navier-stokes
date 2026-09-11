#!/usr/bin/env python3
"""Exact symbolic complex phase-holonomy witness for the P2 NSE triad attack.

This checker uses the same unnormalised real divergence-free basis convention as
the existing all-n P2 motif checkers.  For every positive integer n it derives
four actual Fourier-Leray scalar interaction channels

  A: (0,0,1)/e1 + (n,-n,-1)/e1 -> (n,-n,0)/e1
  B: (0,0,1)/e1 + (n,-n,-1)/e1 -> (n,-n,0)/e2
  C: (0,0,1)/e2 + (n,-n,0)/e1  -> (n,-n,1)/e1
  D: (0,0,1)/e2 + (n,-n,0)/e2  -> (n,-n,1)/e1

with exact scalar coefficients

  c_A = -n
  c_B = -1/n
  c_C = -n^3/(n^2+1)
  c_D = +n^3/(n^2+1).

For a channel p+q=k with coefficient c, the scalar complex ODE contribution is

  z'_k = -i c z_p z_q,

so the target-mode quadratic transfer is

  d|z_k|^2/dt = 2 c Im(z_p z_q conjugate(z_k)).

Thus outward saturation asks for the incidence phase
  phi_p + phi_q - phi_k
to equal sign(c)*pi/2 modulo 2*pi.

The four incidence rows obey A-B+C-D=0 exactly, while their target quarter-turns
obey (-1)-(-1)+(-1)-(+1)=-2, i.e. a pi mismatch modulo 2*pi.  Hence the four
outward saturation equations are exactly UNSAT for every positive integer n.

The associated geometric consequence is that at least one channel has circular
phase error >= pi/4.  Therefore, for nonnegative channel amplitude prefactors
a_A,...,a_D and outward contributions T_i,

  sum T_i <= sum a_i - (1-1/sqrt(2))*min_i a_i.

This is a local complex-network frustration tax / frustration-or-cut motif.
It is NOT a dyadic-boundary coverage theorem and does NOT prove global scale
contraction.
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
    if slot == "e1":
        return e1
    if slot == "e2":
        return e2
    raise AssertionError(slot)


def coupling(p, pslot, q, qslot, k, kslot):
    """Exact scalar coefficient c in z'_k = -i c z_p z_q.

    Both ordered NSE convection contributions (p,q) and (q,p) are included.
    Testing the Leray-projected vector against the divergence-free output basis
    vector is equivalent to testing the unprojected vector, since h_k dot k=0.
    """
    pv, qv, kv = sp.Matrix(p), sp.Matrix(q), sp.Matrix(k)
    assert all(sp.simplify((pv + qv - kv)[i]) == 0 for i in range(3))
    hp = slot_vector(p, pslot)
    hq = slot_vector(q, qslot)
    hk = slot_vector(k, kslot)
    hk2 = sp.expand(hk.dot(hk))
    c = (
        hp.dot(qv) * hk.dot(hq)
        + hq.dot(pv) * hk.dot(hp)
    ) / hk2
    return sp.factor(sp.simplify(c))


p = (0, 0, 1)
km = (n, -n, -1)
k0 = (n, -n, 0)
kp = (n, -n, 1)

CHANNELS = (
    ("A", p, "e1", km, "e1", k0, "e1"),
    ("B", p, "e1", km, "e1", k0, "e2"),
    ("C", p, "e2", k0, "e1", kp, "e1"),
    ("D", p, "e2", k0, "e2", kp, "e1"),
)

EXPECTED = (
    -n,
    -sp.Integer(1) / n,
    -n**3 / (n**2 + 1),
    n**3 / (n**2 + 1),
)

# Phase vertices.  Each incidence row represents phi_p + phi_q - phi_k.
VERTICES = (
    "p:e1",
    "p:e2",
    "km:e1",
    "k0:e1",
    "k0:e2",
    "kp:e1",
)

ROWS = (
    (1, 0, 1, -1, 0, 0),  # A
    (1, 0, 1, 0, -1, 0),  # B
    (0, 1, 0, 1, 0, -1),  # C
    (0, 1, 0, 0, 1, -1),  # D
)

# Units are quarter turns pi/2.  sign(c) fixes the saturation target.
TARGETS = (-1, -1, -1, +1)
RELATION = (+1, -1, +1, -1)


def main():
    got = tuple(
        coupling(pv, ps, qv, qs, kv, ks)
        for _, pv, ps, qv, qs, kv, ks in CHANNELS
    )
    for g, e in zip(got, EXPECTED):
        assert sp.simplify(g - e) == 0, (g, e)

    # Exact all-n sign obligations are immediate from n>0 and n^2+1>0.
    assert all(sp.ask(sp.Q.negative(g)) for g in got[:3])
    assert sp.ask(sp.Q.positive(got[3]))

    # Exact integer incidence dependency A-B+C-D = 0.
    combined_row = tuple(
        sum(RELATION[i] * ROWS[i][j] for i in range(4))
        for j in range(len(VERTICES))
    )
    assert combined_row == (0,) * len(VERTICES)

    # But the same combination of requested targets is -2 quarter turns = -pi,
    # nonzero modulo four quarter turns (2*pi).
    target_holonomy = sum(RELATION[i] * TARGETS[i] for i in range(4))
    assert target_holonomy == -2
    assert target_holonomy % 4 != 0

    # Quantitative tax constant from the pi/4 minimax phase error.
    tax = sp.simplify(1 - sp.sqrt(2) / 2)
    assert sp.ask(sp.Q.positive(tax))
    assert sp.simplify(sp.cos(sp.pi / 4) - sp.sqrt(2) / 2) == 0

    print("NS P2 exact complex phase holonomy")
    print("coefficients:", [sp.factor(v) for v in got])
    print("incidence relation: A - B + C - D = 0")
    print("target quarter-turn relation:", target_holonomy, "= -pi")
    print("result: outward-saturation phase system is UNSAT for every integer n>=1")
    print("phase error consequence: max_i d_i >= pi/4")
    print("local tax: sum(T_i) <= sum(a_i) - (1-1/sqrt(2))*min(a_i)")
    print("scope: one all-n overlapping-channel motif; dyadic coverage remains OPEN")
    print("NS-P2 COMPLEX PHASE HOLONOMY ALL-N PASS")


if __name__ == "__main__":
    main()
