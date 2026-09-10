#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from observableflow.openfoam import load_probes
from observableflow.openfoam_benchmark import benchmark_probe_reference_case

UPSTREAM_REPO = "https://github.com/OpenFOAM/OpenFOAM-13"
UPSTREAM_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
UPSTREAM_CASE = "tutorials/incompressibleFluid/cavity"


def _hash_tree(root: Path) -> dict[str, str]:
    out = {}
    if not root.exists():
        return out
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _costs_for(ds, p_cost=1.0, u_component_cost=2.0):
    costs = []
    for name in ds.channel_names:
        costs.append(p_cost if name.startswith("p[") else u_component_cost)
    return costs


def run_one(case: Path, fields: list[str], *, pod_rank: int, max_depth: int, max_sensors: int):
    ds = load_probes(case, object_name="observableFlowCandidates", fields=fields)
    return benchmark_probe_reference_case(
        case,
        candidate_object="observableFlowCandidates",
        reference_object="observableFlowReference",
        candidate_fields=fields,
        reference_fields=["p", "U"],
        pod_rank=pod_rank,
        train_fraction=0.70,
        max_depth=max_depth,
        max_sensors=max_sensors,
        depth_unit_cost=0.25,
        noise_fraction=0.01,
        ridge=1e-10,
        min_sigma=0.0,
        seed=20260910,
        costs=_costs_for(ds),
    )


def _assess_design(block: dict, kind: str, *, max_condition: float, max_noiseless_nrmse: float, max_noisy_nrmse: float) -> dict:
    design = block.get(f"{kind}_design")
    noiseless = block.get(f"{kind}_holdout_noiseless")
    noisy = block.get(f"{kind}_holdout_noisy")
    reasons: list[str] = []
    if not design or not design.get("feasible"):
        reasons.append("rank/information feasibility failed")
    if not noiseless:
        reasons.append("no noiseless holdout reconstruction")
    if not noisy:
        reasons.append("no noisy holdout reconstruction")
    if design and design.get("condition_number", float("inf")) > max_condition:
        reasons.append(f"condition_number>{max_condition:g}")
    if noiseless and noiseless.get("nrmse", float("inf")) > max_noiseless_nrmse:
        reasons.append(f"noiseless_nrmse>{max_noiseless_nrmse:g}")
    if noisy and noisy.get("nrmse", float("inf")) > max_noisy_nrmse:
        reasons.append(f"noisy_nrmse>{max_noisy_nrmse:g}")
    return {
        "kind": kind,
        "pass": not reasons,
        "reasons": reasons,
        "design": design,
        "holdout_noiseless": noiseless,
        "holdout_noisy": noisy,
    }


def _deployment_verdict(block: dict, *, max_condition: float, max_noiseless_nrmse: float, max_noisy_nrmse: float) -> dict:
    candidates = [
        _assess_design(block, "static", max_condition=max_condition, max_noiseless_nrmse=max_noiseless_nrmse, max_noisy_nrmse=max_noisy_nrmse),
        _assess_design(block, "temporal", max_condition=max_condition, max_noiseless_nrmse=max_noiseless_nrmse, max_noisy_nrmse=max_noisy_nrmse),
    ]
    passing = [c for c in candidates if c["pass"]]
    selected = None
    if passing:
        selected = min(
            passing,
            key=lambda c: (
                c["design"]["total_cost"],
                c["design"]["condition_number"],
                len(c["design"]["selected"]),
                c["design"]["depth"],
            ),
        )
    return {
        "pass": selected is not None,
        "selected_kind": None if selected is None else selected["kind"],
        "selected_design": None if selected is None else selected["design"],
        "criteria": {
            "max_condition_number": max_condition,
            "max_noiseless_nrmse": max_noiseless_nrmse,
            "max_noisy_nrmse": max_noisy_nrmse,
            "note": "Declared engineering benchmark gates; not a theorem or universal physical threshold.",
        },
        "candidates": candidates,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze the real OpenFOAM-13 cavity run with ObservableFlow")
    ap.add_argument("case")
    ap.add_argument("--output", required=True)
    ap.add_argument("--pod-rank", type=int, default=4)
    ap.add_argument("--max-depth", type=int, default=12)
    ap.add_argument("--max-sensors", type=int, default=8)
    ap.add_argument("--max-condition", type=float, default=1e3)
    ap.add_argument("--max-noiseless-nrmse", type=float, default=0.5)
    ap.add_argument("--max-noisy-nrmse", type=float, default=1.0)
    args = ap.parse_args()
    case = Path(args.case)

    pressure = run_one(case, ["p"], pod_rank=args.pod_rank, max_depth=args.max_depth, max_sensors=args.max_sensors)
    multimodal = run_one(case, ["p", "U"], pod_rank=args.pod_rank, max_depth=args.max_depth, max_sensors=args.max_sensors)

    result = {
        "data_label": "[SimulatedData]",
        "simulation": True,
        "benchmark": "OpenFOAM-13 lid-driven cavity / ObservableFlow v0.4",
        "scope": "Real OpenFOAM solver output; dense probe grid is a sampled reference surrogate, not the native full CFD mesh.",
        "upstream": {
            "repository": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "case": UPSTREAM_CASE,
        },
        "runtime": {
            "openfoam_image": os.environ.get("OPENFOAM_IMAGE", "unknown"),
            "openfoam_image_digest": os.environ.get("OPENFOAM_IMAGE_DIGEST", "unknown"),
            "observableflow_commit": os.environ.get("GITHUB_SHA", "local"),
        },
        "configuration": {
            "pod_rank": args.pod_rank,
            "max_depth": args.max_depth,
            "max_sensors": args.max_sensors,
            "train_fraction": 0.70,
            "noise_fraction_of_train_channel_std": 0.01,
            "depth_unit_cost": 0.25,
            "pressure_channel_cost": 1.0,
            "velocity_component_channel_cost": 2.0,
        },
        "pressure_only": pressure.to_dict(),
        "pressure_velocity": multimodal.to_dict(),
        "postprocessing_sha256": {
            "candidates": _hash_tree(case / "postProcessing" / "observableFlowCandidates"),
            "reference": _hash_tree(case / "postProcessing" / "observableFlowReference"),
        },
    }
    result["deployment_verdict"] = _deployment_verdict(
        result["pressure_velocity"],
        max_condition=args.max_condition,
        max_noiseless_nrmse=args.max_noiseless_nrmse,
        max_noisy_nrmse=args.max_noisy_nrmse,
    )

    mm = result["pressure_velocity"]
    if not mm.get("temporal_design") or not mm["temporal_design"].get("feasible"):
        raise SystemExit("FAIL: no rank-feasible multimodal temporal design")
    if mm.get("temporal_holdout_noiseless") is None or mm.get("static_holdout_noiseless") is None:
        raise SystemExit("FAIL: temporal/static holdout reconstruction was not produced")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "pressure_velocity_static": mm["static_design"],
        "pressure_velocity_static_holdout_noiseless": mm["static_holdout_noiseless"],
        "pressure_velocity_static_holdout_noisy": mm["static_holdout_noisy"],
        "pressure_velocity_temporal": mm["temporal_design"],
        "pressure_velocity_temporal_holdout_noiseless": mm["temporal_holdout_noiseless"],
        "pressure_velocity_temporal_holdout_noisy": mm["temporal_holdout_noisy"],
        "deployment_verdict": result["deployment_verdict"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
