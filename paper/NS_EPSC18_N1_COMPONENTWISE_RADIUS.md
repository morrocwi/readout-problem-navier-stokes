# Componentwise exact-preconditioned radius for the full N=1 finite energy-observability chart

**Status:** post-paper EPSC analytic note with executable finite reproduction. This is a fixed finite `N=1` Fourier-Galerkin result. It is not a continuum-regularity theorem, a turbulence-DNS validation, or a solution of the Clay Navier-Stokes problem.

## 1. Starting point

The preceding exact-preconditioner certificate reconstructs the selected 49-by-49 characteristic-zero Jacobian `J_0` on the translation-transverse `N=1` symmetry slice and computes

\[
A=J_0^{-1}
\]

exactly over the rationals. It certifies

\[
1.28<\|A\|_\infty<1.29
\]

and, when combined with the earlier scalar Hessian majorants, yields

\[
10^{-59}<r_{\rm scalar}\le10^{-58}.
\]

At that point determinant/cofactor slack is no longer the main limitation. The remaining loss comes from collapsing the nonlinear finite Galerkin recurrence to one worst-case scalar operator bound.

## 2. Exact finite coefficient tensor

Write the `C=600` scaled quadratic Galerkin map in the declared 52 real coordinates as

\[
(CB(x,y))_m
=
\sum_{j,k=1}^{52}T_{mjk}x_jy_k,
\qquad
T_{mjk}\in\mathbb Z.
\]

The reproduction checker constructs this entire finite tensor by exact basis-pair evaluation, not by floating fitting. It records

\[
\boxed{2096\ \text{nonzero coefficients}}
\]

and the exact induced infinity bilinear row-sum bound

\[
\boxed{
\max_m\sum_{j,k}|T_{mjk}|=36000.
}
\]

This tensor lets the proof retain which state components actually interact instead of replacing every interaction by the global maximum.

## 3. Componentwise derivative majorants

For the scaled Taylor state coefficients `X_n`, define nonnegative componentwise quantities satisfying

\[
a_{n,m}\ge |X_{n,m}|,
\]

\[
b_{n,m}\ge
\sum_\ell
\left|\frac{\partial X_{n,m}}{\partial x_\ell}\right|,
\]

\[
c_{n,m}\ge
\sum_{\ell,r}
\left|\frac{\partial^2 X_{n,m}}
{\partial x_\ell\partial x_r}\right|.
\]

The recurrence uses the exact absolute tensor `|T_{mjk}|`, the exact integer scaled viscous diagonal, binomial coefficients, and rational initial box bounds. No sampled derivative is promoted to a certificate.

The declared box is centered at the deterministic small-integer full-rank state and has infinity half-width

\[
\boxed{10^{-3}}.
\]

The componentwise recurrence propagates through Taylor order 23 and then through the finite shell-energy output recurrence. For each of the 49 selected observations it produces an exact rational Hessian-row majorant `H_j^{cw}`.

## 4. Exact preconditioner plus componentwise enclosure

Use the exact rational inverse from the preceding certificate:

\[
A=J_0^{-1}.
\]

Set

\[
S_{cw}
=
\max_i
\sum_{j=1}^{49}|A_{ij}|H_j^{cw}.
\]

For points on the same symmetry slice inside the declared box, the mean-value bound gives

\[
\|A(J(x)-J_0)\|_\infty
\le
r S_{cw}.
\]

Therefore

\[
\boxed{
r_{cw}=\frac{1}{2S_{cw}}
}
\]

implies

\[
\boxed{
\|A(J(x)-J_0)\|_\infty\le\frac12<1.
}
\]

The checker also verifies that the resulting radius is contained inside the `10^-3` box on which the componentwise majorants were constructed.

## 5. Reproduced radius

The full reproduction ledger records

\[
\boxed{
10^{-28}<r_{cw}\le10^{-27}.
}
\]

Compared with the same exact `J_0^{-1}` combined with scalar finite majorants,

\[
10^{-59}<r_{\rm scalar}\le10^{-58},
\]

this is a **31-decimal-order improvement** in the lower power-of-ten bracket.

Across the sequence of increasingly faithful finite certificates, the rigorous scale has moved as

\[
\boxed{
10^{-7934}
\longrightarrow
10^{-3878}
\longrightarrow
10^{-59}
\longrightarrow
10^{-28}.
}
\]

These numbers should be read as conservative certified neighborhoods, not estimates of the true inverse radius. Each improvement removes a specific proof overestimate while keeping the fail-closed logic.

## 6. What this changes

The main mathematical lesson is now sharper. The extremely tiny first radii were not evidence that the finite energy-observability inverse itself was catastrophically ill-conditioned. They were largely artifacts of progressively coarser proof envelopes:

1. uniform determinant/Hadamard bound;
2. row-aware determinant/Hadamard bound;
3. exact center inverse but scalar nonlinear derivative majorants;
4. exact center inverse plus componentwise nonlinear derivative majorants.

The current result establishes a much larger positive finite local radius but still does not reach a realistic measurement tolerance.

## 7. Next frontier

The remaining useful target is a genuinely local, entrywise interval enclosure of the selected Jacobian rather than another global majorant. The fail-closed target is

\[
q(B)=\|I-AJ(B)\|_\infty<1
\]

on a branch-certified box `B`, followed by measurement propagation

\[
\rho_1
\le
\frac{\|A\|_\infty}{1-q(B)}
(\sigma_{\rm meas}+\sigma_{\rm res}).
\]

The key unresolved issue is therefore no longer existence of a quantitative inverse at `N=1`; it is whether one can certify a **measurement-informative branch-stable radius** and then extend the construction beyond the single certified finite resolution.

## 8. Reproduction and provenance

Primary executable source:

- `reproduction/checks/check_volume7_eps18_n1_exact_preconditioner.py`
- `reproduction/checks/check_volume7_eps18_n1_componentwise_radius.py`

The generated ledger records separately the exact tensor, the componentwise Hessian enclosure, the componentwise exact-preconditioned radius, its improvement over the scalar exact-preconditioner bound, and the still-open practical local interval problem.

Toledo provenance uses proposal identifier `PROP-EPSC-28`. It is a proposal record with placeholder registry code until canonical review; it is not a canonical Toledo theorem code.

## 9. Claim boundary

This result does not prove global injectivity of energy histories, stable branch selection from experimental data, arbitrary-`N` reconstruction, all-resolution saturation, continuum regularity or blow-up, equality of a finite Galerkin path with an actual continuum solution, turbulent-DNS adequacy, or the Clay Millennium problem.
