#!/usr/bin/env python3
"""Finite checks for the energy-observability -> EPSC composition bridge.

This checker validates only finite bookkeeping/algebra and representative
translation invariance of energy readers. It does NOT prove the all-N
observability conjecture or construct a certified inverse from energy jets.

[SimulatedData] Simulation=Yes
"""
from __future__ import annotations

import cmath
import json
import math


def dN(N: int) -> int:
    return 2 * ((2 * N + 1) ** 3 - 1)


def radii(N: int):
    return sorted({
        i * i + j * j + k * k
        for i in range(-N, N + 1)
        for j in range(-N, N + 1)
        for k in range(-N, N + 1)
        if (i, j, k) != (0, 0, 0)
    })


def scalar_ceiling(N: int, R: int) -> int:
    return min(R + 1, dN(N) - 3)


def shell_ceiling(N: int, R: int) -> int:
    m = len(radii(N))
    return min(m + (m - 1) * R, dN(N) - 3)


def shell_min_depth(N: int) -> int:
    m = len(radii(N))
    return math.ceil((dN(N) - 3 - m) / (m - 1))


def energy_readers(state):
    shells = {}
    total = 0.0
    for k, vec in state.items():
        e = sum(abs(z) ** 2 for z in vec)
        q = sum(x * x for x in k)
        shells[q] = shells.get(q, 0.0) + e
        total += e
    return total, shells


def translate(state, a):
    out = {}
    for k, vec in state.items():
        phase = cmath.exp(1j * sum(k[j] * a[j] for j in range(3)))
        out[k] = tuple(phase * z for z in vec)
    return out


def claim(cid, name, tier, status, evidence):
    return {"id": cid, "name": name, "tier": tier, "status": status, "evidence": evidence}


def main():
    claims = []

    dims = {N: (dN(N), len(radii(N))) for N in (1, 2, 3)}
    ok_dims = dims == {1: (52, 3), 2: (248, 9), 3: (684, 18)}
    claims.append(claim(
        "V7-NSOBS-DIMENSIONS",
        "finite NS observability dimensions and shell counts",
        "finite_diagnostic",
        "PASS" if ok_dims else "FAIL",
        f"computed {dims}",
    ))

    rows = [
        (1, "E", 48, 49),
        (1, "I", 23, 49),
        (2, "E", 244, 245),
        (3, "I", 39, 681),
    ]
    row_results = []
    for N, reader, R, recorded_rank in rows:
        cap = scalar_ceiling(N, R) if reader == "E" else shell_ceiling(N, R)
        row_results.append((N, reader, R, recorded_rank, cap, recorded_rank == cap))
    ok_rows = all(r[-1] for r in row_results)
    claims.append(claim(
        "V7-NSOBS-RECORDED-SATURATION-CAPS",
        "recorded exact saturation ranks equal their structural ceilings",
        "finite_diagnostic",
        "PASS" if ok_rows else "FAIL",
        f"rows={row_results}",
    ))

    depth = {
        "E_N1": dN(1) - 4,
        "E_N2": dN(2) - 4,
        "E_N3": dN(3) - 4,
        "I_N1": shell_min_depth(1),
        "I_N3": shell_min_depth(3),
    }
    ok_depth = depth == {"E_N1": 48, "E_N2": 244, "E_N3": 680, "I_N1": 23, "I_N3": 39}
    claims.append(claim(
        "V7-NSOBS-MEASUREMENT-TIME-BOOKKEEPING",
        "measurement-channel versus temporal-depth structural bookkeeping",
        "finite_diagnostic",
        "PASS" if ok_depth else "FAIL",
        f"depths={depth}",
    ))

    state = {
        (1, 0, 0): (0j, 1 + 2j, -0.5j),
        (-1, 0, 0): (0j, 1 - 2j, 0.5j),
        (0, 1, 1): (1 - 0.25j, 0.5 + 0.75j, -0.5 - 0.75j),
        (0, -1, -1): (1 + 0.25j, 0.5 - 0.75j, -0.5 + 0.75j),
    }
    total0, shells0 = energy_readers(state)
    total1, shells1 = energy_readers(translate(state, (0.37, -0.22, 0.91)))
    inv_err = max([abs(total0 - total1)] + [abs(shells0[q] - shells1[q]) for q in shells0])
    ok_inv = inv_err <= 1e-12
    claims.append(claim(
        "V7-NSOBS-TRANSLATION-INVARIANT-READERS",
        "total and shell energy readers are invariant under Fourier translation phases",
        "finite_diagnostic",
        "PASS" if ok_inv else "FAIL",
        f"max reader difference={inv_err:.3e}",
    ))

    rho, beta = 3.0, 4.0
    composed = math.hypot(rho, beta)
    ok_comp = composed == 5.0 and composed <= rho + beta
    claims.append(claim(
        "V7-EPSC-OBSERVABLE-CONTINUUM-COMPOSITION",
        "orthogonal retained/tail radii compose as sqrt(rho^2+beta^2)",
        "finite_diagnostic",
        "PASS" if ok_comp else "FAIL",
        f"rho={rho}, beta={beta}, composed={composed}",
    ))

    claims.append(claim(
        "V7-EPSC-17-OBSERVABLE-TO-CONTINUUM",
        "conditional observable-to-continuum composition theorem",
        "Dr",
        "DERIVED",
        "paper/NS_OBSERVABLE_TO_CONTINUUM_CERTIFICATES.tex; requires certified rho_N and beta_N",
    ))
    claims.append(claim(
        "V7-EPSC-18-CERTIFIED-ENERGY-JET-INVERSE",
        "quantitative certified inverse from energy jets to retained quotient state",
        "Open",
        "OPEN",
        "rank saturation is local qualitative identifiability and does not yet provide rho_N",
    ))
    claims.append(claim(
        "V7-EPSC-19-NOISE-STABLE-MEASUREMENT-CERTIFICATE",
        "noise-stable measurement-to-continuum certificate",
        "Open",
        "OPEN",
        "requires certified conditioning/noise propagation through the finite observability inverse",
    ))
    claims.append(claim(
        "V7-NSOBS-ALL-N-SATURATION",
        "optimal energy-readout saturation at every finite resolution",
        "Open",
        "OPEN",
        "four exact reader-resolution saturation records do not prove the all-N conjecture",
    ))

    failed = [c for c in claims if c["status"] == "FAIL"]
    print("observable-to-continuum bridge checks")
    for c in claims:
        print(f"{c['id']}: {c['status']} -- {c['evidence']}")
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
