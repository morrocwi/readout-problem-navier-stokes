#!/usr/bin/env python3
"""Exact finite controls for NS-P2B-SCALE-CONTRACTION.

The finite run calibrates the recurrence algebra and its critical-spike falsifier.
It does not prove that actual NSE observations satisfy the recurrence at all scales.
"""
from fractions import Fraction
import json


def main() -> int:
    kappa = Fraction(1, 2)
    B = Fraction(1, 1)
    rho = Fraction(1, 4)
    U = Fraction(1, 1)
    rows = []

    for j in range(1, 13):
        beta = B * (rho ** j)
        U_next = kappa * U + beta
        if not (Fraction(0) <= kappa < 1):
            raise AssertionError("kappa guard failed")
        if not (Fraction(0) <= rho < 1):
            raise AssertionError("rho guard failed")
        if U_next > kappa * U + beta:
            raise AssertionError("recurrence failed")
        rows.append({
            "j": j,
            "U_in": str(U),
            "beta": str(beta),
            "U_out": str(U_next),
        })
        U = U_next

    if not U < Fraction(1, 100):
        raise AssertionError("calibrated strict contraction did not decay enough")

    # Critical-spike control: R_j = 1 cannot satisfy a strict kappa=1/2
    # recurrence with beta_j -> 0. It needs beta >= 1-kappa = 1/2.
    critical_required_beta = Fraction(1) - kappa
    if critical_required_beta != Fraction(1, 2):
        raise AssertionError("critical required defect calculation failed")
    for j in range(2, 8):
        beta = B * (rho ** j)
        if beta >= critical_required_beta:
            raise AssertionError("calibrated vanishing beta should not rescue critical R=1")

    result = {
        "kappa": str(kappa),
        "B": str(B),
        "rho": str(rho),
        "final_U_after_12_steps": str(U),
        "critical_R_sequence": "R_j=1",
        "critical_required_beta_lower_bound": str(critical_required_beta),
        "critical_sequence_with_vanishing_beta": "HOLD/FAILS strict contraction",
        "uniform_nse_contraction": "NOT_PROVED_BY_THIS_CHECKER",
        "scope": "exact recurrence algebra + critical-spike falsifier only",
        "rows": rows,
    }
    print("NS P2B scale-contraction exact controls")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS P2B SCALE-CONTRACTION CONTROL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
