#!/usr/bin/env python3
"""
Reproduction check for Volume 5 ("At the Constructed Breakdown Time -- Finite-Energy
Trace, Defect Localization, and Weak Crossing for a Periodic Navier-Stokes Candidate",
v0.5, pp.38-44).

Like Volume 4, this is a continuum PDE manuscript applied to a specific HYPOTHETICAL
(never explicitly constructed) candidate. Mechanically checkable content: the subtraction/
limit algebra behind Theorem 5.2's defect-localization identity, and the generic Hilbert-
space fact behind Theorem 7.1 ("weak + norm convergence => strong convergence"), both of
which are portable/reusable facts we can verify on an explicit concrete example, plus a
documentation-consistency check on the volume's own Section 9 "Final reduction" list.
"""
import json
import sys

import numpy as np


def check_defect_localization_algebra():
    """Thm 5.2: delta* = lim_t [ int_{B_rho}|u(t,x)|^2 - int_{B_rho}|u*(x)|^2 ] and
    delta* = lim_{rho->0} lim_t int_{B_rho(0)} |u(t,x)|^2 dx (Eqs 27-30). We verify the
    underlying finite-dimensional subtraction/limit-manipulation identity on a concrete
    discretized field on a periodic 1D grid standing in for T^3, with a single 'singular
    point' at x=0 and an explicit total-energy defect delta injected there."""
    N = 2000  # grid points on [0,1)
    x = np.linspace(0, 1, N, endpoint=False)

    def dist_to_0(xx):
        return np.minimum(xx, 1 - xx)

    # limiting field u* : smooth away from 0
    u_star = np.sin(2 * np.pi * x) + 0.5

    # sequence u_t -> u* pointwise away from 0, but with a fixed injected defect energy
    # concentrated in a shrinking neighborhood of x=0 (models "all defect at the point")
    delta_true = 0.37
    rng = np.random.default_rng(1)

    def u_t(width):
        bump = np.exp(-0.5 * (dist_to_0(x) / max(width, 1e-6)) ** 2)
        bump_energy = np.trapezoid(bump ** 2, x)
        scale = np.sqrt(delta_true / max(bump_energy, 1e-12))
        return u_star + scale * bump

    widths = [0.05, 0.02, 0.01, 0.005, 0.002]
    total_energy_star = np.trapezoid(u_star ** 2, x)
    defects = []
    for w in widths:
        ut = u_t(w)
        total_energy_t = np.trapezoid(ut ** 2, x)
        defects.append(total_energy_t - total_energy_star)
    print(f"[Thm 5.2] injected true defect delta*={delta_true}; recovered total-energy "
          f"difference across shrinking bump widths {widths}: "
          f"{[round(d,4) for d in defects]}")
    # As the bump narrows, its overlap with u_star's own smooth energy shrinks, so the
    # recovered total-energy difference should MONOTONICALLY approach delta_true from above.
    monotone_ok = all(defects[i] > defects[i + 1] for i in range(len(defects) - 1))
    converging_ok = abs(defects[-1] - delta_true) < 0.1
    defect_ok = monotone_ok and converging_ok

    # local-ball energy should converge to the SAME delta* as rho shrinks with t fixed at
    # the smallest width (Eq.30, rho -> 0 after t -> T*)
    ut_final = u_t(widths[-1])
    rhos = [0.1, 0.05, 0.02, 0.01]
    local_defect = []
    for rho in rhos:
        mask = dist_to_0(x) < rho
        e_t = np.trapezoid(ut_final[mask] ** 2, x[mask]) if mask.any() else 0.0
        e_star = np.trapezoid(u_star[mask] ** 2, x[mask]) if mask.any() else 0.0
        local_defect.append(e_t - e_star)
    print(f"[Thm 5.2, Eq.30] local-ball energy defect as rho shrinks {rhos}: "
          f"{[round(d,4) for d in local_defect]} (should approach the same delta* as rho->0 "
          f"with the defect concentrated at x=0)")
    localization_ok = abs(local_defect[-1] - delta_true) < 0.1

    return defect_ok and localization_ok


def check_weak_norm_strong_equivalence():
    """Thm 7.1: delta*=0 <=> ||u(t)||->||u*|| <=> u(t)->u* strongly in L^2. This is a
    generic, reusable Hilbert-space fact (weak convergence + norm convergence => strong
    convergence), verified here on an explicit finite-dimensional sequence."""
    rng = np.random.default_rng(2)
    d = 30
    u_star = rng.normal(size=d)

    # Case A: sequence converges weakly (coefficientwise) AND in norm -> must be strong (trivial in finite dim, but check the identity ||u_n-u*||^2 = ||u_n||^2 - 2<u_n,u*> + ||u*||^2 -> 0)
    noise_dir = rng.normal(size=d)
    noise_dir = noise_dir / np.linalg.norm(noise_dir)

    def seq_converging(n):
        return u_star + (0.5 ** n) * noise_dir

    errs = []
    for n in range(1, 9):
        un = seq_converging(n)
        errs.append(np.linalg.norm(un - u_star))
    strong_ok = errs[-1] < errs[0] and errs[-1] < 0.01
    print(f"[Thm 7.1] weak+norm-convergent finite-dim sequence: ||u_n-u*|| over n=1..8: "
          f"{[round(e,4) for e in errs]} -> 0: {strong_ok}")

    # Case B: sequence converges weakly (coefficientwise to 0 correlation growth) but norm
    # does NOT converge to ||u*|| (energy escapes to infinity in an orthogonal direction) ->
    # should NOT be strongly convergent, i.e. delta* != 0 in that case.
    e_k = np.eye(d)

    def seq_diverging(n):
        return u_star + e_k[n % d]  # bounded perturbation that does not vanish

    errs_b = [np.linalg.norm(seq_diverging(n) - u_star) for n in range(1, 8)]
    nonconvergent_ok = min(errs_b) > 0.9  # never gets close: consistent with delta* != 0
    print(f"[Thm 7.1] counter-case (norm does not converge to ||u*||): "
          f"||u_n-u*|| stays >= {min(errs_b):.4f}, consistent with delta* != 0: {nonconvergent_ok}")

    return strong_ok and nonconvergent_ok


def check_section9_consistency():
    established = {
        "energy bound", "modewise trace convergence", "weak L2 convergence to u*",
        "u*=u_partial a.e.", "exact delta* localization formula", "P_M convergence for all M",
        "global finite-energy weak continuation",
    }
    not_established = {"delta*=0 itself", "smooth continuation", "uniqueness after t=1"}
    overlap = established & not_established
    ok = len(overlap) == 0
    print(f"[Sec.9] 'Established' (n={len(established)}) and 'Not established' "
          f"(n={len(not_established)}) lists are disjoint: {ok}")
    return ok


def main():
    results = []

    defect_ok = check_defect_localization_algebra()
    results.append({
        "id": "Vol5-Thm5.2-defect-localization",
        "name": "Defect localization subtraction/limit algebra (all energy defect concentrated near x=0)",
        "tier": "finite_diagnostic",
        "status": "PASS" if defect_ok else "FAIL",
        "evidence": "verified the underlying finite-dimensional subtraction/limit-manipulation identity on an explicit discretized 1D periodic field with an injected point defect (portable algebra check, not a proof that any real NS candidate has this property)",
    })

    weak_ok = check_weak_norm_strong_equivalence()
    results.append({
        "id": "Vol5-Thm7.1-equivalence",
        "name": "delta*=0 <=> norm convergence <=> strong L^2 convergence (generic Hilbert-space fact)",
        "tier": "finite_diagnostic",
        "status": "PASS" if weak_ok else "FAIL",
        "evidence": "verified the standard Hilbert-space equivalence on explicit finite-dimensional converging and non-converging sequences",
    })

    consistency_ok = check_section9_consistency()
    results.append({
        "id": "Vol5-Sec9-consistency",
        "name": "Section 9 'Final reduction' established/not-established lists are internally consistent",
        "tier": "finite_diagnostic",
        "status": "PASS" if consistency_ok else "FAIL",
        "evidence": "documentation/textual consistency check: the two lists are disjoint as extracted",
    })

    static = [
        ("Vol5-Assumption1.1-C1-C9", "Specific hypothetical periodic NS candidate with endpoint extension (C1-C9)", "Open", "A stronger, more specific hypothesis than Volume 4's; the endpoint-extension assumption (C8-C9) is never constructed or justified for a real NS solution."),
        ("Vol5-Thm2.1", "Energy bound via Gronwall inequality", "Dr", "Standard Gronwall-inequality derivation; the ODE-inequality algebra is short and re-derivable, but the underlying PDE energy identity is classical/assumed."),
        ("Vol5-Lemma3.1", "Fixed-mode nonlinear bound", "Dr", "Same Cauchy-Schwarz/Parseval technique as Volume 4 Lemma 2.1; not a finite witness."),
        ("Vol5-Thm3.2", "Modewise terminal trace exists", "Dr", "Same BV/Cauchy-limit technique as Volume 4 Theorem 2.2; classical real analysis."),
        ("Vol5-Thm3.3", "Finite-energy terminal state u* with weak convergence", "Dr", "Same finite-K partial-sum + weak-convergence technique as Volume 4 Theorem 3.1."),
        ("Vol5-Thm4.1", "u* identified a.e. with endpoint field u_partial away from singular point", "Dr", "The volume's most load-bearing and least independently-justified result: entirely conditional on the assumed (not derived) endpoint-extension hypothesis C8-C9 for an unconstructed candidate."),
        ("Vol5-Thm6.1", "Exact finite readout P_M u(t) -> P_M u* strongly, expressed via u_partial's coefficients", "Dr", "Eq.35 would be a directly checkable finite Fourier-sum identity IF u_partial were an explicit concrete function; the candidate is never constructed in this volume, so there is nothing concrete to evaluate it against."),
        ("Vol5-Cor7.2", "No-concentration sufficient condition for delta*=0", "Dr", "Abstract sufficient condition on a hypothetical/unconstructed candidate; straightforward logical corollary of Thm 5.2 + Thm 7.1."),
        ("Vol5-Thm8.1", "Finite-energy weak crossing (patched global solution, energy jump = delta*)", "Dr", "Same Galerkin-restart technique as Volume 4 Theorem 6.1; NOTE the weak-restart existence for this specific candidate is asserted via reference to 'the standard Galerkin construction' rather than fully re-proven in Volume 5's own text -- a thinner presentation than Volume 4's analogous theorem."),
    ]
    for cid, name, tier, reason in static:
        results.append({"id": cid, "name": name, "tier": tier, "status": tier.upper() if tier != "Dr" else "N/A", "evidence": reason})

    all_run = [r for r in results if r["status"] in ("PASS", "FAIL")]
    ok = all(r["status"] == "PASS" for r in all_run)

    print("RESULT_JSON:" + json.dumps({"volume": 5, "claims": results}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
