# FUTURE WORK — P2 direct Navier–Stokes triad attack

**Date:** 2026-09-11  
**Status:** executable handoff plan for another AI/researcher  
**Read first:** `CLAY_P0_P2_RESEARCH_HANDOFF_2026-09-11.md`  
**Current branch:** `research/p2-triad-attack-2026-09-11`  
**Current PR:** `#48`

---

## Mission

Do not restart the programme from energy accounting or larger simulations. The current target is to derive, or falsify with an actual NSE/Fourier counterexample, an NSE-specific mechanism that forces strict cross-scale loss.

The desired end product is a constructive recurrence for

\[
R_j=
\frac{(K_{N_j}^2)^{2p/(p-2)}}{\Lambda_{N_j}},
\qquad
N_j=2^jN_0,
\]

of the form

\[
\boxed{
R_{j+1}\le\kappa R_j+B\rho^j,
\qquad
0\le\kappa<1,
\quad 0\le\rho<1,
}
\]

or a weaker explicitly proved product/summability recurrence still sufficient to force `R_j -> 0`.

The constructor for the constants/certificates must use finite/checkable NSE structure and must not assume the desired uniform regularity.

---

# Active theorem target

## `NS-P2-FRUSTRATION-OR-CUT` — OPEN

At every sufficiently high dyadic transfer boundary, show that a phase-complete set of active Fourier triads cannot maintain critical coherent outward transfer without paying one of two costs:

### Branch A — frustration

Overlapping triad phase requirements are incompatible enough to give a quantitative cancellation deficit.

### Branch B — amplitude cut

At least one required mode/interaction amplitude is small enough that the transfer chain loses a quantitative amount before reaching the next dyadic scale.

The dichotomy must be strong enough to sum/iterate over scale and time.

---

# Known exact facts that the next proof must respect

1. Shell energies alone do not determine signed transfer.
2. An isolated triad can reverse high-shell transfer by changing the phase-sensitive coordinate `r` while keeping shell energies fixed.
3. Viscosity cancels from the logarithmic derivative of normalized isolated-triad phase coherence.
4. For the declared isolated triad, `D=xyz-r^2` satisfies `D'=-16 nu D`; perfect phase locking can persist.
5. Exact N=1 H3 production has finite sign frustration, but a real-coordinate sign conflict inside one complex triad can be a coordinate representation of a freely selectable complex phase; do not call this network frustration without an overlap argument.
6. An all-n symbolic ladder motif exists.
7. A dyadic high-high motif with `q=(n,n,0)`, `r=(n,-n,0)`, `t=(2n,0,0)` has

\[
Q_n=C_n\Im(z_qz_r\overline{z_t}),
\qquad
C_n=8n^7(28n^4+18n^2+3),
\]

and normalized coefficient

\[
\Gamma_n\le\frac{7\sqrt2}{8n^2}.
\]

8. Energy+dissipation accounting and integrated shell balance/total transfer conservation alone do not force a strict exponent gain.

---

# Work package FW-0 — repair repository state before theorem promotion

**Priority:** immediate housekeeping, not mathematical discovery.

- update `CLAY_GOVERNANCE_ACK.json` in the same PR;
- update `CLAY_RESEARCH_TODO.md` so it no longer says the constructive P2 attack is retired;
- keep the valid equivalence theorem `NS-P2-FINAL-EQUIV` recorded as DERIVED;
- explicitly record that the previous stopping inference “equivalence => stop” is withdrawn;
- run both `ns-p2-triad-attack` and `Clay Research Governance` green before merge;
- after merge, pin the exact merge SHA in Toledo; do not pin a moving branch head as final provenance.

**Done when:** PR #48 has no governance HOLD and all exact triad controls are green at one pinned head.

---

# Work package FW-1 — define the genuine complex phase-holonomy problem

The present finite sign test must be lifted from real-coordinate monomial signs to complex triad phases.

For each transfer-active triad/channel `tau=(p,q,k)` define a complex interaction in one fixed divergence-free/helical convention:

\[
T_\tau=A_\tau\sin\Theta_\tau
\]

or the exact equivalent form derived from the Fourier-Leray tensor, where

\[
\Theta_\tau
=
\sigma_{\tau p}\phi_p
+\sigma_{\tau q}\phi_q
+\sigma_{\tau k}\phi_k
+\alpha_\tau.
\]

Do not assume the signs/offsets; derive them from the exact coefficient convention.

For maximal outward transfer each channel requests a phase target such as

\[
\Theta_\tau=\pi/2 \pmod{2\pi}
\]

or the corresponding sign-dependent target.

### Required artifact

Create an exact finite object containing:

```text
modes
complex/helical polarization slots
active triads
exact interaction coefficients
phase-incidence row for each active channel
target phase for outward saturation
amplitude prefactor
```

Suggested file:

```text
reproduction/checks/check_ns_p2_phase_holonomy.py
```

### Falsification question

For a declared finite dyadic network, is there a phase assignment satisfying every outward-saturation equation simultaneously?

```text
SAT   -> naive network-frustration claim is REFUTED for that network
UNSAT -> extract a minimal exact holonomy/conflict cycle
```

Use exact rational/integer incidence plus exact multiples of `pi/2` where possible. Do not infer UNSAT from numerical optimization alone.

---

# Work package FW-2 — search for the smallest genuine overlapping-triad conflict

Start at the smallest cutoff/network in which at least two distinct complex triads share one or more complex mode phases.

Required tests:

1. two overlapping triads;
2. three-triad loop;
3. four-triad loop;
4. one network crossing one dyadic boundary;
5. one network crossing two adjacent dyadic boundaries.

For every conflict, record:

```text
exact wavevectors
polarization/helicity choices
exact coupling coefficients
phase-incidence equations
minimal inconsistent subset
whether the conflict survives symmetry reduction
whether the conflict is a true complex-phase obstruction or only a real-coordinate artifact
```

**Failure is useful:** if all tested networks are phase-satisfiable, record a constructive SAT assignment and sharpen/refute the current conjecture.

---

# Work package FW-3 — convert holonomy inconsistency into a quantitative phase deficit

An UNSAT incidence system is not enough. Need a lower bound on how far at least one channel must be from its maximizing phase.

Suppose a minimal cycle contains `m` channels and the sum of requested phase increments around the cycle differs from the compatible value by a nonzero angle `Delta` modulo `2pi`.

Prove an exact geometric statement of the form

\[
\max_{\tau\in C}
\operatorname{dist}_{\mathbb T}(\Theta_\tau,\Theta_\tau^*)
\ge
\frac{\operatorname{dist}_{\mathbb T}(\Delta,0)}{m}.
\]

Then translate phase distance to transfer loss. If transfer is proportional to `sin Theta`, derive the exact inequality rather than guessing it, e.g. a bound of the schematic form

\[
|T_\tau|
\le
A_\tau(1-\epsilon_C).
\]

The value of `epsilon_C` may depend on cycle length/geometry initially.

### Goal

Produce the first genuine **complex-network frustration tax**.

### Do not do

Do not reuse the four-real-monomial N=1 tax as if it already proves this complex-network result.

---

# Work package FW-4 — frustration-or-amplitude-cut lemma

Even with a phase deficit, the frustrated edge may carry negligible amplitude. Build the dichotomy explicitly.

For a conflict cycle `C`, let

\[
a_\tau=|\text{amplitude prefactor of triad }\tau|.
\]

Pick a declared threshold `lambda_C` relative to a scale-local norm/flux budget.

Prove:

```text
Either some a_tau <= lambda_C       (amplitude cut)
Or all a_tau > lambda_C and phase holonomy forces a quantitative transfer deficit.
```

A generic algebraic form to seek is

\[
\sum_{\tau\in C}T_\tau
\le
\sum_{\tau\in C}a_\tau
-
\operatorname{Tax}_C(a,\Delta),
\]

where `Tax_C>0` whenever all required amplitudes exceed the declared threshold.

The tax must have an explicit scale dependence.

---

# Work package FW-5 — prove coverage of critical dyadic transfer

Existence of one conflict motif is insufficient. The proof needs a covering/packing statement for the actual set of triads contributing to outward transfer through a dyadic boundary.

Let `E_j` denote the transfer-active triad/channel set crossing the boundary near `N_j -> N_{j+1}`.

Need one of the following:

### Option A — conflict-cycle cover

Show that a fixed positive fraction, in the correct weighted sense, of critical outward transfer belongs to overlapping cycles with a quantitative frustration-or-cut tax.

### Option B — decomposition

Decompose

\[
E_j=E_j^{good}\cup E_j^{rem}
\]

such that:

- `E_j^{good}` receives a strict frustration/cut estimate;
- `E_j^{rem}` is bounded by a summable/geometrically decaying remainder.

### Option C — symmetry-orbit reduction

Use exact lattice/permutation/helical symmetries to reduce all boundary-crossing triads to finitely many shape classes, then prove each class either participates in a conflict structure or has a direct small coefficient/remainder bound.

### Immediate computational task

Enumerate exact boundary-crossing triads at small N, classify symmetry orbits and conflict-cycle incidence, then infer candidate all-n formulas. Finite enumeration is for theorem discovery/falsification; the final statement must be symbolic/all-scale.

Suggested artifacts:

```text
reproduction/checks/check_ns_p2_boundary_triad_orbits.py
reproduction/checks/check_ns_p2_holonomy_cycle_cover.py
```

---

# Work package FW-6 — time-window persistence / switching cost

Pointwise phase frustration may not directly control

\[
K_N=
\sup_t
\left(\int_t^{t+\tau_0}\|P_Nu(s)\|_{H^1}^{2p}ds\right)^{1/(2p)}.
\]

The network may switch which channels are phase-aligned over time. Therefore derive a **temporal coherence budget**.

Questions to attack:

1. Can phases switch between competing saturation patterns arbitrarily fast?
2. If they switch fast, what do the exact ODE/PDE phase equations force on amplitudes, gradients, or dissipation?
3. If they switch slowly, can a pointwise frustration tax be integrated over a positive fraction of the time window?
4. Can rapid switching itself be charged to viscosity/dissipation or to an amplitude cut?

The desired dichotomy is schematically:

```text
persistent alignment -> network holonomy tax
fast switching       -> dynamical/dissipative switching tax
small amplitudes      -> amplitude cut
```

This is likely necessary to connect phase geometry to the time-window quantity `K_N`.

---

# Work package FW-7 — aggregate to a dyadic recurrence

Only after FW-3 through FW-6 produce actual inequalities should the proof return to the scale ratio.

Target:

\[
R_{j+1}
\le
(1-\delta_j)R_j+eta_j.
\]

Need to prove one of:

### Strong form

\[
\delta_j\ge\delta_*>0,
\qquad
\beta_j\le B\rho^j,
\quad \rho<1.
\]

### Acceptable weaker form

A nonuniform sequence satisfying an explicit theorem such as

\[
\prod_{m=j_0}^{j}(1-\delta_m)\to0
\]

plus a compatible convolution/summability condition on `beta_j` sufficient to force `R_j->0`.

Do not require a uniform delta if the mathematics naturally yields a provably sufficient nonuniform condition.

---

# Work package FW-8 — recent nonlinear remainder

Earlier work already controls positive-lag Stokes memory and old Duhamel history. The residual `beta_j` should therefore be organized around the recent nonlinear term.

Try to express

```text
recent nonlinear contribution
  = conflict-covered main part
  + symmetry/geometry remainder
  + certified tail/reconstruction error
```

and attach explicit bounds to every remainder.

No naked `lesssim` is acceptable in the final theorem: every constant that affects `kappa`, `delta_j`, `B`, or `rho` must be declared or bounded.

---

# Work package FW-9 — finite certificate layer

Once a symbolic theorem candidate exists, implement fail-closed finite certificates using the P1 safe core.

Certificate should contain enough exact/rational information to verify:

```text
triad incidence / wavevector relations
polarization convention
coupling coefficient interval/exact value
phase-holonomy cycle
amplitude lower/upper thresholds
frustration/cut margin
remainder budget
scale recurrence margin
```

Return `HOLD` if any strict margin is lost.

Use exact rational/integer arithmetic whenever possible; interval enclosures only where analytic quantities cannot remain exact.

---

# Work package FW-10 — formalization

Formalize only stable lemmas, not speculative prose.

Good Coq/Rocq candidates:

1. finite phase-incidence cycle contradiction over a finite cyclic group or rational quarter-turn encoding;
2. cycle-distance pigeonhole lemma;
3. frustration-or-cut finite inequality;
4. finite cover aggregation;
5. nonuniform recurrence composition theorem.

Do not formalize the full PDE before the finite combinatorial/algebraic statement stabilizes.

---

# Work package FW-11 — red-team requirements

Every candidate theorem must be actively attacked before promotion.

Search for actual NSE/Fourier configurations that evade it:

```text
single helical-sign families
Beltrami-like/aligned states
sparse triad trees with no cycles
phase-satisfiable transfer networks
amplitude concentration on cycle-free channels
rapidly switching phase assignments
near-degenerate coupling coefficients
boundary interactions that avoid the known homothetic motif
```

A matching counterexample means `REFUTED` and the statement must be repaired. Failure to find a counterexample is not proof.

---

# Work package FW-12 — adapter audit after recurrence is proved

After a constructive recurrence is actually established:

1. verify exact `P_N`, `Lambda_N`, `N_j`, `tau_0`, H1 norm convention;
2. propagate EPSC/validated path error into `K_N` with the already derived lift;
3. compose the recurrence exactly to prove `R_j->0`;
4. locate a finite `j*` where the finite-observation gate passes;
5. audit every external theorem hypothesis/constant;
6. close regularity on arbitrary finite `[0,T]`;
7. only then invoke global continuation for arbitrary finite T.

---

# AI execution contract

Any AI continuing this work must follow these rules.

## Mathematical honesty

```text
counterexample before REFUTED
proof before DERIVED/PASS
no counterexample + no proof -> OPEN/HOLD
equivalence is not refutation
finite computation is not all-N theorem
CI proves the encoded statement only
```

## Research behavior

- Prefer the smallest load-bearing lemma.
- Use actual NSE Fourier/Leray coefficients, not an abstract energy budget, when the claim is NSE-specific.
- Translate to a finite exact object first; use continuum only through an explicit adapter after the finite theorem.
- Do not abandon a proposal merely because it is difficult or equivalent to the final target.
- Do not rename regularity and count the rename as progress.
- Do not merge Clay-sensitive claim changes while governance is HOLD.

## Git behavior

For every substantive result:

```text
branch
-> exact checker/theorem document
-> claim boundary
-> governance ACK
-> CI
-> PR
-> merge SHA
-> Toledo provenance/status pin
```

Do not record a moving branch SHA in Toledo as final provenance.

---

# Definition of meaningful next progress

The next session is high-value if it achieves at least one of:

1. actual complex phase-holonomy SAT counterexample that refutes naive network frustration;
2. minimal exact UNSAT overlapping-triad cycle;
3. quantitative complex-network phase deficit;
4. exact frustration-or-amplitude-cut lemma;
5. all-scale symbolic cycle-cover/decomposition theorem;
6. temporal switching-cost theorem;
7. a proved scale recurrence with sufficient decay;
8. a counterexample that forces a sharper replacement target.

The highest-priority next target is:

\[
\boxed{
\text{overlapping complex triad phase incidence}
\Longrightarrow?
\text{quantitative frustration-or-cut}
}
\]

Attack this before spending time on larger fixed-N simulations or additional criterion reformulations.
