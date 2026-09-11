#!/usr/bin/env python3
"""Exact interface control for NS-P2B-EPSC-OBS-LIFT.

The analytic theorem is
    K_N(u) <= K_N(v) + tau^(1/(2p)) sqrt(Lambda_N) * eps.
This exact calibration chooses tau=1 and Lambda_N=N^2 so no irrational
arithmetic is needed. It deliberately does not emit the external published
regularity gate as PASS because that paper's absolute constant has not been
pinned into this repository.
"""
from fractions import Fraction
import json


def exact_lift(K_v: Fraction, eps: Fraction, N: int, tau_root: Fraction) -> Fraction:
    if K_v < 0 or eps < 0 or N < 1 or tau_root < 0:
        raise ValueError("nonnegative certificate inputs required")
    # sqrt(Lambda_N)=N in this calibration; tau_root=tau^(1/(2p)).
    return K_v + tau_root * N * eps


def main() -> int:
    p = 4
    N = 16
    Lambda_N = N * N
    tau0 = Fraction(1)
    tau_root = Fraction(1)  # 1^(1/8)
    K_v = Fraction(3, 10)
    eps = Fraction(1, 100 * N)

    K_u_upper = exact_lift(K_v, eps, N, tau_root)
    if K_u_upper != Fraction(31, 100):
        raise AssertionError("unexpected exact observation lift")

    # Monotonicity / fail-closed controls.
    if exact_lift(K_v, 2 * eps, N, tau_root) <= K_u_upper:
        raise AssertionError("larger continuum error must not improve the bound")
    if exact_lift(K_v, eps, 2 * N, tau_root) <= K_u_upper:
        raise AssertionError("larger retained eigenvalue scale must not improve the bound")

    result = {
        "p": p,
        "N": N,
        "Lambda_N": Lambda_N,
        "tau0": str(tau0),
        "K_v_upper": str(K_v),
        "eps_Linf_L2": str(eps),
        "projected_H1_error_term": str(tau_root * N * eps),
        "K_u_upper": str(K_u_upper),
        "lift_status": "PASS exact finite interface calibration",
        "external_adapter_constant": "UNPINNED",
        "external_regularization_gate": "HOLD until a valid explicit constant/normalization is audited for per-instance execution",
        "asymptotic_reduction": "does not require the numerical value of a fixed finite adapter constant",
        "scope": "finite-tape-to-finite-observation upper-bound interface only",
    }
    print("NS P2B finite-observation lift exact control")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("NS P2B FINITE-OBSERVATION LIFT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
