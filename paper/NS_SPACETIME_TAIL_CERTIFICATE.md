# Navier--Stokes Spectral Tail Certificates

## A partial resolution of `PROP-EPSC-04`

**Status:** analytic derivation (`Dr`) plus finite algebraic witnesses.  
**Date:** 2026-09-10.  
**Scope:** incompressible Navier--Stokes on the periodic three-torus for the positive theorem below.  
**Non-claim:** this is **not** a proof of global smoothness, finite-time singularity, uniqueness of Leray-Hopf weak solutions, or the Clay Millennium problem.

This note asks a narrower question left open by the discrete epsilon-completion experiment:

> Can the Fourier information outside a finite cube be bounded by a quantity that is computable from declared finite/problem data and tends to zero as the cutoff grows?

The answer depends on **what target is being certified**.

- For an arbitrary terminal state `u(T)`, retained Fourier coefficients alone are insufficient: there is a simple non-identifiability obstruction.
- For a Leray-Hopf trajectory measured in `L2(0,T;L2_x)`, viscosity and the energy inequality give an explicit certificate decaying like `1/(K+1)`.
- For a terminal state, the same spectral step becomes valid once a pointwise `H^s` bound is separately certified.

This split is the main result of the note.

---

## 1. Setup

Work on the `2*pi` periodic three-torus and use Fourier normalization

\[
\|u\|_{L^2_x}^2=\sum_{k\in\mathbb Z^3}|\widehat u_k|^2,
\qquad
\|\nabla u\|_{L^2_x}^2=\sum_{k\in\mathbb Z^3}|k|_2^2|\widehat u_k|^2.
\]

Let `P_K` retain the symmetric cube

\[
\mathcal K_K=\{k\in\mathbb Z^3:\|k\|_\infty\le K\}.
\]

Every omitted mode satisfies

\[
\|k\|_\infty>K
\quad\Longrightarrow\quad
|k|_2\ge K+1.
\]

The current discrete-native solver in this repository and `information-discrete-math` uses the same integer-mode normalization in its viscous term `-nu |k|^2 u_hat_k`.

---

## 2. Terminal finite-record non-identifiability

### Proposition 1 -- retained terminal modes do not identify the omitted tail

Fix a finite cutoff `K`. There is no finite-record-only function

\[
\beta_K=\beta_K(P_Ku)
\]

that gives a finite universal upper bound on `||(I-P_K)u||_2` over the unrestricted divergence-free `L2` class.

### Proof

Choose

\[
q=(K+1,0,0)
\]

and a nonzero vector `a` with `q dot a=0`, for example `a=(0,A,0)`. Add the conjugate Fourier pair

\[
\widehat v_q=a,
\qquad
\widehat v_{-q}=\overline a,
\]

and zero elsewhere. Then `v` is divergence-free and real-valued after Fourier reconstruction, while

\[
P_Kv=0.
\]

Hence `u` and `u+v` have exactly the same retained record `P_Ku`, but their omitted tails differ by a quantity proportional to `|A|`. Since `A` is arbitrary, the omitted tail is not identified by the retained coefficients. `square`

### Consequence

The original form of `PROP-EPSC-04` was too coarse unless the admissible class/norm was declared. Small nested-refinement defect

\[
\delta_K=\|R_Kx_{K+1}-x_K\|
\]

cannot by itself close an unrestricted terminal tail. This is an information/identifiability obstruction, not a numerical-accuracy defect.

---

## 3. The spectral tail inequality

### Lemma 2 -- `H^s` controls the omitted Fourier tail

For `s>0`, whenever `u` has finite homogeneous `H^s` seminorm,

\[
\|(I-P_K)u\|_2
\le
\frac{\||\nabla|^s u\|_2}{(K+1)^s}.
\]

### Proof

For every omitted mode, `|k|_2 >= K+1`. Therefore

\[
\begin{aligned}
\|(I-P_K)u\|_2^2
&=\sum_{\|k\|_\infty>K}|\widehat u_k|^2\\
&\le\frac1{(K+1)^{2s}}
\sum_{\|k\|_\infty>K}|k|_2^{2s}|\widehat u_k|^2\\
&\le\frac1{(K+1)^{2s}}
\||\nabla|^su\|_2^2.
\end{aligned}
\]

Take square roots. `square`

This elementary inequality is the reusable mathematical core. The real question is where a certified `H^s` quantity comes from.

---

## 4. Unforced Leray-Hopf spacetime certificate

Consider an unforced Leray-Hopf weak solution of three-dimensional incompressible Navier--Stokes with viscosity `nu>0`. The energy inequality is

\[
\frac12\|u(t)\|_2^2
+
\nu\int_0^t\|\nabla u(s)\|_2^2\,ds
\le
\frac12\|u_0\|_2^2.
\]

### Theorem 3 -- computable `L2_t L2_x` omitted-tail certificate

For every `T>0` and finite `K`,

\[
\boxed{
\|(I-P_K)u\|_{L^2(0,T;L^2_x)}
\le
\beta_K^{\rm ST}
:=
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}
}
\]

and `beta_K^ST -> 0` as `K -> infinity`.

### Proof

Apply Lemma 2 with `s=1` at almost every time:

\[
\|(I-P_K)u(t)\|_2^2
\le
\frac{1}{(K+1)^2}\|\nabla u(t)\|_2^2.
\]

Integrating from `0` to `T` gives

\[
\|(I-P_K)u\|_{L^2_tL^2_x}^2
\le
\frac{1}{(K+1)^2}
\int_0^T\|\nabla u(t)\|_2^2dt.
\]

The energy inequality implies

\[
\nu\int_0^T\|\nabla u(t)\|_2^2dt
\le
\frac12\|u_0\|_2^2.
\]

Substitution and square root yield the formula. `square`

### Why this matters

This is a genuine finite-to-infinite certificate in the declared spacetime norm. The bound is computed from

- the finite cutoff `K`,
- viscosity `nu`, and
- the declared initial `L2` norm,

and it converges to zero without assuming global smoothness.

Thus `PROP-EPSC-04` is **closed for this target space and assumption set**, while it remains open for arbitrary terminal reconstruction.

---

## 5. Forced Leray-Hopf certificate

Assume additionally

\[
f\in L^2(0,T;H^{-1}).
\]

Using duality and Young's inequality,

\[
\langle f,u\rangle
\le
\|f\|_{H^{-1}}\|\nabla u\|_2
\le
\frac{1}{2\nu}\|f\|_{H^{-1}}^2
+
\frac\nu2\|\nabla u\|_2^2.
\]

The energy inequality therefore yields

\[
\int_0^T\|\nabla u\|_2^2dt
\le
\frac{\|u_0\|_2^2}{\nu}
+
\frac{\|f\|_{L^2_tH^{-1}}^2}{\nu^2}.
\]

Hence

\[
\boxed{
\|(I-P_K)u\|_{L^2_tL^2_x}
\le
\frac1{K+1}
\sqrt{
\frac{\|u_0\|_2^2}{\nu}
+
\frac{\|f\|_{L^2_tH^{-1}}^2}{\nu^2}}
}.
\]

The unforced theorem uses the sharper factor `1/sqrt(2 nu)` available when the forcing term vanishes.

---

## 6. Readout lift

The Readout programme asks for the error in the **declared answer**, not automatically the whole state.

Let `Q` be Lipschitz on the certified spacetime state with constant `L_Q`:

\[
\|Q(u)-Q(v)\|\le L_Q\|u-v\|_{L^2_tL^2_x}.
\]

Then Theorem 3 gives immediately

\[
\boxed{
\|Q(u)-Q(P_Ku)\|
\le
L_Q\beta_K^{\rm ST}
}.
\]

A concrete case is the time-averaged field

\[
\bar u=\frac1T\int_0^T u(t)dt.
\]

Cauchy--Schwarz gives

\[
\boxed{
\|(I-P_K)\bar u\|_2
\le
\frac{\beta_K^{\rm ST}}{\sqrt T}
}.
\]

This is a certified full Fourier-tail statement about the average field, even though a prescribed terminal state remains harder.

---

## 7. Conditional terminal certificate and the remaining 3-D bottleneck

Suppose a separate argument certifies

\[
\||\nabla|^su(T)\|_2\le M_s(T)
\]

for some `s>0`. Lemma 2 gives

\[
\boxed{
\|(I-P_K)u(T)\|_2
\le
\frac{M_s(T)}{(K+1)^s}
}.
\]

This identifies the real obstacle for arbitrary terminal completion. The Fourier tail estimate itself is elementary; the hard part is producing a globally valid pointwise regularity bound in three dimensions. The epsilon-completion programme therefore does **not** bypass the classical regularity difficulty. It locates exactly where that difficulty enters the certificate.

---

## 8. Connection to the four-repository architecture

### `information-discrete-math`

Owns the reusable computation/certificate layer:

- `idm/ns_retained.py` -- finite Fourier-Galerkin recurrence;
- `idm/ns_epsilon.py` -- nested defect and fail-closed gate;
- `idm/ns_tail_certificate.py` -- the bounds proved in this note.

### `toledo`

Owns proposal/equation provenance. The original open target `PROP-EPSC-04` is refined into:

- terminal finite-record no-go;
- spacetime Leray certificate;
- Lipschitz readout lift;
- conditional terminal `H^s` certificate.

These should remain proposal-tier until Toledo's own review/formalisation procedure promotes them.

### `readout_genesis`

Contributes the epistemic rule that a retained readout must not be silently equated with a richer target. In this note that rule becomes mathematical: the target norm/readout has to be declared before `beta_K` can even be a well-posed certification object.

### this repository

Owns the Navier--Stokes specialization, proof note, finite witnesses and reproduction ledger.

---

## 9. Claim boundary

What is established here at analytic (`Dr`) level:

1. finite retained terminal coefficients alone do not identify the unrestricted omitted terminal tail;
2. the spectral `H^s -> L2-tail` inequality;
3. an explicit `1/(K+1)` spacetime `L2_tL2_x` tail certificate for unforced Leray-Hopf solutions;
4. a forced analogue under `f in L2_t H^{-1}`;
5. propagation of the certified error through Lipschitz readouts;
6. a conditional terminal certificate once a pointwise `H^s` bound is supplied.

What is **not** established:

- a universal terminal-time certificate from finite Fourier coefficients alone;
- global smoothness of 3-D Navier--Stokes;
- finite-time singularity;
- uniqueness of weak solutions;
- physical adequacy of a coarse finite cutoff for turbulent DNS;
- the Clay Millennium problem.

The correct summary is therefore:

\[
\boxed{\text{PROP-EPSC-04: partially resolved by target-space refinement}}
\]

with

\[
\boxed{\text{spacetime/readout certificate: available}}
\]

and

\[
\boxed{\text{arbitrary terminal full-state certificate: conditional/open}}.
\]
