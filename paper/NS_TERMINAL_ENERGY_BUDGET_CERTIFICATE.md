# A Posteriori Terminal Fourier-Tail Certificate from the Navier--Stokes Energy Budget

**Status:** analytic derivation (`Dr`) with fail-closed implementation in `information-discrete-math`.  
**Scope:** unforced Leray--Hopf solutions on the periodic three-torus.  
**Non-claim:** not a proof of global smoothness, uniqueness, finite-time blow-up, or the Clay problem.

This note strengthens the partial resolution of `PROP-EPSC-04` in `NS_SPACETIME_TAIL_CERTIFICATE.md`.
The spacetime certificate gives a universal `1/(K+1)` bound but does not control a prescribed terminal time. Here we show that a prescribed terminal time **can still receive a rigorous finite-K tail bound** from a finite retained energy/dissipation record, provided that record is an exact or certified projection of the actual Leray-Hopf solution.

---

## 1. Setup

Let `u` be an unforced Leray--Hopf solution and let `P_K` be the Fourier projection onto the symmetric cube `||k||_infinity <= K`.
Write

\[
E_0=\frac12\|u_0\|_2^2,
\qquad
E_K(T)=\frac12\|P_Ku(T)\|_2^2,
\]

and the retained viscous dissipation

\[
D_K(T)=\nu\int_0^T\|\nabla P_Ku(t)\|_2^2\,dt.
\]

The full Leray-Hopf energy inequality is

\[
\frac12\|u(T)\|_2^2
+
\nu\int_0^T\|\nabla u(t)\|_2^2\,dt
\le E_0.
\]

Because `P_K` is an orthogonal Fourier projection,

\[
\|u(T)\|_2^2
=
\|P_Ku(T)\|_2^2
+
\|(I-P_K)u(T)\|_2^2,
\]

and

\[
\int_0^T\|\nabla u\|_2^2dt
\ge
\int_0^T\|\nabla P_Ku\|_2^2dt.
\]

---

## 2. Terminal energy-budget theorem

### Theorem 1

For every finite `K`,

\[
\boxed{
\|(I-P_K)u(T)\|_2^2
\le
\|u_0\|_2^2
-
\|P_Ku(T)\|_2^2
-
2\nu\int_0^T\|\nabla P_Ku(t)\|_2^2dt
}
\]

whenever the quantities on the right refer to the actual Leray-Hopf solution.

### Proof

From the energy inequality,

\[
\|u(T)\|_2^2
+
2\nu\int_0^T\|\nabla u\|_2^2dt
\le
\|u_0\|_2^2.
\]

Substitute the orthogonal terminal split

\[
\|u(T)\|_2^2
=
\|P_Ku(T)\|_2^2+
\|(I-P_K)u(T)\|_2^2
\]

and discard only the nonnegative unresolved part of the dissipation:

\[
\int_0^T\|\nabla u\|_2^2dt
\ge
\int_0^T\|\nabla P_Ku\|_2^2dt.
\]

Rearranging yields the claimed bound. `square`

Define

\[
\boxed{
\beta_K^{\rm EB}(T)
=
\left[
\|u_0\|_2^2
-
\|P_Ku(T)\|_2^2
-
2D_K(T)
\right]^{1/2}
}
\]

whenever the bracket is supported by consistent exact/certified bounds.
Then

\[
\|(I-P_K)u(T)\|_2\le\beta_K^{\rm EB}(T).
\]

---

## 3. Certified directional data, not raw surrogate values

The theorem can be made fail-closed when the finite record is itself bounded rather than exact.
Suppose the finite record provides

\[
U_0\ge\|u_0\|_2,
\]

\[
L_K(T)\le\|P_Ku(T)\|_2,
\]

and

\[
\underline D_K(T)
\le
\nu\int_0^T\|\nabla P_Ku(t)\|_2^2dt.
\]

Then

\[
\boxed{
\|(I-P_K)u(T)\|_2
\le
\left[U_0^2-L_K(T)^2-2\underline D_K(T)\right]^{1/2}
}
\]

provided the bracket is nonnegative.

If a numerical implementation produces a materially negative bracket, this is **not** evidence of zero tail. It means the supplied directional certificates are mutually inconsistent, so the correct EPSC verdict is `HOLD`.

This contract is implemented in

`morrocwi/information-discrete-math/idm/ns_terminal_certificate.py`.

Crucially, the finite Fourier-Galerkin trajectory produced by the project is **not automatically** the actual continuum projection `P_Ku`. Its values may be inserted into this theorem only after a separate adapter/error theorem certifies the relation between the finite recurrence and the target Leray-Hopf solution.

---

## 4. What happens as K grows?

Define the energy-inequality slack

\[
\mathcal D_E(T)
:=
\|u_0\|_2^2
-
\|u(T)\|_2^2
-
2\nu\int_0^T\|\nabla u(t)\|_2^2dt
\ge0.
\]

For exact projections,

\[
(\beta_K^{\rm EB})^2
=
\|(I-P_K)u(T)\|_2^2
+
2\nu\int_0^T\|\nabla(I-P_K)u(t)\|_2^2dt
+
\mathcal D_E(T).
\]

Therefore, by monotone convergence of the Fourier energy and dissipation sums,

\[
\boxed{
\lim_{K\to\infty}(\beta_K^{\rm EB})^2
=
\mathcal D_E(T)
}.
\]

This reveals exactly what the energy-budget certificate can and cannot do.

### Corollary 2 -- energy-equality closure

If the solution satisfies energy equality up to `T`, so that

\[
\mathcal D_E(T)=0,
\]

then

\[
\boxed{
\beta_K^{\rm EB}(T)\to0.
}
\]

Hence the finite retained record

\[
\left(
\|P_Ku(T)\|_2,
\nu\int_0^T\|\nabla P_Ku(t)\|_2^2dt
\right)
\]

is sufficient to produce an asymptotically closing **terminal `L2` certificate** for any solution class in which energy equality is independently justified.

For a general Leray-Hopf solution with positive energy-inequality slack, this particular certificate may plateau at `sqrt(D_E)` even though the actual Fourier tail itself still tends to zero.

---

## 5. Relation to the earlier spacetime certificate

The two certificates answer different questions.

### Spacetime certificate

\[
\|(I-P_K)u\|_{L^2_tL^2_x}
\le
\frac{\|u_0\|_2}{\sqrt{2\nu}(K+1)}.
\]

Advantages:

- unconditional for unforced Leray-Hopf solutions;
- explicit `1/K` rate;
- no terminal energy-equality assumption.

Limitation:

- it does not give a bound at one prescribed time.

### Terminal energy-budget certificate

\[
\|(I-P_K)u(T)\|_2
\le
\beta_K^{\rm EB}(T).
\]

Advantages:

- targets a prescribed terminal time;
- can already certify a particular finite `K` if retained terminal energy plus retained dissipation nearly exhaust the global energy budget;
- closes asymptotically under energy equality.

Limitations:

- needs exact/certified retained projection data, not an unverified Galerkin surrogate;
- without energy equality the asymptotic certificate can stop at the energy-defect floor.

---

## 6. Why this fits the four-repository architecture

The derivation combines four existing programme ideas without treating any of them as stronger than they are:

1. **Readout Genesis:** finite records do not automatically identify omitted distinctions; the target reader and admissible class must be declared.
2. **Toledo:** the original EPSC target is split into explicit subclaims and each receives an honest tier rather than being promoted wholesale.
3. **Information Discrete Mathematics:** the certificate is represented as a finite fail-closed computation over directional bounds.
4. **Readout-Navier-Stokes:** the Fourier energy split, viscous dissipation and Leray-Hopf energy inequality provide the domain-specific bridge.

The key retained record is not merely the terminal low modes. It is a short **energy tape**:

\[
\mathcal R_K^{\rm EB}
=
\left(
U_0,
L_K(T),
\underline D_K(T)
\right).
\]

This is exactly the kind of richer retained state suggested by the repository's earlier result that shell energy alone need not determine the nonlinear tape.

---

## 7. Claim boundary

Established at analytic (`Dr`) level:

- the terminal energy-budget inequality above;
- its fail-closed directional-bound form;
- the energy-defect floor identity;
- asymptotic terminal closure under independently justified energy equality.

Still not established:

- that the project's finite Galerkin trajectory equals the actual continuum projection with a certified error;
- unconditional energy equality for every 3-D Leray-Hopf solution;
- an unconditional pointwise regularity certificate at arbitrary prescribed time;
- global regularity, finite-time singularity, uniqueness, or the Clay problem.

The important change is that the terminal problem is no longer simply "no certificate." It now has a **conditional/a-posteriori finite-record certificate with an explicit obstruction floor**.
