#!/usr/bin/env python3
"""
Exact NS -> retained-state bridge check for Volume 6.

This script removes the synthetic eta_M(t) used by check_volume6.py for its generic
finite recurrence test and derives a retained nonlinear tape directly from a concrete
3D periodic Fourier-Galerkin Navier-Stokes trajectory.

Domain: [0,2*pi]^3.
State: divergence-free Fourier coefficients u_hat(k,t), 2/3 dealiased.
Initial data: Taylor-Green vortex.
Forcing: zero.

For each exact k^2 shell q_j, define

    I_j(t) = 1/2 * sum_{|k|^2=q_j} |u_hat_k(t)|^2.

The projected Navier-Stokes equation is

    d u_hat/dt = - P_k FFT[(u.grad)u] - nu |k|^2 u_hat.

Therefore, while the finite Galerkin trajectory is defined,

    d I_j/dt = T_j - D_j,

with

    T_j = - Re sum conj(u_hat_k) . N_hat_k,
    D_j = nu q_j sum |u_hat_k|^2 = 2 nu q_j I_j.

Thus the retained equation is not guessed:

    d I/dt + L_nu I = eta_NS,
    (L_nu)_{jj} = 2 nu q_j,
    eta_NS,j = T_j.

No autonomous closure eta_NS = Gamma(I) is fitted or asserted here.  eta_NS is the
exact finite nonlinear tape read from the resolved 3D Galerkin state.

Tier: finite_diagnostic.  This is a finite-resolution numerical identity check, not a
continuum singularity result and not evidence that eta_NS is an autonomous function of I.
"""
from __future__ import annotations

import json
import sys

import numpy as np


def wavenumbers(n: int) -> np.ndarray:
    # Grid x_l = 2*pi*l/n.  With d=1/n, fftfreq returns the integer Fourier modes.
    return np.fft.fftfreq(n, d=1.0 / n)


def build_grid(n: int):
    x = 2.0 * np.pi * np.arange(n) / n
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    k = wavenumbers(n)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    K2 = KX * KX + KY * KY + KZ * KZ

    # Standard 2/3 product-dealiasing mask.
    kc = n // 3
    dealias = (
        (np.abs(KX) <= kc)
        & (np.abs(KY) <= kc)
        & (np.abs(KZ) <= kc)
    )
    return X, Y, Z, KX, KY, KZ, K2, dealias


def fft3(v: np.ndarray) -> np.ndarray:
    # norm="forward" makes the stored coefficients the usual Fourier-series coefficients.
    return np.fft.fftn(v, axes=(-3, -2, -1), norm="forward")


def ifft3(v_hat: np.ndarray) -> np.ndarray:
    return np.fft.ifftn(v_hat, axes=(-3, -2, -1), norm="forward").real


def project_divfree(
    u_hat: np.ndarray,
    KX: np.ndarray,
    KY: np.ndarray,
    KZ: np.ndarray,
    K2: np.ndarray,
) -> np.ndarray:
    """Leray projection P_k = I - kk^T/|k|^2, mode by mode."""
    dot = KX * u_hat[0] + KY * u_hat[1] + KZ * u_hat[2]
    out = u_hat.copy()
    nz = K2 > 0
    out[0, nz] -= KX[nz] * dot[nz] / K2[nz]
    out[1, nz] -= KY[nz] * dot[nz] / K2[nz]
    out[2, nz] -= KZ[nz] * dot[nz] / K2[nz]
    return out


def taylor_green(n: int) -> np.ndarray:
    X, Y, Z, *_ = build_grid(n)
    u = np.empty((3, n, n, n), dtype=float)
    u[0] = np.sin(X) * np.cos(Y) * np.cos(Z)
    u[1] = -np.cos(X) * np.sin(Y) * np.cos(Z)
    u[2] = 0.0
    return u


def rhs_terms(
    u_hat: np.ndarray,
    nu: float,
    KX: np.ndarray,
    KY: np.ndarray,
    KZ: np.ndarray,
    K2: np.ndarray,
    dealias: np.ndarray,
):
    """Return total RHS, projected convection N_hat, viscous term, and forcing."""
    u = ifft3(u_hat)
    grad = np.empty((3, 3) + K2.shape, dtype=float)  # grad[j,i] = d_i u_j
    Ks = (KX, KY, KZ)
    for j in range(3):
        for i, Ki in enumerate(Ks):
            grad[j, i] = ifft3(1j * Ki * u_hat[j])

    conv = np.zeros_like(u)
    for j in range(3):
        for i in range(3):
            conv[j] += u[i] * grad[j, i]

    N_hat = fft3(conv)
    N_hat *= dealias[None, ...]
    N_hat = project_divfree(N_hat, KX, KY, KZ, K2)

    visc = -nu * K2[None, ...] * u_hat
    force = np.zeros_like(u_hat)
    total = -N_hat + visc + force
    total *= dealias[None, ...]
    return total, N_hat, visc, force


def shell_ids(K2: np.ndarray, dealias: np.ndarray) -> list[int]:
    values = np.unique(K2[dealias & (K2 > 0)].astype(int))
    return [int(v) for v in values]


def shell_readout(
    u_hat: np.ndarray,
    total: np.ndarray,
    N_hat: np.ndarray,
    visc: np.ndarray,
    force: np.ndarray,
    nu: float,
    K2: np.ndarray,
    dealias: np.ndarray,
    shells: list[int],
):
    I, dI, T, D, F, eta, residual = ([] for _ in range(7))

    for q in shells:
        mask = dealias & (K2 == q)
        abs2 = np.sum(np.abs(u_hat[:, mask]) ** 2)
        Ij = 0.5 * abs2

        # Differentiate I_j directly using the Fourier-space NS RHS.
        dIj = np.real(np.sum(np.conj(u_hat[:, mask]) * total[:, mask]))
        Tj = -np.real(np.sum(np.conj(u_hat[:, mask]) * N_hat[:, mask]))
        Dj = -np.real(np.sum(np.conj(u_hat[:, mask]) * visc[:, mask]))
        Fj = np.real(np.sum(np.conj(u_hat[:, mask]) * force[:, mask]))

        # Since q=|k|^2 is constant inside this shell:
        # D_j = nu*q*sum|u_hat|^2 = 2*nu*q*I_j.
        Lnu_Ij = 2.0 * nu * q * Ij
        eta_j = Tj

        # Exact retained balance for the unforced run:
        # dI_j + (L_nu I)_j - F_j - eta_j = 0.
        rj = dIj + Lnu_Ij - Fj - eta_j

        I.append(Ij)
        dI.append(dIj)
        T.append(Tj)
        D.append(Dj)
        F.append(Fj)
        eta.append(eta_j)
        residual.append(rj)

    return {
        "I": np.asarray(I, dtype=float),
        "dI": np.asarray(dI, dtype=float),
        "T": np.asarray(T, dtype=float),
        "D": np.asarray(D, dtype=float),
        "F": np.asarray(F, dtype=float),
        "eta": np.asarray(eta, dtype=float),
        "residual": np.asarray(residual, dtype=float),
    }


def rk4_step(
    u_hat: np.ndarray,
    dt: float,
    nu: float,
    KX: np.ndarray,
    KY: np.ndarray,
    KZ: np.ndarray,
    K2: np.ndarray,
    dealias: np.ndarray,
) -> np.ndarray:
    def R(x):
        return rhs_terms(x, nu, KX, KY, KZ, K2, dealias)[0]

    k1 = R(u_hat)
    k2 = R(u_hat + 0.5 * dt * k1)
    k3 = R(u_hat + 0.5 * dt * k2)
    k4 = R(u_hat + dt * k3)
    out = u_hat + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    out *= dealias[None, ...]
    return project_divfree(out, KX, KY, KZ, K2)


def run_case(n: int = 16, nu: float = 0.005, dt: float = 0.0025, t_end: float = 0.5):
    _, _, _, KX, KY, KZ, K2, dealias = build_grid(n)
    u_hat = fft3(taylor_green(n)) * dealias[None, ...]
    u_hat = project_divfree(u_hat, KX, KY, KZ, K2)
    shells = shell_ids(K2, dealias)
    steps = int(round(t_end / dt))

    rows = []
    max_identity = 0.0
    max_dissipation = 0.0
    max_transfer_sum = 0.0
    max_divergence = 0.0
    initial_energy = 0.5 * np.sum(np.abs(u_hat) ** 2)

    for step in range(steps + 1):
        total, N_hat, visc, force = rhs_terms(
            u_hat, nu, KX, KY, KZ, K2, dealias
        )
        readout = shell_readout(
            u_hat, total, N_hat, visc, force, nu, K2, dealias, shells
        )
        rows.append(readout)

        active = readout["I"] > 1e-18
        if np.any(active):
            max_identity = max(
                max_identity,
                float(np.max(np.abs(readout["residual"][active]))),
            )
            exact_D = 2.0 * nu * np.asarray(shells) * readout["I"]
            max_dissipation = max(
                max_dissipation,
                float(np.max(np.abs((readout["D"] - exact_D)[active]))),
            )

        # The incompressible convective term redistributes energy between shells.
        max_transfer_sum = max(
            max_transfer_sum, float(abs(np.sum(readout["T"])))
        )
        div = KX * u_hat[0] + KY * u_hat[1] + KZ * u_hat[2]
        max_divergence = max(max_divergence, float(np.max(np.abs(div))))

        if step < steps:
            u_hat = rk4_step(u_hat, dt, nu, KX, KY, KZ, K2, dealias)

    final_energy = 0.5 * np.sum(np.abs(u_hat) ** 2)

    # Independent time-stepping consistency check: centered finite differences of the
    # retained trajectory must approach the instantaneous dI read from the NS RHS.
    I_series = np.stack([r["I"] for r in rows])
    dI_series = np.stack([r["dI"] for r in rows])
    fd = (I_series[2:] - I_series[:-2]) / (2.0 * dt)
    denom = max(float(np.linalg.norm(dI_series[1:-1])), 1e-30)
    fd_relative_error = float(np.linalg.norm(fd - dI_series[1:-1]) / denom)

    last = rows[-1]
    active_idx = np.where(
        (last["I"] > 1e-14) | (np.abs(last["eta"]) > 1e-14)
    )[0]
    final_structure = [
        {
            "k2": shells[i],
            "I": float(last["I"][i]),
            "eta_NS": float(last["eta"][i]),
            "Lnu_I": float(2.0 * nu * shells[i] * last["I"][i]),
            "dI": float(last["dI"][i]),
        }
        for i in active_idx
    ]

    return {
        "n": n,
        "nu": nu,
        "dt": dt,
        "t_end": t_end,
        "steps": steps,
        "shell_count": len(shells),
        "max_divergence_fourier": max_divergence,
        "max_exact_shell_identity_residual": max_identity,
        "max_dissipation_formula_residual": max_dissipation,
        "max_nonlinear_total_transfer_defect": max_transfer_sum,
        "central_difference_relative_error": fd_relative_error,
        "initial_energy": float(initial_energy),
        "final_energy": float(final_energy),
        "final_structure": final_structure,
    }


def main() -> int:
    report = run_case()

    identity_ok = report["max_exact_shell_identity_residual"] < 1e-12
    dissipation_ok = report["max_dissipation_formula_residual"] < 1e-12
    transfer_ok = report["max_nonlinear_total_transfer_defect"] < 1e-12
    divergence_ok = report["max_divergence_fourier"] < 1e-12
    trajectory_ok = report["central_difference_relative_error"] < 1e-4

    print("[NS -> retained shell bridge]")
    print(
        "  max |dI + L_nu I - eta_NS| = "
        f"{report['max_exact_shell_identity_residual']:.3e}"
    )
    print(
        "  max |D - 2 nu k^2 I| = "
        f"{report['max_dissipation_formula_residual']:.3e}"
    )
    print(
        "  max |sum_j eta_NS,j| = "
        f"{report['max_nonlinear_total_transfer_defect']:.3e}"
    )
    print(
        "  max |k.u_hat| = "
        f"{report['max_divergence_fourier']:.3e}"
    )
    print(
        "  centered-difference relative error for dI = "
        f"{report['central_difference_relative_error']:.3e}"
    )
    print(
        f"  total retained energy: {report['initial_energy']:.12f} -> "
        f"{report['final_energy']:.12f}"
    )
    print("  final active shell structure:")
    for row in report["final_structure"]:
        print(
            f"    k^2={row['k2']:>3d}  I={row['I']:.6e}  "
            f"eta_NS={row['eta_NS']:+.6e}  LnuI={row['Lnu_I']:.6e}  "
            f"dI={row['dI']:+.6e}"
        )

    claims = [
        {
            "id": "Vol6-NSExact-shell-balance",
            "name": "3D Fourier-Galerkin shell identity dI/dt + L_nu I = eta_NS",
            "tier": "finite_diagnostic",
            "status": "PASS" if identity_ok else "FAIL",
            "evidence": (
                "eta_NS is read directly from the projected nonlinear Navier-Stokes term; "
                f"max shell residual={report['max_exact_shell_identity_residual']:.3e}"
            ),
        },
        {
            "id": "Vol6-NSExact-viscous-operator",
            "name": "Exact shell viscous operator (L_nu)jj = 2 nu |k|^2 on exact k^2 shells",
            "tier": "finite_diagnostic",
            "status": "PASS" if dissipation_ok else "FAIL",
            "evidence": (
                "shells are grouped by exact integer |k|^2, so the viscous contribution "
                f"factorizes; max residual={report['max_dissipation_formula_residual']:.3e}"
            ),
        },
        {
            "id": "Vol6-NSExact-transfer-conservation",
            "name": "Dealiased nonlinear retained tape conserves total kinetic energy",
            "tier": "finite_diagnostic",
            "status": "PASS" if transfer_ok else "FAIL",
            "evidence": (
                "the projected convective term only redistributes energy between retained shells; "
                f"max |sum_j eta_NS,j|={report['max_nonlinear_total_transfer_defect']:.3e}"
            ),
        },
        {
            "id": "Vol6-NSExact-divergence-free",
            "name": "Fourier trajectory remains divergence-free under the Leray projection",
            "tier": "finite_diagnostic",
            "status": "PASS" if divergence_ok else "FAIL",
            "evidence": f"max |k.u_hat|={report['max_divergence_fourier']:.3e}",
        },
        {
            "id": "Vol6-NSExact-trajectory-consistency",
            "name": "Retained dI from the NS RHS agrees with the evolved retained trajectory",
            "tier": "finite_diagnostic",
            "status": "PASS" if trajectory_ok else "FAIL",
            "evidence": (
                "centered finite-difference readout compared with instantaneous RHS readout; "
                f"relative error={report['central_difference_relative_error']:.3e}"
            ),
        },
        {
            "id": "Vol6-NSExact-autonomous-closure",
            "name": "Autonomous closure eta_NS = Gamma(I)",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "not fitted or asserted: this check derives the exact nonlinear tape from the "
                "resolved 3D state only; autonomy/identifiability requires additional tests"
            ),
        },
        {
            "id": "Vol6-NSExact-continuum-singularity",
            "name": "Inference from the finite retained trajectory to a continuum singularity",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "explicitly outside scope: the deterministic N=16 Galerkin run is a finite "
                "diagnostic and does not establish continuum breakdown or regularity"
            ),
        },
    ]

    print("REPORT_JSON:" + json.dumps(report, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))

    active_checks = [c for c in claims if c["status"] in ("PASS", "FAIL")]
    return 0 if all(c["status"] == "PASS" for c in active_checks) else 1


if __name__ == "__main__":
    sys.exit(main())
