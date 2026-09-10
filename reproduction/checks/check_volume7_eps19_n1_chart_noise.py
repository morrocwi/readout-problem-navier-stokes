#!/usr/bin/env python3
"""Branch-conditioned finite noise propagation for the fixed N=1 EPSC chart.

This checker advances EPSC-19 only one explicitly delimited step.

Inputs already certified elsewhere in this repository:
  * the full N=1 translation quotient has an explicit 49-dimensional slice;
  * the selected 49 shell-energy Taylor observations define a square chart H_1;
  * exact centered interval propagation certifies
        q = sup_{x in B} ||I-A DH_1(x)||_inf <= 1/2
    on the finite box B = {||x-x_*||_inf <= 10^-17};
  * the exact characteristic-zero center inverse A=DH_1(x_*)^-1 satisfies
        ||A||_inf < 1.29.

For any x,z in the SAME certified branch box B, the finite mean-value/preconditioned
inverse estimate gives

    ||x-z||_inf <= ||A||_inf/(1-q) * ||H_1(x)-H_1(z)||_inf
                < 2.58 * ||H_1(x)-H_1(z)||_inf.

Hence if measured chart data y obeys ||y-H_1(x)||_inf <= sigma and a candidate z in B
obeys ||H_1(z)-y||_inf <= tau, then

    ||x-z||_inf < (129/50) * (sigma+tau).

Everything here is finite-native. H_1 is the finite selected, row-scaled shell-energy
Taylor chart. This is NOT yet a theorem converting raw noisy time samples into H_1,
NOT a global branch-capture theorem, NOT an arbitrary-N result, and NOT a continuum
regularity or Clay statement.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_exact_preconditioner as exact
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910
BRANCH_RADIUS = Fraction(1, 10**17)
Q_CERTIFIED_UPPER = Fraction(1, 2)
A_INF_DECLARED_UPPER = Fraction(129, 100)
FACTOR_UPPER = A_INF_DECLARED_UPPER / (1 - Q_CERTIFIED_UPPER)  # 129/50 = 2.58


def reproduce_entrywise_gate() -> tuple[bool, dict]:
    """Run the exact interval checker and require its finite q<=1/2 claims."""
    checker = HERE / "check_volume7_eps18_n1_exact_entrywise_interval.py"
    env = dict(os.environ)
    env.setdefault("PYTHONINTMAXSTRDIGITS", "0")
    proc = subprocess.run(
        [sys.executable, str(checker)],
        cwd=str(HERE.parent.parent),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    payload = None
    for line in proc.stdout.splitlines():
        if line.startswith("RESULT_JSON:"):
            payload = json.loads(line[len("RESULT_JSON:"):])
    if proc.returncode != 0 or payload is None:
        return False, {"returncode": proc.returncode, "stderr_tail": proc.stderr[-1000:]}
    by_id = {c["id"]: c for c in payload.get("claims", [])}
    ok = (
        by_id.get("V7-EPSC18-N1-EXACT-ENTRYWISE-INTERVAL", {}).get("status") == "PASS"
        and by_id.get("V7-EPSC18-N1-EXACT-ENTRYWISE-RADIUS", {}).get("status") == "DERIVED"
    )
    return ok, {"returncode": proc.returncode, "claims": by_id}


def exact_center_inverse_norm() -> Fraction:
    """Reconstruct the selected characteristic-zero Jacobian and its exact inverse norm."""
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared N=1 small-integer center did not reproduce")

    x0 = small.small_state(CENTER_SEED, cube.d)
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    selected = [int(v) for v in center["selected_observation_rows"]]
    shells = len(cube.shells)
    if len(free) != 49 or len(selected) != 49:
        raise RuntimeError("checker is scoped to the declared 49-dimensional N=1 chart")

    blocks = exact.exact_scaled_shell_blocks(cube, x0)
    J0 = [
        [int(blocks[r // shells][r % shells, j]) for j in free]
        for r in selected
    ]
    A, det_j0 = exact.exact_inverse(J0)
    if det_j0 == 0:
        raise ArithmeticError("selected exact N=1 Jacobian is singular")
    return max(sum((abs(v) for v in row), Fraction(0)) for row in A)


def main() -> int:
    gate_ok, gate_detail = reproduce_entrywise_gate()
    a_inf = exact_center_inverse_norm()
    a_norm_ok = Fraction(128, 100) < a_inf < A_INF_DECLARED_UPPER
    factor_ok = FACTOR_UPPER == Fraction(129, 50)
    prerequisites_ok = gate_ok and a_norm_ok and factor_ok

    claims = [
        {
            "id": "V7-EPSC19-N1-BRANCH-CHART-PREREQUISITES",
            "name": "fixed N=1 branch box and exact preconditioner support finite noisy-chart propagation",
            "tier": "finite_diagnostic",
            "status": "PASS" if prerequisites_ok else "FAIL",
            "evidence": (
                "re-ran exact N=1 entrywise checker: q<=1/2 on ||x-x_*||_inf<=10^-17; "
                "reconstructed exact center inverse with 1.28<||A||_inf<1.29"
                if prerequisites_ok else
                f"gate_ok={gate_ok}; a_norm_ok={a_norm_ok}; detail={gate_detail}"
            ),
        },
        {
            "id": "V7-EPSC19-N1-SCALED-CHART-NOISE-PROPAGATION",
            "name": "branch-conditioned measurement and forward-residual uncertainty propagate to a finite N=1 state radius",
            "tier": "Dr",
            "status": "DERIVED" if prerequisites_ok else "OPEN",
            "evidence": (
                "for true x and candidate z both in the certified N=1 branch box, "
                "||y-H_1(x)||_inf<=sigma and ||H_1(z)-y||_inf<=tau imply "
                "||x-z||_inf < (129/50)(sigma+tau); H_1 is the selected finite row-scaled shell-energy Taylor chart"
                if prerequisites_ok else
                "the exact branch/preconditioner prerequisites were not reproduced"
            ),
        },
        {
            "id": "V7-EPSC19-N1-RAW-WINDOW-TO-CHART-BRANCH-CAPTURE",
            "name": "raw finite-window energy measurements are converted to the selected N=1 chart with certified branch capture",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the present result begins after a branch box and scaled chart uncertainty are supplied; "
                "a derivative-free finite sample/window map with validated Taylor/flow remainder and branch selection is still required"
            ),
        },
        {
            "id": "V7-EPSC19-ARBITRARY-FINITE-N-NOISE-PROPAGATION",
            "name": "branch-conditioned noisy-chart radius is certified by a uniform construction for arbitrary finite N",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "this checker is fixed N=1 only; N=2 currently has only a very conservative positive local inverse radius, "
                "and no arbitrary-finite-N conditioning law is proved"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "slice_dimension": 49,
        "branch_radius": "1e-17",
        "q_certified_upper": "1/2",
        "exact_inverse_norm_float_display": float(a_inf),
        "declared_inverse_norm_upper": "129/100",
        "noise_to_state_factor_upper": "129/50",
        "noise_to_state_factor_float_display": float(FACTOR_UPPER),
        "chart": "selected C^n n! row-scaled shell-energy Taylor chart H_1",
        "branch_hypothesis": "true state and reconstruction candidate both lie in the same certified local box",
        "finite_first_scope": "fixed finite N=1 quotient chart; no completed-infinity premise",
        "raw_sensor_status": "OPEN",
    }
    print("EPSC-19 fixed-N=1 branch-conditioned chart-noise certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
