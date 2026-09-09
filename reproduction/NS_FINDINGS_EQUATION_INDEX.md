# Navier--Stokes Readout Program: Findings and Equation Index

## Purpose

This file is the master index for the current finite Navier--Stokes / Readout / IDM development line in this repository.

It does not replace the theorem notes or executable checkers. It records where each equation or finding lives, what has been derived, what is only finite-diagnostic, and what remains open.

---

## A. Exact finite NS retained-shell lineage

### A1. Finite projected Navier--Stokes

\[
\partial_t \widehat u_k
=
-\widehat{\mathbb P(u\cdot\nabla u)}_k
-\nu |k|^2\widehat u_k.
\]

Source: `NS_RETAINED_EXACT.md`  
Checker: `checks/check_volume6_ns_exact.py`

### A2. Exact shell energy

\[
I_j
=
\frac12\sum_{|k|^2=q_j}|\widehat u_k|^2.
\]

### A3. Exact viscous operator

\[
\boxed{
L_\nu
=
\operatorname{diag}(2\nu q_1,\ldots,2\nu q_m).
}
\]

### A4. Exact nonlinear tape

\[
\eta_j^{NS}
=
-\Re\sum_{k\in K_j}
\overline{\widehat u_k}\cdot
\widehat{\mathbb P(u\cdot\nabla u)}_k.
\]

### A5. Exact finite retained identity

\[
\boxed{
\dot I+L_\nu I=\eta^{NS}.
}
\]

Status: derived finite Galerkin identity; numerically checked to roundoff in the declared benchmark.

---

## B. Shell-state sufficiency obstruction

### B1. Autonomy condition that would be required

\[
I(u)=I(v)
\Longrightarrow
\eta^{NS}(u)=\eta^{NS}(v).
\]

### B2. Finite counterexample

\[
\boxed{
I(u)=I(v)
\quad\text{but}\quad
\eta^{NS}(u)\neq\eta^{NS}(v).
}
\]

Therefore, on the tested finite admissible state class,

\[
\boxed{
\nexists\Gamma
\text{ with }
\eta^{NS}(u)=\Gamma(I(u))
\text{ globally on that class.}
}
\]

Source: `NS_RETAINED_SUFFICIENCY.md`  
Checker: `checks/check_volume6_ns_readout.py`

Claim boundary: this rules out an exact global memoryless shell-energy closure on the tested finite class; it does not rule out approximate, stochastic, history-conditioned, task-conditioned, or richer-state models.

---

## C. Exact minimal all-future readout state

### C1. Future-shell equivalence

\[
\boxed{
x\sim_I y
\iff
I(\Phi_t x)=I(\Phi_t y)
\quad\forall t\ge0.
}
\]

### C2. Minimal quotient

\[
\boxed{
\mathcal Q_{\min}^{NS}=X_M/\!\sim_I.
}
\]

### C3. Exact quotient evolution

\[
\boxed{
q_{\min}\circ\Phi_t
=
\Phi_t^\sharp\circ q_{\min}.
}
\]

### C4. Readout jet

\[
\boxed{
J_0=I,
\qquad
J_{r+1}=\mathcal L_{F_M}J_r.
}
\]

### C5. First jet level

\[
\boxed{
J_1=-L_\nu I+\eta^{NS}.
}
\]

### C6. Finite-jet existence at fixed Galerkin resolution

There exists finite \(R_M^\star\) such that a finite jet has the same fibers as the all-future quotient.

Source: `NS_MINIMAL_DYNAMIC_READOUT.md`  
Checker for triad/translation lineage: `checks/check_volume6_ns_xi_min.py`

Claim boundary: existence does not imply a small or computationally cheap quotient.

---

## D. Observability, redundancy, and compression gate

### D1. Exact interacting triad

\[
\boxed{R_{\rm triad}^\star=1.}
\]

with exact real reduced system

\[
\dot x=\frac35r-2\nu x,
\]

\[
\dot y=-\frac85r-4\nu y,
\]

\[
\dot z=r-10\nu z,
\]

\[
\dot r=\frac3{10}yz-\frac45xz+\frac12xy-8\nu r.
\]

and exact state reduction

\[
\boxed{6\to4.}
\]

### D2. First full 3D cube

\[
\boxed{d_M=52.}
\]

### D3. Shell-jet rank bound

\[
\boxed{
\operatorname{rank}D(J_0,\ldots,J_R)
\le\min(3+2R,49).
}
\]

### D4. Modular finite witness

For checked \(0\le R\le50\),

\[
\boxed{
\operatorname{rank}_{\mathbb F_p}D(J_0,\ldots,J_R)
=
\min(3+2R,49).
}
\]

### D5. Local saturation order

\[
\boxed{R_{M,\mathrm{rank}}=23.}
\]

### D6. Generic local quotient dimension

\[
\boxed{
\dim\mathcal Q_{\min,\mathrm{loc}}^{NS}=49.
}
\]

Thus

\[
\boxed{
49/52\approx0.9423,
}
\]

so the all-future exact shell quotient is not a strong compression in this truncation.

### D7. Global order status

\[
\boxed{R_M^\star\ge23}
\]

is supported by the local rank result; equality \(R_M^\star=23\) remains open without a global ideal/fiber proof.

Source: `NS_OBSERVABILITY_RANK.md`  
Checker: `checks/check_volume6_ns_observability.py`

---

## E. Exact NS triad reader

For ordered triad \(p+q=k\),

\[
\boxed{
\Theta_{kpq}(u)
=
-\Re\left[
\overline{\widehat u_k}\cdot i(q\cdot\widehat u_p)\widehat u_q
\right].
}
\]

and shell transfer

\[
\boxed{
\eta_j^{NS}
=
\sum_{k\in K_j}\sum_{p+q=k}\Theta_{kpq}.
}
\]

Spatial translation gauge:

\[
(T_a\widehat u)_k=e^{ik\cdot a}\widehat u_k,
\]

with

\[
\Theta_{kpq}(T_a u)=\Theta_{kpq}(u).
\]

Source: `NS_MINIMAL_DYNAMIC_READOUT.md`  
Checker: `checks/check_volume6_ns_xi_min.py`

---

## F. Task-conditioned retained computation

### F1. One-step dependency pullback

\[
\boxed{
D(S)
=
S\cup\{p,q:p+q=k,\ k\in S\}.
}
\]

### F2. Euler finite-horizon relevance

\[
\boxed{
S_t=D(S_{t+1}).
}
\]

Task exactness for the same finite recurrence:

\[
\boxed{
Q_R^{\rm retained}=Q_R^{\rm full}
}
\]

up to arithmetic roundoff when every required dependency is retained.

Source: `NS_RETAINED_FOLD_COMPILER.md`  
Checker: `checks/check_volume6_ns_retained_fold.py`

### F3. Classical RK4 pullback

\[
\boxed{K_4=T,}
\]

\[
\boxed{K_3=D(K_4),}
\]

\[
\boxed{K_2=D(K_3),}
\]

\[
\boxed{K_1=D(K_2),}
\]

\[
\boxed{S_{\rm in}=D(K_1).}
\]

Source: `NS_RETAINED_FOLD_RK4.md`  
Checker: `checks/check_volume6_ns_retained_fold_rk4.py`

### F4. Fail-closed measured cost gate

Retained execution is admissible only when its calibration beats the full backend by the declared margin; otherwise use full RK4.

Status: implementation policy / finite diagnostic, not a mathematical speed-up theorem.

---

## G. Exact physical readers

### G1. Point velocity

\[
\boxed{
u(x^\star,T)=\sum_{k\in K_M}\widehat u_k(T)e^{ik\cdot x^\star}.}
\]

Therefore exact terminal support is dense:

\[
\boxed{S_Q=K_M.}
\]

Consequence: no terminal-support compression.

API implementation: IDM `ns_retained_physical`.

### G2. Plane-average velocity

\[
\boxed{
\bar u(x,T)
=
\frac1{(2\pi)^2}\int\!\!\int u(x,y,z,T)\,dy\,dz
=
\sum_{k\in A_x}\widehat u_k(T)e^{ik_xx}.
}
\]

with

\[
A_x=\{(a,0,0):1\le|a|\le K\}.
\]

Exact saturation theorem:

\[
\boxed{D(A_x)=K_M.}
\]

Exact structural RK4 cost:

\[
\boxed{C_R=(4H-1)C+C_A.}
\]

Exact structural gain:

\[
\boxed{
G_H=\frac{4HC}{(4H-1)C+C_A}
<\frac{4H}{4H-1}.
}
\]

Incompressibility also gives

\[
\boxed{\bar u_x(x,T)=0}
\]

for the zero-mean plane-normal component in the declared finite state.

Source: `NS_PHYSICAL_PLANE_AVERAGE.md`  
Checker: `checks/check_volume6_ns_plane_average.py`  
API: IDM `ns_retained_plane_average`.

### G3. Real harmonic probe

\[
\boxed{
Q_{k_0,\phi}(T)
=
\frac1{(2\pi)^3}\int u(x,T)\cos(k_0\cdot x+\phi)\,dx.
}
\]

Fourier identity:

\[
\boxed{
Q_{k_0,\phi}(T)
=
\frac12\left(
\widehat u_{-k_0}e^{i\phi}
+
\widehat u_{k_0}e^{-i\phi}
\right).
}
\]

Terminal support:

\[
\boxed{S_Q=\{k_0,-k_0\}.}
\]

For \(K=3\), \(k_0=(3,3,3)\), the tested one-step RK4 cone is

\[
\boxed{|K_1|,|K_2|,|K_3|,|K_4|=342,342,126,2.}
\]

and the direct structural work reduction is approximately

\[
\boxed{1.658\times.}
\]

Source: `NS_PHYSICAL_HARMONIC_PROBE.md`  
Checker: `checks/check_volume6_ns_harmonic_probe.py`  
API: IDM `ns_retained_harmonic_probe`.

---

## H. Readout Design as Computational Acceleration

For each physical reader \(Q\), define terminal support

\[
S_Q=\operatorname{supp}\widehat Q.
\]

Let \(K_{n,s}(Q)\) be the exact RK4 stage sets obtained by horizon-wise backward pullback.

Define retained structural work

\[
\boxed{
C_H(Q)
=
\sum_{n=0}^{H-1}\sum_{s=1}^{4}
\sum_{k\in K_{n,s}(Q)}|\mathcal T_k|.
}
\]

For a declared task \(\mathcal T\) with admissible physical-reader family \(\mathscr Q_{\rm adm}(\mathcal T)\), define

\[
\boxed{
Q^\star
\in
\operatorname*{arg\,min}_{Q\in\mathscr Q_{\rm adm}(\mathcal T)}
C_H(Q).
}
\]

Equivalently,

\[
\boxed{
Q^\star
\in
\operatorname*{arg\,max}_{Q\in\mathscr Q_{\rm adm}(\mathcal T)}
G_H(Q).
}
\]

Compact notation:

\[
\boxed{
Q^\star
=
\operatorname*{arg\,min}_{Q\in\mathscr Q_{\rm adm}(\mathcal T)}
C\!\left(D_{\rm RK4}^{(H)}(\operatorname{supp}\widehat Q)\right).
}
\]

Source: `NS_READOUT_DESIGN_ACCELERATION.md`.

Status: canonical optimization target for the current finite program; existence/uniqueness/global optimality are not claimed.

---

## I. Toledo retained-response adapter

Registered Toledo proposal law:

\[
\boxed{
\tau_R\dot I_R+L_RI_R=S_R+\eta_R.
}
\]

For the unforced finite exact shell adapter,

\[
\boxed{
I_R=I,
\qquad
L_R=\tau_RL_\nu,
\qquad
S_R=0,
\qquad
\eta_R=\tau_R\eta^{NS}.
}
\]

Proposal identifiers:

`PROP-URCF-01` / `EQ-URCF-TURB-004`.

The readout-acceleration compiler is a computational adapter built downstream of this finite NS lineage; it does not upgrade the Toledo proposal's registered theorem tier.

---

## J. Current boundary

Established in the finite program:

- exact shell identity;
- exact shell-sufficiency obstruction;
- canonical all-future quotient definition and finite-jet existence at fixed Galerkin resolution;
- exact interacting-triad reduction;
- local 52-to-49 observability/compression result for the first full cube;
- exact task-conditioned Euler/RK4 slicing for declared finite recurrences;
- exact physical reader identities for point, plane-average, and harmonic readers;
- plane-average saturation theorem;
- finite harmonic-probe cone and optimized-kernel diagnostics;
- public IDM solver/API surfaces for retained RK4 and physical readers.

Still open / not claimed:

\[
\boxed{R_M^\star=23}
\]

globally for the 52D cube;

\[
\boxed{
\dim\mathcal Q_{\min}^{NS}\ll d_M
}
\]

for general resolutions;

\[
\boxed{
C(\mathcal Q_{\min}^{NS})\ll C(NS_{3D})
}
\]

as a general all-future exact solver theorem;

global optimality of any physical reader;

continuum exact/task-exact acceleration independent of discretization;

and any resolution of the Navier--Stokes Millennium Prize problem.
