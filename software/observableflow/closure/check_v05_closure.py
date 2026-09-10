#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MANIFEST_PATH = HERE / "OBSERVABLEFLOW_V05_FINAL_MANIFEST.json"


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result_rel = manifest["benchmark_result"]["path"]
    result_path = REPO / result_rel
    result = json.loads(result_path.read_text(encoding="utf-8"))

    assert manifest["project"] == "ObservableFlow"
    assert manifest["version"] == "0.5.0"
    assert manifest["status"] == "CLOSED"
    assert manifest["simulation"] is True
    assert manifest["data_label"] == "[SimulatedData]"

    blob = subprocess.check_output(
        ["git", "hash-object", str(result_path)], cwd=REPO, text=True
    ).strip()
    assert blob == manifest["benchmark_result"]["blob_sha"], (blob, manifest["benchmark_result"]["blob_sha"])

    assert result["simulation"] is True
    assert result["data_label"] == "[SimulatedData]"
    assert result["runtime"]["observableflow_commit"] == manifest["benchmark_execution_commit"]
    assert result["upstream"]["openfoam_commit"] == manifest["upstream_pins"]["openfoam_commit"]
    assert result["upstream"]["pysensors_commit"] == manifest["upstream_pins"]["pysensors_commit"]
    assert result["runtime"]["openfoam_image"] == manifest["upstream_pins"]["openfoam_runtime_image"]

    cfg = manifest["configuration"]
    rcfg = result["configuration"]
    assert rcfg["samples"] == cfg["samples"]
    assert rcfg["channels"] == cfg["scalar_channels"]
    assert rcfg["pod_rank"] == cfg["pod_rank"]
    assert rcfg["train_samples"] == cfg["split"]["train_samples"]
    assert rcfg["validation_samples"] == cfg["split"]["validation_samples"]
    assert rcfg["test_samples"] == cfg["split"]["test_samples"]
    assert rcfg["max_sensors"] == cfg["max_sensors"]
    assert rcfg["max_depth"] == cfg["max_temporal_depth"]
    assert close(rcfg["sensor_channel_cost"], cfg["sensor_channel_cost"])
    assert close(rcfg["depth_unit_cost"], cfg["temporal_depth_unit_cost"])
    assert close(rcfg["noise_std_in_train_standardized_units"], cfg["noise_std_in_train_standardized_units"])
    assert rcfg["selection_objective"] == cfg["selection_objective"]
    assert rcfg["deployment_gates"] == cfg["deployment_gates"]

    of = result["observableflow"]["test"]
    py = result["pysensors"]["test"]
    mof = manifest["test_results"]["observableflow"]
    mpy = manifest["test_results"]["pysensors"]

    assert list(of["design"]["selected"]) == mof["selected_channel_indices"]
    assert of["design"]["depth"] == mof["temporal_depth"]
    assert of["design"]["rank"] == mof["rank"]
    assert of["design"]["target_rank"] == mof["target_rank"]
    assert close(of["design"]["condition_number"], mof["condition_number"])
    assert close(of["design"]["total_cost"], mof["declared_total_cost"])
    assert close(of["full_reference_noiseless"]["nrmse"], mof["full_reference_noiseless_nrmse"])
    assert close(of["full_reference_noisy"]["nrmse"], mof["full_reference_noisy_nrmse"])
    assert bool(of["pass"]) is mof["deployment_pass"]

    assert py["sensor_count"] == mpy["spatial_channels"]
    assert py["depth"] == mpy["temporal_depth"]
    assert py["rank"] == mpy["rank"]
    assert py["target_rank"] == mpy["target_rank"]
    assert close(py["condition_number"], mpy["condition_number"])
    assert close(py["total_cost"], mpy["declared_total_cost"])
    assert close(py["full_reference_noiseless"]["nrmse"], mpy["full_reference_noiseless_nrmse"])
    assert close(py["full_reference_noisy"]["nrmse"], mpy["full_reference_noisy_nrmse"])
    assert bool(py["pass"]) is mpy["deployment_pass"]

    cmp = result["comparison"]
    mcmp = manifest["test_results"]["comparison"]
    assert cmp["observableflow_pareto_dominates_on_test"] is mcmp["observableflow_pareto_dominates_on_declared_test_axes"]
    assert cmp["pysensors_pareto_dominates_on_test"] is mcmp["pysensors_pareto_dominates_on_declared_test_axes"]
    assert cmp["market_superiority_claim"] is False
    assert cmp["observableflow_deployment_pass"] is False
    assert cmp["pysensors_deployment_pass"] is False
    assert mcmp["market_superiority_claim"] is False
    assert mcmp["deployment_ready_claim"] is False

    print("PASS")
    print("Simulation=No (closure metadata consistency check)")
    print("Frozen benchmark data label=[SimulatedData], Simulation=Yes")
    print(f"result_blob={blob}")
    print(f"workflow_run={manifest['benchmark_result']['workflow_run_id']}")


if __name__ == "__main__":
    main()
