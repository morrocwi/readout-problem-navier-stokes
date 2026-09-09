# NS Retained Fold Compiler

## Status

This note instantiates the information-discrete-math retained-fold lineage on a fixed finite Fourier-Galerkin Navier-Stokes recurrence.

It does **not** claim:

- a continuum Navier-Stokes regularity theorem;
- an exact-in-time Navier-Stokes flow solver;
- an all-future reduction;
- a universal speedup theorem.

The executable evidence is finite-diagnostic.

## 1. Lineage from IDM

The adapter uses the same computational roles already present in the IDM retained-fold architecture:

\[
\text{terminal relevance}
\rightarrow
\text{retained boundary}
\rightarrow
\text{forward fold}.
\]

For Navier-Stokes the local records are ordered Fourier triads

\[
p+q=k.
\]

The finite recurrence used in the prototype is explicit Euler on one fixed Galerkin cube:

\[
u_k^{n+1}
=
u_k^n
+
\Delta t
\left[
-iP_k\sum_{p+q=k}(q\cdot u_p^n)u_q^n
-\nu |k|^2u_k^n
\right].
\tag{1}
\]

No closure model is inserted.

## 2. Retained Readout Pullback for a terminal task

Let \(S_R\) be the set of Fourier modes explicitly named by the terminal task at horizon \(R\).

Define backward terminal relevance by

\[
\boxed{
S_t
=
S_{t+1}
\cup
\{p,q:\ p+q=k,\ k\in S_{t+1}\}.
}
\tag{2}
\]

This is the NS-specific Retained Readout Pullback.

Only distinctions in \(S_t\) are required at time layer \(t\).

## 3. Task-exact finite-horizon theorem

Suppose at time layer \(t\) the retained execution and the full execution agree on every mode in \(S_t\).

For any \(k\in S_{t+1}\), equation (1) depends only on

- \(u_k^t\);
- \(u_p^t,u_q^t\) for ordered pairs satisfying \(p+q=k\).

By construction all those modes lie in \(S_t\).

Therefore both executions compute the same \(u_k^{t+1}\).

Induction gives

\[
\boxed{
u_{R,\mathrm{retained}}|_{S_R}
=
u_{R,\mathrm{full}}|_{S_R}
}
\tag{3}
\]

for the same finite mode set, timestep, viscosity, triad ordering and explicit-Euler recurrence.

This is task exactness relative to the declared finite recurrence, not a continuum statement.

## 4. Retained Closure Fusion

Computing every relevant triad in a Python loop is structurally smaller but can still be slower than a vectorized FFT.

The NS adapter therefore fuses all ordered triad contributions for one requested output set into one batch:

\[
\boxed{
\mathcal T_{S}
=
\{(k,p,q): k\in S,\ p+q=k\}.
}
\tag{4}
\]

The batch evaluates

\[
i(q\cdot u_p)u_q
\]

for all retained ordered triads and reduces them by output mode \(k\).

This is the NS arithmetic realization of Retained Closure Fusion.

## 5. FFT admission gate

The full pseudo-spectral backend is not assumed to be equivalent to the direct triad recurrence.

Before it is admitted, the compiler checks one all-mode Euler step:

\[
\boxed{
\max_k
\left|
u_{k,\mathrm{direct}}^{1}
-
u_{k,\mathrm{FFT}}^{1}
\right|
\le \varepsilon_{\mathrm{backend}}.
}
\tag{5}
\]

Only after this gate passes may an FFT layer be used.

## 6. Break-even backend selection

For each time layer the compiler measures two hot structural implementations:

\[
C_{\mathrm{fused}}(S_{t+1}),
\qquad
C_{\mathrm{FFT}}(K_M).
\]

It chooses

\[
\boxed{
B_t
=
\arg\min
\{C_{\mathrm{fused}},C_{\mathrm{FFT}}\}.
}
\tag{6}
\]

This is a finite calibration, not a universal complexity theorem.

## 7. Reproduced finite results

Environment: current Python/NumPy runtime used by the executable check.

Task:

\[
Q=\widehat u_{(1,0,0)}(R\Delta t),
\qquad
\Delta t=10^{-3},
\qquad
\nu=10^{-2}.
\]

### Cube \(K=2\)

There are

\[
124
\]

nonzero Fourier modes and

\[
6486
\]

ordered retained triads.

Measured hot-plan results:

| horizon \(R\) | backward mode counts | selected backends | observed full-FFT / retained |
|---:|---|---|---:|
| 1 | \(99\to1\) | fused | \(25.13\times\) |
| 2 | \(124\to99\to1\) | fused, fused | \(3.00\times\) |
| 3 | \(124\to124\to99\to1\) | fused, fused, fused | \(2.07\times\) |
| 4 | \(124\to124\to124\to99\to1\) | fused ×4 | \(1.84\times\) |
| 5 | \(124\to124\to124\to124\to99\to1\) | fused ×5 | \(1.76\times\) |

The direct-triad/FFT backend gate was

\[
4.34\times10^{-19},
\]

and the terminal target difference was zero in every recorded case.

### Cube \(K=3\)

There are

\[
342
\]

nonzero Fourier modes and

\[
49626
\]

ordered triads.

| horizon \(R\) | backward mode counts | selected backends | observed full-FFT / retained |
|---:|---|---|---:|
| 1 | \(293\to1\) | fused | \(29.93\times\) |
| 2 | \(342\to293\to1\) | FFT, fused | \(1.89\times\) |
| 3 | \(342\to342\to293\to1\) | FFT, FFT, fused | \(1.45\times\) |

The backend equivalence gate was

\[
1.73\times10^{-18},
\]

and the terminal target difference was zero in every recorded case.

## 8. What this resolves

The previous all-future quotient result showed that a full future shell reader can force the retained state close to the full state.

The finite-horizon task compiler shows a different fact:

\[
\boxed{
\text{all-future exact compression can fail}
\quad\text{while}\quad
\text{task-conditioned finite-horizon exact slicing can still accelerate}.
}
\tag{7}
\]

The gain is largest before the backward relevance cone saturates the full mode cube.

## 9. Current boundary

Established on the tested finite recurrence:

\[
\boxed{
Q_R^{\mathrm{retained}}
=
Q_R^{\mathrm{full}}
}
\]

and measured hot-plan speedups \(>1\) in all recorded \(K=2\) and \(K=3\) cases above.

Still open:

1. replace explicit Euler with the repository's RK4 pseudo-spectral trajectory while preserving a formally correct stage-by-stage relevance pullback;
2. test multi-mode and physical-space task readouts;
3. scale to larger \(K\) and GPU/compiled backends;
4. derive a backend-independent cost certificate rather than a hot timing calibration;
5. determine the horizon/task regimes for which the relevance cone remains sub-full.

The next mathematical target is therefore

\[
\boxed{
\text{RK4 stage-conditioned retained relevance}
}
\]

rather than a new closure law.
