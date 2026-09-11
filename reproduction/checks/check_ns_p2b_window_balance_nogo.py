#!/usr/bin/env python3
"""Exact integrated shell-accounting countermodel for P2B.

The model satisfies integrated shell balances, integrated nonlinear-transfer
conservation, and finite cumulative energy/dissipation/time budgets while retaining
critical observation scaling. It is NOT claimed to be realizable by the full NSE
triad dynamics.
"""
from fractions import Fraction
import json


def main() -> int:
    p = 4
    transfer_sum = Fraction(0)
    high_diss_sum = Fraction(0)
    reservoir_diss_sum = Fraction(0)
    duration_sum = Fraction(0)
    reservoir_depletion = Fraction(0)
    rows = []

    # Choose 2*nu = 1. Shell index s_j = N_j^2.
    for j in range(1, 13):
        N = 2 ** j
        s = N * N
        I = Fraction(1, N)
        delta = Fraction(1, N * N)
        high_diss = Fraction(s) * I * delta  # = 1/N
        Q_high = high_diss
        delta_I_high = Fraction(0)

        if delta_I_high != Q_high - high_diss:
            raise AssertionError("high-shell integrated balance failed")

        Q_res = -Q_high
        res_diss = Fraction(1, N * N)
        delta_I_res = Q_res - res_diss
        if delta_I_res != Q_res - res_diss:
            raise AssertionError("reservoir integrated balance failed")
        if Q_high + Q_res != 0:
            raise AssertionError("integrated nonlinear transfer not conservative")

        A = Fraction(s) * I  # H1-squared amplitude = N
        k2_power_p = (A ** p) * delta
        Lambda = s
        if k2_power_p != Lambda:
            raise AssertionError("p=4 critical observation identity failed")

        transfer_sum += Q_high + Q_res
        high_diss_sum += high_diss
        reservoir_diss_sum += res_diss
        duration_sum += delta
        reservoir_depletion += -delta_I_res

        rows.append({
            "j": j,
            "N": N,
            "shell_s": s,
            "I_high": str(I),
            "duration": str(delta),
            "Q_high": str(Q_high),
            "Q_reservoir": str(Q_res),
            "high_viscous_loss": str(high_diss),
            "reservoir_viscous_loss": str(res_diss),
            "reservoir_energy_decrement": str(-delta_I_res),
            "K2_power_p_over_Lambda": str(k2_power_p / Lambda),
        })

    if transfer_sum != 0:
        raise AssertionError("global integrated transfer must cancel")
    if not (high_diss_sum < 1 and reservoir_diss_sum < Fraction(1, 3) and duration_sum < Fraction(1, 3)):
        raise AssertionError("finite-prefix budgets should remain below convergent infinite totals")
    # Infinite reservoir depletion is sum 2^-j + 4^-j = 1 + 1/3 = 4/3.
    if not reservoir_depletion < Fraction(4, 3):
        raise AssertionError("finite reservoir depletion prefix exceeds infinite budget")

    result = {
        "p": p,
        "two_nu": "1",
        "integrated_transfer_total": str(transfer_sum),
        "high_dissipation_prefix": str(high_diss_sum),
        "reservoir_dissipation_prefix": str(reservoir_diss_sum),
        "duration_prefix": str(duration_sum),
        "reservoir_depletion_prefix": str(reservoir_depletion),
        "infinite_reservoir_depletion": "4/3",
        "critical_ratio": "(K_N^2)^4/Lambda_N = 1 at every tested scale",
        "full_nse_triad_realizability": "NOT_CLAIMED",
        "ruling": "window balance + transfer conservation + finite budgets do not imply strict scale contraction",
        "rows": rows,
    }
    print("NS P2B integrated window-balance no-go control")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS P2B WINDOW-BALANCE ACCOUNTING NO-GO PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
