# Readout Design as Computational Acceleration

## Status

This note records the current computational target that follows from the exact shell, observability, retained-fold, plane-average, and harmonic-probe results.

It is a **design/optimization problem**, not a theorem that a globally optimal reader exists, is unique, or gives a universal speed-up.

---

## 1. Why the target changed

The all-future shell quotient is mathematically well-defined, but the first full 3D cube diagnostic gives

\[
\boxed{
\dim\mathcal Q_{\min,\mathrm{loc}}^{NS}=49,
\qquad d_M=52.
}
\]

Thus exact all-future shell preservation is not a strong compression in that truncation.

Task-conditioned finite-horizon computation changes the question from

\[
\text{"what state preserves every future shell readout?"}
\]

to

\[
\boxed{
\text{"what distinctions are required for this declared physical readout at this horizon?"}
}
\]

The finite Euler and RK4 retained-fold checkers establish that irrelevant branches of the finite computation graph can be omitted without introducing a learned closure.

---

## 2. Declared physical-reader family

Let

\[
\mathscr Q_{\rm phys}
\]

be a declared family of admissible physical readouts on the finite Fourier-Galerkin state.

For a linear physical reader \(Q\), let

\[
\boxed{
S_Q:=\operatorname{supp}\widehat Q\subseteq K_M
}
\]

be the Fourier modes directly read at the terminal time.

Examples already implemented are:

1. point velocity, for which
   \[
   S_Q=K_M;
   \]
2. plane-average velocity, for which
   \[
   S_Q=A_x=\{(a,0,0):1\le|a|\le K\};
   \]
3. real harmonic probe, for which
   \[
   S_Q=\{k_0,-k_0\}.
   \]

Terminal support size is only the first gate. The true retained cost depends on the nonlinear backward cone.

---

## 3. Navier--Stokes dependency pullback

For a retained mode set \(S\), define

\[
\boxed{
D(S)
=
S\cup
\{p,q\in K_M:\ p+q=k\text{ for some }k\in S\}.
}
\]

For one classical RK4 step with terminal support \(T\), define

\[
\boxed{
\mathfrak R_{\rm RK4}(T)
:=
\bigl(K_1,K_2,K_3,K_4,S_{\rm in}\bigr)
}
\]

by

\[
K_4=T,
\qquad
K_3=D(K_4),
\qquad
K_2=D(K_3),
\]

\[
K_1=D(K_2),
\qquad
S_{\rm in}=D(K_1).
\]

For a horizon of \(H\) time steps, recurse backward by taking the input relevance of step \(n+1\) as the terminal relevance of step \(n\).

Write the resulting stage sets as

\[
K_{n,s}(Q),
\qquad
n=0,\ldots,H-1,
\qquad
s=1,2,3,4.
\]

---

## 4. Structural retained cost

Let

\[
\mathcal T_k
=
\{(p,q)\in K_M^2:p+q=k\}
\]

be the ordered triads contributing to output mode \(k\).

Define one full direct-triad RHS work count

\[
\boxed{
C_{\rm RHS}
:=
\sum_{k\in K_M}|\mathcal T_k|.
}
\]

Then full classical RK4 work over horizon \(H\) is

\[
\boxed{
C_{\rm full}(H)=4H\,C_{\rm RHS}.
}
\]

For a declared reader \(Q\), define its exact retained structural work by

\[
\boxed{
C_H(Q)
:=
\sum_{n=0}^{H-1}
\sum_{s=1}^{4}
\sum_{k\in K_{n,s}(Q)}
|\mathcal T_k|.
}
\]

The corresponding structural gain is

\[
\boxed{
G_H(Q)
:=
\frac{C_{\rm full}(H)}{C_H(Q)}.
}
\]

This is a graph/work-count quantity. It is not identical to wall-clock speed, because FFT cost, memory traffic, vectorization, compilation overhead, and backend-switching also matter.

---

## 5. Readout-design optimization problem

Let

\[
\mathscr Q_{\rm adm}(\mathcal T)
\subseteq
\mathscr Q_{\rm phys}
\]

be the physical readers admitted for a declared task \(\mathcal T\). Membership means the reader is acceptable for that task under separately declared semantic/measurement constraints; this note does not manufacture that admissibility relation.

The readout-design problem is

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

For linear Fourier-readable tasks this can be written suggestively as

\[
\boxed{
Q^\star
=
\operatorname*{arg\,min}_{Q\in\mathscr Q_{\rm adm}(\mathcal T)}
C\!\left(
D_{\rm RK4}^{(H)}
\bigl(\operatorname{supp}\widehat Q\bigr)
\right),
}
\]

where \(D_{\rm RK4}^{(H)}\) denotes the complete stage-wise, horizon-wise dependency expansion, not merely \(D^H\) on one Euler graph.

This is the canonical equation record for **Readout Design as Computational Acceleration** in the present finite NS program.

---

## 6. Three reader examples already separated by the framework

### 6.1 Point velocity

For

\[
u(x^\star,T)=\sum_{k\in K_M}\widehat u_k(T)e^{ik\cdot x^\star},
\]

all retained modes appear directly, so

\[
\boxed{S_Q=K_M.}
\]

There is no terminal-support compression.

### 6.2 Plane-average velocity

For the plane average normal to \(x\),

\[
S_Q=A_x,
\qquad |A_x|=2K,
\]

but `NS_PHYSICAL_PLANE_AVERAGE.md` proves

\[
\boxed{D(A_x)=K_M.}
\]

Therefore exact RK4 slicing saves only the terminal \(k_4\) stage of the final step, with

\[
\boxed{
C_R=(4H-1)C+C_A
}
\]

and

\[
\boxed{
1<G_H<\frac{4H}{4H-1}.
}
\]

This is sparse support with immediate causal saturation.

### 6.3 Real corner harmonic probe

For

\[
Q_{k_0,\phi}(T)
=
\frac{1}{(2\pi)^3}
\int u(x,T)\cos(k_0\cdot x+\phi)\,dx,
\]

terminal support is exactly

\[
\boxed{S_Q=\{k_0,-k_0\}.}
\]

For the tested cube \(K=3\) and corner probe \(k_0=(3,3,3)\), the one-step RK4 stage sizes are

\[
\boxed{
342,\ 342,\ 126,\ 2
}
\]

for \(K_1,K_2,K_3,K_4\), respectively, and the direct structural work reduction is approximately

\[
\boxed{1.658\times.}
\]

Thus readers with very small terminal support can still differ substantially in causal-cone growth.

---

## 7. Exactness gate before acceleration

For any candidate retained reader, acceleration is admissible only after the task agreement gate

\[
\boxed{
\|Q_R^{\rm retained}-Q_R^{\rm full}\|
\le\varepsilon_Q
}
\]

is satisfied for the declared finite recurrence and test class.

For the present checkers,

\[
\varepsilon_Q=10^{-12}
\]

is the finite numerical gate.

Runtime acceleration is then a separate gate:

\[
\boxed{
C_{\rm measured,retained}
<
C_{\rm measured,full}.
}
\]

The existing RK4 compiler uses a fail-closed calibration policy: if retained execution does not beat full RK4 by the declared margin, it falls back to full RK4.

---

## 8. Interpretation

The central result is not that every physical question can be made cheap. The point-velocity and plane-average obstructions explicitly show otherwise.

The design principle is

\[
\boxed{
\text{reader dimension}
\neq
\text{causal-cone dimension}
\neq
\text{runtime cost}.
}
\]

Therefore the acceleration problem must optimize the reader together with its exact dependency cone, rather than minimizing output dimension alone.

In Readout/IDM language:

\[
\boxed{
\text{Task}
\to
\text{Admissible Reader}
\to
\text{Terminal Support}
\to
\text{RRP Pullback}
\to
\text{RFT/RCF Execution}
\to
\text{Cost Gate}.
}
\]

---

## 9. Claim boundary

This note defines and motivates an optimization target from already derived finite structures. It does **not** prove:

- existence or uniqueness of \(Q^\star\) for an arbitrary task family;
- global optimality of the tested corner harmonic probe;
- a universal wall-clock speed-up;
- a continuum Navier--Stokes reduced solver;
- any statement resolving the Millennium Prize problem.

The next mathematical/computational problem is to characterize reader families whose exact NS backward cone grows submaximally with resolution and horizon, and to compare those structural gains against the best admitted full-solver backend.
