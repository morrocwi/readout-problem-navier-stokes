#!/usr/bin/env python3
"""Exact finite packing/hitting-set audit for four-channel pi-holonomy cycles.

The general theorem is analytic and recorded in the accompanying paper note.
This checker audits the greedy construction on an overlapping rational fixture
and verifies the exact amplitude decomposition, hitting property, packing bound
and aggregate tax algebra.
"""
from fractions import Fraction

# Six channels with exact positive amplitude budgets.
A = [Fraction(x) for x in (5, 4, 6, 3, 7, 2)]
CYCLES = [
    (0, 1, 2, 3),
    (2, 3, 4, 5),
    (0, 1, 4, 5),
]
L = 4


def greedy_pack(amplitudes, cycles):
    r = list(amplitudes)
    allocations = []
    while True:
        active = None
        for C in cycles:
            if all(r[e] > 0 for e in C):
                active = C
                break
        if active is None:
            break
        x = min(r[e] for e in active)
        allocations.append((active, x))
        for e in active:
            r[e] -= x
    return r, allocations


def main():
    r, allocations = greedy_pack(A, CYCLES)
    P = sum((x for _, x in allocations), Fraction(0))
    S = sum(A, Fraction(0))
    H = {e for e, rr in enumerate(r) if rr == 0}

    # Exact per-edge decomposition A_e = residual + packed cycle portions.
    used = [Fraction(0) for _ in A]
    for C, x in allocations:
        for e in C:
            used[e] += x
    assert all(A[e] == r[e] + used[e] for e in range(len(A)))

    # Greedy termination means every declared conflict cycle meets H.
    assert all(any(e in H for e in C) for C in CYCLES)

    # Saturated hitting-set mass <= L times packed mass.
    AH = sum((A[e] for e in H), Fraction(0))
    assert AH <= L * P

    # Fixture values are intentionally transparent.
    assert allocations == [
        ((0, 1, 2, 3), Fraction(3)),
        ((0, 1, 4, 5), Fraction(1)),
    ]
    assert P == 4
    assert S == 27
    assert H == {1, 3}
    assert AH == 7

    # Aggregate pi-holonomy tax coefficient is c0=1-1/sqrt(2).
    # We audit only the exact rational multiplier P here; irrational c0 is
    # kept symbolic in the theorem note and existing holonomy checker.
    assert L * P == 16

    print("NS P2 holonomy packing/hitting-set fixture")
    print("amplitude total S =", S)
    print("packed mass P =", P)
    print("allocations =", allocations)
    print("residual =", r)
    print("saturated hitting set H =", sorted(H), "mass =", AH)
    print("bound: mass(H) <= 4 P =", L * P)
    print("aggregate tax: T_total <= S - (1-1/sqrt(2))*P")
    print("dichotomy: P>=eta*S gives relative tax; P<eta*S gives small hitting set")
    print("scope: finite aggregation theorem; actual dyadic flux coverage remains OPEN")
    print("NS-P2 HOLONOMY PACKING DICHOTOMY PASS")


if __name__ == "__main__":
    main()
