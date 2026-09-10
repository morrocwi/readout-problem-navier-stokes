#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Iterable

import numpy as np

from observableflow.openfoam import (
    ProbeDataset,
    fit_lti_probe_model,
    load_probes,
    pod_reduce_snapshots,
)
from observableflow.openfoam_benchmark import _affine_observation_system, _fit_affine
from observableflow.stability import StabilityCandidate, stability_greedy_candidates

PYSENSORS_REPO = "https://github.com/dynamicslab/pysensors"
PYSENSORS_COMMIT = "65400cd12e2f2b79e8a24d16852dd1371c14aa4e"
OPENFOAM_REPO = "https://github.com/OpenFOAM/OpenFOAM-13"
OPENFOAM_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
OPENFOAM_CASE = "tutorials/incompressibleFluid/cavity"


def _metrics(pred: np.ndarray, truth: np.ndarray) -> dict:
    pred = np.asarray(pred, dtype=float)
    truth = np.asarray(truth, dtype=float)
    err = pred - truth
    rmse = float(np.sqrt(np.mean(err * err)))
    scale = float(np.sqrt(np.mean(truth * truth)))
    nrmse = rmse / scale if scale > 0 else float("inf")
    sample_l2 = np.sqrt(np.mean(err * err, axis=1))
    return {
        "rmse": rmse,
        "nrmse": nrmse,
        "median_sample_rmse": float(np.median(sample_l2)),
        "p95_sample_rmse": float(np.quantile(sample_l2, 0.95)),
        "samples": int(len(truth)),
    }


def _basis_rank_condition(basis: np.ndarray, selected: Iterable[int], rtol: float = 1e-10) -> tuple[int, float]:
    rows = np.asarray(basis, dtype=float)[list(selected)]
    if rows.size == 0:
        return 0, float("inf")
    s = np.linalg.svd(rows, compute_uv=False)
    if len(s) == 0 or s[0] == 0:
        return 0, float("inf")
    rank = int(np.count_nonzero(s > rtol * s[0]))
    cond = float(s[0] / s[rank - 1]) if rank else float("inf")
    if rank < basis.shape[1]:
        cond = float("inf")
    return rank, cond


def _objective(cost: float, cond: float, noiseless_nrmse: float, noisy_nrmse: float) -> float:
    if not math.isfinite(cond):
        return float("inf")
    return float(
        cost
        + 0.25 * math.log10(max(cond, 1.0))
        + 4.0 * noiseless_nrmse
        + 2.0 * noisy_nrmse
    )


def _passes(metrics0: dict, metrics1: dict, cond: float) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not math.isfinite(cond) or cond > 1_000.0:
        reasons.append("condition_number>1000")
    if metrics0["nrmse"] > 0.50:
        reasons.append("noiseless_nrmse>0.5")
    if metrics1["nrmse"] > 1.00:
        reasons.append("noisy_nrmse>1")
    return len(reasons) == 0, reasons


def _subset(ds: ProbeDataset, start: int, stop: int, values: np.ndarray) -> ProbeDataset:
    return ProbeDataset(
        ds.times[start:stop].copy(),
        np.asarray(values[start:stop], dtype=float).copy(),
        ds.channel_names,
        ds.channel_locations,
        ds.fields,
        ds.source_files,
    )


def _observableflow_predict(
    Z: np.ndarray,
    X: np.ndarray,
    *,
    pod_mean: np.ndarray,
    pod_basis: np.ndarray,
    A: np.ndarray,
    C: np.ndarray,
    state_offset: np.ndarray,
    measurement_offset: np.ndarray,
    selected: tuple[int, ...],
    depth: int,
    noise: np.ndarray | None,
) -> tuple[np.ndarray, np.ndarray]:
    O, q = _affine_observation_system(
        A,
        C,
        state_offset,
        measurement_offset,
        selected,
        depth,
    )
    pinv = np.linalg.pinv(O)
    xhat: list[np.ndarray] = []
    zhat: list[np.ndarray] = []
    for t in range(len(Z) - depth):
        blocks = []
        for k in range(depth + 1):
            y = Z[t + k, list(selected)].copy()
            if noise is not None:
                y = y + noise[t + k, list(selected)]
            blocks.append(y)
        x0 = pinv @ (np.concatenate(blocks) - q)
        xhat.append(x0)
        zhat.append(pod_mean + x0 @ pod_basis.T)
    return np.asarray(xhat), np.asarray(zhat)


def _evaluate_observableflow_candidate(
    candidate: StabilityCandidate,
    *,
    Z: np.ndarray,
    X: np.ndarray,
    pod_mean: np.ndarray,
    pod_basis: np.ndarray,
    A: np.ndarray,
    C: np.ndarray,
    state_offset: np.ndarray,
    measurement_offset: np.ndarray,
    noise: np.ndarray,
) -> dict:
    d = candidate.design
    x0, z0 = _observableflow_predict(
        Z,
        X,
        pod_mean=pod_mean,
        pod_basis=pod_basis,
        A=A,
        C=C,
        state_offset=state_offset,
        measurement_offset=measurement_offset,
        selected=d.selected,
        depth=d.depth,
        noise=None,
    )
    x1, z1 = _observableflow_predict(
        Z,
        X,
        pod_mean=pod_mean,
        pod_basis=pod_basis,
        A=A,
        C=C,
        state_offset=state_offset,
        measurement_offset=measurement_offset,
        selected=d.selected,
        depth=d.depth,
        noise=noise,
    )
    truth_z = Z[: len(z0)]
    truth_x = X[: len(x0)]
    m0 = _metrics(z0, truth_z)
    m1 = _metrics(z1, truth_z)
    r0 = _metrics(x0, truth_x)
    r1 = _metrics(x1, truth_x)
    passed, reasons = _passes(m0, m1, d.condition_number)
    return {
        "design": d.to_dict(),
        "structural_score": candidate.score,
        "validation_or_test_objective": _objective(
            d.total_cost, d.condition_number, m0["nrmse"], m1["nrmse"]
        ),
        "full_reference_noiseless": m0,
        "full_reference_noisy": m1,
        "reduced_state_noiseless": r0,
        "reduced_state_noisy": r1,
        "pass": passed,
        "reasons": reasons,
    }


def _run_pysensors(
    Z_train: np.ndarray,
    Z_eval: np.ndarray,
    *,
    pod_mean: np.ndarray,
    pod_basis: np.ndarray,
    max_sensors: int,
    noise_eval: np.ndarray,
    seed: int,
) -> list[dict]:
    try:
        from pysensors import SSPOR
        from pysensors.basis import Custom
        from pysensors.optimizers import QR
    except Exception as exc:  # pragma: no cover - exercised in external benchmark CI
        raise RuntimeError(
            "PySensors is required for this benchmark. Install the pinned baseline commit."
        ) from exc

    train_centered = Z_train - pod_mean
    eval_centered = Z_eval - pod_mean
    basis = Custom(pod_basis, n_basis_modes=pod_basis.shape[1])
    model = SSPOR(basis=basis, optimizer=QR(), n_sensors=max_sensors)
    model.fit(train_centered, seed=seed)

    out: list[dict] = []
    for k in range(1, max_sensors + 1):
        model.set_number_of_sensors(k)
        selected = tuple(int(i) for i in model.get_selected_sensors())
        rank, cond = _basis_rank_condition(pod_basis, selected)
        for method in ("unregularized", "regularized"):
            kwargs = {"method": "unregularized"} if method == "unregularized" else {"noise": 0.01}
            pred0 = model.predict(eval_centered[:, list(selected)], **kwargs) + pod_mean
            pred1 = model.predict(
                eval_centered[:, list(selected)] + noise_eval[:, list(selected)], **kwargs
            ) + pod_mean
            m0 = _metrics(pred0, Z_eval)
            m1 = _metrics(pred1, Z_eval)
            passed, reasons = _passes(m0, m1, cond)
            out.append(
                {
                    "method": method,
                    "selected": list(selected),
                    "sensor_count": k,
                    "depth": 0,
                    "rank": rank,
                    "target_rank": int(pod_basis.shape[1]),
                    "condition_number": cond,
                    "total_cost": float(k),
                    "validation_or_test_objective": _objective(k, cond, m0["nrmse"], m1["nrmse"]),
                    "full_reference_noiseless": m0,
                    "full_reference_noisy": m1,
                    "pass": passed,
                    "reasons": reasons,
                }
            )
    return out


def _best(candidates: list[dict]) -> dict:
    rank_feasible = [c for c in candidates if c["rank"] >= c["target_rank"]]
    pool = rank_feasible or candidates
    return min(
        pool,
        key=lambda c: (
            not c["pass"],
            c["validation_or_test_objective"],
            c["total_cost"],
        ),
    )


def _dominates(a: dict, b: dict) -> bool:
    ac = float(a["total_cost"])
    bc = float(b["total_cost"])
    a0 = float(a["full_reference_noiseless"]["nrmse"])
    b0 = float(b["full_reference_noiseless"]["nrmse"])
    a1 = float(a["full_reference_noisy"]["nrmse"])
    b1 = float(b["full_reference_noisy"]["nrmse"])
    weak = ac <= bc and a0 <= b0 and a1 <= b1
    strict = ac < bc or a0 < b0 or a1 < b1
    return bool(weak and strict)


def main() -> None:
    ap = argparse.ArgumentParser(description="ObservableFlow v0.5 vs pinned PySensors on one OpenFOAM trajectory")
    ap.add_argument("case")
    ap.add_argument("--output", required=True)
    ap.add_argument("--pod-rank", type=int, default=8)
    ap.add_argument("--max-depth", type=int, default=12)
    ap.add_argument("--max-sensors", type=int, default=8)
    ap.add_argument("--seed", type=int, default=20260910)
    args = ap.parse_args()

    if args.pod_rank < 1 or args.max_sensors < args.pod_rank:
        raise SystemExit("max_sensors must be >= pod_rank for the certificate-matched lane")

    ds = load_probes(args.case, object_name="observableFlowReference", fields=["p", "U"])
    Y = np.asarray(ds.values, dtype=float)
    n = len(Y)
    n_train = int(math.floor(0.60 * n))
    n_val = int(math.floor(0.20 * n))
    n_test = n - n_train - n_val
    if n_train <= args.pod_rank + 2 or n_val < args.max_depth + 2 or n_test < args.max_depth + 2:
        raise SystemExit("not enough samples for requested train/validation/test split")

    mu = Y[:n_train].mean(axis=0)
    sd = Y[:n_train].std(axis=0, ddof=1)
    floor = max(float(np.max(np.abs(Y[:n_train]))) * 1e-12, 1e-12)
    sd = np.maximum(sd, floor)
    Z = (Y - mu) / sd

    pod = pod_reduce_snapshots(Z[:n_train], rank=args.pod_rank)
    X = (Z - pod.mean) @ pod.basis

    train_ds = _subset(ds, 0, n_train, Z)
    model = fit_lti_probe_model(
        X[:n_train],
        train_ds,
        costs=np.ones(ds.n_channels),
        noise_std=np.full(ds.n_channels, 0.01),
        ridge=1e-10,
    )
    Bd, state_offset = _fit_affine(X[: n_train - 1], X[1:n_train], 1e-10)
    Bm, measurement_offset = _fit_affine(X[:n_train], Z[:n_train], 1e-10)
    A = Bd.T
    C = Bm.T

    raw_of = stability_greedy_candidates(
        model.transitions,
        model.measurement_jacobians,
        model.sensors,
        target_rank=args.pod_rank,
        max_depth=args.max_depth,
        max_sensors=args.max_sensors,
        depth_unit_cost=0.25,
        min_sigma=0.0,
        max_condition_number=1_000.0,
        condition_weight=0.25,
    )
    if not raw_of:
        raise SystemExit("ObservableFlow produced no full-rank candidates")

    val_start = n_train
    test_start = n_train + n_val
    Z_val, X_val = Z[val_start:test_start], X[val_start:test_start]
    Z_test, X_test = Z[test_start:], X[test_start:]
    rng_val = np.random.default_rng(args.seed + 1)
    rng_test = np.random.default_rng(args.seed + 2)
    noise_val = rng_val.normal(0.0, 0.01, size=Z_val.shape)
    noise_test = rng_test.normal(0.0, 0.01, size=Z_test.shape)

    of_val = [
        _evaluate_observableflow_candidate(
            c,
            Z=Z_val,
            X=X_val,
            pod_mean=pod.mean,
            pod_basis=pod.basis,
            A=A,
            C=C,
            state_offset=state_offset,
            measurement_offset=measurement_offset,
            noise=noise_val,
        )
        for c in raw_of
    ]
    of_selected_val = _best(of_val)
    of_key = (
        tuple(of_selected_val["design"]["selected"]),
        int(of_selected_val["design"]["depth"]),
    )
    selected_candidate = next(
        c for c in raw_of if (c.design.selected, c.design.depth) == of_key
    )
    of_test = _evaluate_observableflow_candidate(
        selected_candidate,
        Z=Z_test,
        X=X_test,
        pod_mean=pod.mean,
        pod_basis=pod.basis,
        A=A,
        C=C,
        state_offset=state_offset,
        measurement_offset=measurement_offset,
        noise=noise_test,
    )

    py_val = _run_pysensors(
        Z[:n_train],
        Z_val,
        pod_mean=pod.mean,
        pod_basis=pod.basis,
        max_sensors=args.max_sensors,
        noise_eval=noise_val,
        seed=args.seed,
    )
    py_selected_val = _best(py_val)

    # Recreate the pinned PySensors fit and evaluate only the validation-selected
    # method/sensor count on the untouched final test interval.
    py_test_candidates = _run_pysensors(
        Z[:n_train],
        Z_test,
        pod_mean=pod.mean,
        pod_basis=pod.basis,
        max_sensors=args.max_sensors,
        noise_eval=noise_test,
        seed=args.seed,
    )
    py_test = next(
        c for c in py_test_candidates
        if c["method"] == py_selected_val["method"]
        and c["selected"] == py_selected_val["selected"]
    )

    # Normalize the ObservableFlow output shape to the baseline shape for the
    # comparison block while retaining the richer design record elsewhere.
    of_cmp = {
        "total_cost": of_test["design"]["total_cost"],
        "full_reference_noiseless": of_test["full_reference_noiseless"],
        "full_reference_noisy": of_test["full_reference_noisy"],
    }
    py_cmp = {
        "total_cost": py_test["total_cost"],
        "full_reference_noiseless": py_test["full_reference_noiseless"],
        "full_reference_noisy": py_test["full_reference_noisy"],
    }

    result = {
        "data_label": "[SimulatedData]",
        "simulation": True,
        "benchmark": "ObservableFlow v0.5 stability-aware vs PySensors SSPOR/QR",
        "scope": (
            "Certificate-matched reduced-order benchmark on one OpenFOAM-13 cavity trajectory. "
            "The 7x7 p,U probe grid is a dense sampled surrogate, not the native CFD mesh."
        ),
        "upstream": {
            "openfoam_repository": OPENFOAM_REPO,
            "openfoam_commit": OPENFOAM_COMMIT,
            "openfoam_case": OPENFOAM_CASE,
            "pysensors_repository": PYSENSORS_REPO,
            "pysensors_commit": PYSENSORS_COMMIT,
        },
        "runtime": {
            "observableflow_commit": os.environ.get("GITHUB_SHA", "local"),
            "openfoam_image": os.environ.get("OPENFOAM_IMAGE", "unknown"),
        },
        "configuration": {
            "samples": n,
            "channels": ds.n_channels,
            "pod_rank": args.pod_rank,
            "pod_train_energy_fraction": float(np.sum(pod.explained_energy_ratio)),
            "train_samples": n_train,
            "validation_samples": n_val,
            "test_samples": n_test,
            "max_sensors": args.max_sensors,
            "max_depth": args.max_depth,
            "sensor_channel_cost": 1.0,
            "depth_unit_cost": 0.25,
            "noise_std_in_train_standardized_units": 0.01,
            "selection_objective": "cost + 0.25*log10(kappa) + 4*validation_nrmse + 2*validation_noisy_nrmse",
            "deployment_gates": {
                "max_condition_number": 1000.0,
                "max_noiseless_nrmse": 0.50,
                "max_noisy_nrmse": 1.00,
            },
            "anti_leakage": "POD/ROM/sensor ranking fit on train only; design/method chosen on validation; final metrics from untouched test only.",
        },
        "observableflow": {
            "candidate_count": len(of_val),
            "validation_selected": of_selected_val,
            "test": of_test,
        },
        "pysensors": {
            "baseline": "SSPOR + QR with PySensors Custom basis set to the exact same training POD basis",
            "validation_candidate_count": len(py_val),
            "validation_selected": py_selected_val,
            "test": py_test,
        },
        "comparison": {
            "observableflow_pareto_dominates_on_test": _dominates(of_cmp, py_cmp),
            "pysensors_pareto_dominates_on_test": _dominates(py_cmp, of_cmp),
            "observableflow_test_objective": _objective(
                of_cmp["total_cost"],
                of_test["design"]["condition_number"],
                of_cmp["full_reference_noiseless"]["nrmse"],
                of_cmp["full_reference_noisy"]["nrmse"],
            ),
            "pysensors_test_objective": py_test["validation_or_test_objective"],
            "market_superiority_claim": False,
            "note": "A single benchmark can support a benchmark-specific comparison, not a general market-superiority claim.",
        },
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "observableflow_validation_selected": of_selected_val,
        "observableflow_test": of_test,
        "pysensors_validation_selected": py_selected_val,
        "pysensors_test": py_test,
        "comparison": result["comparison"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
