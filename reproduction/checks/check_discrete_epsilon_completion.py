#!/usr/bin/env python3
"""
Readout-NS Discrete-Native epsilon-Completion Prototype v0.1

Independent reproduction implementation for the NS application of the
Discrete Epsilon-Completion Programme.

Toledo proposal lineage:
- PROP-EPSC-01  nested readout consistency defect
- PROP-EPSC-02  NS Fourier boundary-energy diagnostic
- PROP-EPSC-03  fail-closed epsilon-completion acceptance gate
- PROP-EPSC-04  computable omitted-information tail certificate target (OPEN)

The production path in this checker stores only integer Fourier-mode records
and ordered triads p+q=k.  It does not construct a spatial x/y/z grid and does
not use an FFT to advance the solution.  A padded FFT evaluator is included
only as an independent finite-algebra validation gate.

Evidence tier: finite_diagnostic
[SimulatedData] Simulation=Yes

This checker does NOT prove continuum convergence, a Navier-Stokes regularity
theorem, or that a finite cutoff contains literally all continuum information.
Its adaptive epsilon criterion is an operational finite diagnostic based on
nested-cutoff agreement plus boundary-mode energy.  Continuum certification
remains HOLD until PROP-EPSC-04 is supplied by a proved tail bound.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np


@dataclass
class Plan:
    K: int
    modes: np.ndarray
    index: dict
    out_idx: np.ndarray
    p_idx: np.ndarray
    q_idx: np.ndarray
    k2: np.ndarray


def build_modes(K: int):
    modes = [
        k for k in itertools.product(range(-K, K + 1), repeat=3)
        if k != (0, 0, 0)
    ]
    arr = np.asarray(modes, dtype=np.int64)
    index = {tuple(k): i for i, k in enumerate(arr)}
    return arr, index


@lru_cache(maxsize=None)
def build_plan(K: int) -> Plan:
    modes, index = build_modes(K)
    out_idx, p_idx, q_idx = [], [], []

    # Purely discrete triad tape. No spatial grid is constructed.
    for oi, k in enumerate(modes):
        for pi, p in enumerate(modes):
            q = tuple(k - p)
            qi = index.get(q)
            if qi is not None:
                out_idx.append(oi)
                p_idx.append(pi)
                q_idx.append(qi)

    return Plan(
        K=K,
        modes=modes,
        index=index,
        out_idx=np.asarray(out_idx, dtype=np.int32),
        p_idx=np.asarray(p_idx, dtype=np.int32),
        q_idx=np.asarray(q_idx, dtype=np.int32),
        k2=np.sum(modes * modes, axis=1).astype(np.float64),
    )


def leray_project(v: np.ndarray, modes: np.ndarray) -> np.ndarray:
    """Project each vector coefficient onto k-perp."""
    k2 = np.sum(modes * modes, axis=1).astype(np.float64)
    kv = np.sum(modes * v, axis=1)
    return v - modes * (kv / k2)[:, None]


def rhs_direct(u: np.ndarray, nu: float, plan: Plan) -> np.ndarray:
    """Direct mode-native Galerkin RHS on the finite triad tape."""
    qvec = plan.modes[plan.q_idx]
    q_dot_up = np.sum(qvec * u[plan.p_idx], axis=1)
    terms = q_dot_up[:, None] * u[plan.q_idx]

    conv = np.zeros_like(u, dtype=np.complex128)
    np.add.at(conv, plan.out_idx, terms)
    conv *= 1j
    conv = leray_project(conv, plan.modes)

    return -conv - nu * plan.k2[:, None] * u


def rk4_step_direct(u: np.ndarray, dt: float, nu: float, plan: Plan) -> np.ndarray:
    k1 = rhs_direct(u, nu, plan)
    k2 = rhs_direct(u + 0.5 * dt * k1, nu, plan)
    k3 = rhs_direct(u + 0.5 * dt * k2, nu, plan)
    k4 = rhs_direct(u + dt * k3, nu, plan)
    return u + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def evolve_direct(u0: np.ndarray, T: float, dt: float, nu: float, plan: Plan):
    nsteps = int(round(T / dt))
    if not np.isclose(nsteps * dt, T, rtol=0, atol=1e-14):
        raise ValueError("T must be an integer multiple of dt in this prototype.")
    u = u0.copy()
    for _ in range(nsteps):
        u = rk4_step_direct(u, dt, nu, plan)
    return u


def shear_state(plan: Plan, amplitude: float = 1.0) -> np.ndarray:
    """Fourier records for u=(0,A sin x,0); nonlinear term is exactly zero."""
    u = np.zeros((len(plan.modes), 3), dtype=np.complex128)
    u[plan.index[(1, 0, 0)]] = (0, -0.5j * amplitude, 0)
    u[plan.index[(-1, 0, 0)]] = (0, 0.5j * amplitude, 0)
    return u


def taylor_green_state(plan: Plan) -> np.ndarray:
    """Standard Taylor-Green initial coefficients entered directly in mode space."""
    u = np.zeros((len(plan.modes), 3), dtype=np.complex128)
    if plan.K < 1:
        return u
    for k in itertools.product((-1, 1), repeat=3):
        u[plan.index[k]] = (-1j*k[0]/8.0, 1j*k[1]/8.0, 0.0)
    return u


def random_smooth_mode_state(plan: Plan, seed: int = 20260910,
                             alpha: float = 0.35, amplitude: float = 0.2):
    """Deterministic nested smooth spectrum, built directly in coefficient space."""
    u = np.zeros((len(plan.modes), 3), dtype=np.complex128)

    def canonical(k):
        for a in k:
            if a != 0:
                return a > 0
        return False

    for karr in plan.modes:
        k = tuple(int(x) for x in karr)
        if not canonical(k):
            continue
        ss = np.random.SeedSequence([seed, k[0] + 100, k[1] + 100, k[2] + 100])
        rng = np.random.default_rng(ss)
        z = rng.normal(size=3) + 1j * rng.normal(size=3)
        kk = np.asarray(k, dtype=float)
        z = z - kk * (kk @ z) / (kk @ kk)
        z *= amplitude * math.exp(-alpha * float(kk @ kk))
        u[plan.index[k]] = z
        u[plan.index[tuple(-kk.astype(int))]] = np.conj(z)
    return u


# Independent validation route. This routine uses an FFT grid ONLY to compare
# against the direct triad algebra. The mode-native production path above does
# not call it.
def rhs_fft_validator(u: np.ndarray, nu: float, plan: Plan) -> np.ndarray:
    K = plan.K
    N = 3*K + 1  # N > 3K blocks quadratic aliasing into the retained cube.
    kvals = np.fft.fftfreq(N, d=1.0/N).astype(int)
    imap = {int(k): i for i, k in enumerate(kvals)}

    coeff = np.zeros((3, N, N, N), dtype=np.complex128)
    for mi, k in enumerate(plan.modes):
        coeff[:, imap[int(k[0])], imap[int(k[1])], imap[int(k[2])]] = u[mi]

    scale = N**3
    u_phys = np.fft.ifftn(coeff * scale, axes=(1,2,3))
    convection = np.zeros_like(u_phys)

    for d in range(3):
        shape = [1, 1, 1]
        shape[d] = N
        kd = kvals.reshape(shape)
        deriv = np.fft.ifftn(
            (1j * kd[None, ...] * coeff) * scale,
            axes=(1,2,3),
        )
        convection += u_phys[d][None, ...] * deriv

    conv_hat = np.fft.fftn(convection, axes=(1,2,3)) / scale
    out = np.zeros_like(u)

    for mi, k in enumerate(plan.modes):
        kk = np.asarray(k, dtype=float)
        ksq = float(kk @ kk)
        v = conv_hat[:, imap[int(k[0])], imap[int(k[1])], imap[int(k[2])]]
        pv = v - kk * (kk @ v) / ksq
        out[mi] = -pv - nu * ksq * u[mi]

    return out


def rk4_step_generic(u, dt, rhs):
    k1 = rhs(u)
    k2 = rhs(u + 0.5*dt*k1)
    k3 = rhs(u + 0.5*dt*k2)
    k4 = rhs(u + dt*k3)
    return u + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)


def diagnostics(u: np.ndarray, plan: Plan):
    absmax = np.max(np.abs(plan.modes), axis=1)
    boundary = absmax == plan.K
    energy = 0.5 * float(np.sum(np.abs(u)**2))
    boundary_energy_value = 0.5 * float(np.sum(np.abs(u[boundary])**2))
    div = float(np.max(np.abs(np.sum(plan.modes * u, axis=1))))
    reality = 0.0
    for i, k in enumerate(plan.modes):
        j = plan.index[tuple(-k)]
        reality = max(reality, float(np.max(np.abs(u[j] - np.conj(u[i])))))
    return {
        "energy": energy,
        "boundary_energy": boundary_energy_value,
        "max_divergence_constraint": div,
        "max_reality_symmetry_error": reality,
    }


def overlap_difference(u_large, plan_large, u_small, plan_small):
    embedded = np.asarray([
        u_large[plan_large.index[tuple(k)]]
        for k in plan_small.modes
    ])
    d = embedded - u_small
    return {
        "overlap_l2": float(np.linalg.norm(d)),
        "overlap_max_component": float(np.max(np.abs(d))),
    }


def test_analytic_shear():
    K, nu, dt, T = 1, 0.1, 0.01, 1.0
    plan = build_plan(K)
    u0 = shear_state(plan)
    nonlinear_only = rhs_direct(u0, 0.0, plan)
    uf = evolve_direct(u0, T, dt, nu, plan)
    exact = u0 * math.exp(-nu*T)
    err = float(np.max(np.abs(uf - exact)))
    nl = float(np.max(np.abs(nonlinear_only)))
    return {
        "K": K, "nu": nu, "dt": dt, "T": T,
        "max_nonlinear_rhs_at_t0": nl,
        "max_error_vs_exact_decay": err,
        "pass_1e-12": bool(err <= 1e-12 and nl <= 1e-12),
    }


def test_independent_fft_gate():
    K, nu, dt = 2, 0.01, 0.0025
    plan = build_plan(K)
    u0 = random_smooth_mode_state(plan)
    rd = rhs_direct(u0, nu, plan)
    rf = rhs_fft_validator(u0, nu, plan)

    ud = rk4_step_direct(u0, dt, nu, plan)
    uf = rk4_step_generic(u0, dt, lambda x: rhs_fft_validator(x, nu, plan))

    rhs_err = float(np.max(np.abs(rd-rf)))
    step_err = float(np.max(np.abs(ud-uf)))
    return {
        "K": K, "modes": len(plan.modes), "ordered_triads": len(plan.out_idx),
        "nu": nu, "dt": dt,
        "max_rhs_difference": rhs_err,
        "max_one_rk4_step_difference": step_err,
        "pass_1e-12": bool(rhs_err <= 1e-12 and step_err <= 1e-12),
    }


def adaptive_epsilon_completion(
    K_values=(1,2,3,4,5),
    nu=0.01,
    dt=0.005,
    T=0.05,
    eps_overlap=1e-6,
    eps_boundary_energy=1e-8,
    confirmations=2,
):
    """Operational finite diagnostic; NOT a rigorous infinite-tail bound."""
    rows = []
    prev_u = None
    prev_plan = None
    consecutive = 0
    first_passing_K = None
    confirmed_K = None

    for K in K_values:
        plan = build_plan(K)
        u0 = taylor_green_state(plan)

        start = time.perf_counter()
        uf = evolve_direct(u0, T, dt, nu, plan)
        elapsed = time.perf_counter() - start

        row = {
            "K": K,
            "modes": int(len(plan.modes)),
            "ordered_triads": int(len(plan.out_idx)),
            "runtime_seconds": elapsed,
            **diagnostics(uf, plan),
            "overlap_l2": None,
            "overlap_max_component": None,
            "passes_epsilon_gate": False,
        }

        if prev_u is not None:
            row.update(overlap_difference(uf, plan, prev_u, prev_plan))
            row["passes_epsilon_gate"] = bool(
                row["overlap_l2"] <= eps_overlap
                and row["boundary_energy"] <= eps_boundary_energy
            )
            if row["passes_epsilon_gate"]:
                consecutive += 1
                if first_passing_K is None:
                    first_passing_K = K
                if consecutive >= confirmations:
                    confirmed_K = K
            else:
                consecutive = 0
                first_passing_K = None

        rows.append(row)
        prev_u, prev_plan = uf, plan

    return {
        "task": "full retained Fourier state at terminal time for Taylor-Green initial data",
        "nu": nu,
        "dt": dt,
        "T": T,
        "eps_overlap_l2": eps_overlap,
        "eps_boundary_energy": eps_boundary_energy,
        "required_consecutive_passes": confirmations,
        "first_passing_K": first_passing_K if confirmed_K else None,
        "confirmed_K": confirmed_K,
        "continuum_certificate": "HOLD",
        "continuum_hold_reason": "PROP-EPSC-04 proved omitted-information bound not supplied",
        "rows": rows,
    }


def run_all():
    return {
        "status": "finite_diagnostic",
        "simulation_label": "[SimulatedData]",
        "simulation": True,
        "production_solver_uses_spatial_grid": False,
        "production_solver_uses_fft": False,
        "toledo": ["PROP-EPSC-01", "PROP-EPSC-02", "PROP-EPSC-03", "PROP-EPSC-04"],
        "analytic_shear_test": test_analytic_shear(),
        "independent_fft_gate": test_independent_fft_gate(),
        "adaptive_epsilon_completion": adaptive_epsilon_completion(),
    }


def print_summary(r):
    print("Readout-NS discrete-native prototype v0.1")
    print("[SimulatedData] Simulation=Yes | evidence=finite_diagnostic")
    print("continuum certificate: HOLD (PROP-EPSC-04 remains open)")
    print()
    a = r["analytic_shear_test"]
    print("A) Analytic shear-decay test")
    print(f"   nonlinear RHS max : {a['max_nonlinear_rhs_at_t0']:.3e}")
    print(f"   exact-decay error : {a['max_error_vs_exact_decay']:.3e}")
    print(f"   pass <=1e-12      : {a['pass_1e-12']}")
    print()
    b = r["independent_fft_gate"]
    print("B) Independent finite-algebra FFT gate")
    print(f"   K={b['K']}, modes={b['modes']}, triads={b['ordered_triads']}")
    print(f"   RHS difference    : {b['max_rhs_difference']:.3e}")
    print(f"   RK4-step diff     : {b['max_one_rk4_step_difference']:.3e}")
    print(f"   pass <=1e-12      : {b['pass_1e-12']}")
    print()
    c = r["adaptive_epsilon_completion"]
    print("C) Nested-cutoff epsilon-completion diagnostic")
    print(f"   eps_overlap={c['eps_overlap_l2']:.1e}, eps_boundary={c['eps_boundary_energy']:.1e}")
    print("   K | modes | triads | boundary_E | overlap_L2 | gate")
    for x in c["rows"]:
        ol2 = "n/a" if x["overlap_l2"] is None else f"{x['overlap_l2']:.3e}"
        print(f"   {x['K']:>1} | {x['modes']:>5} | {x['ordered_triads']:>7} | "
              f"{x['boundary_energy']:.3e} | {ol2:>9} | {x['passes_epsilon_gate']}")
    print(f"   confirmed cutoff  : K={c['confirmed_K']} "
          f"(two consecutive passing cutoffs; first pass K={c['first_passing_K']})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="discrete_epsilon_completion_v01.json")
    args = ap.parse_args()

    r = run_all()
    Path(args.json).write_text(json.dumps(r, indent=2), encoding="utf-8")
    print_summary(r)


if __name__ == "__main__":
    main()
