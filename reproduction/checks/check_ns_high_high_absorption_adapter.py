#!/usr/bin/env python3
"""Exact finite checker for the High--High absorption adapter interface.

This checker verifies only finite rational inequalities of the form
    T_plus <= eta * V_minus + rho_plus
and an optional finite-prefix weighted remainder budget.

The generic interface accepts a declared strict eta_cap<=1. The independently
audited mapping to the current Inage preprint uses eta_cap=3/4 because the proof
text requires eta < 3 c0/4 and the displayed dyadic normalization permits c0=1.

It does NOT prove that the supplied bounds enclose true PDE quantities, extend a
finite shell prefix to all shells, or validate the external continuum theorem.
"""
from fractions import Fraction
import json


def verify_cell(eta: Fraction, T_plus: Fraction, V_minus: Fraction,
                rho_plus: Fraction, eta_cap: Fraction = Fraction(1)) -> bool:
    if not (Fraction(0) < eta_cap <= Fraction(1)):
        return False
    if not (Fraction(0) <= eta < eta_cap):
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
    audited_eta_cap = Fraction(3, 4)
    eta = Fraction(2, 3)

    pass_cell = {
        "eta": eta,
        "T_plus": Fraction(19, 6),
        "V_minus": Fraction(4, 1),
        "rho_plus": Fraction(1, 2),
        "eta_cap": audited_eta_cap,
    }
    # 19/6 <= (2/3)*4 + 1/2 = 19/6, exact boundary acceptance.
    hold_cell = dict(pass_cell)
    hold_cell["T_plus"] = Fraction(16, 5)

    if not verify_cell(**pass_cell):
        raise AssertionError("valid audited absorption cell should PASS")
    if verify_cell(**hold_cell):
        raise AssertionError("insufficient absorption margin should HOLD")

    # Mapping-specific negative controls.
    if verify_cell(Fraction(3, 4), Fraction(0), Fraction(1), Fraction(0), audited_eta_cap):
        raise AssertionError("eta at audited cap must HOLD")
    if verify_cell(Fraction(9, 10), Fraction(0), Fraction(1), Fraction(0), audited_eta_cap):
        raise AssertionError("eta above audited cap must HOLD")

    prefix = [
        (Fraction(1), Fraction(1, 100)),
        (Fraction(4), Fraction(1, 400)),
        (Fraction(16), Fraction(1, 3200)),
    ]
    remainder = weighted_remainder(prefix)
    declared_budget = Fraction(3, 100)
    if remainder > declared_budget:
        raise AssertionError("finite weighted remainder budget exceeded")

    result = {
        "cell_pass": True,
        "cell_hold": True,
        "audited_eta_cap": str(audited_eta_cap),
        "eta_guard": True,
        "finite_prefix_weighted_remainder": str(remainder),
        "declared_prefix_budget": str(declared_budget),
        "finite_prefix_within_budget": remainder <= declared_budget,
        "all_shell_extension": "NOT_PROVED_BY_THIS_CHECKER",
        "external_preprint_adapter": "HOLD_PENDING_CORRECTED_CONTINUUM_CLOSURE",
        "continuum_adapter_hypothesis": "NOT_PROVED_BY_THIS_CHECKER",
        "scope": "exact finite arithmetic interface only; external continuum theorem is not validated here",
    }
    print("NS High-High absorption adapter exact finite checker")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS HIGH-HIGH ADAPTER FINITE CHECKER PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
