#!/usr/bin/env python3
"""
Reproduction check for Volume 3 ("State Breakdown Is Not Readout Breakdown -- A
Fourier-Mode Separation for Navier-Stokes Readouts", v0.3, pp.24-29).

Volume 3 is mostly continuum Fourier/Sobolev analysis (Gronwall-type bounded-variation
arguments, weak-* compactness) applied to an ASSUMED hypothetical breakdown solution --
none of that is mechanically checkable, and the extraction pass correctly classified
almost every numbered result as such. The two genuinely mechanical items are:
  (a) Theorem 9.1, which the paper itself states is an exact restatement of Volume 2's
      Theorem 3.1 (the same 8-state witness) -- re-derived here, but the ledger treats
      it as ONE claim with two citation sites, not two independent claims.
  (b) Prop 5.1's finite constant C_M = (sum_{k in K_M} |k|^2)^{1/2} over a finite mode
      set K_M -- a directly computable finite sum for any concrete M.
"""
import itertools
import json
import sys

import numpy as np


def check_witness_restated():
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

    dyn = sum(qD(F(s)) == FD(qD(s)) for s in S)
    obs = sum(O(s) == OD(qD(s)) for s in S)
    f2 = all(F(F(s)) == s for s in S)
    ok = (dyn == 8) and (obs == 8) and f2
    print(f"[Thm 9.1] restated 8-state witness (identical to Vol.2 Thm 3.1 / Vol.1 NSR-01): "
          f"dyn={dyn}/8 obs={obs}/8 F^2=Id:{f2}")
    return ok


def check_finite_mode_constant():
    """Prop 5.1: C_M = (sum_{k in K_M} |k|^2)^{1/2} for a 3D cubic mode cutoff K_M."""
    results = {}
    for M in (1, 2, 3):
        K_M = [k for k in itertools.product(range(-M, M + 1), repeat=3)]
        C_M = float(np.sqrt(sum(sum(ki ** 2 for ki in k) for k in K_M)))
        results[M] = (len(K_M), C_M)
        print(f"[Prop 5.1] M={M}: |K_M|={len(K_M)} finite modes, C_M = {C_M:.6f}")
    # sanity: C_M must be strictly increasing in M (more/larger modes -> larger constant)
    ok = results[1][1] < results[2][1] < results[3][1]
    print(f"[Prop 5.1] C_M strictly increasing in M (sanity check): {ok}")
    return ok


def main():
    results = []

    witness_ok = check_witness_restated()
    results.append({
        "id": "Vol3-Thm9.1",
        "name": "Exact welded domain difference with permanent reader equivalence (restatement of Vol.2 Thm 3.1)",
        "tier": "finite_diagnostic",
        "status": "PASS" if witness_ok else "FAIL",
        "evidence": "identical construction to Vol.2 Thm 3.1 / Vol.1 NSR-01; ledger treats this as the SAME claim cited from three sites, not three independent claims",
    })

    cm_ok = check_finite_mode_constant()
    results.append({
        "id": "Vol3-Prop5.1-CM",
        "name": "Finite-cutoff constant C_M = (sum_{k in K_M}|k|^2)^(1/2) is a computable finite sum",
        "tier": "finite_diagnostic",
        "status": "PASS" if cm_ok else "FAIL",
        "evidence": "computed for M=1,2,3 over a cubic Fourier mode cutoff; strictly increasing as expected",
    })

    static = [
        ("Vol3-Assumption1.1", "Bounded-energy breakdown regime (hypothesis)", "Open", "Explicitly conditional hypothesis, not a proved claim; consistent with Vol.1's refusal to assert NS singularities actually occur."),
        ("Vol3-Lemma2.1", "Fixed-mode nonlinear bound |N_k(t)|<=|k|E^2", "Dr", "Standard Cauchy-Schwarz/Parseval estimate for an ARBITRARY hypothetical smooth solution u, not a fixed concrete instance; algebra is elementary but not finitely enumerable."),
        ("Vol3-Thm2.2", "Finite limit of every fixed Fourier mode", "Dr", "Bounded-total-variation / Cauchy-sequence argument in a Banach space; classical real analysis, not mechanically checkable."),
        ("Vol3-Thm3.1", "Finite-mode continuation for fixed cutoff M", "Dr", "Applies Thm 2.2 to finitely many k; inherits Thm 2.2's non-finite-witness status."),
        ("Vol3-Cor3.2", "NS finite-mode separation (Sigma_s does not imply Sigma_M)", "Dr", "Logical/analytic corollary of Thm 3.1; same status."),
        ("Vol3-Thm4.1", "Tail localization (finite part bounded, tail unbounded)", "Dr", "Sobolev-norm decomposition + proof-by-contradiction; classical functional analysis, not a finite witness."),
        ("Vol3-Prop5.1-full", "Finite residual bound ||eta_M(t)|| <= C_M E^2 (full claim, beyond C_M itself)", "Dr", "The C_M arithmetic itself is checked above; the bound applying to an arbitrary hypothetical u depends on the non-finite-witness Lemma 2.1."),
        ("Vol3-Thm6.1", "Finite retained-state continuation (complex case)", "Dr", "Same variation-of-constants argument as Vol.2 Thm 6.1, generalized to C^m; no worked numeric example given in Vol.3 analogous to Vol.2 Sec.13."),
        ("Vol3-Cor6.2", "Fourier retained state as an exact instance of the general model", "Dr", "Bookkeeping identification, not a new numeric claim; inherits Prop 5.1 and Thm 6.1 status."),
        ("Vol3-Thm7.1", "Continuous finite readers survive the limit", "Dr", "Continuity of Phi applied to the non-finite-witness Fourier-mode convergence theorem."),
        ("Vol3-Thm8.1", "Three-level separation (Sigma_s, Sigma_M, Sigma_Phi,M)", "Dr", "Pure logical combination of three prior analytic (non-finite-witness) results."),
        ("Vol3-Sec10", "Conclusion (summary restatement)", "Dr", "Summary; inherits the checkability status of the results it restates."),
        ("Vol3-vs-Vol2-overlap", "Volume 2 vs. GLS-2026-006 public content", "N/A", "Extraction confirmed Volume 2's body text (pp.16-23) is byte-identical (modulo a pdftotext trailing-newline artifact) to the already-public State_Breakdown_Math_Only_v0_2.pdf; not a Volume 3 claim, recorded here for ledger completeness per the extraction agent's finding."),
    ]
    for cid, name, tier, reason in static:
        results.append({"id": cid, "name": name, "tier": tier, "status": tier.upper() if tier != "Dr" else "N/A", "evidence": reason})

    all_run = [r for r in results if r["status"] in ("PASS", "FAIL")]
    ok = all(r["status"] == "PASS" for r in all_run)

    print("RESULT_JSON:" + json.dumps({"volume": 3, "claims": results}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
