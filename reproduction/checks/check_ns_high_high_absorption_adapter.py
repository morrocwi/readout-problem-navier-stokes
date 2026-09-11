#!/usr/bin/env python3
"""Exact finite checker for the High--High absorption adapter interface.

This checker verifies only finite rational inequalities of the form
    T_plus <= eta * V_minus + rho_plus
and an optional finite-prefix weighted remainder budget.
It does NOT prove that the supplied bounds enclose the true PDE quantities and does NOT
extend a finite shell prefix to all shells. Those are explicit adapter obligations.
"""
from fractions import Fraction
import json


def verify_cell(eta: Fraction, T_plus: Fraction, V_minus: Fraction, rho_plus: Fraction) -> bool:
    if not (Fraction(0) <= eta < Fraction(1)):
        return False
    if V_minus < 0 or rho_plus < 0:
        return False
    return T_plus <= eta * V_minus + rho_plus


def weighted_remainder(prefix):
    total = Fraction(0)
    for weight, rho in prefix:
        if weight < 0 or rho < 0:
            raise ValueError("weights and remainders must be nonnegative")
        total += weight * rho
    return total


def main() -> int:
    eta = Fraction(3, 4)

    pass_cell = {
        "eta": eta,
        "T_plus": Fraction(7, 2),
        "V_minus": Fraction(4, 1),
        "rho_plus": Fraction(1, 2),
    }
    # 7/2 <= (3/4)*4 + 1/2 = 7/2, exact boundary acceptance.
    hold_cell = {
        "eta": eta,
        "T_plus": Fraction(18, 5),
        "V_minus": Fraction(4, 1),
        "rho_plus": Fraction(1, 2),
    }
    bad_eta = {
        "eta": Fraction(1, 1),
        "T_plus": Fraction(0),
        "V_minus": Fraction(1),
        "rho_plus": Fraction(0),
    }

    if not verify_cell(**pass_cell):
        raise AssertionError("valid absorption cell should PASS")
    if verify_cell(**hold_cell):
        raise AssertionError("insufficient absorption margin should HOLD")
    if verify_cell(**bad_eta):
        raise AssertionError("eta>=1 must HOLD")

    prefix = [
        (Fraction(1), Fraction(1, 100)),
        (Fraction(4), Fraction(1, 400)),
        (Fraction(16), Fraction(1, 3200)),
    ]
    remainder = weighted_remainder(prefix)
    declared_budget = Fraction(3, 100)
    if remainder > declared_budget:
        raise AssertionError("finite weighted remainder budget exceeded")

    # Negative control: a finite prefix says nothing about an omitted tail by itself.
    # We encode this as metadata rather than pretending the checker can infer an infinite sum.
    result = {
        "cell_pass": True,
        "cell_hold": True,
        "eta_guard": True,
        "finite_prefix_weighted_remainder": str(remainder),
        "declared_prefix_budget": str(declared_budget),
        "finite_prefix_within_budget": remainder <= declared_budget,
        "all_shell_extension": "NOT_PROVED_BY_THIS_CHECKER",
        "continuum_adapter_hypothesis": "NOT_PROVED_BY_THIS_CHECKER",
        "scope": "exact finite arithmetic interface only; enclosure soundness, shell/time coverage, and all-shell summability remain separate obligations",
    }
    print("NS High-High absorption adapter exact finite checker")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS HIGH-HIGH ADAPTER FINITE CHECKER PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
