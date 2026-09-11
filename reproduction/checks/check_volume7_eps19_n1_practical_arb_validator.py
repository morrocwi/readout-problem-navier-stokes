#!/usr/bin/env python3
"""Rigorous Arb/a-posteriori validator for a practical N=1 direct sample schedule.

This is a computer-assisted finite-dimensional certificate attempt for the square
49-sample shell-energy map at the simple nondimensional spacing h=1/14.  Unlike the
floating target-selection probes, all *validation* arithmetic is performed with Arb
balls (python-flint) and an a-posteriori residual argument.  SciPy is used only to
propose a piecewise-linear path; the path is then treated as declared decimal data and
is independently enclosed by residual inequalities.

The state and 49 slice tangents are validated step by step.  The resulting sample
Jacobian enclosure is combined with a fixed midpoint preconditioner.  A second scalar
variational propagation then attempts to certify a nonzero initial-state branch with
q<=1/2 and a positive raw-data margin.

If any bootstrap fails the checker returns OPEN, never a fabricated certificate.
The physical cadence corresponding to h is h*L/U under the usual declared advective
time scale; no values of L or U are assumed here.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from flint import arb, arb_mat, ctx

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as comp
import check_volume7_eps18_n1_small_witness as small

ctx.dps = 50

CENTER_SEED = 20260910
C = 600
NU_DEN = 200
H_NUM = 1
H_DEN = 14
MAX_NODE = 23
SUBSTEPS_PER_SAMPLE = 8
Q_TARGET = arb("1/2")


def A(q) -> arb:
    if isinstance(q, arb):
        return q
    if isinstance(q, int):
        return arb(q)
    return arb(str(q))


def up(x: arb) -> arb:
    return x.upper()


def max_arb(items) -> arb:
    out = arb(0)
    for x in items:
        xu = up(x)
        if out < xu:
            out = xu
    return out


def vec_inf(v) -> arb:
    return max_arb(x.abs_upper() for x in v)


def mat_inf(M: arb_mat) -> arb:
    vals = []
    for i in range(M.nrows()):
        s = arb(0)
        for j in range(M.ncols()):
            s += M[i, j].abs_upper()
        vals.append(s)
    return max_arb(vals)


def mat_row_sums(M: arb_mat):
    out = []
    for i in range(M.nrows()):
        s = arb(0)
        for j in range(M.ncols()):
            s += M[i, j].abs_upper()
        out.append(up(s))
    return out


def to_arb_vec(values):
    return [arb(repr(float(x))) for x in values]


def to_arb_mat(values):
    return arb_mat([[arb(repr(float(x))) for x in row] for row in values])


def sparse_tensor(cube):
    Td = comp.scaled_bilinear_tensor(cube)
    nz = np.argwhere(Td != 0)
    return [(int(m), int(j), int(k), int(Td[m, j, k])) for m, j, k in nz]


def linear_diag(cube):
    out = []
    for k in cube.reps:
        val = -sum(int(v) * int(v) for v in k)
        out.extend([arb(f"{val}/{NU_DEN}")] * 4)
    return out


def bvec(terms, x, y, d):
    out = [arb(0) for _ in range(d)]
    cden = arb(C)
    for m, j, k, c in terms:
        out[m] += arb(c) * x[j] * y[k] / cden
    return out


def fvec(terms, L, x):
    B = bvec(terms, x, x, len(x))
    return [L[i] * x[i] + B[i] for i in range(len(x))]


def dfmat(terms, L, x, *, include_linear=True):
    d = len(x)
    rows = [[arb(0) for _ in range(d)] for _ in range(d)]
    if include_linear:
        for i in range(d):
            rows[i][i] += L[i]
    cden = arb(C)
    for m, j, k, c in terms:
        cc = arb(c) / cden
        rows[m][j] += cc * x[k]
        rows[m][k] += cc * x[j]
    return arb_mat(rows)


def mat_scale(M: arb_mat, s):
    return M * A(s)


def mat_add(X: arb_mat, Y: arb_mat):
    return X + Y


def mat_sub(X: arb_mat, Y: arb_mat):
    return X - Y


def neg(M: arb_mat):
    return M * arb(-1)


def identity(n):
    return arb_mat([[1 if i == j else 0 for j in range(n)] for i in range(n)])


def float_operators(cube, Td):
    T = np.asarray(Td, dtype=np.float64) / float(C)
    L = np.repeat(
        np.asarray([-sum(float(v) * float(v) for v in k) / NU_DEN for k in cube.reps]),
        4,
    )
    W = np.asarray(cube.weights, dtype=np.float64)
    return T, L, W


def rhs_factory(T, L, d, nf):
    def rhs(_t, y):
        x = y[:d]
        G = y[d:].reshape(d, nf)
        dx = L * x + np.einsum("mjk,j,k->m", T, x, x, optimize=True)
        dG = (
            L[:, None] * G
            + np.einsum("mjk,ja,k->ma", T, G, x, optimize=True)
            + np.einsum("mjk,j,ka->ma", T, x, G, optimize=True)
        )
        return np.concatenate([dx, dG.reshape(-1)])
    return rhs


def choose_state_sup(e0, dt, R, K0, D2):
    denom0 = arb(1) - dt * K0
    if not (arb(0) < denom0):
        return None
    base = up((e0 + dt * R) / denom0)
    cap = up(base * 2 + arb("1e-40"))
    for _ in range(20):
        K = up(K0 + D2 * cap)
        rhs = up(e0 + dt * (R + K * cap))
        if rhs <= cap and dt * K < 1:
            return cap, rhs, K
        cap = up(cap * 2)
    return None


def choose_branch_state_sup(p0, dt, Kc, Binf):
    denom0 = arb(1) - dt * Kc
    if not (arb(0) < denom0):
        return None
    cap = up(p0 / denom0 * 2 + arb("1e-50"))
    for _ in range(20):
        rhs = up(p0 + dt * (Kc * cap + Binf * cap * cap))
        if rhs <= cap:
            return cap, rhs
        cap = up(cap * 2)
    return None


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared N=1 center did not reproduce")
    xinit = small.small_state(CENTER_SEED, cube.d).astype(float)
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    nf = len(free)
    d = cube.d
    if d != 52 or nf != 49:
        raise RuntimeError("unexpected N=1 dimensions")

    Td = comp.scaled_bilinear_tensor(cube)
    terms = sparse_tensor(cube)
    Larb = linear_diag(cube)
    Tfloat, Lfloat, Wfloat = float_operators(cube, Td)
    Warb = [[arb(int(v)) for v in row] for row in np.asarray(cube.weights, dtype=int)]

    row_abs = [0 for _ in range(d)]
    for m, _j, _k, c in terms:
        row_abs[m] += abs(c)
    Binf = arb(max(row_abs)) / C
    D2 = 2 * Binf

    nsteps = MAX_NODE * SUBSTEPS_PER_SAMPLE
    dt_num = H_NUM
    dt_den = H_DEN * SUBSTEPS_PER_SAMPLE
    dt = arb(f"{dt_num}/{dt_den}")
    total_t = MAX_NODE / H_DEN
    grid = np.linspace(0.0, float(total_t), nsteps + 1)

    Ginit = np.zeros((d, nf), dtype=float)
    for a, j in enumerate(free):
        Ginit[j, a] = 1.0
    y0 = np.concatenate([xinit, Ginit.reshape(-1)])
    sol = solve_ivp(
        rhs_factory(Tfloat, Lfloat, d, nf),
        (0.0, float(total_t)),
        y0,
        method="DOP853",
        t_eval=grid,
        rtol=2e-12,
        atol=2e-14,
        max_step=float(dt) / 2 if False else 0.002,
    )
    if not sol.success or sol.y.shape[1] != nsteps + 1:
        raise RuntimeError("floating proposal path integration failed")
    Xf = sol.y[:d, :].T.copy()
    Gf = sol.y[d:, :].T.reshape(nsteps + 1, d, nf).copy()
    Xf[0, :] = xinit
    Gf[0, :, :] = Ginit

    ex = arb(0)
    eg = arb(0)
    sample_records = {0: (up(ex), up(eg))}
    step_Kc = []
    step_Gc = []
    validation_ok = True

    for step in range(nsteps):
        x0 = to_arb_vec(Xf[step])
        x1 = to_arb_vec(Xf[step + 1])
        xm = [(x0[i] + x1[i]) / 2 for i in range(d)]
        xp = [(x1[i] - x0[i]) / dt for i in range(d)]
        G0 = to_arb_mat(Gf[step])
        G1 = to_arb_mat(Gf[step + 1])
        Gm = (G0 + G1) / 2
        Gp = (G1 - G0) / dt

        D0 = dfmat(terms, Larb, x0)
        D1 = dfmat(terms, Larb, x1)
        Dm = dfmat(terms, Larb, xm)
        Dp = dfmat(terms, Larb, xp, include_linear=False)
        K0 = max_arb([mat_inf(D0), mat_inf(D1)])

        fm = fvec(terms, Larb, xm)
        rmid = [xp[i] - fm[i] for i in range(d)]
        rprime_vec = neg(Dm * arb_mat([[v] for v in xp]))
        Bpp = bvec(terms, xp, xp, d)
        rsecond = [arb(-2) * v for v in Bpp]
        Rstate = up(
            vec_inf(rmid)
            + dt / 2 * mat_inf(rprime_vec)
            + dt * dt / 8 * vec_inf(rsecond)
        )

        state_choice = choose_state_sup(ex, dt, Rstate, K0, D2)
        if state_choice is None:
            validation_ok = False
            break
        exsup, ex_next, K = state_choice

        RGmid = Gp - Dm * Gm
        RGprime = neg(Dp * Gm + Dm * Gp)
        RGsecond = neg((Dp * Gp) * 2)
        RG = up(mat_inf(RGmid) + dt / 2 * mat_inf(RGprime) + dt * dt / 8 * mat_inf(RGsecond))
        Gapp = max_arb([mat_inf(G0), mat_inf(G1)])
        denomG = arb(1) - dt * K
        if not (arb(0) < denomG):
            validation_ok = False
            break
        egsup = up((eg + dt * (RG + D2 * exsup * Gapp)) / denomG)
        eg_next = egsup

        ex, eg = ex_next, eg_next
        step_Kc.append(up(K))
        step_Gc.append(up(Gapp + egsup))
        if (step + 1) % SUBSTEPS_PER_SAMPLE == 0:
            sample_records[(step + 1) // SUBSTEPS_PER_SAMPLE] = (up(ex), up(eg))

    if not validation_ok or len(sample_records) != MAX_NODE + 1:
        claims = [{
            "id": "V7-EPSC19-N1-PRACTICAL-ARB-CENTER-VALIDATION",
            "name": "Arb a-posteriori validation of the h=1/14 center flow and tangent",
            "tier": "Open",
            "status": "OPEN",
            "evidence": f"center residual bootstrap failed at step={len(step_Kc)} of {nsteps}; increase piecewise resolution or improve the residual path",
        }]
        print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
        return 0

    # Build declared approximate sample map/Jacobian and validation row-l1 radii.
    Jrows = []
    Jerr = []
    ycenter = []
    yscale = []
    obs_meta = []
    for shell in (0, 1):
        for node in range(24):
            idx = node * SUBSTEPS_PER_SAMPLE
            xv = to_arb_vec(Xf[idx])
            Gv = to_arb_mat(Gf[idx])
            exn, egn = sample_records[node]
            grow = mat_row_sums(Gv)
            row = []
            for a in range(nf):
                s = arb(0)
                for m in range(d):
                    w = Warb[shell][m]
                    if w:
                        s += 2 * w * xv[m] * Gv[m, a]
                row.append(s)
            Jrows.append(row)
            err = arb(0)
            for m in range(d):
                w = Warb[shell][m]
                if w:
                    err += 2 * w * (exn * grow[m] + (xv[m].abs_upper() + exn) * egn)
            Jerr.append(up(err))
            yy = arb(0)
            for m in range(d):
                if Warb[shell][m]:
                    yy += Warb[shell][m] * xv[m] * xv[m]
            ycenter.append(yy)
            sc = max(1.0, abs(float(str(yy.mid()))))
            yscale.append(arb(repr(sc)))
            obs_meta.append((shell, node))
    # third shell at time zero
    xv = to_arb_vec(Xf[0])
    Gv = to_arb_mat(Gf[0])
    row = []
    for a in range(nf):
        s = arb(0)
        for m in range(d):
            w = Warb[2][m]
            if w:
                s += 2 * w * xv[m] * Gv[m, a]
        row.append(s)
    Jrows.append(row)
    Jerr.append(arb(0))
    yy = arb(0)
    for m in range(d):
        if Warb[2][m]:
            yy += Warb[2][m] * xv[m] * xv[m]
    ycenter.append(yy)
    yscale.append(arb(repr(max(1.0, abs(float(str(yy.mid())))))))
    obs_meta.append((2, 0))

    # Fixed rowwise calibration creates a dimensionless relative-like chart.
    Jscaled = arb_mat([[Jrows[j][a] / yscale[j] for a in range(nf)] for j in range(49)])
    Escaled = [up(Jerr[j] / yscale[j]) for j in range(49)]
    Apre = Jscaled.mid().inv().mid()
    q0 = up(mat_inf(identity(nf) - Apre * Jscaled))
    qval_rows = []
    for i in range(nf):
        s = arb(0)
        for j in range(49):
            s += Apre[i, j].abs_upper() * Escaled[j]
        qval_rows.append(s)
    qval = max_arb(qval_rows)
    qcenter = up(q0 + qval)
    Ainf = mat_inf(Apre)

    # Propagate a state/tangent difference from the center for candidate branch radii.
    def branch_q(r_text):
        p = arb(r_text)
        qg = arb(0)
        Psample = {0: up(p)}
        Qsample = {0: arb(0)}
        ok = True
        for step in range(nsteps):
            ps = choose_branch_state_sup(p, dt, step_Kc[step], Binf)
            if ps is None:
                ok = False
                break
            psup, pnext = ps
            Kb = up(step_Kc[step] + D2 * psup)
            den = arb(1) - dt * Kb
            if not (arb(0) < den):
                ok = False
                break
            qsup = up((qg + dt * D2 * psup * step_Gc[step]) / den)
            p, qg = pnext, qsup
            if (step + 1) % SUBSTEPS_PER_SAMPLE == 0:
                node = (step + 1) // SUBSTEPS_PER_SAMPLE
                Psample[node] = up(p)
                Qsample[node] = up(qg)
        if not ok:
            return None

        rowvar = []
        for shell in (0, 1):
            for node in range(24):
                idx = node * SUBSTEPS_PER_SAMPLE
                xv = to_arb_vec(Xf[idx])
                Gv = to_arb_mat(Gf[idx])
                exn, egn = sample_records[node]
                pp, qq = Psample[node], Qsample[node]
                grows = mat_row_sums(Gv)
                err = arb(0)
                for m in range(d):
                    w = Warb[shell][m]
                    if w:
                        xcb = xv[m].abs_upper() + exn
                        gcb = grows[m] + egn
                        err += 2 * w * (pp * (gcb + qq) + xcb * qq)
                rowvar.append(up(err / yscale[len(rowvar)]))
        rowvar.append(arb(0))
        qrows = []
        for i in range(nf):
            s = arb(0)
            for j in range(49):
                s += Apre[i, j].abs_upper() * rowvar[j]
            qrows.append(s)
        qb = max_arb(qrows)
        return up(qcenter + qb), Psample, Qsample

    branch_candidates = [
        "1e-2", "3e-3", "1e-3", "3e-4", "1e-4", "3e-5", "1e-5",
        "3e-6", "1e-6", "3e-7", "1e-7", "3e-8", "1e-8", "1e-9", "1e-10",
    ]
    chosen = None
    qchosen = None
    for rtxt in branch_candidates:
        bq = branch_q(rtxt)
        if bq is not None and bq[0] <= Q_TARGET:
            chosen = arb(rtxt)
            qchosen = bq[0]
            break

    direct_ok = chosen is not None and qcenter < Q_TARGET
    if direct_ok:
        factor = up(Ainf / (1 - qchosen))
        sensor_margin = up((1 - qchosen) * chosen / Ainf)
    else:
        factor = None
        sensor_margin = None

    claims = [
        {
            "id": "V7-EPSC19-N1-PRACTICAL-ARB-CENTER-VALIDATION",
            "name": "Arb a-posteriori validation of the h=1/14 center flow and tangent",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": f"validated {nsteps} piecewise-linear residual steps over T=23/14; final state error <= {ex.str(8)}, final tangent error <= {eg.str(8)}",
        },
        {
            "id": "V7-EPSC19-N1-PRACTICAL-SQUARE-Q",
            "name": "practical-turnover-scale square sample map has a certified local q<1 branch",
            "tier": "Dr" if direct_ok else "Open",
            "status": "DERIVED" if direct_ok else "OPEN",
            "evidence": (
                f"h=1/14; q_center<={qcenter.str(8)}; branch r={chosen.str(8)}; q<={qchosen.str(8)}; Ainf<={Ainf.str(8)}; scaled raw-data margin>0 up to {sensor_margin.str(8)}"
                if direct_ok else f"h=1/14 center q<={qcenter.str(8)} but no tested branch reached q<=1/2"
            ),
        },
    ]
    summary = {
        "cutoff": 1,
        "h_nondimensional": "1/14",
        "window_nondimensional": "23/14",
        "substeps_per_sample": SUBSTEPS_PER_SAMPLE,
        "validated_steps": nsteps,
        "q_center_upper": qcenter.str(16),
        "preconditioner_inf_upper": Ainf.str(16),
        "branch_radius": chosen.str(16) if chosen is not None else None,
        "q_branch_upper": qchosen.str(16) if qchosen is not None else None,
        "scaled_sensor_data_margin": sensor_margin.str(16) if sensor_margin is not None else None,
        "inverse_factor_upper": factor.str(16) if factor is not None else None,
        "physical_time_rule": "Delta t_phys=(1/14)L/U; total window=(23/14)L/U",
        "sensor_rule": "chart rows use fixed center-energy calibration scales; a physical sensor/model budget must be converted to this scaled infinity norm before applying the margin",
        "claim_boundary": "fixed N=1 local finite Galerkin certificate only; no N=1 physical adequacy, continuum tail, arbitrary N, DNS accuracy, or Clay claim",
    }
    print("EPSC-19 N=1 practical Arb validator")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
