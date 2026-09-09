#!/usr/bin/env python3
"""
Finite readout-sufficiency witness for the NS retained-shell state.

The exact 3D check in check_volume6_ns_exact.py defines

    I_j(u)      = 1/2 sum_{|k|^2=q_j} |u_hat_k|^2,
    eta_NS,j(u) = -Re sum_{|k|^2=q_j} conj(u_hat_k) . N_hat_k(u),

where N_hat is the Leray-projected Fourier transform of (u.grad)u.

This script asks the next question without proposing any closure:

    does I(u)=I(v) force eta_NS(u)=eta_NS(v)?

If not, then there is no exact autonomous map Gamma on this retained state alone with

    eta_NS = Gamma(I)

on the whole finite admissible state space.

Construction:
1. Generate two independent real 3D fields.
2. Fourier transform, 2/3-dealias, and Leray-project them.
3. Normalize the second field shell-by-shell so its complete retained shell-energy vector
   agrees with the first.
4. Read eta_NS from the actual projected nonlinear NS term for both fields.

Shellwise scalar rescaling preserves conjugate symmetry and divergence freedom, while it
does not preserve triadic phase/orientation information.  The test therefore isolates a
readout-information question rather than introducing a new dynamical law.

Tier: finite_diagnostic.  This is a finite floating-point witness.  It does not say that no
useful approximate/stochastic/history-dependent closure exists, and it does not address a
continuum singularity.
"""
from __future__ import annotations

import json
import sys

import numpy as np

from check_volume6_ns_exact import (
    build_grid,
    fft3,
    project_divfree,
    rhs_terms,
    shell_ids,
)


def random_admissible_state(n: int, seed: int, target_energy: float = 0.125):
    _, _, _, KX, KY, KZ, K2, dealias = build_grid(n)
    rng = np.random.default_rng(seed)

    # A real physical-space field gives conjugate-symmetric Fourier coefficients.
    u = rng.normal(size=(3, n, n, n))
    u_hat = fft3(u) * dealias[None, ...]
    u_hat = project_divfree(u_hat, KX, KY, KZ, K2)
    u_hat[:, K2 == 0] = 0.0

    energy = 0.5 * np.sum(np.abs(u_hat) ** 2)
    u_hat *= np.sqrt(target_energy / energy)
    return u_hat, (KX, KY, KZ, K2, dealias)


def shell_energy(u_hat, K2, dealias, shells):
    return np.asarray(
        [
            0.5 * np.sum(np.abs(u_hat[:, dealias & (K2 == q)]) ** 2)
            for q in shells
        ],
        dtype=float,
    )


def match_shell_energy(source, target, K2, dealias, shells):
    """Rescale target shell-by-shell so I(target)=I(source), in exact arithmetic."""
    I_source = shell_energy(source, K2, dealias, shells)
    I_target = shell_energy(target, K2, dealias, shells)
    out = target.copy()

    for i, q in enumerate(shells):
        mask = dealias & (K2 == q)
        if I_source[i] == 0.0:
            out[:, mask] = 0.0
        elif I_target[i] > 0.0:
            out[:, mask] *= np.sqrt(I_source[i] / I_target[i])
        else:
            raise RuntimeError("target has zero energy in a shell that source retains")

    return out


def nonlinear_tape(u_hat, nu, KX, KY, KZ, K2, dealias, shells):
    _, N_hat, _, _ = rhs_terms(u_hat, nu, KX, KY, KZ, K2, dealias)
    return np.asarray(
        [
            -np.real(
                np.sum(
                    np.conj(u_hat[:, dealias & (K2 == q)])
                    * N_hat[:, dealias & (K2 == q)]
                )
            )
            for q in shells
        ],
        dtype=float,
    )


def max_fourier_divergence(u_hat, KX, KY, KZ):
    div = KX * u_hat[0] + KY * u_hat[1] + KZ * u_hat[2]
    return float(np.max(np.abs(div)))


def run_case(n: int = 16, nu: float = 0.005):
    u_a, ctx = random_admissible_state(n=n, seed=10)
    u_b0, _ = random_admissible_state(n=n, seed=11)
    KX, KY, KZ, K2, dealias = ctx
    shells = shell_ids(K2, dealias)

    u_b = match_shell_energy(u_a, u_b0, K2, dealias, shells)

    I_a = shell_energy(u_a, K2, dealias, shells)
    I_b = shell_energy(u_b, K2, dealias, shells)
    eta_a = nonlinear_tape(u_a, nu, KX, KY, KZ, K2, dealias, shells)
    eta_b = nonlinear_tape(u_b, nu, KX, KY, KZ, K2, dealias, shells)

    max_I_difference = float(np.max(np.abs(I_a - I_b)))
    eta_difference = float(np.linalg.norm(eta_a - eta_b))
    eta_a_norm = float(np.linalg.norm(eta_a))
    relative_eta_difference = eta_difference / max(eta_a_norm, 1e-30)
    transfer_defect_a = float(abs(np.sum(eta_a)))
    transfer_defect_b = float(abs(np.sum(eta_b)))
    div_a = max_fourier_divergence(u_a, KX, KY, KZ)
    div_b = max_fourier_divergence(u_b, KX, KY, KZ)

    order = np.argsort(np.abs(eta_a - eta_b))[::-1]
    largest_differences = [
        {
            "k2": shells[i],
            "I": float(I_a[i]),
            "eta_A": float(eta_a[i]),
            "eta_B": float(eta_b[i]),
            "delta_eta": float(eta_b[i] - eta_a[i]),
        }
        for i in order[:10]
    ]

    return {
        "n": n,
        "nu": nu,
        "shell_count": len(shells),
        "max_shell_energy_difference": max_I_difference,
        "eta_A_norm": eta_a_norm,
        "eta_difference_norm": eta_difference,
        "relative_eta_difference": relative_eta_difference,
        "total_transfer_defect_A": transfer_defect_a,
        "total_transfer_defect_B": transfer_defect_b,
        "max_divergence_A": div_a,
        "max_divergence_B": div_b,
        "largest_shell_tape_differences": largest_differences,
    }


def main() -> int:
    report = run_case()

    same_readout = report["max_shell_energy_difference"] < 1e-14
    different_tape = report["relative_eta_difference"] > 1e-2
    conservative_a = report["total_transfer_defect_A"] < 1e-12
    conservative_b = report["total_transfer_defect_B"] < 1e-12
    admissible = (
        report["max_divergence_A"] < 1e-12
        and report["max_divergence_B"] < 1e-12
    )

    print("[same retained shell state, different nonlinear tape]")
    print(
        "  max_j |I_A,j - I_B,j| = "
        f"{report['max_shell_energy_difference']:.3e}"
    )
    print(
        "  ||eta_A - eta_B|| / ||eta_A|| = "
        f"{report['relative_eta_difference']:.6f}"
    )
    print(
        "  |sum eta_A|, |sum eta_B| = "
        f"{report['total_transfer_defect_A']:.3e}, "
        f"{report['total_transfer_defect_B']:.3e}"
    )
    print(
        "  max divergence A, B = "
        f"{report['max_divergence_A']:.3e}, {report['max_divergence_B']:.3e}"
    )
    print("  largest shell tape differences:")
    for row in report["largest_shell_tape_differences"]:
        print(
            f"    k^2={row['k2']:>3d} I={row['I']:.6e} "
            f"eta_A={row['eta_A']:+.6e} eta_B={row['eta_B']:+.6e} "
            f"delta={row['delta_eta']:+.6e}"
        )

    witness_ok = same_readout and different_tape and conservative_a and conservative_b and admissible

    claims = [
        {
            "id": "Vol6-NSReadout-same-I-different-eta",
            "name": "Finite witness: identical shell-energy readout does not determine the exact nonlinear NS tape",
            "tier": "finite_diagnostic",
            "status": "PASS" if witness_ok else "FAIL",
            "evidence": (
                f"max shell-energy mismatch={report['max_shell_energy_difference']:.3e}; "
                f"relative tape difference={report['relative_eta_difference']:.6f}; "
                "both states remain divergence-free and each nonlinear tape conserves total energy"
            ),
        },
        {
            "id": "Vol6-NSReadout-no-global-Gamma-I",
            "name": "No exact global autonomous map eta_NS = Gamma(I) for shell-energy I alone on the tested finite state class",
            "tier": "finite_diagnostic",
            "status": "PASS" if witness_ok else "FAIL",
            "evidence": (
                "the constructed pair has the same complete retained shell-energy vector but "
                "different exact NS nonlinear tapes; a single-valued Gamma(I) cannot return both"
            ),
        },
        {
            "id": "Vol6-NSReadout-next-state",
            "name": "Minimal richer retained state sufficient to determine eta_NS",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the witness only proves shell energies are insufficient; it does not yet identify "
                "the minimal additional phase/triad/history distinctions required"
            ),
        },
    ]

    print("REPORT_JSON:" + json.dumps(report, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))
    return 0 if witness_ok else 1


if __name__ == "__main__":
    sys.exit(main())
