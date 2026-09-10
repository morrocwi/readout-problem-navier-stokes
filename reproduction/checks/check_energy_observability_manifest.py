#!/usr/bin/env python3
"""Quick deterministic verifier for the committed energy-observability package.

This does not rerun the expensive formal Taylor/tangent calculations. It checks
that the committed machine-readable certificates have the expected invariant
fields and that the all-N dimension/shell formulas agree with those records.
Use `bash reproduction/reproduce_energy_observability.sh` for a full rerun.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPRO = HERE.parent
ROOT = REPRO.parent
RESULTS = REPRO / "results"


def d_n(n: int) -> int:
    return 2 * ((2 * n + 1) ** 3 - 1)


def shells(n: int) -> list[int]:
    return sorted({x*x + y*y + z*z for x,y,z in itertools.product(range(-n,n+1), repeat=3) if (x,y,z)!=(0,0,0)})


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def load(name: str) -> dict:
    p = RESULTS / name
    require(p.exists(), f"missing result file: {p}")
    return json.loads(p.read_text())


def main() -> int:
    k2 = load("k2_energy_observability_mod251.json")
    k3 = load("k3_shell_energy_observability_mod683.json")

    require(d_n(1) == 52 and d_n(2) == 248 and d_n(3) == 684, "dimension formula mismatch")
    require(shells(1) == [1,2,3], "K=1 shell set mismatch")
    require(shells(3) == [1,2,3,4,5,6,8,9,10,11,12,13,14,17,18,19,22,27], "K=3 shell set mismatch")

    require(k2.get("status") == "PASS", "K=2 stored certificate is not PASS")
    require(k2.get("N") == 2 and k2.get("prime") == 251, "K=2 metadata mismatch")
    require(k2.get("real_state_dimension") == 248, "K=2 d_N mismatch")
    require(k2.get("translation_ceiling") == 245, "K=2 translation ceiling mismatch")
    require(k2.get("scalar_min_possible_order") == 244, "K=2 earliest scalar order mismatch")
    require(k2.get("final_rank_R244") == 245, "K=2 final rank mismatch")
    for r, rec in k2.get("milestones", {}).items():
        R = int(r)
        require(int(rec["rank"]) == min(R+1,245), f"K=2 milestone mismatch at R={R}")

    require(k3.get("status") == "PASS", "K=3 stored certificate is not PASS")
    require(k3.get("simulation") is False, "K=3 must be marked Simulation=No")
    require(k3.get("N") == 3 and k3.get("prime") == 683, "K=3 metadata mismatch")
    require(k3.get("real_state_dimension") == 684, "K=3 d_N mismatch")
    require(k3.get("translation_ceiling") == 681, "K=3 translation ceiling mismatch")
    require(k3.get("shell_count") == 18 and k3.get("shells") == shells(3), "K=3 shell metadata mismatch")
    require(k3.get("earliest_possible_shell_order") == 39, "K=3 earliest shell order mismatch")
    require(k3.get("final_rank") == 681, "K=3 final rank mismatch")
    for r, rank in k3.get("milestones", {}).items():
        R = int(r)
        require(int(rank) == min(18 + 17*R, 681), f"K=3 milestone mismatch at R={R}")

    expected_paths = [
        ROOT / "paper" / "NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex",
        HERE / "check_volume6_ns_observability.py",
        HERE / "check_positive_viscosity_scaling.py",
        HERE / "check_k2_energy_observability.py",
        HERE / "check_k3_shell_energy_observability.py",
    ]
    for p in expected_paths:
        require(p.exists(), f"missing source: {p}")

    report = {
        "status": "PASS",
        "simulation": False,
        "checked": {
            "all_N_dimensions": {"1": 52, "2": 248, "3": 684},
            "K1_expected_from_exact_checker": {"scalar": {"R": 48, "rank": 49}, "shell": {"R": 23, "rank": 49}},
            "K2_stored": {"R": 244, "rank": 245, "prime": 251},
            "K3_stored": {"R": 39, "rank": 681, "prime": 683, "channels": 18},
        },
    }
    print("RESULT_JSON:" + json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
