#!/usr/bin/env python3
"""
NS Retained Fold Compiler (NS-RFC): task-conditioned finite-horizon Fourier-Galerkin solver.

Lineage:
  IDM RFT  : terminal readout -> retained causal boundary -> forward fold
  IDM RRP  : terminal relevance is unfolded backward to only the modes required
             by the declared terminal task
  IDM RCF  : ordered triad contributions for the retained outputs are fused into
             one vectorized batch
  FRA guard: each time layer may use either the fused retained backend or a full
             pseudo-spectral FFT backend; the faster hot backend is selected by
             an explicit finite calibration, never assumed.

Finite recurrence
-----------------
For a fixed Fourier cube K_M and explicit Euler,

  u_k^{n+1}
    = u_k^n + dt[-i P_k sum_{p+q=k}(q.u_p^n)u_q^n
                 - nu |k|^2 u_k^n].

For terminal target modes S_R,

  S_t = S_{t+1} union {p,q : p+q=k, k in S_{t+1}}.

Induction gives task exactness relative to the SAME finite recurrence:
if the retained state equals the full state on S_t, the next retained state
equals the full state on S_{t+1}. Hence the terminal task is identical.

The pseudo-spectral backend is admitted only after a finite all-mode check that
one Euler step agrees with the direct triad-Galerkin step on the same mode cube.

Claim boundary
--------------
This is:
  * exact task slicing for the declared finite explicit-Euler recurrence;
  * a finite_diagnostic timing comparison.

This is NOT:
  * an exact-in-time Navier-Stokes flow;
  * a continuum regularity/singularity theorem;
  * an all-future reduction;
  * a universal speedup theorem.

The structural plan may be reused for repeated solves with the same K, target,
horizon, dt, and backend topology.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from typing import Iterable

import numpy as np

Mode = tuple[int, int, int]


def cube_modes(K: int) -> list[Mode]:
    return [
        (i, j, k)
        for i in range(-K, K + 1)
        for j in range(-K, K + 1)
        for k in range(-K, K + 1)
        if (i, j, k) != (0, 0, 0)
    ]


def triads_by_output(modes: Iterable[Mode]) -> dict[Mode, tuple[tuple[Mode, Mode], ...]]:
    modes = list(modes)
    mode_set = set(modes)
    out = {}
    for k in modes:
        pairs = []
        for p in modes:
            q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
            if q in mode_set:
                pairs.append((p, q))
        out[k] = tuple(pairs)
    return out


def project_vectors(a: np.ndarray, kvec: np.ndarray) -> np.ndarray:
    k2 = np.einsum("ij,ij->i", kvec, kvec)
    dot = np.einsum("ij,ij->i", kvec, a)
    return a - kvec * (dot / k2)[:, None]


def project_one(a: np.ndarray, k: Mode) -> np.ndarray:
    kv = np.asarray(k, dtype=float)
    return project_vectors(a[None, :], kv[None, :])[0]


def canonical_half(k: Mode) -> bool:
    for x in k:
        if x > 0:
            return True
        if x < 0:
            return False
    return False


def random_real_divfree_state(
    modes: list[Mode], seed: int = 20260909, target_energy: float = 0.125
) -> np.ndarray:
    idx = {k: i for i, k in enumerate(modes)}
    mode_set = set(modes)
    rng = np.random.default_rng(seed)
    U = np.zeros((len(modes), 3), dtype=complex)
    done = set()
    for k in modes:
        if k in done or not canonical_half(k):
            continue
        neg = (-k[0], -k[1], -k[2])
        if neg not in mode_set:
            raise ValueError("mode cube is not conjugate symmetric")
        z = rng.normal(size=3) + 1j * rng.normal(size=3)
        z = project_one(z, k)
        U[idx[k]] = z
        U[idx[neg]] = np.conjugate(z)
        done.add(k)
        done.add(neg)
    energy = 0.5 * float(np.sum(np.abs(U) ** 2))
    U *= math.sqrt(target_energy / energy)
    return U


def backward_relevance_layers(
    triads: dict[Mode, tuple[tuple[Mode, Mode], ...]],
    targets: Iterable[Mode],
    steps: int,
) -> list[set[Mode]]:
    layers = [set() for _ in range(steps + 1)]
    layers[steps] = set(targets)
    for t in range(steps - 1, -1, -1):
        needed = set(layers[t + 1])
        for k in layers[t + 1]:
            for p, q in triads[k]:
                needed.add(p)
                needed.add(q)
        layers[t] = needed
    return layers


@dataclass(frozen=True)
class FusedTriadPlan:
    outputs: tuple[Mode, ...]
    k_idx: np.ndarray
    kvec: np.ndarray
    k2: np.ndarray
    p_idx: np.ndarray
    q_idx: np.ndarray
    qvec: np.ndarray
    out_slot: np.ndarray

    @staticmethod
    def compile(
        modes: list[Mode],
        triads: dict[Mode, tuple[tuple[Mode, Mode], ...]],
        outputs: Iterable[Mode],
    ) -> "FusedTriadPlan":
        idx = {k: i for i, k in enumerate(modes)}
        outs = tuple(sorted(outputs))
        k_idx = np.asarray([idx[k] for k in outs], dtype=int)
        kvec = np.asarray(outs, dtype=float)
        k2 = np.einsum("ij,ij->i", kvec, kvec)
        p_idx = []
        q_idx = []
        qvec = []
        slot = []
        for oi, k in enumerate(outs):
            for p, q in triads[k]:
                p_idx.append(idx[p])
                q_idx.append(idx[q])
                qvec.append(q)
                slot.append(oi)
        return FusedTriadPlan(
            outs,
            k_idx,
            kvec,
            k2,
            np.asarray(p_idx, dtype=int),
            np.asarray(q_idx, dtype=int),
            np.asarray(qvec, dtype=float),
            np.asarray(slot, dtype=int),
        )

    @property
    def triad_count(self) -> int:
        return int(len(self.p_idx))

    def update_selected(self, U: np.ndarray, dt: float, nu: float) -> np.ndarray:
        up = U[self.p_idx]
        uq = U[self.q_idx]
        q_dot_up = np.einsum("ij,ij->i", self.qvec, up)
        contributions = 1j * q_dot_up[:, None] * uq

        conv = np.zeros((len(self.outputs), 3), dtype=complex)
        np.add.at(conv, self.out_slot, contributions)
        conv = project_vectors(conv, self.kvec)

        rhs = -conv - nu * self.k2[:, None] * U[self.k_idx]
        return U[self.k_idx] + dt * rhs


@dataclass(frozen=True)
class FFTPlan:
    K: int
    n: int
    mode_grid_indices: tuple[np.ndarray, np.ndarray, np.ndarray]
    KX: np.ndarray
    KY: np.ndarray
    KZ: np.ndarray
    K2: np.ndarray
    mask: np.ndarray

    @staticmethod
    def compile(modes: list[Mode], K: int) -> "FFTPlan":
        # n > 4K keeps every p+q generated by the retained cube below the FFT wrap boundary.
        n = 4 * K + 4
        kvals = np.fft.fftfreq(n, d=1.0 / n).astype(int)
        lookup = {int(k): i for i, k in enumerate(kvals)}
        ii = np.asarray([lookup[k[0]] for k in modes], dtype=int)
        jj = np.asarray([lookup[k[1]] for k in modes], dtype=int)
        ll = np.asarray([lookup[k[2]] for k in modes], dtype=int)
        k = kvals.astype(float)
        KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
        K2 = KX * KX + KY * KY + KZ * KZ
        mask = (
            (np.abs(KX) <= K)
            & (np.abs(KY) <= K)
            & (np.abs(KZ) <= K)
            & (K2 > 0)
        )
        return FFTPlan(K, n, (ii, jj, ll), KX, KY, KZ, K2, mask)

    def to_grid(self, U: np.ndarray) -> np.ndarray:
        out = np.zeros((3, self.n, self.n, self.n), dtype=complex)
        ii, jj, ll = self.mode_grid_indices
        out[:, ii, jj, ll] = U.T
        return out

    def from_grid(self, uh: np.ndarray) -> np.ndarray:
        ii, jj, ll = self.mode_grid_indices
        return uh[:, ii, jj, ll].T.copy()

    def project_grid(self, uh: np.ndarray) -> np.ndarray:
        dot = self.KX * uh[0] + self.KY * uh[1] + self.KZ * uh[2]
        out = uh.copy()
        nz = self.K2 > 0
        out[0, nz] -= self.KX[nz] * dot[nz] / self.K2[nz]
        out[1, nz] -= self.KY[nz] * dot[nz] / self.K2[nz]
        out[2, nz] -= self.KZ[nz] * dot[nz] / self.K2[nz]
        return out

    def rhs_grid(self, uh: np.ndarray, nu: float) -> np.ndarray:
        def ifft3(a):
            return np.fft.ifftn(a, axes=(-3, -2, -1), norm="forward").real
        def fft3(a):
            return np.fft.fftn(a, axes=(-3, -2, -1), norm="forward")

        u = ifft3(uh)
        grad = np.empty((3, 3) + self.K2.shape, dtype=float)
        Ks = (self.KX, self.KY, self.KZ)
        for j in range(3):
            for i, Ki in enumerate(Ks):
                grad[j, i] = ifft3(1j * Ki * uh[j])

        conv = np.zeros_like(u)
        for j in range(3):
            for i in range(3):
                conv[j] += u[i] * grad[j, i]

        Nh = fft3(conv)
        Nh *= self.mask[None, ...]
        Nh = self.project_grid(Nh)
        total = -Nh - nu * self.K2[None, ...] * uh
        total *= self.mask[None, ...]
        return total

    def full_step(self, U: np.ndarray, dt: float, nu: float) -> np.ndarray:
        uh = self.to_grid(U)
        uh_next = uh + dt * self.rhs_grid(uh, nu)
        return self.from_grid(uh_next)


def median_seconds(fn, repeats: int) -> float:
    rows = []
    for _ in range(repeats):
        started = time.perf_counter()
        fn()
        rows.append(time.perf_counter() - started)
    return float(np.median(np.asarray(rows)))


@dataclass
class CompiledLayer:
    t: int
    fused: FusedTriadPlan
    backend: str
    fused_calibration_seconds: float
    fft_calibration_seconds: float


@dataclass
class CompiledTaskPlan:
    modes: list[Mode]
    target: Mode
    layers: list[set[Mode]]
    layer_plans: list[CompiledLayer]
    fft: FFTPlan
    backend_equivalence_error: float


def compile_task_plan(
    K: int,
    target: Mode,
    steps: int,
    U_probe: np.ndarray,
    dt: float,
    nu: float,
    calibration_repeats: int,
) -> CompiledTaskPlan:
    modes = cube_modes(K)
    idx = {k: i for i, k in enumerate(modes)}
    if target not in idx:
        raise ValueError("target outside mode cube")
    triads = triads_by_output(modes)
    layers = backward_relevance_layers(triads, [target], steps)
    fft = FFTPlan.compile(modes, K)

    # Gate FFT against the direct all-mode Galerkin convolution before admitting it.
    all_fused = FusedTriadPlan.compile(modes, triads, modes)
    direct_all = U_probe.copy()
    direct_all[all_fused.k_idx] = all_fused.update_selected(U_probe, dt, nu)
    fft_all = fft.full_step(U_probe, dt, nu)
    backend_equivalence_error = float(np.max(np.abs(direct_all - fft_all)))

    fft_seconds = median_seconds(
        lambda: fft.full_step(U_probe, dt, nu), calibration_repeats
    )
    plans = []
    for t in range(steps):
        fused = FusedTriadPlan.compile(modes, triads, layers[t + 1])

        def fused_call():
            out = U_probe.copy()
            out[fused.k_idx] = fused.update_selected(U_probe, dt, nu)
            return out

        fused_seconds = median_seconds(fused_call, calibration_repeats)
        backend = "fused_retained" if fused_seconds <= fft_seconds else "full_fft"
        plans.append(
            CompiledLayer(
                t=t,
                fused=fused,
                backend=backend,
                fused_calibration_seconds=fused_seconds,
                fft_calibration_seconds=fft_seconds,
            )
        )
    return CompiledTaskPlan(
        modes, target, layers, plans, fft, backend_equivalence_error
    )


def execute_plan(
    plan: CompiledTaskPlan, U0: np.ndarray, dt: float, nu: float
) -> np.ndarray:
    U = U0.copy()
    for layer in plan.layer_plans:
        if layer.backend == "full_fft":
            U = plan.fft.full_step(U, dt, nu)
        else:
            selected = layer.fused.update_selected(U, dt, nu)
            U_next = U.copy()
            U_next[layer.fused.k_idx] = selected
            U = U_next
    return U


def full_fft_rollout(
    fft: FFTPlan, U0: np.ndarray, dt: float, nu: float, steps: int
) -> np.ndarray:
    U = U0.copy()
    for _ in range(steps):
        U = fft.full_step(U, dt, nu)
    return U


def run_case(
    K: int,
    steps: int,
    dt: float,
    nu: float,
    repeats: int,
    calibration_repeats: int,
    target: Mode = (1, 0, 0),
) -> dict:
    modes = cube_modes(K)
    triads = triads_by_output(modes)
    U0 = random_real_divfree_state(modes)

    plan = compile_task_plan(
        K, target, steps, U0, dt, nu, calibration_repeats
    )
    idx = {k: i for i, k in enumerate(modes)}

    retained = execute_plan(plan, U0, dt, nu)
    full = full_fft_rollout(plan.fft, U0, dt, nu, steps)
    target_abs = float(np.linalg.norm(retained[idx[target]] - full[idx[target]]))
    target_rel = target_abs / max(float(np.linalg.norm(full[idx[target]])), 1e-30)

    retained_seconds = median_seconds(
        lambda: execute_plan(plan, U0, dt, nu), repeats
    )
    full_seconds = median_seconds(
        lambda: full_fft_rollout(plan.fft, U0, dt, nu, steps), repeats
    )

    total_triads = sum(len(v) for v in triads.values())
    retained_triad_tokens = sum(
        layer.fused.triad_count
        for layer in plan.layer_plans
        if layer.backend == "fused_retained"
    )
    fft_layers = sum(layer.backend == "full_fft" for layer in plan.layer_plans)

    return {
        "K": K,
        "mode_count": len(modes),
        "ordered_triad_count": total_triads,
        "target": list(target),
        "steps": steps,
        "dt": dt,
        "nu": nu,
        "layer_mode_counts": [len(x) for x in plan.layers],
        "layer_backends": [x.backend for x in plan.layer_plans],
        "layer_output_counts": [len(x.fused.outputs) for x in plan.layer_plans],
        "layer_fused_triad_counts": [x.fused.triad_count for x in plan.layer_plans],
        "fft_layers": int(fft_layers),
        "retained_fused_triad_tokens": int(retained_triad_tokens),
        "backend_equivalence_max_abs_error": plan.backend_equivalence_error,
        "target_vector_abs_error": target_abs,
        "target_vector_rel_error": target_rel,
        "full_fft_median_seconds": full_seconds,
        "retained_hybrid_median_seconds": retained_seconds,
        "observed_speedup_full_over_retained": full_seconds / retained_seconds,
        "status": (
            "PASS"
            if target_rel < 1e-12 and plan.backend_equivalence_error < 1e-12
            else "FAIL"
        ),
        "tier": "finite_diagnostic",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--K", type=int, default=2)
    p.add_argument("--max-steps", type=int, default=5)
    p.add_argument("--dt", type=float, default=0.001)
    p.add_argument("--nu", type=float, default=0.01)
    p.add_argument("--repeats", type=int, default=21)
    p.add_argument("--calibration-repeats", type=int, default=9)
    args = p.parse_args()

    rows = [
        run_case(
            K=args.K,
            steps=R,
            dt=args.dt,
            nu=args.nu,
            repeats=args.repeats,
            calibration_repeats=args.calibration_repeats,
        )
        for R in range(1, args.max_steps + 1)
    ]
    for r in rows:
        print(
            f"K={r['K']} R={r['steps']} "
            f"layers={r['layer_mode_counts']} "
            f"backends={r['layer_backends']} "
            f"speed={r['observed_speedup_full_over_retained']:.3f}x "
            f"target_relerr={r['target_vector_rel_error']:.3e} "
            f"backend_err={r['backend_equivalence_max_abs_error']:.3e} "
            f"{r['status']}"
        )
    result = {
        "name": "NS Retained Fold Compiler",
        "tier": "finite_diagnostic",
        "claim_boundary": {
            "exactness": "terminal task exact relative to same finite explicit-Euler Galerkin recurrence",
            "fft_gate": "pseudo-spectral layer admitted only after finite all-mode agreement with direct triad step",
            "timing": "hot-plan median on this runtime only",
            "not_claimed": [
                "continuum Navier-Stokes theorem",
                "exact-in-time flow",
                "all-future reduction",
                "universal speedup",
            ],
        },
        "cases": rows,
    }
    print("RESULT_JSON:" + json.dumps(result, sort_keys=True))
    return 0 if all(r["status"] == "PASS" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
