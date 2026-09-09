# Exact NS → Retained-Shell Lineage


after projection to a finite divergence-free Fourier set,

\[
\partial_t \widehat u_k
=
-\widehat{\mathbb P(u\cdot\nabla u)}_k
-\nu |k|^2\widehat u_k,
\qquad k\in K_M.
\]

For each exact shell

\[
K_j=\{k\in K_M:|k|^2=q_j\},
\]

define

\[
I_j(t)
=
\frac12\sum_{k\in K_j}|\widehat u_k(t)|^2.
\]

Differentiate directly:

\[
\dot I_j
=
\Re\sum_{k\in K_j}
\overline{\widehat u_k}\cdot\partial_t\widehat u_k.
\]

Hence

\[
\dot I_j=T_j-D_j,
\]

where

\[
T_j
=
-\Re\sum_{k\in K_j}
\overline{\widehat u_k}\cdot
\widehat{\mathbb P(u\cdot\nabla u)}_k,
\]

and, because \(|k|^2=q_j\) on one shell,

\[
D_j
=
\nu q_j\sum_{k\in K_j}|\widehat u_k|^2
=
2\nu q_j I_j.
\]

Define only the operator already forced by the viscous term,

\[
L_\nu
=
\operatorname{diag}(2\nu q_1,\ldots,2\nu q_m),
\]

and read the nonlinear tape directly,

\[
\eta_j^{\mathrm{NS}}:=T_j.
\]

Therefore

\[
\boxed{
\dot I+L_\nu I=\eta^{\mathrm{NS}}
}
\]

for the unforced finite Galerkin system.

No closure

\[
\eta^{\mathrm{NS}}=\Gamma(I)
\]

is assumed.

For the deterministic test

\[
N=16,
\qquad
\nu=0.005,
\qquad
\Delta t=0.0025,
\qquad
0\le t\le0.5,
\]

with Taylor-Green initial data and 2/3 dealiasing,

\[
\max_{t,j}
\left|
\dot I_j+2\nu q_jI_j-\eta_j^{\mathrm{NS}}
\right|
=
2.6020852139652106\times10^{-18},
\]

\[
\max_{t,j}
\left|
D_j-2\nu q_jI_j
\right|
=
4.336808689942018\times10^{-19},
\]

\[
\max_t
\left|
\sum_j\eta_j^{\mathrm{NS}}
\right|
=
3.535196447299567\times10^{-18},
\]

\[
\max_{t,k}|k\cdot\widehat u_k|
=
8.673617379884035\times10^{-19}.
\]

The retained energy changes from

\[
E(0)=0.125
\]

to

\[
E(0.5)=0.12312302602250529.
\]

At \(t=0.5\), the leading transfer is

\[
\eta^{\mathrm{NS}}_{q=3}
=-7.3934251189\times10^{-3},
\]

while

\[
\eta^{\mathrm{NS}}_{q=8}
=+6.9843956551\times10^{-3},
\]

so the nonlinear term removes retained energy from the low shell and places it into higher shells while

\[
\sum_j\eta_j^{\mathrm{NS}}\approx0.
\]

## Current status of the closure question

The historical next step after deriving this exact shell identity was to test whether the nonlinear tape could factor through shell energy alone,

\[
\eta^{\mathrm{NS}}(u)=\Gamma(I(u)).
\]

That autonomy test has now been answered negatively on the tested finite admissible state class. `NS_RETAINED_SUFFICIENCY.md` constructs states satisfying

\[
I(u)=I(v)
\]

within machine tolerance while

\[
\eta^{\mathrm{NS}}(u)\neq\eta^{\mathrm{NS}}(v).
\]

Therefore the current program does **not** treat

\[
\widehat\eta(I)
\]

as the canonical unresolved target.

The exact all-future state-sufficiency target is instead

\[
\boxed{
\mathcal Q_{\min}^{NS}
=
X_M/\!\sim_I,
\qquad
x\sim_I y
\iff
I(\Phi_t x)=I(\Phi_t y)
\ \forall t\ge0,
}
\]

with finite readout-jet realization discussed in `NS_MINIMAL_DYNAMIC_READOUT.md` and local observability/compression results in `NS_OBSERVABILITY_RANK.md`.

For acceleration, the active branch is task-conditioned finite-horizon retained computation:

\[
\boxed{
Q
\longrightarrow
\text{terminal support}
\longrightarrow
\text{exact NS triad pullback}
\longrightarrow
\text{retained Euler/RK4 computation}
\longrightarrow
Q.
}
\]

That branch is documented in `NS_RETAINED_FOLD_COMPILER.md`, `NS_RETAINED_FOLD_RK4.md`, `NS_PHYSICAL_PLANE_AVERAGE.md`, `NS_PHYSICAL_HARMONIC_PROBE.md`, and `NS_READOUT_DESIGN_ACCELERATION.md`.

Thus the current lineage is

\[
\boxed{
\text{exact retained identity}
\to
\text{shell-sufficiency obstruction}
\to
\text{minimal exact quotient / observability}
\to
\text{task-horizon retained computation}
\to
\text{readout-design cost optimization}.
}
\]
