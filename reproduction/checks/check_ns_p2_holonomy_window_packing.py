#!/usr/bin/env python3
"""Exact fixture for integrating the non-overcounted holonomy tax over time.

The analytic theorem is pointwise integration.  This checker audits an exact
symbolic finite-window fixture with c0 = 1 - 1/sqrt(2), including the integrated
hitting-set budget.
"""

import sympy as sp

c0 = 1 - 1/sp.sqrt(2)

# Exact time-cell widths, channel envelopes S_i, packed masses P_i.
dt = [sp.Rational(1, 5), sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(1, 6)]
S = [sp.Rational(5), sp.Rational(7, 2), sp.Rational(9, 2), sp.Rational(6)]
P = [sp.Rational(1), sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(3, 4)]

# Saturate the pointwise upper bound in the fixture.
T = [sp.simplify(S[i] - c0*P[i]) for i in range(len(S))]

# Pointwise hitting-set weights chosen below the exact 4P envelope.
H = [sp.Rational(3), sp.Rational(3, 2), sp.Rational(5), sp.Rational(2)]


def integrate(vals):
    return sp.simplify(sum(dt[i]*vals[i] for i in range(len(vals))))


def main():
    for i in range(len(S)):
        assert sp.simplify(T[i] - (S[i] - c0*P[i])) == 0
        assert H[i] <= 4*P[i]

    SI = integrate(S)
    PI = integrate(P)
    TI = integrate(T)
    HI = integrate(H)

    assert sp.simplify(TI - (SI - c0*PI)) == 0
    assert HI <= 4*PI

    # Audit one explicit window-threshold implication using eta = 1/10.
    eta = sp.Rational(1, 10)
    assert PI >= eta*SI
    assert sp.simplify(TI - (1-c0*eta)*SI) <= 0

    print("NS P2 holonomy window packing fixture")
    print("S_I =", SI)
    print("P_I =", PI)
    print("T_I =", TI)
    print("H_I =", HI)
    print("c0 =", c0)
    print("eta =", eta)
    print("window tax exact: T_I = S_I - c0 P_I")
    print("integrated hitting cut: H_I <= 4 P_I")
    print("NS-P2 HOLONOMY WINDOW PACKING PASS")


if __name__ == "__main__":
    main()
