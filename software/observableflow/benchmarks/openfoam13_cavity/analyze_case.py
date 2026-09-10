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


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze the real OpenFOAM-13 cavity run with ObservableFlow")
    ap.add_argument("case")
    ap.add_argument("--output", required=True)
    ap.add_argument("--pod-rank", type=int, default=4)
    ap.add_argument("--max-depth", type=int, default=12)
    ap.add_argument("--max-sensors", type=int, default=8)
    args = ap.parse_args()
    case = Path(args.case)

    pressure = run_one(case, ["p"], pod_rank=args.pod_rank, max_depth=args.max_depth, max_sensors=args.max_sensors)
    multimodal = run_one(case, ["p", "U"], pod_rank=args.pod_rank, max_depth=args.max_depth, max_sensors=args.max_sensors)

    result = {
        "data_label": "[SimulatedData]",
        "simulation": True,
        "benchmark": "OpenFOAM-13 lid-driven cavity / ObservableFlow v0.3",
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

    mm = result["pressure_velocity"]
    if not mm.get("temporal_design") or not mm["temporal_design"].get("feasible"):
        raise SystemExit("FAIL: no feasible multimodal temporal design")
    if mm.get("holdout_noiseless") is None or mm.get("holdout_noisy") is None:
        raise SystemExit("FAIL: holdout reconstruction was not produced")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "pressure_only_temporal": result["pressure_only"]["temporal_design"],
        "pressure_velocity_temporal": result["pressure_velocity"]["temporal_design"],
        "pressure_velocity_holdout_noiseless": result["pressure_velocity"]["holdout_noiseless"],
        "pressure_velocity_holdout_noisy": result["pressure_velocity"]["holdout_noisy"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
