# NS P2 — audit of the candidate Uniform Full-Convolution Scale-Loss statement

**Date:** 2026-09-12  
**Candidate (author's proposal):** `NS-P2-UNIFORM-FULLCONV-SCALE-LOSS`  
**Checker:** `reproduction/checks/check_ns_p2_uniform_scale_loss_audit.py`  
**Governing rule:** `paper/NS_P2_FINAL_CLOSURE_EQUIVALENCE.md` §8 (anti-reopening)  
**Clay Navier–Stokes regularity:** OPEN

## 1. The candidate

\[
\text{(SL)}\qquad
\exists\,\delta>0,\ C<\infty,\ 0<\rho<1\quad\forall j:\qquad
\mathcal T_j^{\rm full}\le(1-\delta)\,\nu\mathcal D_j+C\rho^j,
\]

with the claimed chain (SL) ⇒ `R_{j+1} ≤ κR_j + Bρ^j` ⇒ `R_j → 0` ⇒ finite-observation gate ⇒ regularity. Conventions (Section 71 and eq. (106.3) of the standalone; P2B): shell energy `E_j = ‖|D|χ_j u‖₂²`, `D_j = ‖∇|D|χ_j u‖₂²`, exact balance `½Ė_j + νD_j = T_j`, coercivity `D_j ≥ a²N_j²E_j`, `R_j = (K_{N_j}²)^r/Λ_j`, `r = 2p/(p−2)`. `T_j` and `νD_j` are rates of H¹ shell energy; the remainder is a rate (pointwise) or an energy (windowed).

Three readings: **(SL-pt)** pointwise in time; **(SL-win\*)** on every sub-interval of every window; **(SL-win)** on fixed-length windows only.

## 2. The "⇐" arrow is an identity — the whole content is one shell ratio

`K_N` uses the cumulative projector, so `‖P_{N_{j+1}}u‖²_{H¹} = ‖P_{N_j}u‖²_{H¹} + E_{j+1}` and `K_{N_{j+1}}² ≤ K_{N_j}² + S_{j+1}` with `S_{j+1} := sup_t(∫_t^{t+τ₀}E_{j+1}^p)^{1/p}`. Convexity of `x ↦ x^r` gives, for every `η > 0`,

\[
\boxed{
R_{j+1}\le\kappa R_j+C_\eta R^{\rm sh}_{j+1},\qquad
\kappa=\frac{(1+\eta)^{r-1}}{4},\qquad
C_\eta=(1+1/\eta)^{r-1},\qquad
R^{\rm sh}_{j+1}:=\frac{S_{j+1}^{\,r}}{\Lambda_{j+1}},
}
\]

with `κ < 1` iff `η < 4^{1/(r−1)} − 1` (p = 4: `η < 4^{1/3} − 1`). Also `R_{j+1} ≥ R_j/4` always. So a scale recurrence is equivalent to **the shell-(j+1) own critical ratio being geometrically small** — not to an inflow bound from shell j.

Under (SL-pt) or (SL-win\*), Gronwall on the shell balance gives
`E_j(t+τ) ≤ e^{−2δνa²N_j²τ}E_j(t) + Cρ^j/(δνa²N_j²)`, hence `R^{sh}_j ≤ B'ρ'^j` for an H³ datum and the chain closes. Under (SL-win) alone there is no intra-window `sup` control, so the L^p window norm `K` is not controlled: the arrow fails.

### Status

`NS-P2-SCALE-LOSS-RECURRENCE-IDENTITY` — **DERIVED** (exact convexity fixture PASS).  
`(SL-pt) ⇒ R_j → 0` — **DERIVED**; `(SL-win) ⇒ R_j → 0` — **OPEN / insufficient**.

## 3. Pointwise (SL) with universal constants — REFUTED

At the repository's exact isolated-triad state (`check_ns_p2_triad_phase_stress.py`, `x=y=z=1`, `r=+1`, `ν=1/200`), the high mode `c` (shell 1) has transfer `T = 2c_c r = 1` and dissipation `D = 2νs_c z = 1/20`:

\[
\boxed{T/D = 20,\qquad T-(1-\delta)D\ \ge\ 19/20\ \ \forall\delta\in(0,1]},
\]

at a state of a globally regular fixed-`N` Galerkin solution; the instantaneous rates at the datum coincide with those of the NSE solution started there, so this pointwise refutation transfers to NSE. Two supporting scaling arguments are **analytic (`Dr`), not executed checks**: the homothetic law (vorticity coefficients `n`-independent, `s_k → n²s_k`) on the coherent state `x=y=z=E`, `r=E^{3/2}` gives `T/D = 20√E/n²`, and tuning `√E = n²/10` makes `T = 2D` with excess growing like `n⁶` (the checker verifies only the algebra given the law); and regular 2.5-D flows with amplitude `A` fill shell 1 at rate `∼A⁴W₀t`, unbounded in `A` (unchecked analytic scaling).

### Status

`NS-P2-SCALE-LOSS-POINTWISE-UNIVERSAL` — **REFUTED** (exact witness PASS at the datum; scaling arguments `Dr`).

## 4. Windowed (SL) at the same state — 3-mode Galerkin truncation only

The computations in this section are on the **closed 3-mode triad ODE**, a fixed-`N` Galerkin truncation; it is not an NSE solution (its full convolution forces six outside modes). They transfer to NSE only for windows short enough that continuity from `ż(0) = 19/20 > 0` applies; the specific numbers below do **not** transfer. Exact identity on the truncation: `∫_I T − ∫_I D = z(t₁) − z(t₀)`. A validated exact-interval Taylor integration (order 24, step 1/50, outward rounding to `2^{−160}`; **scratch computation, not reproduced in-repo**) gives `z > 1` on `(0, 91/50]` with first return `t* ∈ (1.82, 1.84)`, so on the truncation (SL-win) fails for every window `|I| ≤ 91/50` and holds for the long viscous window `|I| = 1/(νn²) = 200` (`z(200) ≤ 3e^{−2} < 1`, any `δ ≤ 2/75`). Lengthening the window only moves the witness to a growth phase.

### Status

`NS-P2-SCALE-LOSS-WINDOW-SHORT` — **REFUTED on the 3-mode truncation** (short windows, by continuity from the exact datum rate); NSE windowed form beyond that — **OPEN**.

## 5. Abstract critical budget

In the P2C-3 budget (`N_j = 2^j`, `e_j = N_j^{−1}`, `A_j = N_j`, `δ_j = N_j^{−2}`) an episode that builds shell `j` from zero has `∫T_j = e_j + ∫D_j`, `∫D_j = 2νA_jδ_j`, so

\[
\boxed{\frac{\int T_j}{\int D_j} = 1+\frac{1}{2\nu}\quad\text{for every }j}
\]

(= 101 at `ν = 1/200`): `O(1)`, `j`-independent, strictly above 1, with summable budgets. Within this budget the ratio is arithmetic on the definition `∫T_j = e_j + ∫D_j`; it shows that energy/dissipation accounting **in the P2C-3 critical budget** cannot produce `δ > 0`, consistent with the P2B `R_j ≡ 1` no-go.

### Status

`NS-P2-SCALE-LOSS-BUDGET-RATIO` — **DERIVED** (exact PASS).

## 6. Solution-dependent constants — regularity-equivalent

If `C` may depend on the solution, (SL-pt) holds for every H³-regular solution with **any** `δ ∈ (0,1]`: `|T_j| ≤ C M₃³ 8^{−j}` with `M₃ = sup_t‖u‖_{H³}`. Conversely (SL-pt) ⇒ uniform H¹ bound on `[0,T]` (sum the Gronwall bounds over `j`) ⇒ regularity by the classical H¹ continuation criterion (standard analytic result, relayed, `Dr`) — the `R_j` machinery is not even needed. Hence

\[
\boxed{\text{(SL-pt) with solution-dependent constants}\iff\text{regularity on }[0,T]},
\]

the same situation as `NS-P2-FINAL-EQUIV`. By §8 of that note this is recorded as **REGULARITY-EQUIVALENT / HOLD**, not as an open bridge.

Corrected minimal statement that still feeds the derived recurrence: `∫_t^s T_{j+1} ≤ (1−δ)ν∫_t^s D_{j+1} + c_{j+1}(u)(s−t)` on every sub-interval, with the remainder rate allowed to grow polynomially, `c_j(u) ≤ δνa²N_j²(BΛ_jρ^j)^{1/r}` (p = 4: `∝ N_j^{2.5}ρ^{j/4}`). `Σ_j ε_j < ∞` is the wrong summability (too strong; a uniform H¹ bound outright). This corrected form is still regularity-equivalent; its only non-equivalent residue is the **constructive generator** of `c_j(u)` or `R^{sh}_j ≤ Bρ^j` from finite tape/transfer records without an `M₃` oracle — which is `NS-P2B-SCALE-CONTRACTION-UNIFORM`, already OPEN.

Normalising by amplitude removes every counterexample above (`T/(D√E) = 20·4^{−j}`, geometric) — that is exactly the passage to the dimensionless shell ratio, i.e. back to the OPEN statement.

### Status

`NS-P2-UNIFORM-FULLCONV-SCALE-LOSS` — **REGULARITY-EQUIVALENT / HOLD** (solution-dependent constants); **REFUTED** (universal constants).

## 7. Boundary

```text
recurrence identity R_{j+1} <= kappa R_j + C_eta R^sh_{j+1}          DERIVED / PASS
(SL-pt) => R_j -> 0                                                  DERIVED
(SL-win) fixed windows => R_j -> 0                                   OPEN / insufficient
(SL-pt), universal constants                                         REFUTED (exact T/D = 20 witness; n^6 / 2.5-D scalings analytic Dr)
(SL-win) short windows, 3-mode Galerkin truncation                   REFUTED on the truncation (scratch integration, not in-repo)
(SL-win) long viscous window on the truncation                       holds there; NSE windowed form OPEN
critical-budget ratio 1 + 1/(2 nu) (P2C-3 budget)                    DERIVED
(SL) with solution-dependent constants                               REGULARITY-EQUIVALENT / HOLD
constructive generator of shell ratios (NS-P2B-SCALE-CONTRACTION-UNIFORM)  OPEN
Clay Navier-Stokes regularity                                        OPEN
```
