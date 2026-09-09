# NS Retained Fold Compiler — RK4 Extension

## Status

This note extends `NS_RETAINED_FOLD_COMPILER.md` from explicit Euler to the classical four-stage RK4 recurrence on one fixed finite Fourier-Galerkin Navier-Stokes mode cube.

It is an IDM-lineage computation:

\[
\text{terminal task}
\xrightarrow{\text{RRP pullback}}
\text{stage relevance}
\xrightarrow{\text{RCF}}
\text{retained triad execution}
\xrightarrow{\text{break-even guard}}
\text{retained or full FFT backend}.
\]

No learned closure is inserted.

This note does **not** claim a continuum Navier-Stokes regularity theorem, an exact-in-time flow solver, an all-future reduction, or a universal speed theorem.

---

## 1. Finite vector field

On a fixed symmetric Fourier cube \(K_M\), write the finite projected Galerkin system as

\[
\dot u = F_M(u),
\]

with

\[
F_{M,k}(u)
=
-iP_k\sum_{p+q=k}(q\cdot u_p)u_q
-\nu |k|^2u_k.
\tag{1}
\]

The ordered triads \(p+q=k\) are the local causal records.

Define the exact one-layer dependency expansion

\[
\boxed{
D(S)
=
S\cup\{p,q:\ p+q=k,\ k\in S\}.
}
\tag{2}
\]

---

## 2. RK4 recurrence

For one timestep \(h\),

\[
k_1=F_M(u_n),
\]

\[
k_2=F_M\!\left(u_n+\frac h2k_1\right),
\]

\[
k_3=F_M\!\left(u_n+\frac h2k_2\right),
\]

\[
k_4=F_M(u_n+hk_3),
\]

\[
u_{n+1}
=u_n+\frac h6(k_1+2k_2+2k_3+k_4).
\tag{3}
\]

Let the terminal task expose only modes in \(T\) at the end of the step.

Pull relevance backward through the RK4 stage graph:

\[
\boxed{
K_4=T,
\qquad
K_3=D(K_4),
\qquad
K_2=D(K_3),
\qquad
K_1=D(K_2),
\qquad
S_{\rm in}=D(K_1).
}
\tag{4}
\]

This is the RK4-specific Retained Readout Pullback.

---

## 3. Stage-conditioned task-exactness theorem

Assume retained and full states agree on \(S_{\rm in}\) at the start of the step.

Because every output of \(F_M\) on a set \(S\) depends only on modes in \(D(S)\):

1. equality on \(S_{\rm in}=D(K_1)\) implies equality of \(k_1\) on \(K_1\);
2. equality of the required input combination then implies equality of \(k_2\) on \(K_2\);
3. the same argument gives equality of \(k_3\) on \(K_3\);
4. then equality of \(k_4\) holds on \(K_4=T\);
5. equation (3) therefore gives the same terminal update on \(T\).

Hence

\[
\boxed{
\left.u_{n+1}^{\rm retained}\right|_T
=
\left.u_{n+1}^{\rm full}\right|_T.
}
\tag{5}
\]

For a horizon of \(R\) RK4 steps, apply (4) recursively backward through time. Induction on the time-step DAG gives

\[
\boxed{
Q_R^{\rm retained}=Q_R^{\rm full}
}
\tag{6}
\]

for the same finite mode cube, viscosity, timestep, RK4 algebra, triad convention and admitted backend arithmetic.

This is exact task slicing of the declared finite recurrence. It is not exactness with respect to the continuum PDE.

---

## 4. Retained Closure Fusion

For any requested output set \(S\), the retained arithmetic batches

\[
\mathcal T_S
=
\{(k,p,q):k\in S,\ p+q=k\}
\]

and evaluates the ordered triad contributions

\[
i(q\cdot u_p)u_q
\]

in one vectorized retained batch before reduction by output mode.

This is the NS realization of IDM Retained Closure Fusion.

---

## 5. FFT admission gate

The retained direct-triad RHS and pseudo-spectral FFT RHS are checked on the same finite mode cube before the FFT backend is admitted:

\[
\boxed{
\max_k
\|F_{M,k}^{\rm triad}(u)-F_{M,k}^{\rm FFT}(u)\|
\le10^{-12}.
}
\tag{7}
\]

In the executed checks the observed backend defects were approximately

\[
2.08\times10^{-17}\quad(K=2),
\]

and

\[
1.40\times10^{-17}\quad(K=3).
\]

These are finite floating-point diagnostics.

---

## 6. Two-level break-even guard

The compiler first chooses a backend separately for each RK stage:

\[
B_{n,s}
=\arg\min\{C_{\rm fused}(S_{n,s}),C_{\rm FFT}(K_M)\}.
\tag{8}
\]

A second fail-closed gate then compares the complete hybrid rollout against complete full RK4.

The retained rollout is enabled only if

\[
\boxed{
C_{\rm hybrid}^{\rm calibration}
\le0.95\,C_{\rm fullRK4}^{\rm calibration}.
}
\tag{9}
\]

Otherwise the compiled plan is

\[
\boxed{\texttt{full_rk4}.}
\]

Thus an unconvincing or negative speed result does not become an acceleration claim.

---

## 7. Finite reproduced diagnostic matrix

Executed target:

\[
Q=\widehat u_{(1,0,0)}(R\Delta t),
\qquad
\Delta t=0.0025,
\qquad
\nu=0.005.
\]

### Cube K=2

\[
|K_M|=124.
\]

Latest local reference run of the same algorithmic implementation gave:

| RK4 horizon | selected plan | terminal absolute error | observed full/selected |
|---:|---|---:|---:|
| 1 | hybrid retained | \(0\) | about \(1.9\times\) |
| 2 | hybrid retained | \(1.73\times10^{-18}\) | about \(1.6\times\) |
| 3 | hybrid retained | \(1.73\times10^{-18}\) | about \(1.7\times\) |

### Cube K=3

\[
|K_M|=342.
\]

| RK4 horizon | selected plan in the reference run | terminal absolute error | observed full/selected |
|---:|---|---:|---:|
| 1 | hybrid retained | \(0\) | about \(1.3\times\) |
| 2 | full RK4 fallback | \(0\) | no retained speed claim |
| 3 | calibration-dependent hybrid/full boundary | \(0\) | approximately break-even |

Timings are environment-sensitive and are therefore `finite_diagnostic`, not theorem-level complexity claims.

The structural result is more stable: as horizon increases, the backward triad relevance cone saturates the full cube, so the available task-conditioned saving shrinks.

---

## 8. Relation to the earlier all-future quotient result

The earlier observability result showed that exact **all-future** shell readout on the first full 3D cube is generically close to full-state dimension.

The RK4 retained-fold result does not contradict that result. It changes the quantifier:

\[
\boxed{
\text{all future readouts}
\neq
\text{one declared task at one finite horizon}.
}
\]

The latter permits the causal cone to be sliced before it saturates.

Thus the current computational statement is

\[
\boxed{
\text{task-conditioned finite-horizon exact slicing can accelerate}
}
\]

on admitted finite cases, even when an all-future exact quotient is not strongly compressive.

---

## 9. Current boundary and next target

Established for the tested finite Fourier-Galerkin RK4 recurrence:

- exact stage-by-stage dependency pullback;
- terminal task agreement to the numerical backend gate;
- fused retained triad execution;
- stage-level retained/FFT switching;
- whole-rollout fail-closed fallback.

Still open:

1. multi-mode task sets;
2. physical-space point/force/flux readouts;
3. larger mode cubes and compiled/GPU backends;
4. a backend-independent work certificate;
5. continuous-time or adaptive-horizon readout guarantees;
6. characterization of task/horizon regions before causal-cone saturation.

The executable checker is

`reproduction/checks/check_volume6_ns_retained_fold_rk4.py`.
