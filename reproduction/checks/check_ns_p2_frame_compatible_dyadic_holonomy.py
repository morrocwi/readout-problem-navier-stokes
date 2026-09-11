#!/usr/bin/env python3
"""Exact all-n 3D frame-compatible dyadic holonomy for the P2 NSE attack.

Network, for integer n>=1:

  a=n(1,0,0), b=n(0,0,1), c=n(0,1,0),
  p=a+b=n(1,0,1), q=p+c=n(1,1,1), k=p+q=n(2,1,2).

Triads:
  T0: a+b=p
  T1: p+c=q
  T2: p+q=k

At shared mode p, the T0 adapted normal and T1/T2 adapted normal are
orthogonal, so they define the same projective polarization frame (mod pi/2).
At q, T1 and T2 adapted normals are parallel. Hence the incident projective
frame dispersion is exactly zero at both shared modes.

Nevertheless, in one global compatible real divergence-free frame, four
actual Fourier-Leray scalar channels across T1 and T2 obey an exact incidence
relation while their outward-saturation targets differ by pi. Thus exact
frame compatibility (D=0) does not imply phase satisfiability.

This is an all-n exact structural family. It does not prove all-boundary
coverage, a time-window tax, an R_j recurrence, or NSE regularity.
"""

import sympy as sp

n = sp.symbols("n", positive=True, integer=True)

V = {
    "a": sp.Matrix((n, 0, 0)),
    "b": sp.Matrix((0, 0, n)),
    "c": sp.Matrix((0, n, 0)),
    "p": sp.Matrix((n, 0, n)),
    "q": sp.Matrix((n, n, n)),
    "k": sp.Matrix((2*n, n, 2*n)),
}

# One global frame field compatible with all three triad-adapted projective
# frames. Vectors are intentionally unnormalised; physical H3 weights include
# their Euclidean norms exactly.
y = sp.Matrix((0, 1, 0))
d = sp.Matrix((-1, 0, 1))
H = {
    "a": (y, sp.Matrix((0, 0, -1))),
    "b": (y, sp.Matrix((1, 0, 0))),
    "p": (y, d),
    "c": (d, sp.Matrix((-1, 0, -1))),
    "q": (d, sp.Matrix((-1, 2, -1))),
    "k": (d, sp.Matrix((-1, 4, -1))),
}

for mode, v in V.items():
    h0, h1 = H[mode]
    assert sp.simplify(v.dot(h0)) == 0
    assert sp.simplify(v.dot(h1)) == 0
    assert sp.simplify(h0.dot(h1)) == 0


def coupling(m1, s1, m2, s2, out, so):
    v1, v2, vo = V[m1], V[m2], V[out]
    assert v1 + v2 == vo
    h1, h2, ho = H[m1][s1], H[m2][s2], H[out][so]
    return sp.factor(
        (h1.dot(v2)*ho.dot(h2) + h2.dot(v1)*ho.dot(h1)) / ho.dot(ho)
    )


def h3_hom_weight(mode, slot):
    v = V[mode]
    h = H[mode][slot]
    return sp.factor(h.dot(h) * (v.dot(v))**3)


def gamma_hom(ch):
    m1, s1, m2, s2, out, so = ch
    cc = coupling(*ch)
    return sp.factor(
        2*cc*sp.sqrt(h3_hom_weight(out, so))
        / sp.sqrt(h3_hom_weight(m1, s1)*h3_hom_weight(m2, s2))
    )

# All nonzero channels in the chosen global compatible gauge.
CHANNELS = {
    "T0A": ("a", 0, "b", 1, "p", 0),
    "T0B": ("a", 1, "b", 0, "p", 0),
    "T1A": ("p", 0, "c", 0, "q", 0),
    "T1B": ("p", 0, "c", 1, "q", 1),
    "T1C": ("p", 1, "c", 1, "q", 0),
    "T2A": ("p", 0, "q", 0, "k", 0),
    "T2B": ("p", 0, "q", 1, "k", 1),
    "T2C": ("p", 1, "q", 1, "k", 0),
}
EXPECTED_COEFFS = {
    "T0A": n,
    "T0B": -n,
    "T1A": n,
    "T1B": -n/3,
    "T1C": -2*n,
    "T2A": n,
    "T2B": n/9,
    "T2C": -2*n,
}
EXPECTED_GAMMA_HOM = {
    "T0A": 4*sp.sqrt(2)/n**2,
    "T0B": -4*sp.sqrt(2)/n**2,
    "T1A": 3*sp.sqrt(6)/(2*n**2),
    "T1B": -3*sp.sqrt(2)/(2*n**2),
    "T1C": -3*sp.sqrt(3)/n**2,
    "T2A": 3*sp.sqrt(6)/(2*n**2),
    "T2B": sp.sqrt(2)/(2*n**2),
    "T2C": -3/n**2,
}

# Minimal four-channel holonomy cycle: T1C - T1B + T2A - T2C = 0.
# Phase variables: p0,p1,c1,q0,q1,k0. A row means phi_in1+phi_in2-phi_out.
ROWS = {
    "T1B": (1, 0, 1, 0, -1, 0),
    "T1C": (0, 1, 1, -1, 0, 0),
    "T2A": (1, 0, 0, 1, 0, -1),
    "T2C": (0, 1, 0, 0, 1, -1),
}
RELATION = {"T1C": 1, "T1B": -1, "T2A": 1, "T2C": -1}

# Outward saturation target in quarter turns pi/2 is sign(c).
TARGETS = {name: (1 if EXPECTED_COEFFS[name] > 0 else -1) for name in ROWS}


def main():
    for name, ch in CHANNELS.items():
        got = coupling(*ch)
        assert sp.simplify(got - EXPECTED_COEFFS[name]) == 0, (name, got)
        gg = gamma_hom(ch)
        assert sp.simplify(gg - EXPECTED_GAMMA_HOM[name]) == 0, (name, gg)

    # Triad-plane projective frames: T0 normal y; T1/T2 normal d.
    n0 = V["a"].cross(V["b"])
    n1 = V["p"].cross(V["c"])
    n2 = V["p"].cross(V["q"])
    assert sp.simplify(n0.dot(n1)) == 0
    assert n1.cross(n2) == sp.zeros(3, 1)
    # Orthogonal normals represent the same unordered projective frame; hence
    # all incident projective frames coincide at shared p and q: D_p=D_q=0.

    combined = tuple(
        sum(RELATION[name]*ROWS[name][j] for name in ROWS)
        for j in range(6)
    )
    assert combined == (0, 0, 0, 0, 0, 0)

    target_holonomy_quarters = sum(RELATION[name]*TARGETS[name] for name in ROWS)
    assert target_holonomy_quarters == 2  # pi mismatch

    # Every channel in the minimal cycle has a homogeneous-H3 coefficient
    # magnitude at least 3 sqrt(2)/(2 n^2).
    cycle = ("T1B", "T1C", "T2A", "T2C")
    floor_hom = 3*sp.sqrt(2)/(2*n**2)
    for name in cycle:
        assert sp.simplify(abs(EXPECTED_GAMMA_HOM[name]) - floor_hom) >= 0

    # For nonzero integer wavevectors, Gamma_inh/Gamma_hom >= 1/8.
    floor_inh = sp.simplify(floor_hom/8)
    assert floor_inh == 3*sp.sqrt(2)/(16*n**2)

    print("NS P2 frame-compatible 3D dyadic holonomy")
    print("coefficients:", {k: sp.factor(v) for k, v in EXPECTED_COEFFS.items()})
    print("minimal cycle relation: T1C - T1B + T2A - T2C = 0")
    print("target holonomy: pi")
    print("shared projective-frame dispersion: D_p = D_q = 0")
    print("homogeneous H3 cycle floor:", floor_hom)
    print("inhomogeneous H3 conservative cycle floor:", floor_inh)
    print("final output mode k/n = (2,1,2): reaches max-coordinate dyadic boundary")
    print("scope: one exact all-n 3D network; full boundary coverage remains OPEN")
    print("NS-P2 FRAME-COMPATIBLE DYADIC HOLONOMY PASS")


if __name__ == "__main__":
    main()
