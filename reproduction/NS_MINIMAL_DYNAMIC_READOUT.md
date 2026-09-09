# Minimal Dynamically Sufficient Navier--Stokes Readout

## Status

This note closes the **finite-Galerkin state-sufficiency question** that remained open after
`NS_RETAINED_SUFFICIENCY.md`.

It does **not** claim:

- a continuum Navier--Stokes regularity theorem,
- a small or fast exact closure at production resolution,
- empirical validation against external DNS or experiment,
- resolution of Readout Genesis T2.

The working symbol `Xi_min` is deprecated here because Readout Genesis already reserves
`\Xi_n` for its `orientation_selecting_order` state slot.  The canonical symbol in this
Navier--Stokes development is therefore

\[
\boxed{\mathcal Q_{\min}^{NS}}.
\]

---

# 1. Fixed finite Navier--Stokes system

Fix one finite, symmetric, divergence-free Fourier--Galerkin truncation \(K_M\) of the
periodic three-dimensional incompressible Navier--Stokes equation.  Write its real finite
state as

\[
x\in X_M\subset \mathbb R^{d_M}.
\]

For the unforced case used by the executable checks,

\[
\dot x = F_M(x),
\]

where

\[
F_M(x)=A_\nu x+B_M(x,x)
\]

is polynomial of degree at most two.

Let

\[
\Phi_t:X_M\to X_M
\]

be the finite Galerkin flow.

For exact \(k^2\)-shells

\[
K_j=\{k\in K_M:|k|^2=q_j\},
\]

define the retained shell reader

\[
I_j(x)
=
\frac12
\sum_{k\in K_j}
|\widehat u_k|^2,
\qquad
I=(I_1,\ldots,I_m).
\]

Thus

\[
I:X_M\to\mathbb R^m
\]

is polynomial of degree two.

---

# 1A. Readout Universe lens: loss must be named before closure

Readout Universe treats every record as a translation of a richer state rather than the
state itself.  For the present finite Navier--Stokes problem, the shell reader

\[
u\longmapsto I(u)
\]

is therefore admitted only with an explicit loss statement.

The same-\(I\)/different-\(\eta^{NS}\) witness identifies that loss concretely:

\[
I(u)=I(v)
\]

does not imply

\[
\eta^{NS}(u)=\eta^{NS}(v).
\]

Hence phase/orientation distinctions capable of changing triad transfer were erased by the
reader and cannot be reconstructed from \(I\) alone.

The repair must therefore occur at the **retention / translation layer**:

\[
\boxed{
\text{retain exactly the distinctions that change future declared readouts}
}
\]

rather than at the report layer by fitting an unconstrained law after the distinctions have
already been collapsed.

This is a lens constraint, not an imported Navier--Stokes law.  All dynamical equations
below continue to be derived from the finite Galerkin Navier--Stokes vector field itself.

---

# 2. Exact nonlinear tape from Navier--Stokes triads

For

\[
k=p+q,
\]

the ordered-pair contribution to the Fourier coefficient of the convective term is

\[
i\,(q\cdot\widehat u_p)\widehat u_q.
\]

Because the retained coefficient \(\widehat u_k\) is divergence-free,

\[
\overline{\widehat u_k}\cdot P_k a
=
\overline{\widehat u_k}\cdot a.
\]

Therefore define the ordered-triad shell-transfer contribution

\[
\boxed{
\Theta_{kpq}(u)
=
-\Re\!\left[
\overline{\widehat u_k}\cdot
i\,(q\cdot\widehat u_p)\widehat u_q
\right],
\qquad
p+q=k.
}
\tag{2.1}
\]

The exact nonlinear tape is then

\[
\boxed{
\eta_j^{NS}(u)
=
\sum_{k\in K_j}
\sum_{p+q=k}
\Theta_{kpq}(u).
}
\tag{2.2}
\]

The viscous shell operator is forced directly by Navier--Stokes:

\[
\boxed{
L_\nu
=
\operatorname{diag}
(2\nu q_1,\ldots,2\nu q_m).
}
\tag{2.3}
\]

Hence the exact finite retained equation is

\[
\boxed{
\dot I+L_\nu I=\eta^{NS}.
}
\tag{2.4}
\]

No autonomous law

\[
\eta^{NS}=\Gamma(I)
\]

is assumed.

The already-executed same-\(I\)/different-\(\eta\) witness proves that shell energy alone
is not sufficient.

---

# 3. Readout-equivalence is the object to minimize

Readout Genesis defines a valid domain translation as **minimal, sufficient, and
dynamically closed**.  Therefore the correct question is not

\[
\text{Which feature vector looks useful?}
\]

but

\[
\text{Which distinctions can be identified without changing any future declared readout?}
\]

Define the future-shell-readout equivalence relation

\[
\boxed{
x\sim_I y
\iff
I(\Phi_t x)=I(\Phi_t y)
\quad
\forall t\ge0.
}
\tag{3.1}
\]

Define

\[
\boxed{
\mathcal Q_{\min}^{NS}
:=
X_M/\!\sim_I
}
\tag{3.2}
\]

with quotient map

\[
q_{\min}:X_M\to\mathcal Q_{\min}^{NS},
\qquad
q_{\min}(x)=[x]_I.
\tag{3.3}
\]

This is the canonical exact answer to the finite state-sufficiency problem.

---

# 4. Minimal dynamic quotient theorem

## Theorem 4.1

The quotient \(\mathcal Q_{\min}^{NS}\) is the coarsest exact retained state that

1. reproduces the shell readout,
2. carries a well-defined autonomous evolution,
3. preserves every future shell readout.

### Proof

Define

\[
\Phi_t^\sharp([x]_I)
:=
[\Phi_t x]_I.
\tag{4.1}
\]

This is well-defined.  If

\[
x\sim_I y,
\]

then for every \(s\ge0\),

\[
I(\Phi_s(\Phi_t x))
=
I(\Phi_{s+t}x)
=
I(\Phi_{s+t}y)
=
I(\Phi_s(\Phi_t y)),
\]

so

\[
\Phi_t x\sim_I\Phi_t y.
\]

Thus

\[
\boxed{
q_{\min}\circ\Phi_t
=
\Phi_t^\sharp\circ q_{\min}.
}
\tag{4.2}
\]

Define

\[
I^\sharp([x]_I):=I(x).
\tag{4.3}
\]

This is well-defined because \(x\sim_Iy\) implies equality at \(t=0\).  Hence

\[
\boxed{
I=I^\sharp\circ q_{\min}.
}
\tag{4.4}
\]

Now let

\[
q:X_M\to Z
\]

be any other exact retained state with dynamics \(G_t\) and reader \(R\) satisfying

\[
q\circ\Phi_t=G_t\circ q,
\qquad
I=R\circ q.
\tag{4.5}
\]

If

\[
q(x)=q(y),
\]

then for every \(t\ge0\),

\[
I(\Phi_t x)
=
R(G_t(q(x)))
=
R(G_t(q(y)))
=
I(\Phi_t y).
\]

Therefore

\[
q(x)=q(y)\Longrightarrow x\sim_Iy.
\tag{4.6}
\]

So every exact retained state separates at least as many distinctions as
\(\mathcal Q_{\min}^{NS}\).  Equivalently, on the reachable image of \(q\) there is a
unique factor map

\[
\pi:q(X_M)\to\mathcal Q_{\min}^{NS}
\]

such that

\[
\boxed{
q_{\min}=\pi\circ q.
}
\tag{4.7}
\]

Thus \(\mathcal Q_{\min}^{NS}\) is the coarsest exact dynamically sufficient retained
state. \(\square\)

---

# 5. The quotient is generated directly from Navier--Stokes, not guessed

The quotient definition is exact but not yet a coordinate representation.

Define the Navier--Stokes readout jet recursively by Lie differentiation along the
finite Galerkin vector field:

\[
\boxed{
J_0:=I,
\qquad
J_{r+1}:=\mathcal L_{F_M}J_r
=
D J_r(x)\,F_M(x).
}
\tag{5.1}
\]

The first level is already known exactly:

\[
\boxed{
J_1
=
\dot I
=
-L_\nu I+\eta^{NS}.
}
\tag{5.2}
\]

Using the triad decomposition,

\[
\boxed{
J_{1,j}
=
-2\nu q_j I_j
+
\sum_{k\in K_j}\sum_{p+q=k}\Theta_{kpq}.
}
\tag{5.3}
\]

Every higher level is generated by the same finite Navier--Stokes vector field:

\[
J_2
=
D J_1\,F_M,
\qquad
J_3
=
D J_2\,F_M,
\quad\ldots
\tag{5.4}
\]

No new physical law enters.

Because

\[
\deg F_M\le2,
\qquad
\deg J_0=2,
\]

we have

\[
\boxed{
\deg J_r\le r+2.
}
\tag{5.5}
\]

Thus every \(J_r\) is a finite polynomial readout of the finite Galerkin state.

---

# 6. Finite-jet realization theorem

The future-readout quotient does not require an actually infinite record at a fixed
Galerkin resolution.

For two independent state variables \(x,y\in X_M\), define

\[
\Delta_{r,\ell}(x,y)
=
J_r^\ell(x)-J_r^\ell(y),
\qquad
\ell=1,\ldots,m.
\tag{6.1}
\]

In the polynomial ring

\[
\mathbb R[x,y],
\]

define the ascending ideals

\[
\mathfrak a_R
=
\left\langle
\Delta_{r,\ell}
:
0\le r\le R,\;
1\le\ell\le m
\right\rangle.
\tag{6.2}
\]

Then

\[
\mathfrak a_0
\subseteq
\mathfrak a_1
\subseteq
\mathfrak a_2
\subseteq\cdots.
\tag{6.3}
\]

## Theorem 6.1

For every fixed finite polynomial Galerkin truncation there exists a finite integer
\(R_M^\star\) such that

\[
\boxed{
J_r(x)=J_r(y)
\quad
0\le r\le R_M^\star
}
\tag{6.4}
\]

if and only if

\[
\boxed{
J_r(x)=J_r(y)
\quad
\forall r\ge0.
}
\tag{6.5}
\]

### Proof

The polynomial ring \(\mathbb R[x,y]\) is Noetherian.  Therefore the ascending chain
\(\mathfrak a_R\) stabilizes:

\[
\exists R_M^\star<\infty
\quad
\text{such that}
\quad
\mathfrak a_{R_M^\star}
=
\mathfrak a_{R_M^\star+1}
=
\cdots.
\tag{6.6}
\]

Hence every later difference polynomial satisfies

\[
\Delta_{r,\ell}\in\mathfrak a_{R_M^\star},
\qquad
r>R_M^\star.
\tag{6.7}
\]

If all generators through \(R_M^\star\) vanish at \((x,y)\), every polynomial in
\(\mathfrak a_{R_M^\star}\) vanishes there, so every later
\(\Delta_{r,\ell}\) vanishes as well.  The reverse implication is immediate.
\(\square\)

---

# 7. From finite jet equality to future readout equality

The finite Galerkin vector field \(F_M\) is polynomial and therefore analytic.  Its shell
reader \(I\) is polynomial.  Along every finite Galerkin trajectory,

\[
t\mapsto I(\Phi_t x)
\]

is analytic on its interval of existence.

Its Taylor derivatives satisfy

\[
\frac{d^r}{dt^r}I(\Phi_t x)\bigg|_{t=0}
=
J_r(x).
\tag{7.1}
\]

Therefore

\[
J_r(x)=J_r(y)
\quad\forall r
\]

implies equality of the analytic shell-readout trajectories, and conversely future
trajectory equality implies equality of all jets.

Combining with Theorem 6.1,

\[
\boxed{
x\sim_I y
\iff
J_r(x)=J_r(y)
\quad
0\le r\le R_M^\star.
}
\tag{7.2}
\]

Hence the finite map

\[
\boxed{
q_{\mathrm{jet}}(x)
=
\left(
J_0(x),J_1(x),\ldots,J_{R_M^\star}(x)
\right)
}
\tag{7.3}
\]

has exactly the same fibers as \(q_{\min}\).

Therefore its image is a finite coordinate realization of the canonical quotient:

\[
\boxed{
q_{\mathrm{jet}}(X_M)
\cong
\mathcal Q_{\min}^{NS}.
}
\tag{7.4}
\]

The coordinate list may be redundant; the quotient, not the raw coordinate count, is the
canonical minimal object.

---

# 8. Translation phase is gauge, arbitrary phase is not

For a spatial translation \(a\in\mathbb T^3\),

\[
(T_a\widehat u)_k
=
e^{ik\cdot a}\widehat u_k.
\tag{8.1}
\]

Shell energy is unchanged:

\[
I(T_a u)=I(u).
\tag{8.2}
\]

For every ordered triad \(p+q=k\),

\[
e^{-ik\cdot a}
e^{ip\cdot a}
e^{iq\cdot a}
=
1.
\tag{8.3}
\]

Therefore

\[
\boxed{
\Theta_{kpq}(T_a u)
=
\Theta_{kpq}(u)
}
\tag{8.4}
\]

and

\[
\boxed{
\eta^{NS}(T_a u)=\eta^{NS}(u).
}
\tag{8.5}
\]

Navier--Stokes translation equivariance then gives

\[
\boxed{
T_a u\sim_Iu.
}
\tag{8.6}
\]

Thus the minimal state must discard translation phase.

But the already-executed same-shell-energy/different-tape witness shows that arbitrary
phase/orientation changes do not lie in the same future-readout class.

So the correct statement is

\[
\boxed{
\text{retain phase only modulo genuine future-readout symmetries}.
}
\tag{8.7}
\]

---

# 9. Toledo lineage

Toledo proposal

\[
\texttt{PROP-URCF-01}
\equiv
\texttt{EQ-URCF-TURB-004}
\]

states

\[
\tau_R\dot I_R+L_RI_R=S_R+\eta_R,
\qquad
\tau_R>0.
\tag{9.1}
\]

For the unforced finite Navier--Stokes shell system, multiply (2.4) by any declared
\(\tau_R>0\):

\[
\tau_R\dot I
+
\tau_RL_\nu I
=
\tau_R\eta^{NS}.
\tag{9.2}
\]

Thus the exact finite Navier--Stokes adapter is

\[
\boxed{
I_R=I,
\qquad
L_R^{NS}=\tau_RL_\nu,
\qquad
S_R=0,
\qquad
\eta_R^{NS}=\tau_R\eta^{NS}.
}
\tag{9.3}
\]

This is an instance of the Toledo functional form.

It does **not** assert that the viscous diagonal operator is identical to Toledo
`root/EQ-008`'s graph-Laplacian construction.  It is used only as the declared positive
linear restoration operator in this Navier--Stokes adapter.

The minimal quotient now changes the interpretation of the residual:

\[
\boxed{
\eta_R^{NS}
=
\pi_\eta(\mathcal Q_{\min}^{NS})
}
\tag{9.4}
\]

for a well-defined readout \(\pi_\eta\) on the sufficient state.

Equivalently, using the finite jet realization,

\[
\boxed{
\eta_R^{NS}
=
\tau_R
\left(
J_1+L_\nu J_0
\right).
}
\tag{9.5}
\]

So \(\eta_R\) is not a free error bin.  Once the state is sufficient, it is a deterministic
readout of that state.

---

# 10. Consequence for Genesis T2

The earlier low-viscosity failure of a shell-energy-only affine closure showed

\[
I
\not\Rightarrow
\eta^{NS}.
\]

It did **not** prove that one must replace

\[
L_R
\]

by a state-dependent operator

\[
L_R[I_R].
\]

After state sufficiency is repaired, a fixed viscous operator remains exact:

\[
\dot I+L_\nu I=\eta^{NS},
\]

while the nonlinearity is carried by the sufficient retained state.

Therefore

\[
\boxed{
\text{shell-only failure}
\not\Rightarrow
\text{Genesis T2 is required}.
}
\tag{10.1}
\]

Genesis T2 remains a distinct open modeling option, not a consequence of this failure.

---

# 11. What is now closed

For every fixed finite polynomial Fourier--Galerkin Navier--Stokes truncation:

\[
\boxed{
\text{shell energy alone is insufficient}
}
\]

\[
\boxed{
\eta^{NS}
\text{ is exactly generated by NS triads}
}
\]

\[
\boxed{
\mathcal Q_{\min}^{NS}
=
X_M/\!\sim_I
\text{ is the canonical minimal exact dynamically sufficient state}
}
\]

and

\[
\boxed{
\exists R_M^\star<\infty:
\quad
q_{\mathrm{jet}}
=
(J_0,\ldots,J_{R_M^\star})
\text{ realizes }
\mathcal Q_{\min}^{NS}.
}
\]

Thus the finite exact closure problem is no longer

\[
\text{guess }\widehat\eta(I).
\]

It is

\[
\boxed{
\text{compute the quotient / finite jet efficiently}.
}
\]

---

# 12. What remains open

The following are separate computational or continuum questions:

\[
\boxed{
R_M^\star
\text{ at useful 3D resolutions}
}
\]

\[
\boxed{
\text{a nonredundant coordinate chart for }
\mathcal Q_{\min}^{NS}
}
\]

\[
\boxed{
C(\mathcal Q_{\min}^{NS})
\ll
C(\text{full 3D Galerkin NS})
}
\]

\[
\boxed{
M\to\infty
\text{ continuum behavior}
}
\]

and external DNS / experimental validation.

Therefore the exact finite mathematical state-sufficiency question is closed, while the
**acceleration question remains empirical/computational**.

---

# 13. Equation lineage

\[
\boxed{
\text{finite NS}
\rightarrow
\Theta_{kpq}
\rightarrow
\eta^{NS}
\rightarrow
J_1
\rightarrow
J_2
\rightarrow\cdots
\rightarrow
\mathcal Q_{\min}^{NS}
\rightarrow
\text{Toledo retained readout}
}
\]

with no inserted phenomenological law between the finite Navier--Stokes vector field and
the retained state.
