# Readout–Navier–Stokes Discrete-Native Epsilon-Completion

**Status:** finite numerical diagnostic  
**[SimulatedData] Simulation=Yes**  
**Executed:** 2026-09-10 in the ChatGPT Python/NumPy runtime used for the recorded run.

This is the first Navier-Stokes application record of the cross-repository **Discrete Epsilon-Completion Programme**.

## Cross-repository ownership

- General mathematics/API: `morrocwi/information-discrete-math`, `idm/ns_epsilon.py` and `docs/DISCRETE_EPSILON_COMPLETION.md`.
- Equation/proposal provenance: `morrocwi/toledo`, `registry/proposals/discrete_epsilon_completion.json`.
- This file/repository: NS-specific independent reproduction, numerical evidence, and claim boundary.
- `morrocwi/readout_genesis`: interpretation/application map only; this finite result does not become a root/ontological theorem.

## Toledo proposal lineage

- `PROP-EPSC-01` — Nested Readout Consistency Defect
  \[
  \delta_K=\|R_Kx_{K+1}-x_K\|.
  \]
- `PROP-EPSC-02` — NS Fourier boundary-energy diagnostic
  \[
  E_{\partial K}=\frac12\sum_{\|k\|_\infty=K}|\widehat u_k|^2.
  \]
- `PROP-EPSC-03` — fail-closed epsilon-completion gate.
- `PROP-EPSC-04` — **OPEN** computable omitted-information/tail certificate.

The codes above are proposal identifiers, not canonical verified Toledo theorem codes.

## Question

Can a Navier-Stokes computation be run directly on discrete Fourier records, without treating a spatial continuum grid as the computational primitive, and can nested finite refinement supply an operational stopping diagnostic?

## Discrete-native state and evolution

The production state of the reproduction checker is only

\[
\{(k,\widehat u_k):k\in K_M\},\qquad k\in\mathbb Z^3,
\]

with

\[
k\cdot\widehat u_k=0,
\qquad
\widehat u_{-k}=\overline{\widehat u_k}.
\]

The finite Galerkin vector field is

\[
\frac{d\widehat u_k}{dt}
=-\nu|k|^2\widehat u_k
-iP_k\sum_{p+q=k}(q\cdot\widehat u_p)\widehat u_q.
\]

The production route never constructs x/y/z coordinates and never calls an FFT. A padded FFT evaluator is used only as an independently written finite-algebra comparator.

## Operational diagnostic

For increasing cutoffs K, compare the shared finite state

\[
\Delta_K=\|u^K(T)|_{K-1}-u^{K-1}(T)\|_2
\]

and measure the outermost retained-shell energy

\[
E_{\partial K}=\frac12\sum_{\|k\|_\infty=K}|\widehat u_k(T)|^2.
\]

The recorded operational gate required

\[
\Delta_K\le10^{-6},\qquad E_{\partial K}\le10^{-8}
\]

at two consecutive cutoffs. **Passing this gate is finite-diagnostic only.** Under the general fail-closed protocol, continuum/infinite-object completion remains `HOLD` because no proved `beta_K` from `PROP-EPSC-04` was supplied.

## Test A — analytic shear-decay sanity check

Initial Fourier records represent `u=(0,sin x,0)`. The nonlinear term is exactly zero and the active coefficients decay as `exp(-nu t)`.

- max nonlinear RHS at t=0: **0.000e+00**
- max error against exact decay after T=1: **3.886e-16**
- 1e-12 gate: **PASS**

## Test B — independent finite-algebra gate

At K=2 a smooth deterministic divergence-free mode state was evaluated by the direct triad code and by an independent padded pseudo-spectral FFT evaluator.

- modes: **124**
- ordered triads: **6486**
- max RHS discrepancy: **1.041e-16**
- max discrepancy after one RK4 step: **8.674e-19**
- 1e-12 gate: **PASS**

This supports agreement of two finite implementations on the tested state. It is not a proof for every admissible state.

## Test C — nested-cutoff Taylor-Green diagnostic

Parameters: `nu=0.01`, `dt=0.005`, `T=0.05`.

| K | modes | ordered triads | boundary energy | overlap L2 | overlap max | max k·u | operational gate |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 1 | 26 | 264 | 1.246e-01 | — | — | 0.000e+00 | — |
| 2 | 124 | 6,486 | 1.939e-05 | 3.891e-05 | 9.728e-06 | 0.000e+00 | — |
| 3 | 342 | 49,626 | 5.691e-09 | 1.140e-06 | 2.352e-07 | 4.337e-19 | — |
| **4** | 728 | 224,796 | **2.089e-12** | **3.551e-08** | 4.696e-09 | 5.082e-21 | **PASS** |
| **5** | 1,330 | 749,580 | **1.031e-15** | **7.741e-10** | 1.124e-10 | 4.337e-19 | **PASS** |

K=4 is the first passing cutoff and K=5 supplies the required second consecutive pass for this operational finite diagnostic.

## What this establishes

The executed evidence supports only these finite statements:

1. The checker can evolve the declared finite Fourier-Galerkin system directly on integer modes and triads without using a spatial grid in its production path.
2. The direct triad RHS agrees with an independent padded-FFT finite evaluator on the tested state to roundoff-scale error.
3. For the short declared Taylor-Green run, the nested finite state satisfies the declared repeated-pass diagnostic at K=4 and K=5.

## What remains open

The result does **not** establish that K=5 contains literally all continuum information. The missing mathematical object is a useful proved computable bound

\[
\|(I-P_K)u(T)\|\le\beta_K(\mathcal R_K),
\qquad \beta_K\to0,
\]

from finite records and stated assumptions. This is `PROP-EPSC-04` and remains **Open**.

Accordingly,

\[
\boxed{\text{operational finite diagnostic: PASS}}
\]

but

\[
\boxed{\text{continuum / infinite-object epsilon certificate: HOLD}}.
\]

This distinction is mandatory.

## Reproduction

```bash
python3 reproduction/checks/check_discrete_epsilon_completion.py \
  --json discrete_epsilon_completion_v01.json
```

Requires NumPy. The recorded values are frozen in `reproduction/results/discrete_epsilon_completion_v01.json`. Runtime values are machine-dependent and are not used as speedup claims.
