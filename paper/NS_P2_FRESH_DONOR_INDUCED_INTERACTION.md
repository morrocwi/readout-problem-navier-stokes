# NS P2 — induced off-tree interaction in the dyadic fresh-donor escape

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_fresh_donor_induced_interaction.py`

## 1. Purpose

`NS_P2_DYADIC_FRESH_DONOR_TREE_ESCAPE.md` proves that static phase incidence and H1 coupling geometry alone do not control the conflict-free remainder: a selected dyadic tree can be phase-SAT and have a cutoff-uniform H1 coupling floor.

That selected tree is not, however, dynamically closed under the Navier--Stokes convolution.

This note attacks the first two donor steps directly and proves an exact alternative:

```text
both consecutive fresh donors are simultaneously nonzero
    -> an off-tree mode is generated with cutoff-uniform H1 coupling;

avoid that induced interaction
    -> at least one donor must be absent/small or the donors must be temporally separated,
       unless additional modes provide a cancelling nonlinear contribution.
```

This is a genuine move from static channel geometry toward the dynamics required to close P2.

---

## 2. Consecutive donor modes

Use the first two donor modes in the exact fresh-donor tree:

\[
q_0=n(1,0,1),
\qquad
q_1=n(2,0,-1).
\]

They are both in the `xz` plane.  Let

\[
N=(0,1,0)
\]

and use the unit tangential polarization

\[
T_\ell=\frac{N\times\ell}{|\ell|}.
\]

Their sum is the off-tree mode

\[
\boxed{
r=q_0+q_1=n(3,0,0).}
\]

This mode is not a member of the selected backbone/donor tree at that two-step stage.

---

## 3. Exact Fourier--Leray coefficient

For the channel

\[
q_0/T_{q_0}+q_1/T_{q_1}\longrightarrow r/T_r,
\]

the checker derives

\[
\boxed{
c_{01}=\frac{3\sqrt{10}}{10}\,n.}
\]

The coefficient is nonzero for every positive integer `n`.

### Status

`NS-P2-FRESH-DONOR-INDUCED-COEFF-ALLN` — **PASS**.

---

## 4. Cutoff-uniform H1 strength

With unit polarizations, homogeneous H1 normalization gives

\[
\Gamma_{01}^{H^1,hom}
=2c_{01}\frac{|r|}{|q_0||q_1|}.
\]

Since

\[
|q_0|=\sqrt2\,n,
\qquad
|q_1|=\sqrt5\,n,
\qquad
|r|=3n,
\]

the normalized coefficient is exactly

\[
\boxed{
\Gamma_{01}^{H^1,hom}=\frac95.
}
\]

For physical inhomogeneous H1 weights, the standard integer-mode comparison gives a ratio at least `1/2`, hence

\[
\boxed{
|\Gamma_{01}^{H^1,inh}|\ge\frac9{10}.
}
\]

Thus the induced interaction is not a high-frequency coefficient-decay effect.

### Status

`NS-P2-FRESH-DONOR-INDUCED-H1-FLOOR` — **DERIVED**.

---

## 5. Exact instantaneous generation from tree support

Consider an instant at which the Fourier state is supported on the first two-step fresh-donor tree and its reality-conjugate modes, with the off-tree coordinate `z_r` equal to zero.

For the declared tangential donor polarizations, the ordered `q_0,q_1` contributions combine into

\[
\dot z_r\big|_{q_0,q_1}
=-i c_{01} z_{q_0}z_{q_1}.
\]

The viscous term vanishes at that instant because `z_r=0`.

Within the declared two-step tree support, the only other reality-allowed pair summing to `r` is

\[
P_2+(-P_0)=r,
\]

where `P_0=n(1,0,0)` and `P_2=n(4,0,0)`.  Those wavevectors are collinear and both backbone velocities use the normal polarization `N`, so their Fourier--Leray coefficient is exactly zero.

Therefore, on that declared support,

\[
\boxed{
\dot z_r=-i c_{01}z_{q_0}z_{q_1}.
}
\]

If both donor coordinates are nonzero, the off-tree coordinate is generated immediately.

### Status

`NS-P2-FRESH-DONOR-TREE-NOT-INVARIANT` — **DERIVED** for the declared exact two-step Fourier support.

---

## 6. Dynamical remainder dichotomy

The result gives a sharper form of the conflict-free remainder problem.

For two consecutive dyadic fresh-donor steps, one cannot simultaneously have

```text
both donor coordinates nonzero,
no additional cancelling modes,
and exact confinement to the selected tree support.
```

Hence an actual solution trying to realize this phase-SAT escape must pay at least one of the following costs:

1. **donor amplitude cut:** one consecutive donor is small/absent;
2. **temporal separation:** consecutive donor activations do not significantly overlap;
3. **induced interaction:** the off-tree mode `r` is generated with cutoff-uniform H1 coefficient;
4. **cancellation complexity:** additional Fourier modes are present and contribute a matching cancellation to the `r` equation.

This is not yet a quantitative all-network theorem, but it removes the possibility that the exact fresh-donor tree is itself an invariant nonlinear cascade mechanism.

### Status

`NS-P2-FRESH-DONOR-OVERLAP-OR-DYNAMIC-COST` — **DERIVED** for the declared two-step support and exact coefficient calculation.

---

## 7. What remains before P2 closure

The remaining hard branch is now precise:

\[
\boxed{
\text{conflict-poor critical transfer}
\Longrightarrow
\text{small donor overlap}
\ \text{or}\
\text{off-tree/cancellation mass that can be recursively charged}.
}
\]

The next theorem must aggregate this local induced-interaction fact across a dyadic window and show that repeated attempts to maintain a fresh-donor escape either create enough additional interaction structure to enter the holonomy packing branch or pay a summable amplitude/dissipation/time cost.

Current boundary:

```text
fresh-donor selected tree phase-SAT and H1-nondegenerate        DERIVED
fresh-donor selected tree exactly invariant                     REFUTED
consecutive donor overlap -> uniform-H1 off-tree generation     DERIVED on declared support
window aggregation of induced interactions                       OPEN
cancellation-chain closure / recursive charge                    OPEN
channel-envelope -> K_N / R_j contraction                        OPEN
constructive R_j recurrence                                      OPEN
NS-P2-FRUSTRATION-OR-CUT                                         OPEN
Clay Navier-Stokes regularity                                    OPEN
```
