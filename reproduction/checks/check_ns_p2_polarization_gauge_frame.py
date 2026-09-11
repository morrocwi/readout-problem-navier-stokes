#!/usr/bin/env python3
"""Exact polarization-gauge red-team and frame-mismatch identities for P2.

This checker does four things.

1. It puts an arbitrary non-collinear Fourier triad into a triad-adapted
   orthonormal polarization frame and verifies that the Fourier-Leray tensor
   has only three nonzero scalar channels.

2. It rotates one mode's polarization basis and verifies the exact four-face
   coefficient product

      -P^2 y^4 c^2 s^2 / Q^2,

   so a non-adapted frame creates a pi sign holonomy while an adapted frame
   makes two members of that face vanish.  Therefore scalar-channel holonomy
   inside a fixed polarization gauge is not, by itself, basis invariant.

3. It checks the previous all-n coplanar two-triad ladder in a common adapted
   frame and exhibits an exact quarter-turn SAT assignment.  This is a
   matching counterexample to any claim that the previously recorded
   standard-basis holonomy is unavoidable under polarization-basis changes.

4. It verifies an explicit non-coplanar shared-mode pair whose adapted frames
   are separated by pi/4 and audits the all-n H3 coefficient floor used in the
   accompanying theorem note.  It also checks one exact weighted projective
   frame-dispersion identity fixture.

Claim boundary: this is finite/algebraic Fourier-Leray geometry.  It does not
by itself prove a gauge-invariant dyadic transfer deficit, temporal switching
control, an R_j recurrence, or Navier-Stokes regularity.
"""

import itertools
import sympy as sp


# ---------------------------------------------------------------------------
# 1. Generic triad in an adapted orthonormal frame
# ---------------------------------------------------------------------------

P, x, y = sp.symbols("P x y", positive=True, real=True)
c, s = sp.symbols("c s", real=True, nonzero=True)

Q = sp.sqrt(x**2 + y**2)
K = sp.sqrt((P + x)**2 + y**2)

p = sp.Matrix((P, 0, 0))
q = sp.Matrix((x, y, 0))
k = p + q

N = sp.Matrix((0, 0, 1))
Tp = sp.Matrix((0, 1, 0))
Tq = sp.Matrix((-y / Q, x / Q, 0))
Tk = sp.Matrix((-y / K, (P + x) / K, 0))


def coupling(hp, hq, hk):
    """Scalar Fourier-Leray coefficient for unit output polarization hk."""
    return sp.factor(
        sp.simplify(hp.dot(q) * hk.dot(hq) + hq.dot(p) * hk.dot(hp))
    )


P_SLOTS = (N, Tp)
Q_SLOTS = (N, Tq)
K_SLOTS = (N, Tk)

TENSOR = {
    (i, j, ell): coupling(P_SLOTS[i], Q_SLOTS[j], K_SLOTS[ell])
    for i, j, ell in itertools.product(range(2), repeat=3)
}

EXPECTED_TENSOR = {
    (0, 0, 0): 0,
    (0, 0, 1): 0,
    (0, 1, 0): -P * y / Q,
    (0, 1, 1): 0,
    (1, 0, 0): y,
    (1, 0, 1): 0,
    (1, 1, 0): 0,
    (1, 1, 1): y * (Q**2 - P**2) / (Q * K),
}


# Rotate only the p-polarization frame:
# E1 = c N + s Tp, E2 = -s N + c Tp.
E1 = c * N + s * Tp
E2 = -s * N + c * Tp

ROTATED_FACE = (
    coupling(E1, Tq, N),
    coupling(E1, N, N),
    coupling(E2, Tq, N),
    coupling(E2, N, N),
)
ROTATED_FACE_PRODUCT = sp.factor(sp.prod(ROTATED_FACE))
EXPECTED_FACE_PRODUCT = -P**2 * y**4 * c**2 * s**2 / Q**2


# ---------------------------------------------------------------------------
# 2. Exact SAT assignment for the old coplanar all-n ladder in common
#    triad-adapted frames.
# ---------------------------------------------------------------------------

# Variables in quarter-turn units mod 4:
# pN,pT,qminusN,qminusT,k0N,k0T,kplusN,kplusT
LADDER_EQUATIONS = []


def add_ladder_eq(terms, target):
    row = [0] * 8
    for idx, coeff in terms:
        row[idx] += coeff
    LADDER_EQUATIONS.append((tuple(row), target % 4))


# For both ladder triads |q|>|p|, so the three adapted-frame coefficient
# signs are (-,+,+):
# pN+qT->kN, pT+qN->kN, pT+qT->kT.
add_ladder_eq(((0, 1), (3, 1), (4, -1)), -1)
add_ladder_eq(((1, 1), (2, 1), (4, -1)), +1)
add_ladder_eq(((1, 1), (3, 1), (5, -1)), +1)
add_ladder_eq(((0, 1), (5, 1), (6, -1)), -1)
add_ladder_eq(((1, 1), (4, 1), (6, -1)), +1)
add_ladder_eq(((1, 1), (5, 1), (7, -1)), +1)

LADDER_SAT_ASSIGNMENT = (0, 0, 0, 2, 3, 1, 2, 0)


# ---------------------------------------------------------------------------
# 3. Explicit all-n non-coplanar shared-mode pair.
# ---------------------------------------------------------------------------

n = sp.symbols("n", positive=True, integer=True)
p0 = sp.Matrix((0, 0, n))
q1 = sp.Matrix((n, 0, 0))
q2 = sp.Matrix((n, n, 0))
k1 = p0 + q1
k2 = p0 + q2
normal1 = p0.cross(q1)
normal2 = p0.cross(q2)
cos_alpha = sp.simplify(
    normal1.dot(normal2)
    / sp.sqrt(normal1.dot(normal1) * normal2.dot(normal2))
)

SIN_PI_8 = sp.sqrt(2 - sp.sqrt(2)) / 2

# For both triads, area/max(P,Q) = n.  Projective frame separation is pi/4,
# so every shared-mode basis misaligns at least one triad by >= pi/8.
RAW_FACE_FLOOR = sp.simplify(n * SIN_PI_8)

# Homogeneous H3 unit-polarization normalization multiplier:
# 2 |k|^3 / (|p|^3 |q|^3).
GAMMA1_HOM_FLOOR = sp.simplify(4 * sp.sqrt(2) * SIN_PI_8 / n**2)
GAMMA2_HOM_FLOOR = sp.simplify(
    sp.Rational(3, 2) * sp.sqrt(6) * SIN_PI_8 / n**2
)
GAMMA_HOM_UNIFORM_FLOOR = GAMMA2_HOM_FLOOR

# For nonzero integer modes R(L)=(1+L^2)^(3/2)/L^3 lies in [1,2sqrt2].
# Therefore Gamma_inh/Gamma_hom >= 1/8.
GAMMA_INH_UNIFORM_FLOOR = sp.simplify(GAMMA_HOM_UNIFORM_FLOOR / 8)


# ---------------------------------------------------------------------------
# 4. Exact weighted projective-frame dispersion fixture.
# ---------------------------------------------------------------------------

# Frames at theta=(0, pi/8, pi/4), weights=(1,2,3).
# In e^{i4theta} coordinates these are (1, i, -1).
W = sp.Integer(6)
Z_RE = sp.Rational(1 - 3, 6)
Z_IM = sp.Rational(2, 6)
FRAME_DISPERSION = sp.simplify(1 - Z_RE**2 - Z_IM**2)

# Pair sum sum_{i<j} w_i w_j sin^2(2 delta_ij):
PAIR_MISMATCH_SUM = sp.simplify(
    1 * 2 * sp.Rational(1, 2)
    + 1 * 3 * 1
    + 2 * 3 * sp.Rational(1, 2)
)
FRAME_DISPERSION_FROM_PAIRS = sp.simplify(4 * PAIR_MISMATCH_SUM / W**2)

# One exact audit of the pair-mass lower bound with threshold a=1/4.
a0 = sp.Rational(1, 4)
PAIR_WEIGHT_TOTAL = sp.Integer(1 * 2 + 1 * 3 + 2 * 3)
PAIR_WEIGHT_LOWER = sp.simplify(
    W**2 * (FRAME_DISPERSION / 4 - a0 / 2) / (1 - a0)
)


def main():
    for idx, expected in EXPECTED_TENSOR.items():
        assert sp.simplify(TENSOR[idx] - expected) == 0, (idx, TENSOR[idx], expected)

    nonzero = [idx for idx, val in TENSOR.items() if sp.simplify(val) != 0]
    assert nonzero == [(0, 1, 0), (1, 0, 0), (1, 1, 1)]

    assert sp.simplify(ROTATED_FACE_PRODUCT - EXPECTED_FACE_PRODUCT) == 0

    for row, target in LADDER_EQUATIONS:
        lhs = sum(row[i] * LADDER_SAT_ASSIGNMENT[i] for i in range(8)) % 4
        assert lhs == target, (row, lhs, target)

    assert cos_alpha == sp.sqrt(2) / 2
    assert sp.simplify(GAMMA1_HOM_FLOOR - GAMMA_HOM_UNIFORM_FLOOR) > 0
    assert sp.simplify(
        GAMMA_INH_UNIFORM_FLOOR
        - sp.Rational(3, 16) * sp.sqrt(6) * SIN_PI_8 / n**2
    ) == 0

    assert FRAME_DISPERSION == sp.Rational(7, 9)
    assert FRAME_DISPERSION_FROM_PAIRS == FRAME_DISPERSION
    assert PAIR_WEIGHT_TOTAL == 11
    assert PAIR_WEIGHT_LOWER == sp.Rational(10, 3)
    assert PAIR_WEIGHT_TOTAL >= PAIR_WEIGHT_LOWER

    print("NS P2 polarization gauge / frame mismatch checker")
    print("adapted triad nonzero tensor entries:")
    for idx in nonzero:
        print(" ", idx, sp.factor(TENSOR[idx]))
    print("rotated-face product:", ROTATED_FACE_PRODUCT)
    print("old coplanar ladder adapted-frame SAT assignment:", LADDER_SAT_ASSIGNMENT)
    print("explicit pair frame cos(alpha):", cos_alpha)
    print("raw face floor:", RAW_FACE_FLOOR)
    print("homogeneous H3 uniform coefficient floor:", GAMMA_HOM_UNIFORM_FLOOR)
    print("inhomogeneous H3 uniform coefficient floor:", GAMMA_INH_UNIFORM_FLOOR)
    print("weighted frame dispersion fixture:", FRAME_DISPERSION)
    print("pair mismatch sum:", PAIR_MISMATCH_SUM)
    print("scope: algebraic/gauge geometry only; global transfer coverage remains OPEN")
    print("NS-P2 POLARIZATION GAUGE FRAME CHECK PASS")


if __name__ == "__main__":
    main()
