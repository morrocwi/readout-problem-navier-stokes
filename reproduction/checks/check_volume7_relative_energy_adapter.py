#!/usr/bin/env python3
"""Finite witnesses for the Volume-7 relative-energy adapter.

The continuum relative-energy theorem is analytic tier Dr.  This script checks
only the finite algebraic consequences and Fourier residual formulas used by
the implementation.  The continuous-time RK4 tape enclosure is owned by
check_volume7_rk4_continuous_enclosure.py so the reproduction ledger has one
authoritative status row for that obligation.
"""
from __future__ import annotations

import json
import math


def relative_energy_formula():
    nu = 0.5
    e0 = 0.1
    Gint = 0.2
    B = 0.03
    A = 2.0 * Gint
    E2 = math.exp(A) * (e0 * e0 + B / nu)
    Z2 = (e0 * e0 + A * E2 + B / nu) / nu
    ok = E2 > 0 and Z2 > 0 and math.isfinite(E2) and math.isfinite(Z2)
    return ok, {"A": A, "B": B, "terminal_error_beta": math.sqrt(E2), "grad_error_L2t_upper": math.sqrt(Z2)}


def shear_snapshot_residual():
    # v=(0,sin x,0). All q.u_p contractions vanish exactly.
    state = {
        (1, 0, 0): (0j, -0.5j, 0j),
        (-1, 0, 0): (0j, 0.5j, 0j),
    }
    K = 1
    residual = {}
    keys = tuple(state)
    for p in keys:
        up = state[p]
        for q in keys:
            uq = state[q]
            out = tuple(p[i] + q[i] for i in range(3))
            if out == (0, 0, 0) or max(abs(x) for x in out) <= K:
                continue
            qdot = sum(q[i] * up[i] for i in range(3))
            term = tuple(1j * qdot * uq[i] for i in range(3))
            old = residual.get(out, (0j, 0j, 0j))
            residual[out] = tuple(old[i] + term[i] for i in range(3))
    norm = math.sqrt(sum(abs(z) ** 2 for v in residual.values() for z in v))
    return norm <= 1e-15, {"unresolved_convective_residual_l2": norm}


def finite_grad_linf_bound_example():
    # One Fourier coefficient at k=(2,0,0), |u_hat|=5 gives coefficient bound 10.
    k = (2, 0, 0)
    v = (0j, 3 + 4j, 0j)
    bound = math.sqrt(sum(x*x for x in k)) * math.sqrt(sum(abs(z)**2 for z in v))
    return math.isclose(bound, 10.0), {"bound": bound}


def terminal_tail_projection_contraction():
    # If v is K-supported, omitted(u) = omitted(u-v); orthogonal projection is contractive.
    err_modes = {
        (1, 0, 0): 3.0,
        (3, 0, 0): 4.0,
        (0, 4, 0): 12.0,
    }
    K = 2
    full = math.sqrt(sum(a*a for a in err_modes.values()))
    tail = math.sqrt(sum(a*a for k, a in err_modes.items() if max(abs(x) for x in k) > K))
    return tail <= full + 1e-15, {"full_error": full, "terminal_tail": tail}


def main():
    f_ok, f = relative_energy_formula()
    s_ok, s = shear_snapshot_residual()
    g_ok, g = finite_grad_linf_bound_example()
    p_ok, p = terminal_tail_projection_contraction()
    finite_ok = f_ok and s_ok and g_ok and p_ok

    claims = [
        {
            "id": "V7-EPSC-RE-ALGEBRA",
            "name": "relative-energy adapter finite formula and projection contraction",
            "tier": "finite_diagnostic",
            "status": "PASS" if (f_ok and p_ok) else "FAIL",
            "evidence": f"beta={f['terminal_error_beta']:.6e}; omitted tail={p['terminal_tail']:.6e} <= full error={p['full_error']:.6e}",
        },
        {
            "id": "V7-EPSC-GALERKIN-RESIDUAL-SHEAR",
            "name": "finite unresolved nonlinear residual vanishes for shear solution",
            "tier": "finite_diagnostic",
            "status": "PASS" if s_ok else "FAIL",
            "evidence": f"snapshot unresolved convective residual L2={s['unresolved_convective_residual_l2']:.3e}",
        },
        {
            "id": "V7-EPSC-GRAD-LINF-FOURIER",
            "name": "finite Fourier coefficient upper bound for comparison-path gradient",
            "tier": "finite_diagnostic",
            "status": "PASS" if g_ok else "FAIL",
            "evidence": f"single-mode coefficient bound={g['bound']:.6g}",
        },
        {
            "id": "V7-EPSC-RELATIVE-ENERGY-ADAPTER",
            "name": "residual-based Leray-Hopf terminal L2 adapter theorem",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": "paper/NS_RELATIVE_ENERGY_ADAPTER_CERTIFICATE.md: standard relative-energy inequality + H^-1 Young bound + Gronwall",
        },
    ]

    print("Volume 7 -- relative-energy adapter finite witnesses")
    print("formula:", json.dumps(f))
    print("shear residual:", json.dumps(s))
    print("grad Linf coefficient bound:", json.dumps(g))
    print("projection contraction:", json.dumps(p))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if finite_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
