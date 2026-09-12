# NS P2 — audit of the Uniform Retention Gap sketch (H³ shell readouts, Duhamel window)

**Date:** 2026-09-12  
**Candidate (author's sketch):** `NS-P2-UNIFORM-RETENTION-GAP` — the recent-window bilinear bound (RRB) below  
**Checker:** `reproduction/checks/check_ns_p2_retention_gap_audit.py`  
**Governing rule:** `paper/NS_P2_FINAL_CLOSURE_EQUIVALENCE.md` §8 (anti-reopening)  
**Predecessor audit:** `paper/NS_P2_UNIFORM_SCALE_LOSS_AUDIT.md` (H¹ shell energy budget; this note moves the same question to H³ coordinates and a Duhamel window)  
**Clay Navier–Stokes regularity:** OPEN  
**Toledo objects (proposal entries in `morrocwi/toledo`, `registry/proposals/ns_p2_critical_quotient.json`; no canonical codes yet):** `PROP-P3-H3-SHELL-READOUT-01` (Definition, `R_j^N`), `PROP-P3-DUHAMEL-WINDOW-SPLIT-01` (`Dr`, old-history factor), `PROP-P3-WINDOW-BILINEAR-CONSTANT-01` (Definition, `α_j^N`), `PROP-P3-RETENTION-GAP-RECURRENCE-01` (`Dr`, the chain), `PROP-P3-RECENT-RETENTION-BOUND-ENERGY-ONLY-REFUTED` (`Dr`, analytic; this note supplies the exact proxy instances), `PROP-P3-UNIFORM-RETENTION-GAP-01` (Open; REGULARITY-EQUIVALENT / HOLD)

## 1. The candidate

Torus, mean-zero, Galerkin index `N`. Shells `S_j = {λ_j ≤ |k| < λ_{j+1}}`, `λ_j = 2^j`. Shell readout

\[
R_j^N(T) := \sup_{t\le T}\Big(\sum_{k\in S_j}|k|^6\,|\hat u^N_k(t)|^2\Big)^{1/2}.
\]

Duhamel at scale `j+1` with window `τ_j = c/(νλ_{j+1}²)`:

\[
\lambda_{j+1}^3\|P_{j+1}u(t)\|_2\ \le\ \underbrace{\lambda_{j+1}^3\|e^{\nu\Delta\tau_j}P_{j+1}u(t-\tau_j)\|_2}_{\text{old history}\ \le\ e^{-c}R_{j+1}}\ +\ \underbrace{\lambda_{j+1}^3\Big\|\int_{t-\tau_j}^{t}e^{\nu\Delta(t-s)}P_{j+1}\mathbb P\nabla\!\cdot(u\otimes u)\,ds\Big\|_2}_{=:\ \mathcal N_{j+1}(t)} .
\]

The one open inequality:

\[
\text{(RRB)}\qquad \mathcal N_{j+1}\le\alpha R_j + C\,2^{-\sigma j}B,\qquad \alpha<1-e^{-c},\ \sigma>0,
\]

with the claimed chain (RRB) ⇒ `(1−e^{−c})R_{j+1} ≤ αR_j + C2^{−σj}B` ⇒ `R_{j+1} ≤ qR_j + C′2^{−σj}B`, `q = α/(1−e^{−c})` ⇒ `R_j ≤ C_Tθ^j`, `θ = max(q, 2^{−σ})` ⇒ `Σ_j R_j < ∞` ⇒ `sup_N sup_t ‖u_N‖_{H³} < ∞` ⇒ compactness ⇒ global smooth.

The audit separates (i) the algebra of the chain, which is checkable exactly; (ii) what `B` is allowed to depend on, which is where the content sits; (iii) the equivalence sketch, which is not checked.

## 2. The chain from (RRB) — DERIVED

Everything after (RRB) is elementary and is fixture-checked exactly:

- **Old-history factor.** For `|k| ≥ λ_{j+1}` and `τ_j = c/(νλ_{j+1}²)`, `ν|k|²τ_j = c|k|²/λ_{j+1}² ≥ c`, so `e^{−ν|k|²τ_j} ≤ e^{−c}` (exact exponent comparison, symbolic in `ν, c`, several `j` and lattice `k`); and `λ_{j+1}³‖P_{j+1}u‖₂ ≤ (Σ_{S_{j+1}}|k|⁶|û_k|²)^{1/2} = R_{j+1}` since `|k| ≥ λ_{j+1}` on the shell (exact finite example).
- **Recurrence.** With `E := e^{−c}` a symbol in `(0,1)`, dividing by `1−E` gives `R_{j+1} ≤ qR_j + C′2^{−σj}B`, `q = α/(1−E)`, `C′ = C/(1−E)`, and `q < 1 ⇔ α < 1−E` (exact rational instances both ways). The equality iteration `R_j = q^jR_0 + C′BΣ_{m<j}q^{j−1−m}2^{−σm}` is the maximal sequence; with `r = 2^{−σ}` and `θ = max(q, r)`, the convolution is exactly `(q^j − r^j)/(q − r) ≤ θ^j/|q − r|` when `q ≠ r`, hence `R_j ≤ C_Tθ^j` with `C_T = R_0 + C′B/|q − r|`. **Refinement:** when `q = 2^{−σ}` exactly the convolution is `jθ^{j−1}`, so the bound is `(R_0 + C′Bj/θ)θ^j`, not `C_Tθ^j`; summability `Σ_j R_j < ∞` holds in both cases (`θ < 1`). Checked exactly for `j ≤ 14` on four instances including the coincident one.
- **Σ_j R_j < ∞ ⇒ uniform H³.** Pointwise in `t`, `‖u‖²_{Ḣ³} = Σ_k|k|⁶|û_k|² = Σ_j R_j(t)² ≤ (Σ_j R_j(t))² ≤ (Σ_j sup_t R_j)²` — ℓ¹ over shells dominates ℓ² (cross terms `2Σ_{i<j}R_iR_j ≥ 0`, verified with the shell readouts kept as exact square roots on a finite example; the symbolic identity is also checked). The step `sup_N sup_t ‖u_N‖_{H³} < ∞ ⇒ compactness ⇒ global smooth` is the standard Galerkin-limit argument (relayed, `Dr`; not a fixture).

Two boundary remarks on the chain (observations, `Dr`, not fixtures): (1) for `t < τ_j` the old-history term is the datum `λ_{j+1}³‖e^{νΔt}P_{j+1}u₀‖₂ ≤ R_{j+1}(u₀)`, and `Σ_j R_j(u₀) < ∞` is the dyadic-ℓ¹ condition (`B³_{2,1}`), slightly stronger than `u₀ ∈ H³`, unless the datum shell readouts are folded into the `2^{−σj}B` remainder; (2) all constants must be `N`-independent for the `sup_N` — the chain as written has that property since (RRB) is assumed uniform in `N`.

### Status

`NS-P2-RETENTION-GAP-CHAIN` — **DERIVED** (exact fixtures PASS; `q ≠ 2^{−σ}` needed for the pure `C_Tθ^j` form, `jθ^{j−1}` otherwise; last two steps relayed).

## 3. Energy-only remainder — REFUTED-as-stated (at the `t = 0` rate proxy)

The content of (RRB) is what `B` depends on. Read it with `B = B(E₀, ν, T)` — a function of the energy, the viscosity and the horizon only, independent of the spectral shape of the datum. Then `Σ_j 2^{−σj}B < ∞` for free and the chain would give an `H³` bound depending only on `(E₀, ν, T, u₀)`.

**The finite object measured.** At `t = 0`, for a datum supported in shell `j₀`, replace the windowed `𝒩_{j₀+1}` by its first-order-in-window proxy

\[
\mathcal N_{j_0+1}\ \approx\ \tau_{j_0}\cdot\text{rate},\qquad \text{rate}^2 := \sum_{k\in S_{j_0+1}}|k|^6\,|F_k|^2,\qquad F=\mathbb P\nabla\!\cdot(u\otimes u),
\]

(the `t = 0` `H³`-shell rate times the window length; the checker also reports the `λ_{j₀+1}³‖P_{j₀+1}F‖₂` variant). `F_k = i(I − kkᵀ/|k|²)v_k`, `v_k = Σ_{k′}(a_{k′}·k)a_{k−k′}` (divergence-free), computed by exact integer triad convolution and projected onto `S_{j₀+1}`; `|F_k|² = |v_k|² − (k·v_k)²/|k|²` is rational. With `a_k = c e_k` (integer polarizations `e_k`, one scalar `c` fixing `E₀`),

\[
\Big(\frac{\mathcal N_{j_0+1}}{R_{j_0}}\Big)^2=\frac{c_w^2E_0}{\nu^2}\,G,\qquad
\boxed{G:=\frac{S_F}{S_R\,S_E\,\lambda_{j_0+1}^4}},\qquad
S_F=\sum_{S_{j_0+1}}|k|^6|F_k/c^2|^2,\ S_R=\sum_{S_{j_0}}|k|^6|e_k|^2,\ S_E=\sum|e_k|^2 ,
\]

a pure lattice number (`c_w` the window constant `c`, written `c_w` to avoid the amplitude). Amplitudes are **not** equal mode by mode in any family below (for the cross polarization `|e_k|` varies by exactly a factor `√2` on family A at every `λ₀`, and by `√2, √(13/4), √(61/13), √5 ≈ 1.41, 1.80, 2.17, 2.24` on family B at `λ₀ = 1, 2, 4, 8` — exact fixture; the Leray-z family has `|a_k|² = 1 − k_z²/|k|²`); this is a weakening of the sketch's "equal amplitudes", forced by exactness (unit-normalised polarizations introduce products of distinct square roots).

**Exact results** (`λ₀ = 2^{j₀}`; every `G` is an exact rational in the checker output):

| family | `λ₀ = 1` | `2` | `4` | `8` | trend |
|---|---|---|---|---|---|
| A cube surface `|k|_∞ = λ₀`, cross polarization (26 / 98 / 386 modes) | `13469/57960 ≈ 0.2324` | `≈ 0.0728` | `≈ 0.0389` | — | **decreases** |
| B full dyadic shell `λ₀ ≤ |k| < 2λ₀`, cross polarization (26 / 224 / 1852 / 14968 modes) | `13469/57960 ≈ 0.2324` | `17672286311/74288167296 ≈ 0.2379` | `≈ 0.3401` | `≈ 0.6474` | **increases**; step ratios `1.024, 1.430, 1.904` |
| C full dyadic shell, coherent Leray-z polarization `a_k ∝ (I − kkᵀ/|k|²)e_z` | `55021/264576 ≈ 0.2080` | `≈ 0.2167` | `≈ 0.4069` | — | **increases**; step ratios `1.042, 1.878` |
| D few-mode `±λ₀(1,0,0)`, `±λ₀(1,1,0)` | `125/576` | `125/2304` | `125/9216` | `125/36864` | **decreases**, exactly `∝ λ₀^{−2}` (closed form `S_F = 250λ₀⁸, S_R = 18λ₀⁶, S_E = 4`) |

Family B at `λ₀ = 8` is an int64 vectorised convolution with an a-priori overflow bound (`3·e_max²·λ_{j₀+2}·#modes < 2⁶²`), cross-checked exactly against the pure big-integer path at `λ₀ ≤ 4`. The `λ_{j₀+1}³‖·‖₂` variant of `G` is **not** monotone at the `λ₀ = 1 → 2` step for B/C and is not asserted.

**Reading.** Bernstein saturation `‖u‖_∞ ∼ λ^{3/2}‖u‖₂` predicts `rate ∼ λ^{11/2}E₀`, `R_{j₀} ∼ λ³√E₀`, hence `𝒩/R ∼ λ^{1/2}√E₀/ν`, i.e. `G ∼ λ₀` (step ratio `2`). That prediction is analytic (`Dr`); the exact finite sequences B and C approach it (`1.90` and `1.88` at the last doubling). The cube-surface family A — the datum as first sketched — has only `∼λ₀²` modes and incoherent polarizations, is far from Bernstein saturation, and its ratio **falls**: the refutation of an energy-only `B` needs data that fill the dyadic shell (`∼λ₀³` modes) with constructive interference; family D, the few-mode datum, shows the complementary `λ₀^{−1}` decay of the ratio, so no few-mode or shell-surface experiment can see the obstruction. This contrast is the point.

**What is refuted.** Dividing (RRB) by `R_{j₀}`: `𝒩_{j₀+1}/R_{j₀} ≤ α + C2^{−σj₀}B/R_{j₀}`, and `R_{j₀}² = E₀S_R/S_E ≥ λ₀⁶E₀` (checked). At fixed `(E₀, ν, T)` the remainder `B(E₀, ν, T)` is a fixed number, so at fixed `(α, C, σ)` the right side tends to `α < 1` as `j₀` grows, while the exact proxy ratio `(c_w√E₀/ν)√G` increases along B/C for `λ₀ ≤ 8` (`G > 0` on every instance) and, by the `Dr` scaling `G ∼ λ₀`, without bound. Because `B` may depend on `E₀`, no conclusion is drawn from varying `E₀` at fixed `λ₀`. Two honest fences: (i) this is the **`t = 0` rate × window proxy**, first order in the window — the true `𝒩` carries the in-window heat factor (between `e^{−4c}` and `1` on the target shell, a constant) and the evolution of `u` across the window, and precisely in the regime where the proxy is large (`λ^{1/2}√E₀/ν ≫ 1`) the nonlinear time `1/(λ‖u‖_∞)` is shorter than `τ_j`, so the proxy is not a proof about the windowed quantity. The windowed quantity itself is not computed in this note (that is protocol v2, §5); (ii) the growth beyond `λ₀ = 8` (B) / `4` (C) is the `Dr` scaling, not an executed check. Nothing here contradicts regularity of these data; it says an energy-only remainder is the wrong form.

### Status

`NS-P2-RRB-ENERGY-ONLY-REMAINDER` — **REFUTED-as-stated** (exact full-dyadic-shell instances of the `t = 0` proxy, `λ₀ ≤ 8`; `√λ` scaling analytic `Dr`; cube-surface and few-mode data give the opposite trend and are recorded as the negative control). The object refuted by fixture is the `t = 0` rate × window proxy of `𝒩`; the windowed inequality (RRB) with an energy-only remainder is not evaluated by any fixture here — its refutation is the analytic scaling argument, tier `Dr`, registered as `PROP-P3-RECENT-RETENTION-BOUND-ENERGY-ONLY-REFUTED`.

## 4. Datum-dependent remainder — REGULARITY-EQUIVALENT / HOLD

If `B` may depend on the solution (through `M₃ = sup_t‖u‖_{H³}` or any `u`-dependent Besov quantity), (RRB) holds for every `H³`-regular solution on `[0, T]` with `α = 0`: `𝒩_{j+1} ≤ τ_jλ_{j+1}³·sup_t‖P_{j+1}ℙ∇·(u⊗u)‖₂ ≲ (c/ν)λ_{j+1}·λ_{j+1}^{−2}M₃² = C(c/ν)M₃²2^{−j}`, i.e. `σ = 1` (product estimate in `H³`, standard, relayed `Dr`). Conversely (RRB) ⇒ uniform `H³` ⇒ regularity is the chain of §2. Hence

\[
\boxed{\text{(RRB) with solution-dependent }B\iff\text{regularity on }[0,T]},
\]

the same situation as `NS-P2-FINAL-EQUIV` and `NS-P2-UNIFORM-FULLCONV-SCALE-LOSS`. By §8 of the final-closure note this is recorded as **REGULARITY-EQUIVALENT / HOLD**, not as an open bridge. The only non-equivalent residue is, as before, a constructive generator of `2^{−σj}B` from finite records without an `M₃` oracle — `NS-P2B-SCALE-CONTRACTION-UNIFORM`, already OPEN. The two directions of the equivalence sketch are **not** checked by any fixture and nothing is asserted about them beyond this relayed classification.

### Status

`NS-P2-RRB-DATUM-REMAINDER` — **REGULARITY-EQUIVALENT / HOLD** (§8).

## 5. The measured quantity — Definition, protocol v2

**Definition (window bilinear constant).** For a fixed-`N` Galerkin solution on `[0, T]`, window constant `c`, and shell `j`,

\[
\alpha_j^N(T) := \sup_{t\in[\tau_j,\,T]}\ \frac{\mathcal N_{j+1}(t)}{R_j^N(T)}\qquad(\mathcal N_{j+1}\text{ as in §1, with the full Duhamel integral}).
\]

(RRB) with any remainder is the statement `α_j^N ≤ α + C2^{−σj}B/R_j^N`; an energy-only remainder demands `limsup_j α_j^N ≤ α < 1 − e^{−c}` uniformly over data of fixed `E₀`.

**Protocol v2** (replaces the `t = 0` rate × window proxy of §3, "v1"): (1) integrate the Galerkin system exactly enough that `𝒩_{j+1}(t)` is an enclosure (validated interval Taylor; the scale-loss audit used such an integration only as scratch work, not in this repository — protocol v2 requires it reproduced in-repo); (2) evaluate the Duhamel integral over `[t − τ_j, t]` by quadrature with the heat factor kept, not by the endpoint rate; (3) report `α_j^N(T)` for the family-B/C data of §3 at `λ₀ = 1, 2, 4` and two values of `E₀`; (4) the falsifiable prediction from §3 is `α_j^N ∝ √(E₀λ₀)/ν` up to constants — a decrease, or saturation below `1 − e^{−c}`, would refute §3's `Dr` reading, not (RRB).

### Status

`NS-P2-WINDOW-BILINEAR-CONSTANT` — **DEFINITION** (not measured; v1 proxy values are the `G` table of §3).

## 6. Readout lens

A singularity is not a primitive of this audit: what exists at every stage is a finite shell readout `R_j^N`, a finite window, and a finite bilinear convolution. (RRB) asks the recent window to *retain* at most a fraction `α` of the previous shell's readout plus a summable remainder — "perfect retention" would be `α = 0` with `B` independent of the datum. §3 says that attempted perfect retention has a cost that does not vanish: the more a datum fills a shell coherently, the larger the fraction pushed outward per window, so the compatibility constraint "keep the outward channel below `α`" tightens with `λ₀` instead of loosening. In the standalone's language this is the Generative Constraint Accumulation Principle (§114.1): nonlinear generation plus systematic suppression of future-relevant novelty accumulates constraints; the outward-window excess is one component of the defect vector `D = D_disp + D_hol + D_cancel + D_visc + D_dead` (§51.2), and the quantity that would have to be positive uniformly is the path minimum `δ = min_m Δ_m` (§60). None of this is promoted: the lens organises what the fixtures measured; it proves nothing about the windowed quantity or about regularity.

## 7. Boundary

```text
old-history factor e^{-nu|k|^2 tau_j} <= e^{-c}, lambda^3||P u|| <= R              DERIVED / PASS
recurrence q = alpha/(1-E) < 1 iff alpha < 1-E; R_j <= C_T theta^j                DERIVED / PASS (q != 2^-sigma; j theta^{j-1} if equal)
sum_j R_j < inf => sup_t ||u||_{H^3-hom} < inf                                    DERIVED / PASS
uniform H^3 => compactness => global smooth                                        relayed (Dr), not a fixture
(RRB) with energy-only remainder B(E_0, nu, T)                                     REFUTED-as-stated (t=0 proxy, exact; sqrt(lambda) scaling Dr)
cube-surface / few-mode data                                                       ratio decreases (negative control, exact)
(RRB) with solution-dependent remainder                                            REGULARITY-EQUIVALENT / HOLD
equivalence sketch, both directions                                                not checked; nothing asserted
window bilinear constant alpha_j^N (protocol v2)                                   DEFINITION, not measured
constructive generator of the remainder (NS-P2B-SCALE-CONTRACTION-UNIFORM)         OPEN
Clay Navier-Stokes regularity                                                      OPEN
```
