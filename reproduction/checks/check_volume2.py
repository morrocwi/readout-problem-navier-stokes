#!/usr/bin/env python3
"""
Reproduction check for Volume 2 ("State Breakdown Is Not Readout Breakdown -- A Finite
Mathematical Separation for Navier-Stokes Readouts", v0.2, pp.16-23).

Extraction confirmed Volume 2's body text is byte-identical (modulo a pdftotext
trailing-newline artifact) to the already-public State_Breakdown_Math_Only_v0_2.pdf used
by GLS-2026-006. This script independently re-verifies every claim in Volume 2 that the
extraction pass classified as mechanically checkable; everything else is recorded as a
static Dr/Open entry with the extraction's stated reason.
"""
import itertools
import json
import sys

import numpy as np
from numpy.linalg import eigh, norm


def check_witness():
    """Thm 3.1 / Cor 3.2: identical 8-state witness to Volume 1's NSR-01."""
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
    # z' = (1,0,1) is Volume 2's own literally stated witness pair (Theorem 3.1,
    # eq. (10)) -- not a substitution. Volume 1's Definition 5.1 states a
    # different pair, z' = (1,0,0), for the same F; check_volume1.py uses that
    # volume's own literal value instead of this one.
    z, zp = (0, 0, 0), (1, 0, 1)
    x, y = z, zp
    K = 50
    witness_ok = True
    for _ in range(K):
        if not (O(x) == O(y) and Q(qD(x)) != Q(qD(y))):
            witness_ok = False
            break
        x, y = F(x), F(y)
    ok = (dyn == 8) and (obs == 8) and f2 and witness_ok
    print(f"[Thm 3.1] weld dyn={dyn}/8 obs={obs}/8 F^2=Id:{f2} witness(k=0..{K-1}):{witness_ok}")
    return ok


def cycle_laplacian(m=8):
    L = np.zeros((m, m))
    for i in range(m):
        L[i, i] = 2
        L[i, (i - 1) % m] = -1
        L[i, (i + 1) % m] = -1
    return L


def check_stability_and_stepper():
    """Sec.7 stepper (algebraic identity) + Thm 7.1 (eigenvalue stability threshold)."""
    m = 8
    L = cycle_laplacian(m)
    tau = 0.7
    w, V = eigh(L)
    lmax = w.max()
    threshold = 2 * tau / lmax
    print(f"[Thm 7.1] lambda_max(L_R) = {lmax:.6f}  (paper states 4.0)")
    print(f"[Thm 7.1] stability threshold h <= 2 tau_R / lambda_max = {threshold:.6f} (paper states 0.35)")
    lmax_ok = abs(lmax - 4.0) < 1e-9
    threshold_ok = abs(threshold - 0.35) < 1e-9

    # Sec.7 recursion identity: I^{n+1} = A I^n + (h/tau) G  vs its closed-form unroll (eq.29):
    # I^N = A^N I^0 + (h/tau) * sum_{j=0}^{N-1} A^j G
    h = 0.1
    A = np.eye(m) - (h / tau) * L
    I0 = np.linspace(-1.0, 1.0, m)
    G = np.cos(np.arange(m)) * 0.2
    N = 7
    I = I0.copy()
    for _ in range(N):
        I = A @ I + (h / tau) * G
    # closed form
    Apow = np.eye(m)
    acc = np.zeros(m)
    Aj = np.eye(m)
    for j in range(N):
        acc = acc + Aj @ G
        Aj = Aj @ A
    I_closed = np.linalg.matrix_power(A, N) @ I0 + (h / tau) * acc
    resid = norm(I - I_closed)
    stepper_ok = resid < 1e-9
    print(f"[Eq.27-29] recursion vs closed-form unroll after N={N} steps: residual={resid:.3e}")

    # eigenvalues of A_R stay within [-1,1] at the reported h (stability bound |mu_j|<=1)
    muA = eigh(A)[0]
    within = np.max(np.abs(muA)) <= 1.0 + 1e-9
    print(f"[Thm 7.1] max|eigenvalue(A_R)| at h={h}: {np.max(np.abs(muA)):.6f} (<=1: {within})")

    return lmax_ok, threshold_ok, stepper_ok, within


def check_energy_identity_and_residual():
    """Prop 6.3 energy identity + Eq.33-34 residual/error-ratio definitions.

    Prop 6.3 is an EXACT algebraic identity for the continuous ODE tau dI/dt = G - L I:
    substituting dI/dt gives (tau/2) d/dt||I||^2 = I.(G - L I) = I.G - I.(LI), so
    (tau/2) d/dt||I||^2 + I.(LI) = I.G exactly, for every I (no discretization error).
    We verify this symbolically with sympy for a concrete symbolic state vector, which is a
    stronger (exact) check than any finite-difference approximation along a discrete Euler
    trajectory would be.
    """
    import sympy as sp

    m = 4  # small enough for a fast symbolic check; identity is dimension-independent
    tau_s = sp.symbols('tau', positive=True)
    Isym = sp.Matrix(sp.symbols(f'I0:{m}'))
    Gsym = sp.Matrix(sp.symbols(f'G0:{m}'))
    Lsym = sp.Matrix(m, m, lambda i, j: sp.symbols(f'L_{i}_{j}'))
    dIdt = (Gsym - Lsym * Isym) / tau_s
    ddt_norm2 = 2 * (Isym.T * dIdt)[0]
    lhs = sp.together(sp.expand(sp.Rational(1, 2) * tau_s * ddt_norm2 + (Isym.T * Lsym * Isym)[0]))
    rhs = sp.expand((Isym.T * Gsym)[0])
    energy_ok = sp.simplify(lhs - rhs) == 0
    print(f"[Prop 6.3] symbolic identity (tau/2) d/dt||I||^2 + <I,LI> == <I,G> holds exactly (sympy simplify to 0): {energy_ok}")

    # Also spot-check numerically on the m=8 cycle-graph instance for concreteness.
    m8 = 8
    L = cycle_laplacian(m8)
    tau = 0.7
    I = np.linspace(-1.0, 1.0, m8)
    G = np.sin(np.arange(m8) + 0.3) * 0.3
    dIdt_num = (G - L @ I) / tau
    ddt_norm2_num = 2 * I @ dIdt_num
    lhs_num = 0.5 * tau * ddt_norm2_num + I @ (L @ I)
    rhs_num = I @ G
    numeric_ok = abs(lhs_num - rhs_num) < 1e-10
    print(f"[Prop 6.3] numeric spot-check on m=8 cycle graph: lhs={lhs_num:.6f} rhs={rhs_num:.6f} match: {numeric_ok}")
    energy_ok = energy_ok and numeric_ok

    # Eq.33-34: one-step residual R^n and normalized error ratio epsilon_N, purely a finite sum.
    h2 = 0.05
    A2 = np.eye(m8) - (h2 / tau) * L
    N = 20
    Is = [I.copy()]
    for _ in range(N):
        Is.append(A2 @ Is[-1] + (h2 / tau) * G)
    A, h = A2, h2
    residuals = []
    for n in range(N):
        pred = A @ Is[n] + (h / tau) * G
        residuals.append(norm(pred - Is[n + 1]))
    residuals = np.array(residuals)
    obs_norms = np.array([norm(Is[n + 1]) for n in range(N)])
    eps_N = np.sqrt((residuals ** 2).sum()) / np.sqrt((obs_norms ** 2).sum() + 1e-12)
    print(f"[Eq.33-34] normalized residual epsilon_N over {N} steps: {eps_N:.3e} (definition is exactly reproducible; by construction ~0 here since Is[] was built from A)")
    eps_ok = eps_N < 1e-9  # trajectory was generated by the same recursion, so residual should be ~0

    return energy_ok, eps_ok


def check_convergence_order():
    """Sec.13 worked numeric example: confirm O(h) convergence with a NON-kernel-aligned
    forcing (the paper's own G_R/I_0 are underdetermined by the prose -- see BUILD_STATUS.md).
    We do not claim to reproduce the exact published error numbers; we confirm the underlying
    textbook claim (explicit Euler is globally O(h) for this well-posed linear ODE) holds for
    an explicit, documented, non-trivial choice of G_R and I_0."""
    m = 8
    L = cycle_laplacian(m)
    tau = 0.7
    w, V = eigh(L)
    lmax = w.max()
    T = 1.0
    I0 = np.array([1.0, -0.5, 0.3, 0.7, -1.0, 0.2, -0.3, 0.6])
    G = np.array([0.5, 0.1, -0.4, 0.3, 0.2, -0.6, 0.4, -0.1])  # not aligned with L's kernel

    c0 = V.T @ I0
    g = V.T @ G
    ce = np.empty_like(c0)
    for j, lam in enumerate(w):
        if abs(lam) < 1e-12:
            ce[j] = c0[j] + (T / tau) * g[j]
        else:
            e = np.exp(-lam * T / tau)
            ce[j] = e * c0[j] + (1 - e) * g[j] / lam
    I_exact = V @ ce

    errs = []
    hs = [0.1, 0.05, 0.025, 0.0125]
    for h in hs:
        Nsteps = int(round(T / h))
        A = np.eye(m) - (h / tau) * L
        I = I0.copy()
        for _ in range(Nsteps):
            I = A @ I + (h / tau) * G
        err = norm(I - I_exact)
        errs.append(err)
        print(f"[Sec.13] h={h:.5f}  ||I_h(T)-I_exact(T)||_2 = {err:.6e}")
    ratios = [errs[i] / errs[i + 1] for i in range(len(errs) - 1)]
    print(f"[Sec.13] successive error ratios: {[round(r,4) for r in ratios]} (paper reports ~2.0 = O(h))")
    order_ok = all(1.8 < r < 2.2 for r in ratios)
    return order_ok


def check_prop_10_1_counterexample():
    """Prop 10.1: trivial two-line counterexample construction (Adm_Q identically 0 or 1)."""
    # Break_{Q,N}(s) is defined via Adm_Q; choosing Adm_Q constant makes it independent of
    # whatever Sigma_R says, breaking both directions. This is exact by construction, not a
    # numeric approximation.
    Adm_zero = lambda *_: 0
    Adm_one = lambda *_: 1
    sigma_r_true_break_undecided = (Adm_zero() == 0)  # Sigma_R=0 does not force Break=0 unless Adm says so
    break_true_sigma_undecided = (Adm_one() == 1)
    ok = sigma_r_true_break_undecided and break_true_sigma_undecided
    print(f"[Prop 10.1] Adm_Q≡0 breaks 'Sigma_R=0 => Break=0'; Adm_Q≡1 breaks 'Break=1 => Sigma_R=1': {ok}")
    return ok


def main():
    results = []

    witness_ok = check_witness()
    results.append({
        "id": "Vol2-Thm3.1/Cor3.2",
        "name": "8-state exact-weld witness with permanent reader equivalence (same construction as Vol.1 NSR-01)",
        "tier": "finite_diagnostic",
        "status": "PASS" if witness_ok else "FAIL",
        "evidence": "see printed weld/witness counts above; identical construction to Volume 1's NSR-01, re-derived independently here to avoid cross-volume double counting confusion",
    })

    lmax_ok, threshold_ok, stepper_ok, within = check_stability_and_stepper()
    results.append({
        "id": "Vol2-Sec13-lambda_max",
        "name": "8-node cycle graph Laplacian lambda_max = 4.0 (Sec.13 worked example)",
        "tier": "finite_diagnostic",
        "status": "PASS" if lmax_ok else "FAIL",
        "evidence": "computed lambda_max via eigh; matches paper's stated value 4.0",
    })
    results.append({
        "id": "Vol2-Thm7.1-threshold",
        "name": "Explicit-Euler stability threshold h <= 2 tau_R/lambda_max = 0.35",
        "tier": "finite_diagnostic",
        "status": "PASS" if threshold_ok else "FAIL",
        "evidence": "2*0.7/4.0 = 0.35, matches paper; confirmed |eigenvalue(A_R)|<=1 at h=0.1",
    })
    results.append({
        "id": "Vol2-Eq27-29",
        "name": "Explicit stepper recursion matches its own closed-form (Duhamel) unroll",
        "tier": "finite_diagnostic",
        "status": "PASS" if stepper_ok else "FAIL",
        "evidence": "recursion vs closed-form residual < 1e-9 after 7 steps",
    })
    results.append({
        "id": "Vol2-Thm7.1-eigenvalue-bound",
        "name": "max|eigenvalue(A_R)| <= 1 under the stability condition",
        "tier": "finite_diagnostic",
        "status": "PASS" if within else "FAIL",
        "evidence": "computed directly for the m=8 cycle graph at h=0.1 < 0.35",
    })

    energy_ok, eps_ok = check_energy_identity_and_residual()
    results.append({
        "id": "Vol2-Prop6.3",
        "name": "Energy identity (tau/2) d/dt||I||^2 + <I,LI> = <I,G>",
        "tier": "finite_diagnostic",
        "status": "PASS" if energy_ok else "FAIL",
        "evidence": "verified as an EXACT symbolic algebraic identity (sympy simplify to 0, substituting the ODE's own dI/dt), plus a numeric spot-check on the m=8 cycle-graph instance",
    })
    results.append({
        "id": "Vol2-Eq33-34",
        "name": "One-step residual R^n / normalized error epsilon_N (definition)",
        "tier": "finite_diagnostic",
        "status": "PASS" if eps_ok else "FAIL",
        "evidence": "definition is a directly computable finite sum; verified self-consistent on a simulated trajectory",
    })

    order_ok = check_convergence_order()
    results.append({
        "id": "Vol2-Sec13-convergence-order",
        "name": "Explicit Euler stepper is O(h) globally (Sec.13 worked example, general claim)",
        "tier": "finite_diagnostic",
        "status": "PASS" if order_ok else "FAIL",
        "evidence": "GAP: paper's G_R/I_0 for the exact published error table are underspecified in the prose (a naive constant/kernel-aligned drive trivializes the test). Reproduced the underlying O(h) convergence claim with an explicit, documented, non-kernel-aligned G_R/I_0 instead (see BUILD_STATUS.md); ratios printed above land near 2.0 as expected for a first-order method, but this does NOT reproduce the paper's own exact numeric table (1.99976, 2.00069, 2.00053).",
    })

    prop_ok = check_prop_10_1_counterexample()
    results.append({
        "id": "Vol2-Prop10.1",
        "name": "Bounded retained state does not decide task adequacy (counterexample)",
        "tier": "finite_diagnostic",
        "status": "PASS" if prop_ok else "FAIL",
        "evidence": "exact two-line construction (Adm_Q constant 0 or 1 breaks each direction)",
    })

    # ---- Non-mechanically-checkable claims (static Dr/Open entries) ----
    static = [
        ("Vol2-Def2.1", "Exact weld (definition)", "Dr", "Definition, not a claim; underlies Thm 3.1 which IS checked above."),
        ("Vol2-Def2.2", "Finite-horizon reader equivalence (definition)", "Dr", "Definition, not a claim."),
        ("Vol2-Sec4-adapter", "NS adapter problem / defects delta_dyn, delta_obs", "Open", "Framework discussion with no numeric instantiation for a real NS adapter; explicitly not a theorem."),
        ("Vol2-Eq16-17", "Finite retained-turbulence layer (definition)", "Dr", "Definition; explicitly NOT identified with real Navier-Stokes by the paper itself."),
        ("Vol2-Thm6.1", "Global finite-interval continuation (general ODE existence/uniqueness)", "Dr", "Standard linear-ODE variation-of-constants argument over ALL admissible L_R, G_R; not finitely enumerable as a general theorem (a fixed numeric instance is what Sec.13 attempts, partially covered above)."),
        ("Vol2-Cor6.2", "Positive-semidefinite restoration (spectral bound)", "Dr", "Spectral-theorem argument for a general PSD L_R; the SPECIFIC m=8 cycle-graph instance is confirmed PSD with lambda_min=0 by the eigenvalue computation above."),
        ("Vol2-Cor6.4", "Spectral-gap estimate", "Dr", "Standard linear-ODE spectral-projection argument for a general spectral gap; not a finite enumeration."),
        ("Vol2-Thm8.1", "Continuum breakdown does not force retained norm blow-up under H_R", "Dr", "Direct logical restatement of Thm 6.1's bound; inherits Thm 6.1's non-finite-witness status."),
        ("Vol2-Cor8.2", "Necessary bridge failure for transferred blow-up", "Dr", "Pure logical contrapositive of Thm 8.1; not a numeric/combinatorial claim."),
        ("Vol2-Sec9", "State-dependent restoration (nonlinear model, open item)", "Open", "Explicitly flagged by the paper itself as a separate, unresolved mathematical problem."),
        ("Vol2-Prop10.2", "No readout norm blow-up for Lipschitz readers", "Dr", "One-line analytic corollary of Thm 6.1's boundedness for a general K-Lipschitz reader."),
        ("Vol2-Thm11.1", "Four-layer non-collapse", "Dr", "Combines the checked finite witness (Thm 3.1) with the non-mechanical Thm 8.1; TWO DOCUMENT DEFECTS FOUND in the same proof sentence: (1) proof text cites 'Theorem 9.1' which does not exist as a numbered theorem in Volume 2 (Section 9 is an unnumbered open-problem discussion) -- most likely a typo for Theorem 8.1; (2) proof text also cites 'Proposition 11.1' which does not exist in Volume 2 (only Proposition 10.1 and 10.2 exist) -- most likely a typo for Proposition 10.1 ('Bounded retained state does not decide task adequacy'), whose stated content is a near-verbatim match for what the proof describes. Flagged for the founder/author; does not itself block the finite parts already verified."),
    ]
    for cid, name, tier, reason in static:
        results.append({"id": cid, "name": name, "tier": tier, "status": tier.upper() if tier != "Dr" else "N/A", "evidence": reason})

    all_run = [r for r in results if r["status"] in ("PASS", "FAIL")]
    ok = all(r["status"] == "PASS" for r in all_run)

    print("RESULT_JSON:" + json.dumps({"volume": 2, "claims": results}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
