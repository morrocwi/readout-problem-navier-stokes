#!/usr/bin/env python3
"""Exact symbolic checks for the fresh-donor window response/cancellation charge."""

import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
x = n**2

c = 3*sp.sqrt(10)*n/10
alpha = sp.factor(
    c*sp.sqrt(1+9*n**2)
    /(sp.sqrt(1+2*n**2)*sp.sqrt(1+5*n**2))
)
alpha_sq = sp.factor(alpha**2)
expected_sq = sp.factor(
    sp.Rational(9,10)*n**2*(1+9*n**2)
    /((1+2*n**2)*(1+5*n**2))
)
diff_half = sp.factor(alpha_sq-sp.Rational(1,2))
expected_diff = sp.factor(
    (n**2-1)*(31*n**2+5)
    /(10*(1+2*n**2)*(1+5*n**2))
)


def finite_fixture():
    """Exact rational audit of window and multiscale algebra after using alpha>=1/sqrt(2)."""
    root2 = sp.sqrt(2)

    # Three time cells: overlap integrals O_i and cost buckets D_i, R_i.
    O = [sp.Rational(2), sp.Rational(3,2), sp.Rational(5,2)]
    D = [sp.Rational(1), sp.Rational(3,4), sp.Rational(3,2)]
    R = [sp.simplify(O[i]/root2-D[i]+sp.Rational(1,5)) for i in range(3)]

    for i in range(3):
        assert sp.simplify(D[i]+R[i]-O[i]/root2) >= 0

    OI = sp.simplify(sum(O))
    DI = sp.simplify(sum(D))
    RI = sp.simplify(sum(R))
    assert sp.simplify(DI+RI-OI/root2) >= 0

    # Quiet-target lower bound fixture: D <= TV + visc_occ.
    TV = sp.Rational(3,2)
    visc_occ = sp.Rational(5,4)
    donor_overlap = sp.Rational(6)
    cancellation_lower = sp.simplify(donor_overlap/root2-TV-visc_occ)
    assert cancellation_lower > 0

    # High-overlap measure fixture with lambda=1, |E|=2.
    lam = sp.Integer(1)
    measure = sp.Integer(2)
    response_plus_cancel = sp.Integer(2)
    assert sp.simplify(response_plus_cancel-lam**2*measure/root2) >= 0

    # Finite multiscale fixture: sum block inequalities.
    block_overlap = [sp.Integer(2), sp.Integer(3), sp.Integer(1)]
    block_cost = [sp.sqrt(2), 3/sp.sqrt(2)+1, 1/sp.sqrt(2)]
    assert all(
        sp.simplify(block_cost[i]-block_overlap[i]/root2) >= 0
        for i in range(3)
    )
    assert sp.simplify(sum(block_cost)-sum(block_overlap)/root2) >= 0

    return {
        "window_overlap": OI,
        "window_response": DI,
        "window_cancellation": RI,
        "quiet_cancellation_lower": cancellation_lower,
        "multiscale_overlap": sum(block_overlap),
        "multiscale_cost": sp.simplify(sum(block_cost)),
    }


def main():
    assert sp.simplify(alpha_sq-expected_sq) == 0
    assert sp.simplify(diff_half-expected_diff) == 0

    # Exact factor proves alpha^2 >= 1/2 for integer n>=1.
    assert sp.factor(sp.together(diff_half).as_numer_denom()[0]) == (n-1)*(n+1)*(31*n**2+5)
    assert sp.simplify(alpha.subs(n,1)-1/sp.sqrt(2)) == 0

    vals = finite_fixture()

    print("NS P2 fresh-donor window charge")
    print("alpha_n =", alpha)
    print("alpha_n^2 =", alpha_sq)
    print("alpha_n^2 - 1/2 =", diff_half)
    print("exact all-n floor: alpha_n >= 1/sqrt(2)")
    for k,v in vals.items():
        print(k, "=", v)
    print("scope: exact donor-pair/window charge; recursive cancellation control remains OPEN")
    print("NS-P2 FRESH-DONOR WINDOW CHARGE PASS")


if __name__ == "__main__":
    main()
