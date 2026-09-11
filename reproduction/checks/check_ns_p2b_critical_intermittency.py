#!/usr/bin/env python3
"""Exact controls for the P2B energy-budget criticality no-go.

This constructs an abstract dyadic budget sequence. It is NOT an NSE solution.
It tests only whether the standard L-infinity_t L2 and L2_t H1 budgets alone
force subcritical finite-observation scaling. They do not.
"""
from fractions import Fraction
import json


def main() -> int:
    p = 4
    rows = []
    energy_sum = Fraction(0)
    diss_sum = Fraction(0)

    for j in range(1, 13):
        N = 2 ** j
        lam = N * N
        e = Fraction(1, N)
        A = Fraction(N, 1)
        delta = Fraction(1, N * N)
        # For p=4: (K_N^2)^4 = A^4 * delta.
        k2_fourth = (A ** p) * delta
        if A != lam * e:
            raise AssertionError("H1 amplitude relation A = Lambda * e failed")
        if A * delta != e:
            raise AssertionError("dissipation cost should equal 1/N")
        if k2_fourth != lam:
            raise AssertionError("critical observation scaling identity failed")
        energy_sum += e
        diss_sum += A * delta
        rows.append({
            "j": j,
            "N": N,
            "Lambda": lam,
            "energy_cost": str(e),
            "dissipation_cost": str(A * delta),
            "K2_power_p": str(k2_fourth),
            "K2_power_p_over_Lambda": str(k2_fourth / lam),
        })

    # Infinite sums from j=1 are exactly 1; finite prefixes must stay below 1.
    if not (energy_sum < 1 and diss_sum < 1):
        raise AssertionError("finite budget prefix should be below the convergent total")

    result = {
        "p": p,
        "finite_prefix_energy_sum": str(energy_sum),
        "finite_prefix_dissipation_sum": str(diss_sum),
        "infinite_energy_budget": "sum_{j>=1} 2^-j = 1",
        "infinite_dissipation_budget": "sum_{j>=1} 2^-j = 1",
        "critical_identity": "(K_N^2)^p = Lambda_N for every tested dyadic scale",
        "subcritical_sigma_from_energy_only": "NOT_PROVED; abstract budget reaches sigma=0 exactly",
        "nse_solution_claim": "NONE",
        "scope": "no-go for inference from energy+dissipation budgets alone",
        "rows": rows,
    }
    print("NS P2B critical-intermittency exact control")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS P2B ENERGY-CRITICAL NO-GO PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
