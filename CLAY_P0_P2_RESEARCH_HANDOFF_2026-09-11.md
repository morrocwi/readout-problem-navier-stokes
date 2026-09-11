# Clay finite-first programme — P0–P2 complete research handoff

**Date:** 2026-09-11  
**Primary repository:** `morrocwi/readout-problem-navier-stokes`  
**Companion repositories:** `morrocwi/information-discrete-math`, `morrocwi/toledo`, `morrocwi/readout_genesis`  
**Purpose:** give the next researcher/AI one self-contained record of what P0–P2 established, what was refuted, what remains open, and the exact point from which the Navier–Stokes attack should continue.  
**Claim discipline:** `PASS` = finite executable verification, `DERIVED` = theorem from declared assumptions, `OPEN` = unproved theorem, `HOLD` = insufficient evidence/adapter/process, `REFUTED` = matching counterexample or contradiction for the precise statement.

---

## 0. Mandatory reading order for a new AI

Read these before changing theorem status:

1. `CLAY_READ_FIRST.md`
2. `CLAY_MULTI_PROBLEM_FINITE_BRIDGE_PROGRAM.md`
3. this file
4. `FUTURE_WORK_P2_TRIAD_ATTACK.md`
5. `paper/NS_P2_TRIAD_PHASE_READOUT_ATTACK.md`
6. `paper/NS_P2B_FINITE_OBSERVATION_WINDOW_ATTACK.md`
7. `paper/NS_P2B_SCALE_CONTRACTION.md`
8. `paper/NS_P2_FINAL_CLOSURE_EQUIVALENCE.md`
9. IDM `docs/UNIVERSAL_FINITE_OBSTRUCTION_UNIFORM_BRIDGE_KERNEL.md`
10. IDM `docs/CLAY_P1_SAFE_CORE_FORMAL.md`
11. IDM `docs/CLAY_P2_NEGATIVE_CONTROLS.md`

The current active NS research branch is:

```text
research/p2-triad-attack-2026-09-11
```

PR: `morrocwi/readout-problem-navier-stokes#48`.

---

# P0 — orientation, audit, and claim boundary

## P0 objective

P0 was not theorem discovery. It froze the actual state of the programme before Clay-sensitive work and separated:

```text
finite evidence
formal evidence
open bridge theorems
process/governance state
```

Source snapshot: `CLAY_P0_AUDIT_2026-09-11.md`.

## P0 findings

### P0-1. Shared architecture fixed

The programme uses the finite-first chain

```text
finite/native object
  -> exact finite law/certificate
  -> uniform theorem over all admissible finite objects
  -> explicit semantic/domain adapter
  -> target/global theorem
```

Two jumps are forbidden unless separately proved:

```text
many finite cases  -/->  all finite cases
all finite cases   -/->  global/continuum theorem
```

Later P1/P2 added two more forbidden jumps:

```text
small adjacent discrepancy  -/->  all-refinement Cauchy control
finite defect existence      -/->  efficient constructive capture
```

### P0-2. Governance exists but GitHub hard enforcement was not complete

NS, IDM and Toledo contain a fail-closed `clay-governance` workflow and `CLAY_GOVERNANCE_ACK.json` convention. At the P0 audit, `main` branches were reported unprotected, so governance existed as workflow/process but was not guaranteed against direct push.

**Status:** process hardening `HOLD` until branch protection/rulesets require the governance check.

### P0-3. P-vs-NP lane blockers identified

At the frozen P0 snapshot the IDM branch `research/p-vs-np-readout` was diverged from current main, and the formal lane had a real Coq 8.20 proof-script failure in:

```text
formal/IDM_SATRestrictionDefect.v
wrong_root_forces_positive_defect
```

There was also a separate lexical false positive in the no-`Admitted` scanner caused by ordinary English `admit` in comments.

These are process/formal blockers, not mathematical counterexamples.

### P0-4. NS finite assets were usable but no global bridge existed

Existing NS work already contained fixed-cutoff exact observability, local inverse, finite tape, retained/tail composition, and residual/relative-energy machinery. P0 explicitly did not promote these to global regularity.

### P0 ruling

```text
P0 audit = CLOSED
shared finite evidence = usable
NS global bridge = OPEN
PNP unrestricted bridge = OPEN
Toledo canonicalization gate = OPEN
```

---

# P1 — safe finite theorem core

Primary source: IDM `docs/CLAY_P1_SAFE_CORE_FORMAL.md`.

IDM PR #125 merged as:

```text
1ddf295ea6fd9c504a10e6296fdea5bb97cf78fd
```

The P1 safe core is machine-checked under Coq 8.20 and contains 11 axiom-free theorems.

## P1-1. Strict-margin and fail-closed semantics — `Th_coqc`

Promoted theorems:

```text
strict_margin_pass_sound
strict_margin_pass_complete
strict_margin_hold_when_not_strict
missing_certificate_holds
gated_pass_requires_certificate_and_margin
```

Meaning: a finite PASS requires a real certificate plus a strict certified margin; missing or non-strict evidence returns HOLD rather than silently passing.

## P1-2. Finite uncertainty/error composition — `Th_coqc`

```text
error_budget_monotone
error_budget_additive
finite_chain_budget_composition
compatibility_two_step
```

These prove safe finite bookkeeping and finite-chain composition. They do **not** create an all-resolution tail theorem.

## P1-3. Symmetry transport — `Th_coqc`

```text
symmetry_transport_pass
```

Transport is valid only under an explicitly declared verifier-invariance hypothesis.

## P1-4. Local finite-defect soundness — `Th_coqc`

```text
verified_local_defect_sound
```

A local verifier has semantic force only under an explicitly supplied checker-soundness hypothesis.

## P1 boundary

P1 does **not** prove:

```text
GlobalFailure -> finite witness
finite defect -> efficient capture
finite adjacent compatibility -> global compatible object
NS regularity
P != NP
```

Those are separate domain/global theorems.

---

# P2A — generic adversarial controls

Primary source: IDM `docs/CLAY_P2_NEGATIVE_CONTROLS.md`.

P2 first attacked over-broad bridge schemas before doing NS-specific work.

## P2A-1. Naive finite obstruction principle — `REFUTED`

Counterexample:

\[
a_n=n.
\]

Every finite prefix is bounded, but the full sequence is not bounded. Therefore

```text
arbitrary global failure -> natural finite-prefix failure
```

is false without a domain-specific finite-detectability hypothesis.

Strengthened `PROP-FUB-03` remains `OPEN`.

## P2A-2. Adjacent compatibility is not a global Cauchy theorem — `REFUTED`

Harmonic partial sums satisfy

\[
H_n-H_{n-1}=1/n\to0,
\]

while cumulative drift is unbounded. Therefore

```text
adjacent discrepancy -> 0
```

does not imply all-refinement Cauchy control.

A viable bridge needs a Cauchy modulus, summable tail, or equivalent true uniform control.

## P2A-3. Defect existence does not imply efficient generic capture — `REFUTED` in the declared black-box model

A single hidden defect in a universe of size `2^n` can be hit by a `poly(n)` generic support with probability only `poly(n)/2^n`.

This does **not** refute a structure-aware SAT/circuit constructor. It refutes only the inference

```text
defect exists -> efficient generic capture
```

without an access/structure/resource hypothesis.

## P2A-4. Two P1 hypotheses were proved necessary by finite controls

- symmetry transport can fail without verifier invariance;
- checker acceptance can fail semantically without checker soundness.

---

# P2B/NS-1 — finite singularity-sensitive witness stack

The NS lane then isolated a regularity-sensitive finite object rather than relying on weak state agreement.

## NS-1.1 `NS-FUB-A1E` — `DERIVED` under declared continuation/Galerkin adapters

Finite-time singularity forces arbitrarily large finite-Galerkin `H^3` exceedances. This identifies a finite regularity-sensitive signal, conditional on the stated standard adapters.

Source: `paper/NS_FUB_A1_H3_FINITE_WITNESS.md`.

## NS-1.2 `A1V` exact finite `H^3` exceedance verifier — `PASS`

Exact rational interval arithmetic verifies a strict finite statement of the form

```text
certified finite interval enclosure
  -> lower_bound(||v_N||_{H^3}^2) > B^2
```

without floating-point arithmetic in the PASS/HOLD decision.

Checker: `reproduction/checks/check_ns_fub_a1_h3_certificate.py`.

## NS-1.3 Fixed-N validated dynamics stack — finite theorem/certificate machinery established

The project built:

```text
validated finite tube
-> tube chain
-> residual-centered tube
-> finite rational strict-witness certificate
-> completeness/semi-decision for the declared finite rational polynomial/Galerkin setting
```

Key sources:

```text
paper/NS_FUB_A1C_VALIDATED_TUBE.md
paper/NS_FUB_A1C_TUBE_CHAIN.md
paper/NS_FUB_A1C_RESIDUAL_TUBE.md
paper/NS_FUB_A1C_FINITE_CERTIFICATE_COMPLETENESS.md
```

Meaning: at fixed finite rational Galerkin dimension, the certificate language is not the main obstruction. This does not imply uniform-in-N regularity.

---

# P2B/NS-2 — no-go results that removed false bridges

## NS-2.1 `L2`/energy tail does not control omitted `H^3` tail — `REFUTED`

Small omitted energy can coexist with arbitrarily large high-derivative weight. Therefore an energy-tail argument alone cannot close the `H^3` bridge.

Source: `paper/NS_FUB_A1_H3_TAIL_NO_GO.md`.

## NS-2.2 Fixed-N certificate/trajectory breakdown is not a singularity witness — `REFUTED`

Every fixed finite unforced Galerkin ODE remains a finite-dimensional system with global extension. Therefore failure of one finite numerical/certificate procedure is not by itself PDE blow-up evidence.

Source: `paper/NS_FUB_A1_FIXED_N_EXTENSIBILITY_NO_GO.md`.

## NS-2.3 Local/adjacent compatibility is insufficient — inherited `REFUTED` generic inference

Increasing N and observing local agreement does not provide a uniform all-refinement regularity theorem.

## NS-2.4 Larger fixed N / longer finite integration is not the missing proof

These may improve evidence but do not establish the quantified uniform theorem.

---

# P2B/NS-3 — positive all-scale tail pieces

## NS-3.1 Positive-lag Stokes tail — `DERIVED`

The project obtained an explicit all-scale `H^3` tail envelope of the form

\[
\|Q_Ne^{\nu\tau\Delta}f\|_{H^3,F}^2
\le
\frac{192}{(2\nu\tau)^4(N+1)^2}\|f\|_2^2.
\]

## NS-3.2 Old-Duhamel tail — `DERIVED`

For nonlinear history separated from the endpoint by a positive time gap `delta`,

\[
\|D_{old}(t)\|_{H^3,F}^2
\le
\frac{960}{(2\nu\delta)^5(N+1)^2}A_F^2.
\]

Source: `paper/NS_FUB_A1_STOKES_NONLINEAR_TAIL_SPLIT.md`.

These results isolate the difficult piece as **recent nonlinear transfer**, not old history.

---

# P2B/NS-4 — adapter-neutral `H^3` margin reduction

Source: `paper/NS_P2_FINITE_TO_CONTINUUM_CLOSURE.md`.

For finite Galerkin solution define

\[
X_N=\|u_N\|_{H^3}^2,
\qquad
\mathcal D_N=\nu\|\nabla\Lambda^3u_N\|_2^2,
\]

with exact identity

\[
\frac12X_N'+\mathcal D_N=\mathcal P_N.
\]

If there are cutoff-independent constants

\[
0\le\theta<1,
\qquad C_T<\infty
\]

such that for all N and all `t in [0,T]`,

\[
\boxed{
\mathcal P_N(t)
\le
\theta\mathcal D_N(t)+C_T(1+X_N(t)),
}
\]

then Gronwall yields

\[
1+X_N(t)
\le
(1+\|u_0\|_{H^3}^2)e^{2C_TT}.
\]

### Ruling

The implication

```text
uniform dissipative margin -> uniform H3 bound
```

is `DERIVED`.

The difficult theorem is constructing the margin non-vacuously from NSE structure.

---

# P2B/NS-5 — High–High subroute and geometric lifting

With dyadic `H^3` weight `64^j`, if a true shell defect tail obeys

\[
d_j\le Aq^j(1+X_3),
\qquad 64q<1,
\]

then the weighted tail is explicitly summable:

\[
\sum 64^jd_j\le C_R(1+X_3).
\]

`NS-P2-HH-GEOM-LIFT` is `DERIVED` as weighted-tail arithmetic.

It does **not** prove the required nonlinear defect envelope.

The external High–High preprint route was audited and put on `HOLD`; it is not a trusted final adapter in this programme.

---

# P2C — finite-observation window route

The project then translated IDM/EPSC finite accounting to a modal finite-observation regularity criterion.

Sources:

```text
paper/NS_P2B_FINITE_OBSERVATION_WINDOW_ATTACK.md
paper/NS_P2B_SCALE_CONTRACTION.md
paper/NS_P2B_WINDOW_BALANCE_NO_GO.md
```

Define

\[
K_N(u)
=
\sup_t
\left(\int_t^{t+\tau_0}\|P_Nu(s)\|_{H^1}^{2p}ds\right)^{1/(2p)},
\qquad p>2.
\]

## P2C-1. EPSC observation lift — `DERIVED`

If a certified path satisfies

\[
\sup_s\|u(s)-v(s)\|_2\le\varepsilon
\]

and `Lambda_N` is the largest retained Stokes scale, then

\[
\boxed{
K_N(u)
\le
K_N(v)+\tau_0^{1/(2p)}\sqrt{\Lambda_N}\,\varepsilon.
}
\]

Identifier: `NS-P2B-EPSC-OBS-LIFT`.

## P2C-2. Subcritical modal scaling reduction — `DERIVED`

Let

\[
\alpha_p=\frac{p-2}{2p}.
\]

If for every finite T there exist `C_T<infinity`, `sigma>0`, independent of N, with

\[
K_N(u)^2\le C_T\Lambda_N^{\alpha_p-\sigma}
\]

for sufficiently large N, then the finite-observation gate eventually passes.

Identifier: `NS-P2B-SUBCRITICAL-OBS`.

## P2C-3. Energy+dissipation alone does not force the strict exponent gain — `REFUTED inference`

Abstract dyadic critical-spike budget:

\[
N_j=2^j,
\quad e_j=N_j^{-1},
\quad A_j=N_j,
\quad\delta_j=N_j^{-2}
\]

has finite energy/dissipation budgets but produces critical observation scaling

\[
K_{N_j}^2\sim\Lambda_j^{(p-2)/(2p)}.
\]

This is an abstract budget countermodel, not an NSE solution. It refutes only the inference from energy/dissipation accounting alone.

## P2C-4. Exact window balance + transfer conservation still do not force strict contraction — `REFUTED inference`

Even exact integrated shell balance plus total transfer conservation permits an abstract critical cascade budget. Therefore any true theorem must use more than accounting: actual triad coefficients, divergence-free polarization, phase, cancellation, viscosity/scale interaction, or equivalent NSE-specific structure.

## P2C-5. Scale-contraction recurrence — `DERIVED`

Define dyadic ratio

\[
R_j=
\frac{(K_{N_j}^2)^{2p/(p-2)}}{\Lambda_j}.
\]

If finite upper certificates satisfy

\[
R_j\le U_j,
\qquad
U_{j+1}\le\kappa U_j+B\rho^j,
\qquad
0\le\kappa,\rho<1,
\]

then

\[
U_j\to0,
\qquad R_j\to0,
\]

and the finite-observation gate eventually passes.

Identifier: `NS-P2B-SCALE-CONTRACTION`.

---

# P2D — equivalence audit and correction of the stopping rule

Source: `paper/NS_P2_FINAL_CLOSURE_EQUIVALENCE.md`.

Let `SC(T)` be the existence of `j0`, finite nonnegative `U_j`, and `kappa,rho<1`, `B<infinity` with

\[
R_j\le U_j,
\qquad
U_{j+1}\le\kappa U_j+B\rho^j.
\]

Under the declared periodic modal/dyadic finite-observation adapter,

\[
\boxed{
\text{regularity on }[0,T]
\iff
SC(T).
}
\]

### Direction regularity -> SC(T) — `DERIVED`

Regularity gives finite

\[
M_T=\|u\|_{L^\infty(0,T;H^1)}.
\]

Then `K_N^2` is cutoff-independent bounded and

\[
R_j\le C_T^*/\Lambda_j.
\]

For dyadic `Lambda_{j+1}=4Lambda_j`, choose

\[
U_{j+1}=\frac14U_j.
\]

### Direction SC(T) -> regularity — `DERIVED` under declared adapter

The recurrence gives `R_j->0`; a finite observation level eventually satisfies the regularity gate.

## Critical methodological correction

The equivalence theorem remains valid and useful. However, the earlier workflow decision

```text
SC(T) is regularity-equivalent
therefore stop attacking SC(T)
```

is **withdrawn as a stopping rule**.

Correct rule:

```text
equivalence != refutation
```

A statement is rejected only by a matching counterexample/impossibility proof. A constructive route to `SC(T)` from genuinely weaker, finite/checkable NSE structure remains a legitimate direct attack.

Thus the current mathematical status is:

```text
NS-P2B-SCALE-CONTRACTION-UNIFORM = OPEN as a constructive attack target
NS-P2-FINAL-EQUIV = DERIVED equivalence theorem
```

Do not erase the equivalence theorem; do not use it as a reason to stop proving the constructive statement.

---

# P2E — reopened exact triad/phase attack

Active source: `paper/NS_P2_TRIAD_PHASE_READOUT_ATTACK.md` on PR #48.

The attack order follows the project methodology:

```text
IDM exact finite law
-> Readout Genesis minimal dynamically closed readout
-> scale/universe translation
-> NS Fourier laboratory
-> falsification first
-> only then all-scale theorem
```

## P2E-1. Shell energy alone does not determine signed transfer — `REFUTED`

An exact isolated NSE triad has reduced coordinates `(x,y,z,r)` with

\[
\dot x=2c_ar-2\nu s_ax,
\]
\[
\dot y=2c_br-2\nu s_by,
\]
\[
\dot z=2c_cr-2\nu s_cz.
\]

At the declared test state `x=y=z=1`, `nu=1/200`, changing only `r` from `+1` to `-1` changes the high-shell derivative from

\[
\dot z=19/20
\]

to

\[
\dot z=-21/20.
\]

Therefore

```text
shell energies alone -> universal signed transfer / contraction
```

is refuted for this reader class.

Checker: `reproduction/checks/check_ns_p2_triad_phase_stress.py`.

## P2E-2. Viscosity alone does not contract normalized phase coherence — `REFUTED`

For

\[
\chi=\frac{r}{\sqrt{xyz}},
\]

the viscous contribution cancels exactly from `d log|chi|/dt`.

Therefore viscosity by itself is not the missing strict phase-contraction mechanism.

## P2E-3. Isolated triad perfect-locking defect — exact finite identity

Define

\[
D=xyz-r^2.
\]

For the exact isolated-triad reduction used by the checker,

\[
\boxed{D'=-16\nu D.}
\]

Hence `D=0` is invariant. An isolated triad can remain perfectly phase locked; strict decoherence cannot be assumed at the single-triad level.

Checker: `reproduction/checks/check_ns_p2_triad_coherence_defect.py`.

## P2E-4. Exact N=1 H3-production sign-frustration — finite structural `PASS`

Using the repository's exact real-coordinate N=1 Galerkin tensor (`d=52`), the inhomogeneous H3 nonlinear-production cubic polynomial has:

```text
432 nonzero aggregated cubic monomials
218 positive coefficients
214 negative coefficients
```

The GF(2) sign-alignment system is exact `UNSAT`: all nonzero cubic monomial contributions cannot be made simultaneously positive by a real-coordinate sign assignment.

A tracked contradiction uses 4 equations.

Checker: `reproduction/checks/check_ns_p2_n1_h3_sign_frustration.py`.

### Boundary

This proves finite sign frustration at N=1. It does not yet imply an all-N quantitative contraction.

## P2E-5. Four-term exact frustration tax — `DERIVED` finite inequality

For one extracted conflict cycle, write the relevant variables as `a,b,c,d,e`. The subpolynomial has the form

\[
Q_{cycle}=600a[-19bc+18bd-19ce-18de].
\]

Because the four desired signs are inconsistent, at least one term opposes the others. If

\[
S_{cycle}=\sum_i |t_i|,
\qquad
m_{cycle}=\min_i|t_i|,
\]

then

\[
\boxed{|Q_{cycle}|\le S_{cycle}-2m_{cycle}.}
\]

This is an exact local quantitative cancellation tax.

Boundary: `m_cycle/S_cycle` may approach zero if one amplitude collapses, so this alone does not yield a uniform delta.

Checker: `reproduction/checks/check_ns_p2_n1_frustration_tax.py`.

## P2E-6. Symbolic all-n ladder frustration family — `DERIVED` for declared family

For the symbolic family

\[
p=(0,0,1),
\quad k_-=(n,-n,-1),
\quad k_0=(n,-n,0),
\quad k_+=(n,-n,1),
\]

the four relevant coefficients have pattern

\[
A_n,-B_n,A_n,B_n,
\]

with

\[
A_n=n^3(4n^4-6n^2-17),
\]

\[
B_n=2n^3(4n^6-6n^2-7).
\]

For integer `n>=1`, the product is

\[
-A_n^2B_n^2<0,
\]

so the sign-frustration pattern persists for every n in this family.

Checker: `reproduction/checks/check_ns_p2_ladder_frustration_alln.py`.

Boundary: existence of an all-n motif is not the same as coverage of every transfer path.

## P2E-7. Symbolic dyadic high-high motif — `DERIVED` for declared family

Take

\[
q=(n,n,0),
\qquad
r=(n,-n,0),
\qquad
t=(2n,0,0),
\]

so the motif links scale `n` directly to `2n`.

The exact H3 nonlinear-production subpolynomial is

\[
\boxed{
Q_n=C_n\,\Im(z_qz_r\overline{z_t}),
}
\]

with

\[
C_n=8n^7(28n^4+18n^2+3)>0.
\]

After normalization by the inhomogeneous H3 modal weights, the trilinear coefficient obeys the exact symbolic bound

\[
\boxed{
\Gamma_n\le\frac{7\sqrt2}{8n^2}.
}
\]

Checker: `reproduction/checks/check_ns_p2_dyadic_hh_motif_alln.py`.

### Important caveat

For a single complex triad, the phase can maximize

\[
|\Im(z_qz_r\bar z_t)|=|z_qz_rz_t|.
\]

Therefore the four-real-monomial sign pattern of one complex triad must **not** be overinterpreted as genuine network cancellation. The next theorem must involve overlapping triads/phase constraints, not merely one triad rewritten in real coordinates.

---

# Current bottleneck after P0–P2

The remaining attack has been narrowed to an NSE-specific network statement.

The active mathematical question is not

```text
Does one triad cancel?
```

but

```text
Can an overlapping network of transfer-active triads remain phase-aligned strongly enough,
for long enough and across arbitrarily many dyadic boundaries,
to sustain the critical observation ratio without paying a quantitative cancellation or amplitude-cut cost?
```

Each maximal-transfer complex channel imposes a phase condition schematically

\[
\phi_p+\phi_q-\phi_k=\pm\frac\pi2.
\]

Overlapping channels share phases. A genuine network-frustration theorem must show either incompatible phase requirements or a structural amplitude cut.

## Active target: `NS-P2-FRUSTRATION-OR-CUT` — `OPEN`

Prove, for every sufficiently high dyadic boundary and every admissible phase-complete NSE finite state in the declared class, a certified dichotomy strong enough to force one of:

1. **frustration:** overlapping triads cannot all saturate outward transfer simultaneously, yielding a quantitative deficit; or
2. **cut:** one or more required amplitudes are small enough that the transfer chain loses a quantitative amount.

The output must be strong enough to assemble

\[
R_{j+1}
\le
(1-\delta_j)R_j+\beta_j
\]

with a proven decay condition such as

\[
\inf_j\delta_j>0,
\qquad
\beta_j\le B\rho^j,
\quad 0<\rho<1,
\]

or a weaker product/summability condition still sufficient to prove `R_j->0`.

---

# Current final objective for the NS route

Fix exact conventions for

\[
N_j=2^jN_0,
\qquad
K_N=
\sup_t
\left(\int_t^{t+\tau_0}\|P_Nu(s)\|_{H^1}^{2p}ds\right)^{1/(2p)},
\]

and

\[
R_j=
\frac{(K_{N_j}^2)^{2p/(p-2)}}{\Lambda_{N_j}}.
\]

The complete constructive theorem sought by this route is:

\[
\boxed{
\forall u_0,\forall\nu>0,\forall T<\infty,
\exists p>2,j_0,\kappa<1,B<\infty,\rho<1
}
\]

obtained **without assuming the desired regularity**, such that for every `j>=j0`,

\[
\boxed{
R_{j+1}\le\kappa R_j+B\rho^j.
}
\]

Existing P2 algebra then gives `R_j->0`; the declared finite-observation adapter gives regularity on `[0,T]`; arbitrary finite T gives the desired continuation route.

What is missing is the NSE-specific constructive proof of this recurrence, not the recurrence algebra itself.

---

# Do-not-repeat list for the next AI

Do not spend the main effort on any of these unless they directly support the active theorem:

```text
larger fixed cutoff by itself
longer fixed-N integration by itself
energy/L2 tail as a surrogate for H3 tail
fixed-N solver/certificate failure as a blow-up witness
adjacent-resolution agreement as an all-scale theorem
energy+dissipation accounting alone
window balance + total transfer conservation alone
single-triad phase decay
single complex-triad real-coordinate sign pattern as network frustration
relabeling a known regularity criterion and stopping because it is equivalent
```

Reject a proposal only with a matching counterexample/impossibility proof. If neither proof nor counterexample exists, keep `OPEN`/`HOLD` and continue.

---

# Provenance summary

Important merged/source checkpoints:

```text
IDM P1 safe core PR #125
  1ddf295ea6fd9c504a10e6296fdea5bb97cf78fd

NS P2 reduction PR #42
  83e966df251e548fd9574d9553d7f4bf5551877b

NS P2 status handoff PR #43
  4234050311b26d4fba93cff2187c97565c0e42ef

NS P2B finite-observation route PR #45
  9d6f516734d1a151bae987a8df33c05273bcd32b

NS final equivalence audit PR #47
  c25baad7617ce419a012a3b53c9bd40bc6af25b9

Toledo P2 final provenance PR #22
  4440fa6d86b6d60670d865792a0209bd0c41ebbf

Current reopened direct triad attack
  branch: research/p2-triad-attack-2026-09-11
  PR: #48
  current handoff-era head is evolving; pin the final merged SHA before Toledo promotion.
```

---

# Handoff status

```text
P0 audit                                      CLOSED
P1 finite safe core                          PASS / Th_coqc
naive generic FUB-03/04/05 forms            REFUTED in declared controls
fixed-N NS certificate machinery             PASS / DERIVED in declared finite setting
L2->H3 tail shortcut                         REFUTED
fixed-N failure->singularity shortcut        REFUTED
positive-lag Stokes/old-Duhamel tails        DERIVED
H3 dissipative-margin reduction              DERIVED
EPSC -> modal observation lift               DERIVED
energy/accounting-only strict gain           REFUTED inference
scale-contraction -> eventual gate           DERIVED
regularity <-> existential SC(T)              DERIVED under declared adapter
"equivalence means stop" rule                WITHDRAWN
shell-energy-only signed transfer             REFUTED by actual triad
viscosity-only normalized phase contraction  REFUTED
isolated-triad D'=-16nu D                    DERIVED for declared exact reduction
N=1 H3 sign-frustration                       PASS exact finite
N=1 frustration tax                          DERIVED finite inequality
all-n ladder motif                            DERIVED for declared symbolic family
dyadic HH motif + Gamma_n <= 7sqrt2/(8n^2)  DERIVED for declared symbolic family
overlapping-triad phase holonomy             OPEN
NS-P2-FRUSTRATION-OR-CUT                     OPEN
constructive uniform R_j recurrence          OPEN
```

The next AI should begin with the two OPEN lines immediately above, not restart P0/P1 or repeat previously refuted routes.
