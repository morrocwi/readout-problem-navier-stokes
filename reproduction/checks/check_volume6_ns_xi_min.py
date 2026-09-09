#!/usr/bin/env python3
"""
NS triad lineage + exact-readout quotient diagnostics.

This check does NOT fit a closure.

It verifies three structural facts on a finite 3D Fourier-Galerkin Navier-Stokes state:

1) The nonlinear retained tape is the exact ordered-triad sum
       eta_j = sum_{k in K_j} sum_{p+q=k} Theta_{k,p,q}
   with
       Theta_{k,p,q} = -Re[ conj(u_k) . i (q . u_p) u_q ].
   Because u_k is divergence-free, the Leray projector may be omitted inside
   this scalar pairing.

2) Spatial translation is a genuine readout gauge:
       u_k -> exp(i k.a) u_k
   leaves shell energy, every triad transfer, eta, and the future shell-energy
   trajectory invariant.

3) Therefore phase information is not to be retained indiscriminately. The exact
   reduced state must quotient genuine readout symmetries while retaining
   phase/triad distinctions that change future readouts.

The abstract minimal dynamically sufficient state is defined in
reproduction/NS_MINIMAL_DYNAMIC_READOUT.md as future-readout equivalence.
This script supplies the finite NS-specific triad/gauge evidence only.

Tier: finite_diagnostic.
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
    rk4_step,
)


def random_admissible_state(n: int, seed: int = 42, target_energy: float = 0.125):
    _, _, _, KX, KY, KZ, K2, dealias = build_grid(n)
    rng = np.random.default_rng(seed)
    u = rng.normal(size=(3, n, n, n))
    u_hat = fft3(u) * dealias[None, ...]
    u_hat = project_divfree(u_hat, KX, KY, KZ, K2)
    u_hat[:, K2 == 0] = 0.0
    E = 0.5 * np.sum(np.abs(u_hat) ** 2)
    u_hat *= np.sqrt(target_energy / E)
    return u_hat, (KX, KY, KZ, K2, dealias)


def shell_energy(u_hat, K2, dealias, shells):
    return np.asarray([
        0.5 * np.sum(np.abs(u_hat[:, dealias & (K2 == q)]) ** 2)
        for q in shells
    ])


def pseudospectral_eta(u_hat, ctx, nu: float, shells):
    KX, KY, KZ, K2, dealias = ctx
    _, N_hat, _, _ = rhs_terms(u_hat, nu, KX, KY, KZ, K2, dealias)
    return np.asarray([
        -np.real(np.sum(
            np.conj(u_hat[:, dealias & (K2 == q)])
            * N_hat[:, dealias & (K2 == q)]
        ))
        for q in shells
    ])


def integer_mode_index(n: int):
    kvals = np.fft.fftfreq(n, d=1.0 / n).astype(int)
    return {int(k): i for i, k in enumerate(kvals)}


def active_modes(KX, KY, KZ, K2, dealias):
    out = []
    for i, j, l in zip(*np.where(dealias & (K2 > 0))):
        out.append((int(KX[i, j, l]), int(KY[i, j, l]), int(KZ[i, j, l])))
    return out


def triad_eta(u_hat, ctx, shells):
    """Direct ordered-triad convolution; no closure and no fitted coefficients."""
    KX, KY, KZ, K2, dealias = ctx
    n = K2.shape[0]
    idx = integer_mode_index(n)
    modes = active_modes(KX, KY, KZ, K2, dealias)
    mode_set = set(modes)
    eta = {q: 0.0 for q in shells}

    for k in modes:
        ik = tuple(idx[a] for a in k)
        uk = u_hat[:, ik[0], ik[1], ik[2]]
        k2 = k[0] ** 2 + k[1] ** 2 + k[2] ** 2
        if k2 not in eta:
            continue

        for p in modes:
            qv = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
            if qv not in mode_set:
                continue
            ip = tuple(idx[a] for a in p)
            iq = tuple(idx[a] for a in qv)
            up = u_hat[:, ip[0], ip[1], ip[2]]
            uq = u_hat[:, iq[0], iq[1], iq[2]]

            conv_kpq = 1j * (
                qv[0] * up[0] + qv[1] * up[1] + qv[2] * up[2]
            ) * uq

            theta = -np.real(np.vdot(uk, conv_kpq))
            eta[k2] += float(theta)

    return np.asarray([eta[q] for q in shells])


def translate_fourier(u_hat, ctx, a):
    KX, KY, KZ, _, _ = ctx
    phase = np.exp(1j * (KX * a[0] + KY * a[1] + KZ * a[2]))
    return u_hat * phase[None, ...]


def shell_rollout(u_hat, ctx, nu, dt, steps, shells):
    KX, KY, KZ, K2, dealias = ctx
    x = u_hat.copy()
    rows = []
    for n in range(steps + 1):
        rows.append(shell_energy(x, K2, dealias, shells))
        if n < steps:
            x = rk4_step(x, dt, nu, KX, KY, KZ, K2, dealias)
    return np.stack(rows)


def main():
    n = 8
    nu = 0.005
    dt = 0.0025
    steps = 20

    u_hat, ctx = random_admissible_state(n=n)
    KX, KY, KZ, K2, dealias = ctx
    shells = shell_ids(K2, dealias)

    eta_ps = pseudospectral_eta(u_hat, ctx, nu, shells)
    eta_tri = triad_eta(u_hat, ctx, shells)
    triad_residual = float(np.max(np.abs(eta_ps - eta_tri)))
    transfer_defect = float(abs(np.sum(eta_tri)))

    a = np.asarray([0.37, -0.21, 0.44])
    u_shift = translate_fourier(u_hat, ctx, a)

    I = shell_energy(u_hat, K2, dealias, shells)
    I_shift = shell_energy(u_shift, K2, dealias, shells)
    eta_shift = pseudospectral_eta(u_shift, ctx, nu, shells)
    eta_tri_shift = triad_eta(u_shift, ctx, shells)

    shell_translation_defect = float(np.max(np.abs(I - I_shift)))
    eta_translation_defect = float(np.max(np.abs(eta_ps - eta_shift)))
    triad_translation_defect = float(np.max(np.abs(eta_tri - eta_tri_shift)))

    traj = shell_rollout(u_hat, ctx, nu, dt, steps, shells)
    traj_shift = shell_rollout(u_shift, ctx, nu, dt, steps, shells)
    future_readout_translation_defect = float(np.max(np.abs(traj - traj_shift)))

    div = KX * u_hat[0] + KY * u_hat[1] + KZ * u_hat[2]
    max_div = float(np.max(np.abs(div)))

    triad_ok = triad_residual < 1e-12
    conservative_ok = transfer_defect < 1e-12
    gauge_ok = max(
        shell_translation_defect,
        eta_translation_defect,
        triad_translation_defect,
        future_readout_translation_defect,
    ) < 1e-12
    admissible_ok = max_div < 1e-12

    report = {
        "n": n,
        "nu": nu,
        "dt": dt,
        "steps": steps,
        "shell_count": len(shells),
        "max_triad_vs_pseudospectral_eta_residual": triad_residual,
        "nonlinear_total_transfer_defect": transfer_defect,
        "translation_shell_readout_defect": shell_translation_defect,
        "translation_eta_defect": eta_translation_defect,
        "translation_individual_triad_sum_defect": triad_translation_defect,
        "translation_future_shell_readout_defect": future_readout_translation_defect,
        "max_fourier_divergence": max_div,
    }

    print("[NS triad lineage]")
    print(f"  max |eta_triad - eta_pseudospectral| = {triad_residual:.3e}")
    print(f"  |sum eta_triad| = {transfer_defect:.3e}")
    print("[translation readout gauge]")
    print(f"  max |I(T_a u)-I(u)| = {shell_translation_defect:.3e}")
    print(f"  max |eta(T_a u)-eta(u)| = {eta_translation_defect:.3e}")
    print(f"  max |triad-sum(T_a u)-triad-sum(u)| = {triad_translation_defect:.3e}")
    print(f"  max future shell defect over {steps} steps = {future_readout_translation_defect:.3e}")
    print(f"  max |k.u_hat| = {max_div:.3e}")

    claims = [
        {
            "id": "Vol6-NSXiMin-triad-lineage",
            "name": "Direct NS ordered-triad sum reproduces the exact retained nonlinear tape",
            "tier": "finite_diagnostic",
            "status": "PASS" if triad_ok and conservative_ok and admissible_ok else "FAIL",
            "evidence": (
                f"max triad/pseudospectral eta residual={triad_residual:.3e}; "
                f"total nonlinear transfer defect={transfer_defect:.3e}"
            ),
        },
        {
            "id": "Vol6-NSXiMin-translation-gauge",
            "name": "Spatial translation is a future-shell-readout equivalence of the finite NS system",
            "tier": "finite_diagnostic",
            "status": "PASS" if gauge_ok and admissible_ok else "FAIL",
            "evidence": (
                f"shell defect={shell_translation_defect:.3e}; "
                f"eta defect={eta_translation_defect:.3e}; "
                f"future {steps}-step shell defect={future_readout_translation_defect:.3e}"
            ),
        },
        {
            "id": "Vol6-NSXiMin-exact-quotient",
            "name": "Canonical minimal exact dynamically sufficient state is the quotient by future shell-readout equivalence",
            "tier": "Dr",
            "status": "N/A",
            "evidence": (
                "Standard quotient/universal-property theorem stated in "
                "reproduction/NS_MINIMAL_DYNAMIC_READOUT.md; not promoted to a machine-checked tier."
            ),
        },
        {
            "id": "Vol6-NSXiMin-finite-jet",
            "name": "For a fixed finite polynomial Galerkin truncation, a finite Lie-readout jet realizes the future-readout quotient",
            "tier": "Dr",
            "status": "N/A",
            "evidence": (
                "Uses polynomial NS Galerkin dynamics + Hilbert basis theorem + analytic-output identity theorem; "
                "proof and exact lineage are stated in reproduction/NS_MINIMAL_DYNAMIC_READOUT.md."
            ),
        },
    ]

    ok = triad_ok and conservative_ok and gauge_ok and admissible_ok
    print("REPORT_JSON:" + json.dumps(report, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
