# Fixed-N=1 direct raw-sample inverse for EPSC-19 / EPSC-36

## Purpose

This note records the direct finite-time shell-energy route

\[
\text{raw samples}\to\mathcal S_h\to\text{preconditioned sample-map gate}\to\rho_1,
\]

while keeping the repository's finite-first boundary explicit.  The executable checker is
`reproduction/checks/check_volume7_eps19_n1_direct_sample_inverse.py`.

The construction bypasses the numerically hostile intermediate route

\[
\text{samples}\to\text{high-order numerical derivatives}\to\text{Taylor jet}.
\]

## Direct sample map

On the 49-dimensional translation slice of the fixed `N=1` Fourier-Galerkin system, define

\[
\mathcal S_h(x)=
\bigl(I_0(\phi_{jh}(x))\bigr)_{j=0}^{23}
\oplus
\bigl(I_1(\phi_{jh}(x))\bigr)_{j=0}^{23}
\oplus I_2(x),
\]

with the explicit rational spacing

\[
\boxed{h=10^{-200}}.
\]

The spacing is intentionally microscopic.  It is a proof-scale witness, not a practical sensor schedule.

## Exact direct preconditioner

Let `a_{s,n}` denote the time-Taylor coefficients of the shell outputs and use the already certified scaled chart

\[
z_{s,n}=600^n n!\,a_{s,n}.
\]

In sample-channel order the degree-23 sample Jacobian factors as

\[
J_T(h)=P_hJ_z,
\]

where `J_z` is the exact characteristic-zero 49x49 scaled-jet Jacobian and the two primary-shell blocks of `P_h` are

\[
V\,\operatorname{diag}\!\left(\frac{h^n}{600^n n!}\right)_{n=0}^{23},
\qquad V_{jn}=j^n.
\]

Therefore

\[
\boxed{A_h=J_z^{-1}P_h^{-1}}
\]

is an exact rational preconditioner for the degree-23 direct sample Jacobian:

\[
A_hJ_T(h)=I.
\]

This factorization constructs the preconditioner only; noisy measurements are not first converted to high-order Taylor derivatives.

## Finite inequality gate

The checker computes finite operator and remainder bounds over the declared local box and obtains a branch-wide defect estimate of the form

\[
q\le
\max_i\sum_j |(A_h)_{ij}|\,(e_j+rH_j).
\]

If a positive `r` satisfies `q<1`, and if

\[
\delta:=\|y_{obs}-y_T\|_\infty+\sigma+\tau_T
\]

obeys

\[
\boxed{
\|A_h\|_\infty\delta+qr\le r,
}
\]

then the following **finite arithmetic consequences** are certified:

\[
\boxed{
\delta\le\frac{(1-q)r}{\|A_h\|_\infty}
}
\]

and the associated conditional inverse radius is

\[
\boxed{
\rho_{cond}=\frac{\|A_h\|_\infty}{1-q}\,\delta\le r.
}
\]

These inequalities are the native finite gate.  They do not by themselves assert that an exact real root exists or that an infinite contraction sequence attains a limit.

## Foundational fence: finite gate vs real-analysis adapter

If one additionally grants a complete real metric-space interpretation of the branch and of the finite-dimensional ODE flow, then the usual Banach fixed-point theorem turns the same `q<1` and self-map inequalities into existence and uniqueness of a root in that real branch.  Under the repository's epistemic rules that consequence is an **explicit real-analysis adapter**, not a native finite theorem.

Accordingly, the native chain established by the finite checker is

\[
\boxed{
\text{finite sample data + finite model/remainder bounds}
\to
(q,\delta,r,A_h)\text{ gate}
\to
\rho_{cond}.
}
\]

The optional real-analysis chain is separately labelled

\[
\boxed{
[\text{real completeness/existence assumptions}]
+\text{ finite gate}
\to
\text{one local real root in the branch}.
}
\]

## A new obstruction: shell energy cannot globally select one translation branch

`reproduction/checks/check_volume7_eps36_shell_symmetry_obstruction.py` records an independent finite obstruction.  The cubic cutoff and shell energies are invariant under lattice-axis symmetries.  At `N=1`, a one-mode state supported at

\[
k_a=(1,0,0)
\]

and its axis-swapped state supported at

\[
k_b=(0,1,0)
\]

are not related by spatial translation, because translation changes Fourier phases but not wavevector support.  Nevertheless they have the same shell energy, zero quadratic self-interaction, the same viscous rate, and hence for every arbitrary finite derivative order `n`,

\[
I^{(n)}_a(0)=(-2\nu)^n I_a(0)=(-2\nu)^n I_b(0)=I^{(n)}_b(0).
\]

Thus **global unique branch capture modulo translations alone is impossible for shell-energy-only readers**.  EPSC-36 must therefore declare one of three repairs:

1. quotient the additional finite cubic symmetry;
2. add an orientation-breaking measurement/readout; or
3. provide an independent admissible-domain/orientation prior.

This is not a weakness of the local inverse calculation; it is an invariance obstruction that any global measurement theorem must respect.

## What this does and does not close

At fixed `N=1`, once the focused checker passes, the project has an explicit direct-sample preconditioner, finite flow/remainder budgets, a positive `q<1` local gate, and a positive raw-data budget.  That closes the **finite local direct-sample conditioning/gate subproblem**.

It does **not** close global branch selection modulo translations, because the cubic-symmetry obstruction proves that target impossible from shell-energy-only data as stated.  Nor does it provide a practical sensor spacing/tolerance, arbitrary-finite-`N` scaling, a continuum regularity theorem, physical DNS adequacy, or a Clay result.

The correct next form of EPSC-36 is therefore quotient-aware or reader-augmented branch capture, not an attempt to force globally unique orientation out of invariant shell-energy data.
