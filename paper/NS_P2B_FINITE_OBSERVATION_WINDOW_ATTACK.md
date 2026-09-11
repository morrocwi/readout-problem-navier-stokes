# NS P2B — finite-observation window attack

**Date:** 2026-09-11  
**Tracker:** issue #44.  
**Status:** alternate P2 reduction / adversarial audit.  
**Claim boundary:** no Clay solution is claimed. The purpose is to translate the remaining uniform-regularity frontier into a finite-observation readout and identify exactly what the existing energy budget cannot prove.

## 1. Discovery order and source discipline

This route was constructed in the requested order.

1. **IDM.** `morrocwi/information-discrete-math/docs/NS_ENERGY_TRANSFER_OBSERVABILITY.md` supplies the exact finite shell balance and derivative-free time-window transfer identity. `docs/DISCRETE_EPSILON_COMPLETION.md` supplies fail-closed finite-tape residual-to-continuum error accounting.
2. **Readout Genesis.** We use only its architectural rule that a useful domain translation must be sufficient and dynamically closed, and that the translation should commute with the dynamics. Genesis is not theorem evidence for Navier--Stokes.
3. **Readout Universe.** We use its translate-first / bridge-audit / weakest-tier discipline. Universe is not theorem evidence for Navier--Stokes.
4. **External continuum adapter.** Balakrishna--Biswas, *Research in the Mathematical Sciences* 12, 46 (2025), proves periodic 3D NSE regularity criteria based on finitely many observations, including a time-window criterion. That published theorem is an external semantic adapter; its absolute constants and normalization must be audited before an executable per-instance PASS can be emitted.

The finite-native programme therefore does not attempt to manufacture a continuum solution. It attempts to manufacture a finite record satisfying a separately proved regularity gate.

## 2. IDM window readout

For the unforced finite Fourier system, IDM records the shell balance

\[
\dot I_s=T_s-2\nu s I_s
\]

and hence, on a time cell `[t0,t1]`,

\[
\int_{t_0}^{t_1}T_s\,dt
=I_s(t_1)-I_s(t_0)+2\nu s\int_{t_0}^{t_1}I_s\,dt.
\]

This is important because a nonlinear-transfer readout can be certified from finite time-window records without differentiating noisy observations.

The P2B reader is not the instantaneous full state. It is a finite modal time-window quantity.

For `p>2`, window length `tau0>0`, and a finite modal projector `P_N`, define

\[
K_N(u)
:=\sup_t
\left(
\int_t^{t+\tau_0}
\|P_Nu(s)\|_{H^1}^{2p}\,ds
\right)^{1/(2p)}.
\]

This is the finite-observation quantity to be translated into the continuum regularity adapter.

## 3. `NS-P2B-EPSC-OBS-LIFT`

Let `v` be a finite Fourier comparison tape/path on the target interval and suppose an EPSC/relative-energy certificate gives

\[
\sup_s\|u(s)-v(s)\|_{L^2}\le\varepsilon.
\]

Let `Lambda_N` be an upper bound for the largest Stokes eigenvalue retained by `P_N`. Then

\[
\|P_N(u-v)\|_{H^1}
\le \sqrt{\Lambda_N}\,\varepsilon
\]

(up to the declared equivalent `H^1` normalization; the convention must be fixed in an executable adapter).

By Minkowski in `L^{2p}` on every window,

\[
\boxed{
K_N(u)
\le
K_N(v)
+
\tau_0^{1/(2p)}\sqrt{\Lambda_N}\,\varepsilon.
}
\]

**Status:** DERIVED analytic finite-to-observation lift under the declared EPSC error certificate and norm convention.

The right-hand side is finite-native once `v`, `epsilon`, `tau0`, and `Lambda_N` are certified. A dedicated exact checker verifies the rational interface in a square/eighth-power calibration; the general irrational-root enclosure is a standard certified-arithmetic obligation rather than a theorem shortcut.

## 4. Published finite-observation adapter

Balakrishna--Biswas (2025) gives a periodic 3D NSE regularity criterion from finitely many modal/nodal/volume observations. Its alternate criterion uses a quantity of the form `K_h` above with `p>2` and a resolution parameter `h`. Schematically in the unforced case, the observation-dependent term has the form

\[
\left(C(\nu,p,q,\tau_0)K_h^2\right)^{2p/(p-2)}
\lesssim h^{-2}.
\]

For modal observations `h^{-2}` is comparable, with adapter-dependent constants, to the largest retained Stokes scale `Lambda_N`.

We deliberately do **not** bake an unspecified absolute constant from `\lesssim` notation into the finite checker. For a machine-verifiable instance, a concrete valid adapter constant must be extracted from a complete proof audit. For the asymptotic reduction below, only finiteness of the fixed adapter constants is used.

## 5. Subcritical finite-observation theorem

### `NS-P2B-SUBCRITICAL-OBS`

Fix `p>2` and set

\[
\alpha_p:=\frac{p-2}{2p}.
\]

Assume the published finite-observation adapter with fixed finite constants and the declared modal relation `h_N^{-2} \asymp Lambda_N`. Suppose that for every finite target time `T` there exist constants `C_T<infinity` and `sigma>0`, independent of `N`, such that for all sufficiently large modal cutoffs

\[
\boxed{
K_N(u)^2
\le
C_T\Lambda_N^{\alpha_p-\sigma}.
}
\]

Then the observation-dependent term in the adapter grows at most like

\[
\Lambda_N^{1-\frac{2p}{p-2}\sigma},
\]

which is strictly sublinear in `Lambda_N`, while the admissible right-hand side grows linearly in `Lambda_N`. The remaining unforced initial-data and lowest-eigenvalue terms are fixed in `N`. Hence some finite `N` satisfies the adapter gate, and the solution is regular on `[0,T]`. Since `T` is arbitrary, the standard continuation composition yields the periodic global-regularity branch.

**Status:** DERIVED reduction conditional on the published adapter and its modal normalization. It does not prove the displayed subcritical estimate.

This is a stronger research localization than the old generic statement `prove a uniform H3 bound`: any positive exponent slack `sigma` in a finite modal window readout is enough.

## 6. Energy-budget criticality no-go

The next question is whether the standard Leray energy/dissipation budget already forces `sigma>0`. It does not.

Take abstract dyadic scales

\[
N_j=2^j,
\qquad
 e_j=N_j^{-1},
\qquad
 A_j=N_j,
\qquad
 \delta_j=N_j^{-2}.
\]

Interpret `e_j` as the `L2` energy carried by a scale-localized episode, `A_j` as its `H1`-squared amplitude, and `delta_j` as a parabolic-scale lifetime. These choices obey the dimensional relation `A_j=N_j^2 e_j`.

The total budget costs are summable:

\[
\sum_j e_j=\sum_j2^{-j}<\infty,
\qquad
\sum_j A_j\delta_j
=
\sum_j N_j^{-1}<\infty.
\]

But a single such episode contributes

\[
K_{N_j}^2
\sim
(A_j^p\delta_j)^{1/p}
=
N_j^{1-2/p}
=
\Lambda_j^{(p-2)/(2p)}
=
\Lambda_j^{\alpha_p}.
\]

Thus the standard energy/dissipation budgets permit the **exact critical exponent `sigma=0`**.

For the exact control `p=4`,

\[
(K_{N_j}^2)^4=N_j^2=\Lambda_j.
\]

The repository checker verifies this identity and the summable budget by integer/rational arithmetic.

### Scope of the no-go

This is an abstract budget countermodel, not a Navier--Stokes solution. Its conclusion is exactly limited to the inference being tested:

```text
L-infinity_t L2_x energy bound
+ L2_t H1_x dissipation bound
    DOES NOT BY ITSELF FORCE
strictly subcritical finite-observation scaling.
```

It does not refute global regularity. It shows that any successful proof must use structure beyond those two budgets.

## 7. Translation of the remaining problem into the lab language

The Genesis/Universe architectural requirement of a dynamically closed readout translates here into a concrete mathematical demand: the finite window record must have a scale/time evolution law strong enough to rule out critical parabolic spikes.

The IDM shell-window identity gives an exact measurable coordinate for that law. What is missing is not another reader; it is a **strict scale margin**.

### `NS-P2B-ANTI-INTERMITTENCY` — OPEN / Clay-bearing

Prove from finite/checkable NSE structure, without assuming regularity, that for every finite `T` there exist `p>2`, `C_T<infinity`, and `sigma>0` such that

\[
K_N(u)^2
\le C_T\Lambda_N^{(p-2)/(2p)-\sigma}
\]

for all sufficiently large modal cutoffs, or prove an equivalent finite transfer-window recursion that implies this estimate.

Admissible ingredients include:

- exact shell-energy window balances;
- certified nonlinear-transfer intervals;
- cancellation/flux identities;
- viscosity and scale recursion;
- EPSC finite-tape residual certificates;
- a proved dynamically commuting coarse-grained recurrence.

Forbidden shortcuts include assuming a uniform `H1/H3` regularity bound, assuming the finite-observation criterion itself, or using finite numerical absence of spikes as a universal theorem.

## 8. Why the route stops here

IDM supplies the finite window language and EPSC error adapter. Genesis and Universe correctly force us to demand dynamic closure and honest bridge tiers. The published finite-observation theorem supplies a continuum semantic adapter. The remaining `sigma>0` statement is not contained in those repositories and is not implied by the standard energy inequality; proving it would be genuinely new regularity-level mathematics.

Therefore P2B is **CLOSED AS A REDUCTION / OPEN AT ANTI-INTERMITTENCY**.

This is an honest endpoint of the requested cross-repository attack: the route is fully translated, its finite bridge is explicit, its energy-only shortcut is refuted, and its single missing theorem is named. Clay Navier--Stokes remains OPEN.
