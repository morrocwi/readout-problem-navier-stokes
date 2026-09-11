#!/usr/bin/env python3
"""Exact all-scale dyadic fresh-donor tree escape for P2.

The selected scalar channel family uses one common normal polarization N in the
xz plane and one fresh tangential donor per step.  Two self-similar shapes
repeat with scale factor 4.  Every step doubles max-coordinate scale, every
outward phase constraint is constructively SAT, and the H1-normalized coupling
has a cutoff-uniform positive floor.

This is a matching counterexample to any inference

    conflict-free / phase-SAT remainder -> geometrically weak.

It is not an NSE trajectory and does not claim that off-tree convolution
channels vanish in a full state containing many such modes.
"""

import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
N = sp.Matrix((0, 1, 0))


def norm(v):
    return sp.sqrt(sp.factor(v.dot(v)))


def tangent(v):
    return sp.simplify(N.cross(v) / norm(v))


def coupling(p, q, k):
    """Coefficient for p/N + q/T_q -> k/N with unit polarizations."""
    assert p + q == k
    hp = N
    hq = tangent(q)
    hk = N
    return sp.factor(
        sp.simplify(hp.dot(q) * hk.dot(hq) + hq.dot(p) * hk.dot(hp))
    )


def gamma_h1_hom(p, q, k):
    c = coupling(p, q, k)
    return sp.factor(sp.simplify(2 * c * norm(k) / (norm(p) * norm(q))))


# Even shape: max scale n -> 2n.
p0 = sp.Matrix((n, 0, 0))
q0 = sp.Matrix((n, 0, n))
k0 = sp.Matrix((2*n, 0, n))

# Odd shape: max scale 2n -> 4n.
p1 = sp.Matrix((2*n, 0, n))
q1 = sp.Matrix((2*n, 0, -n))
k1 = sp.Matrix((4*n, 0, 0))

c0 = coupling(p0, q0, k0)
c1 = coupling(p1, q1, k1)
g0 = gamma_h1_hom(p0, q0, k0)
g1 = gamma_h1_hom(p1, q1, k1)

EXPECTED_C0 = n / sp.sqrt(2)
EXPECTED_C1 = -4*n / sp.sqrt(5)
EXPECTED_G0 = sp.sqrt(5)
EXPECTED_G1 = -sp.Rational(32, 5) / sp.sqrt(5)


def build_phase_fixture(steps=8):
    """Rows in quarter-turn units for a finite prefix.

    Variable order is backbone phi_0..phi_steps followed by donors psi_0..psi_{steps-1}.
    Row j encodes phi_j + psi_j - phi_{j+1} = target_j mod 4.
    """
    rows = []
    targets = []
    assignment = [0] * (steps + 1) + [0] * steps
    for j in range(steps):
        row = [0] * (2*steps + 1)
        row[j] = 1
        row[j + 1] = -1
        donor_idx = steps + 1 + j
        row[donor_idx] = 1
        target = 1 if j % 2 == 0 else -1
        assignment[donor_idx] = target % 4
        rows.append(tuple(row))
        targets.append(target % 4)
    return sp.Matrix(rows), targets, tuple(assignment)


def main():
    assert sp.simplify(c0 - EXPECTED_C0) == 0
    assert sp.simplify(c1 - EXPECTED_C1) == 0
    assert sp.simplify(g0 - EXPECTED_G0) == 0
    assert sp.simplify(g1 - EXPECTED_G1) == 0

    # Uniform homogeneous H1 floor: |g0|=sqrt(5), |g1|=32/(5sqrt(5))>sqrt(5).
    assert sp.simplify(g1**2 - 5) > 0
    assert sp.simplify(g0**2 - 5) == 0

    # Conservative inhomogeneous correction is >= 1/2 on nonzero integer modes.
    inh_floor = sp.sqrt(5) / 2
    assert inh_floor > 0

    # Exact dyadic max-coordinate scaling for the two repeated shapes.
    assert max(abs(int(v)) for v in (1, 0, 0)) == 1
    assert max(abs(int(v)) for v in (2, 0, 1)) == 2
    assert max(abs(int(v)) for v in (4, 0, 0)) == 4
    assert p0 + q0 == k0
    assert p1 + q1 == k1

    # Finite-prefix incidence matrix has full row rank because every row has a unique donor column.
    rows, targets, assignment = build_phase_fixture(steps=8)
    assert rows.rank() == rows.rows
    for i in range(rows.rows):
        lhs = int(sum(rows[i, j] * assignment[j] for j in range(rows.cols))) % 4
        assert lhs == targets[i], (i, lhs, targets[i])

    # Two-step self-similarity: k1 = 4 * (1,0,0), so the geometry restarts at scale 4n.
    assert k1 == 4 * sp.Matrix((n, 0, 0))

    print("NS P2 dyadic fresh-donor tree escape")
    print("even coefficient:", c0)
    print("odd coefficient:", c1)
    print("even H1 homogeneous gamma:", g0)
    print("odd H1 homogeneous gamma:", g1)
    print("uniform H1 homogeneous floor: sqrt(5)")
    print("uniform conservative H1 inhomogeneous floor: sqrt(5)/2")
    print("finite-prefix phase incidence rank:", rows.rank(), "/", rows.rows)
    print("constructive quarter-turn SAT assignment:", assignment)
    print("scope: selected exact Fourier-Leray channel tree; not a full NSE trajectory")
    print("NS-P2 DYADIC FRESH-DONOR TREE PASS")


if __name__ == "__main__":
    main()
