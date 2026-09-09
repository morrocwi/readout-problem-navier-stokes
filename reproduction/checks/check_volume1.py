#!/usr/bin/env python3
"""
Reproduction check for Volume 1 ("State Breakdown Is Not Readout Breakdown -- A
Discrete-Native Framework for Interpreting Forced Navier-Stokes Singularities", v0.1,
pp.3-15 of the combined 6-volume PDF).

This is the SAME finite witness (NSR-01) already published and independently verified
in this repository at verification/verify_state_breakdown_math.py (GLS-2026-006). This
script re-derives it independently inside the reproduction/ subsystem so that
reproduce_all.sh + generate_ledger.py cover Volume 1 without silently relying on the
older script's exit code.

Prints per-claim evidence, then a single machine-readable RESULT_JSON line consumed by
generate_ledger.py.
"""
import itertools
import json
import sys

S = list(itertools.product([0, 1], repeat=3))


def F(s):
    a, b, c = s
    return (1 - a, b, 1 - c)


def FD(d):
    a, b = d
    return (1 - a, b)


def qD(s):
    a, b, c = s
    return (a, b)


def O(s):
    return s[1]


def OD(d):
    return d[1]


def Q(d):
    return d[0]


def main():
    results = []
    ok = True

    dyn_weld = sum(qD(F(s)) == FD(qD(s)) for s in S)
    obs_weld = sum(O(s) == OD(qD(s)) for s in S)
    f2_id = all(F(F(s)) == s for s in S)

    print("=== Volume 1 / NSR-01: 8-state finite non-entailment witness ===")
    print("finite states |S|:", len(S))
    print("dynamical weld  q_D(F s) == F_D(q_D s):", dyn_weld, "/", len(S))
    print("observational weld  O(s) == O_D(q_D s):", obs_weld, "/", len(S))
    print("F^2 = Id:", f2_id)

    weld_ok = (dyn_weld == len(S)) and (obs_weld == len(S)) and f2_id
    ok = ok and weld_ok
    results.append({
        "id": "NSR-01-weld",
        "name": "Exact weld (dynamical + observational) over all 8 states, F^2=Id",
        "tier": "finite_diagnostic",
        "status": "PASS" if weld_ok else "FAIL",
        "evidence": f"dyn_weld={dyn_weld}/8 obs_weld={obs_weld}/8 F^2=Id:{f2_id}",
    })

    # Witness pair as literally stated in Volume 1 Definition 5.1 (P-NSR-W3):
    # z = (0,0,0), z' = (1,0,0). (Volume 2/3's own restatement of this witness,
    # Theorem 3.1/9.1, uses a different pair z' = (1,0,1) -- each volume's check
    # uses that volume's own literal stated pair, not a shared substitute.)
    z, zp = (0, 0, 0), (1, 0, 0)
    x, y = z, zp
    K = 10000
    witness_ok = True
    for k in range(K):
        same_obs = (O(x) == O(y))
        diff_q = (Q(qD(x)) != Q(qD(y)))
        if not (same_obs and diff_q):
            witness_ok = False
            break
        x, y = F(x), F(y)
    ok = ok and witness_ok
    print(f"witness pair z={z}, z'={zp}: O(F^k z)==O(F^k z') and "
          f"Q(qD(F^k z))!=Q(qD(F^k z')) verified for k=0..{K-1}:", witness_ok)
    results.append({
        "id": "NSR-01-witness",
        "name": "Witness pair stays O-equivalent / Q-inequivalent for every tested finite horizon",
        "tier": "finite_diagnostic",
        "status": "PASS" if witness_ok else "FAIL",
        "evidence": f"verified k=0..{K-1}",
    })

    # Corollary (non-entailment) is an immediate logical corollary of the witness above.
    cor_ok = weld_ok and witness_ok
    results.append({
        "id": "NSR-01-corollary",
        "name": "Non-entailment corollary: exact weld + exact factorization does not imply finite-horizon decidability",
        "tier": "finite_diagnostic",
        "status": "PASS" if cor_ok else "FAIL",
        "evidence": "immediate from NSR-01-weld and NSR-01-witness above",
    })

    # Appendix items, explicitly not machine-checked here.
    results.append({
        "id": "Vol1-AppendixB-code-family",
        "name": "Proposed Toledo code family for NSR-01/NSR-W1/NSR-02/NSR-03/NSR-04 under weld root",
        "tier": "Open",
        "status": "OPEN",
        "evidence": "Explicitly proposal/unregistered status per the paper's own Appendix B; not a registered Toledo canonical entry, nothing to mechanically check.",
    })
    results.append({
        "id": "Vol1-AppendixC-coq-witness",
        "name": "NSR01_finite_witness.v Coq script (arXiv bundle)",
        "tier": "finite_diagnostic",
        "status": "NOT_RUN",
        "evidence": "Coq file exists in the arXiv bundle location but was not compiled with coqc in this workspace or by this reproduction run (self-flagged by the paper itself as not Th_coqc). The Python re-derivation above (NSR-01-weld/witness) independently covers the same finite claim by direct enumeration.",
    })
    results.append({
        "id": "Vol1-AppendixD-weld-exclusion",
        "name": "Deliberate exclusion of weld/M.39.v1 (registry presence != theorem status)",
        "tier": "Dr",
        "status": "N/A",
        "evidence": "A methodological/source-audit statement, not a numeric or combinatorial claim; nothing to run. Confirmed by inspection that Volumes 1-6 never cite weld/M.39.v1 to derive a result.",
    })
    results.append({
        "id": "NSR-02/03/04",
        "name": "Navier-Stokes bridge obligations connecting continuum singularity to finite-readout breakdown",
        "tier": "Open",
        "status": "OPEN",
        "evidence": "Explicitly posed, not answered, by Volume 1 itself. No construction given to check.",
    })

    print("RESULT_JSON:" + json.dumps({"volume": 1, "claims": results}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
